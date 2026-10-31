"""Tests for the schema gate: it must fail on drift and pass on an empty model set."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from sqlalchemy import BigInteger, Column, Float, MetaData, Numeric, Table, Text

from app.db import schema_gate

CONTRACT = {
    "aggregates": [
        {
            "id": "accounts",
            "lifetime": "user",
            "tables": [
                {
                    "name": "accounts",
                    "columns": [
                        {"name": "id", "type": "bigint", "pk": True, "nullable": False},
                        {"name": "email", "type": "text", "pk": False, "nullable": False},
                    ],
                }
            ],
        },
        {
            "id": "market",
            "lifetime": "user",
            "tables": [
                {
                    "name": "market_orders",
                    "columns": [
                        {"name": "id", "type": "bigint", "pk": True, "nullable": False},
                        {"name": "account_id", "type": "bigint", "pk": False, "nullable": False},
                        {"name": "price", "type": "numeric(20,2)", "pk": False, "nullable": False},
                    ],
                }
            ],
        },
    ]
}


@pytest.fixture()
def contract_path(tmp_path: Path) -> Path:
    path = tmp_path / "schema.json"
    path.write_text(json.dumps({"schema": CONTRACT}), encoding="utf-8")
    return path


def test_empty_metadata_passes(contract_path: Path) -> None:
    assert schema_gate.run(contract_path, MetaData()) == []


def test_undeclared_column_fails(contract_path: Path) -> None:
    metadata = MetaData()
    Table(
        "accounts",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("email", Text, nullable=False),
        Column("nickname", Text),
    )
    errors = schema_gate.run(contract_path, metadata)
    assert any("nickname" in error for error in errors)


def test_undeclared_table_fails(contract_path: Path) -> None:
    metadata = MetaData()
    Table(
        "accounts",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("email", Text, nullable=False),
    )
    Table("surprise", metadata, Column("id", BigInteger, primary_key=True))
    errors = schema_gate.run(contract_path, metadata)
    assert any("surprise" in error for error in errors)


def test_float_money_fails(contract_path: Path) -> None:
    metadata = MetaData()
    Table(
        "accounts",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("email", Text, nullable=False),
    )
    Table(
        "market_orders",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("account_id", BigInteger, nullable=False),
        Column("price", Float, nullable=False),
    )
    errors = schema_gate.run(contract_path, metadata)
    assert any("floating point" in error for error in errors)


def test_type_mismatch_fails(contract_path: Path) -> None:
    metadata = MetaData()
    Table(
        "accounts",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("email", Text, nullable=False),
    )
    Table(
        "market_orders",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("account_id", BigInteger, nullable=False),
        Column("price", Numeric(10, 4), nullable=False),
    )
    errors = schema_gate.run(contract_path, metadata)
    assert any("does not match declared" in error for error in errors)


def test_user_table_without_account_path_fails(contract_path: Path) -> None:
    metadata = MetaData()
    Table(
        "accounts",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("email", Text, nullable=False),
    )
    Table(
        "market_orders",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("account_id", BigInteger, nullable=False),
        Column("price", Numeric(20, 2), nullable=False),
    )
    errors = schema_gate.run(contract_path, metadata)
    assert any("must reach accounts" in error for error in errors)
