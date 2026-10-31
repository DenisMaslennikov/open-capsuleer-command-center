"""Schema gate: SQLAlchemy metadata must match the declared contract.

The contract in ``docs/schema/schema.json`` is the source of truth; models are an implementation of
it. This module compares the two and fails on anything the contract does not declare. It lives in
the repository rather than next to the pipeline scripts because it imports the application metadata
(see ADR-0009).

Checks:
1. completeness — a table or column in metadata that the contract does not declare;
2. column shape — type (with precision), nullability, primary key, and the type rules of the data
   model (no floats for money, jsonb only where allowed, ``*_encrypted`` is bytea, ``*_at`` is
   timestamptz);
3. relations — every foreign key resolves, its ``ON DELETE`` matches, and no user or cache table
   points into the SDE aggregate;
4. ownership — a model lives in its aggregate's module, and every user table reaches ``accounts``
   by a chain of foreign keys.

Run from ``backend/``::

    uv run python -m app.db.schema_gate --contract ../docs/schema/schema.json
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path
from typing import Any

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Float,
    Integer,
    LargeBinary,
    MetaData,
    Numeric,
    String,
    Text,
)

from app.db.base import Base

JSONB_ALLOWED = {("esi_responses", "body"), ("notification_events", "payload")}
MONEY_COLUMNS = ("price", "cost", "isk", "value", "amount")

# contract type -> how SQLAlchemy renders it (lowercase, no spaces)
TYPE_ALIASES = {
    "bigint": {"biginteger", "bigint"},
    "integer": {"integer", "int"},
    "smallint": {"smallinteger", "smallint"},
    "text": {"text", "string", "varchar"},
    "boolean": {"boolean", "bool"},
    "timestamptz": {"datetime(timezone=true)", "timestamp(timezone=true)"},
    "date": {"date"},
    "uuid": {"uuid", "uuid(as_uuid=true)"},
    "jsonb": {"jsonb"},
    "bytea": {"largebinary", "bytea"},
    "double precision": {"float", "double"},
    "float": {"float"},
    "real": {"real", "float"},
}


def load_contract(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload.get("schema", payload)


def contract_tables(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        table["name"]: table
        for aggregate in contract.get("aggregates", [])
        for table in aggregate.get("tables", [])
    }


def contract_aggregate_of(contract: dict[str, Any]) -> dict[str, str]:
    return {
        table["name"]: aggregate["id"]
        for aggregate in contract.get("aggregates", [])
        for table in aggregate.get("tables", [])
    }


def contract_lifetime_of(contract: dict[str, Any]) -> dict[str, str]:
    return {
        table["name"]: aggregate.get("lifetime", "user")
        for aggregate in contract.get("aggregates", [])
        for table in aggregate.get("tables", [])
    }


def module_exists(aggregate: str) -> bool:
    try:
        importlib.import_module(f"app.dbhelpers.{aggregate}")
    except ModuleNotFoundError:
        return False
    return True


def normalise_type(contract_type: str) -> str:
    return contract_type.lower().replace(" ", "")


def rendered_type(column: Any) -> str:
    try:
        return str(column.type).lower().replace(" ", "")
    except Exception:  # pragma: no cover - defensive for exotic types
        return ""


def type_matches(column: Any, contract_type: str) -> bool:
    """Compare a column with the contract type by introspection, not by its rendered name.

    SQLAlchemy renders `DateTime(timezone=True)` as `DATETIME`, which no string alias catches, so
    the timezone flag is read from the type itself.
    """
    sql_type = column.type
    wanted = normalise_type(contract_type)
    if wanted.endswith("[]"):
        return hasattr(sql_type, "item_type")
    if wanted.startswith("numeric"):
        if not isinstance(sql_type, Numeric):
            return False
        numbers = wanted.replace("numeric(", "").replace(")", "").split(",")
        precision = int(numbers[0]) if numbers and numbers[0].isdigit() else None
        scale = int(numbers[1]) if len(numbers) > 1 and numbers[1].isdigit() else None
        return sql_type.precision == precision and sql_type.scale == scale
    if wanted.startswith("varchar"):
        return isinstance(sql_type, String) and not isinstance(sql_type, Text)
    if wanted == "text":
        return isinstance(sql_type, (Text, String))
    if wanted == "bigint":
        return isinstance(sql_type, BigInteger)
    if wanted == "integer":
        return isinstance(sql_type, Integer) and not isinstance(sql_type, BigInteger)
    if wanted == "smallint":
        return getattr(sql_type, "__class__", type(sql_type)).__name__.lower().startswith("small")
    if wanted == "boolean":
        return isinstance(sql_type, Boolean)
    if wanted == "timestamptz":
        return isinstance(sql_type, DateTime) and bool(sql_type.timezone)
    if wanted == "date":
        return isinstance(sql_type, Date) and not isinstance(sql_type, DateTime)
    if wanted == "jsonb":
        return type(sql_type).__name__.lower() == "jsonb"
    if wanted == "bytea":
        return isinstance(sql_type, LargeBinary)
    if wanted == "uuid":
        return type(sql_type).__name__.lower() == "uuid"
    if wanted in ("double precision", "float", "real"):
        return isinstance(sql_type, Float)
    return False


def check_completeness(contract: dict[str, Any], metadata: MetaData) -> list[str]:
    declared = contract_tables(contract)
    errors: list[str] = []
    for table in metadata.sorted_tables:
        declared_table = declared.get(table.name)
        if declared_table is None:
            errors.append(
                f"table {table.name} exists in models but is not declared in the contract"
            )
            continue
        declared_columns = {column["name"] for column in declared_table.get("columns", [])}
        model_columns = {column.name for column in table.columns}
        for column in table.columns:
            if column.name not in declared_columns:
                errors.append(f"column {table.name}.{column.name} is not declared in the contract")
        for column_name in declared_columns - model_columns:
            errors.append(
                f"column {table.name}.{column_name} is declared in the contract but "
                "missing in the model"
            )
    for name in declared:
        if name in metadata.tables:
            continue
        aggregate = contract_aggregate_of(contract)[name]
        if module_exists(aggregate):
            errors.append(
                f"table {name} is declared and its aggregate exists, but the model is missing"
            )
    return errors


def check_columns(contract: dict[str, Any], metadata: MetaData) -> list[str]:
    declared = contract_tables(contract)
    errors: list[str] = []
    for table in metadata.sorted_tables:
        declared_table = declared.get(table.name)
        if declared_table is None:
            continue
        expected = {column["name"]: column for column in declared_table.get("columns", [])}
        for column in table.columns:
            spec = expected.get(column.name)
            if spec is None:
                continue
            if not type_matches(column, spec.get("type", "")):
                errors.append(
                    f"{table.name}.{column.name}: type {column.type!r} does not match "
                    f"declared {spec.get('type')!r}"
                )
            if bool(column.nullable) is not bool(spec.get("nullable", True)):
                errors.append(f"{table.name}.{column.name}: nullability differs from the contract")
            if bool(column.primary_key) is not bool(spec.get("pk", False)):
                errors.append(f"{table.name}.{column.name}: primary key differs from the contract")
    errors += check_type_rules(metadata, declared)
    return errors


def check_type_rules(metadata: MetaData, declared: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for table in metadata.sorted_tables:
        for column in table.columns:
            rendered = rendered_type(column)
            is_float = rendered.startswith(("float", "double", "real"))
            name = column.name.lower()
            if is_float and any(word in name for word in MONEY_COLUMNS):
                errors.append(f"{table.name}.{column.name}: floating point is forbidden for money")
            if rendered.startswith("jsonb") and (table.name, column.name) not in JSONB_ALLOWED:
                errors.append(
                    f"{table.name}.{column.name}: jsonb is only allowed for opaque "
                    "external payloads"
                )
            if column.name.endswith("_encrypted") and not rendered.startswith(
                ("largebinary", "bytea")
            ):
                errors.append(f"{table.name}.{column.name}: encrypted secrets must be bytea")
            if column.name.endswith("_at") and not (
                isinstance(column.type, DateTime) and bool(column.type.timezone)
            ):
                errors.append(f"{table.name}.{column.name}: *_at must be timestamptz")
    return errors


def check_composite_keys(contract: dict[str, Any], metadata: MetaData) -> list[str]:
    """A declared table-level foreign key must exist in the model with the same target and rule."""
    errors: list[str] = []
    for name, declared in contract_tables(contract).items():
        for composite in declared.get("foreign_keys") or []:
            table = metadata.tables.get(name)
            if table is None:
                continue
            wanted_columns = tuple(composite.get("columns") or [])
            wanted_target = composite.get("references_table")
            wanted_on_delete = str(composite.get("on_delete") or "cascade").lower()
            found = False
            for constraint in table.foreign_key_constraints:
                columns = tuple(c.name for c in constraint.columns)
                if columns != wanted_columns:
                    continue
                target = {element.column.table.name for element in constraint.elements}
                on_delete = str(constraint.ondelete or "no action").lower()
                if target != {wanted_target}:
                    errors.append(
                        f"{name}{wanted_columns}: composite foreign key points at "
                        f"{sorted(target)}, contract declares {wanted_target}"
                    )
                elif on_delete != wanted_on_delete:
                    errors.append(
                        f"{name}{wanted_columns}: composite foreign key ON DELETE "
                        f"{on_delete}, contract declares {wanted_on_delete}"
                    )
                found = True
            if not found:
                errors.append(
                    f"{name}: composite foreign key {wanted_columns} -> {wanted_target} "
                    "is declared in the contract but missing in the model"
                )
    return errors


def check_relations(contract: dict[str, Any], metadata: MetaData) -> list[str]:
    errors: list[str] = []
    lifetime = contract_lifetime_of(contract)
    aggregate_of = contract_aggregate_of(contract)
    errors += check_composite_keys(contract, metadata)
    for table in metadata.sorted_tables:
        for column in table.columns:
            for foreign_key in column.foreign_keys:
                target = foreign_key.column.table.name
                if target not in metadata.tables:
                    errors.append(
                        f"{table.name}.{column.name}: foreign key to unknown table {target}"
                    )
                    continue
                if (
                    lifetime.get(table.name) in ("user", "cache")
                    and aggregate_of.get(target) == "sde"
                ):
                    errors.append(
                        f"{table.name}.{column.name}: a {lifetime.get(table.name)} table "
                        "must not reference SDE by foreign key"
                    )
                declared = contract_tables(contract).get(column.table.name) or {}
                composite = {
                    name
                    for fk in declared.get("foreign_keys") or []
                    for name in fk.get("columns") or []
                }
                if column.name in composite:
                    continue
                spec = next(
                    (c for c in declared.get("columns", []) if c["name"] == column.name), {}
                )
                reference = spec.get("references") or {}
                if reference:
                    if reference.get("table") != target:
                        errors.append(
                            f"{table.name}.{column.name}: foreign key points at {target}, "
                            f"contract declares {reference.get('table')}"
                        )
                    if reference.get("column") != foreign_key.column.name:
                        errors.append(
                            f"{table.name}.{column.name}: foreign key points at "
                            f"{target}.{foreign_key.column.name}, contract declares "
                            f"{reference.get('table')}.{reference.get('column')}"
                        )
                expected_on_delete = reference.get("on_delete", "cascade")
                actual = (foreign_key.ondelete or "no action").lower()
                if expected_on_delete and actual != expected_on_delete.lower():
                    errors.append(
                        f"{table.name}.{column.name}: ON DELETE {actual} does not match "
                        f"declared {expected_on_delete}"
                    )
    return errors


def check_ownership(contract: dict[str, Any], metadata: MetaData) -> list[str]:
    errors: list[str] = []
    lifetime = contract_lifetime_of(contract)
    aggregate_of = contract_aggregate_of(contract)
    errors += check_composite_keys(contract, metadata)
    for table in metadata.sorted_tables:
        aggregate = aggregate_of.get(table.name)
        if aggregate is None:
            continue
        module = f"app.dbhelpers.{aggregate}"
        for model in Base.registry.mappers:
            if model.local_table is not None and model.local_table.name == table.name:
                if model.class_.__module__ != module:
                    errors.append(
                        f"{table.name}: model lives in {model.class_.__module__}, expected {module}"
                    )
    errors += check_account_reachability(metadata, lifetime)
    return errors


def check_account_reachability(metadata: MetaData, lifetime: dict[str, str]) -> list[str]:
    """Every user table must reach accounts through cascading foreign keys."""
    parents: dict[str, set[str]] = {name: set() for name in metadata.tables}
    for table in metadata.sorted_tables:
        for column in table.columns:
            for foreign_key in column.foreign_keys:
                if (foreign_key.ondelete or "").lower() == "cascade":
                    parents.setdefault(table.name, set()).add(foreign_key.column.table.name)

    def reaches_account(name: str, seen: set[str]) -> bool:
        if name == "accounts":
            return True
        if name in seen:
            return False
        seen.add(name)
        return any(reaches_account(parent, seen) for parent in parents.get(name, ()))

    errors: list[str] = []
    for table in metadata.sorted_tables:
        if lifetime.get(table.name) != "user":
            continue
        if table.name == "accounts":
            continue
        if not reaches_account(table.name, set()):
            errors.append(
                f"{table.name}: a user table must reach accounts through cascading foreign keys"
            )
    return errors


def run(contract_path: Path, metadata: MetaData | None = None) -> list[str]:
    contract = load_contract(contract_path)
    if metadata is None:
        # Importing a dbhelpers module registers its models; do it before any table is inspected,
        # otherwise the check sees a half-populated metadata and reports phantom missing models.
        for aggregate in contract.get("aggregates", []):
            module_exists(aggregate.get("id", ""))
        metadata = Base.metadata
    errors = []
    errors += check_completeness(contract, metadata)
    errors += check_columns(contract, metadata)
    errors += check_relations(contract, metadata)
    errors += check_ownership(contract, metadata)
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compare models with the schema contract.")
    parser.add_argument(
        "--contract", default="../docs/schema/schema.json", help="path to the schema contract"
    )
    args = parser.parse_args(argv)
    errors = run(Path(args.contract))
    for error in errors:
        print(f"schema-gate: {error}", file=sys.stderr)
    if errors:
        print(f"schema-gate: {len(errors)} violation(s)", file=sys.stderr)
        return 1
    print("schema-gate: models match the contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
