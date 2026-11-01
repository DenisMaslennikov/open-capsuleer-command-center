"""Scope registry behaviour."""

from __future__ import annotations

from app.core.scopes import Capability, capabilities_for, scopes_for


def test_assets_scope_unlocks_character_assets_capability() -> None:
    caps = capabilities_for({"esi-assets.read_assets.v1"})
    assert caps == frozenset({Capability.ASSETS_CHARACTER})


def test_unknown_scope_unlocks_nothing() -> None:
    assert capabilities_for({"esi-not-a-real-scope.v1"}) == frozenset()


def test_capabilities_are_unioned_across_scopes() -> None:
    caps = capabilities_for({"esi-skills.read_skills.v1", "esi-skills.read_skillqueue.v1"})
    assert caps == frozenset({Capability.SKILLS_READ, Capability.SKILLS_QUEUE})


def test_scope_lookup_inverts_the_registry() -> None:
    assert scopes_for({Capability.ASSETS_CORP}) == frozenset({"esi-assets.read_corporation_assets.v1"})
