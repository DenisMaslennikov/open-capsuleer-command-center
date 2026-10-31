"""Skill-point totals for trained skill levels.

The accumulated cost of the levels below the trained one follows the game rule:
``ceil(250 * rank * sqrt(32) ** (level - 1))`` for levels 1 through 5, and 0 for
level 0.

Arguments:
    rank: skill rank, at least 1.
    level: trained skill level, 0 through 5.

Returns:
    The accumulated skill points spent to reach ``level`` on a skill of the
    given rank.

Raises:
    InvalidSkillLevelError: when ``level`` is below 0 or above 5.
    InvalidSkillRankError: when ``rank`` is below 1.
"""

from app.domain.skills.errors import InvalidSkillLevelError, InvalidSkillRankError

__all__ = ["accumulated_skill_sp"]


def accumulated_skill_sp(*, rank: int, level: int) -> int:
    raise NotImplementedError
