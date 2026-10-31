"""Mapping from EVE scopes to the capabilities those scopes unlock."""

from __future__ import annotations

from enum import StrEnum
from types import MappingProxyType


class Capability(StrEnum):
    """A unit of behaviour the interface may offer."""

    SKILLS_READ = "skills.read"
    SKILLS_QUEUE = "skills.queue"
    SKILLS_IMPLANTS = "skills.implants"
    INDUSTRY_JOBS = "industry.jobs"
    INDUSTRY_CORP_JOBS = "industry.corp_jobs"
    INDUSTRY_BLUEPRINTS = "industry.blueprints"
    ASSETS_CHARACTER = "assets.character"
    ASSETS_CORP = "assets.corp"
    CORP_DIVISIONS = "corp.divisions"
    CORP_ROLES = "corp.roles"
    WALLET_BALANCE = "wallet.balance"
    MARKET_ORDERS = "market.orders"


SCOPE_TO_CAPABILITIES: MappingProxyType[str, frozenset[Capability]] = MappingProxyType(
    {
        "esi-skills.read_skills.v1": frozenset({Capability.SKILLS_READ}),
        "esi-skills.read_skillqueue.v1": frozenset({Capability.SKILLS_QUEUE}),
        "esi-clones.read_implants.v1": frozenset({Capability.SKILLS_IMPLANTS}),
        "esi-industry.read_character_jobs.v1": frozenset({Capability.INDUSTRY_JOBS}),
        "esi-industry.read_corporation_jobs.v1": frozenset({Capability.INDUSTRY_CORP_JOBS}),
        "esi-characters.read_blueprints.v1": frozenset({Capability.INDUSTRY_BLUEPRINTS}),
        "esi-assets.read_assets.v1": frozenset({Capability.ASSETS_CHARACTER}),
        "esi-assets.read_corporation_assets.v1": frozenset({Capability.ASSETS_CORP}),
        "esi-corporations.read_divisions.v1": frozenset({Capability.CORP_DIVISIONS}),
        "esi-characters.read_corporation_roles.v1": frozenset({Capability.CORP_ROLES}),
        "esi-wallet.read_character_wallet.v1": frozenset({Capability.WALLET_BALANCE}),
        "esi-markets.read_character_orders.v1": frozenset({Capability.MARKET_ORDERS}),
    }
)


def capabilities_for(granted: frozenset[str] | set[str]) -> frozenset[Capability]:
    """Resolve the capabilities a set of granted scopes provides.

    Args:
        granted: Scope strings returned by the token exchange.

    Returns:
        Capabilities unlocked by those scopes, ignoring unknown scopes.
    """
    found: set[Capability] = set()
    for scope in granted:
        found |= SCOPE_TO_CAPABILITIES.get(scope, frozenset())
    return frozenset(found)


def scopes_for(required: frozenset[Capability] | set[Capability]) -> frozenset[str]:
    """Resolve the scopes needed to satisfy a set of capabilities.

    Args:
        required: Capabilities a feature depends on.

    Returns:
        Scope strings that together provide them.
    """
    needed: set[str] = set()
    for scope, caps in SCOPE_TO_CAPABILITIES.items():
        if required & caps:
            needed.add(scope)
    return frozenset(needed)
