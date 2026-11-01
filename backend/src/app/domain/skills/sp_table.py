"""Skill-point totals for trained skill levels.

The accumulated cost of the levels below the trained one follows the game rule
``ceil(250 * rank * sqrt(32) ** (level - 1))``.  The step from one level to
the next is the difference of two accumulated totals.
"""

from math import isqrt

from app.domain.skills.errors import InvalidSkillLevelError, InvalidSkillRankError

__all__ = ["accumulated_skill_sp", "skill_sp_to_next_level"]

_MIN_LEVEL = 0
_MAX_LEVEL = 5
_BASE_SP = 250


def accumulated_skill_sp(*, rank: int, level: int) -> int:
    """Return the accumulated skill points spent to reach a trained level.

    The accumulated cost of the levels below the trained one follows the game
    rule ``ceil(250 * rank * sqrt(32) ** (level - 1))`` for levels 1 through 5,
    and 0 for level 0.

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

    if level < _MIN_LEVEL or level > _MAX_LEVEL:
        raise InvalidSkillLevelError(f"level {level} outside {_MIN_LEVEL}..{_MAX_LEVEL}")
    if rank < 1:
        raise InvalidSkillRankError(f"rank {rank} below 1")
    if level == 0:
        return 0
    # sqrt(32) ** (level - 1) == 32 ** whole * sqrt(32) ** half; keeping the
    # math in integers avoids float rounding above the true value, which
    # would make ceil overshoot by 1 (e.g. level 3 -> 8001 instead of 8000).
    whole, half = divmod(level - 1, 2)
    scaled = _BASE_SP * rank * 32**whole
    if half == 0:
        return scaled
    # half == 1: scaled * sqrt(32) == 4 * scaled * sqrt(2), irrational, so
    # the ceiling is floor + 1 and floor comes from the exact isqrt.
    m = 4 * scaled
    return isqrt(2 * m * m) + 1


def skill_sp_to_next_level(*, rank: int, level: int) -> int:
    """Return the skill points needed to train from a level to the next.

    The step to the next level is the difference of two accumulated totals:
    ``accumulated_skill_sp(level + 1) - accumulated_skill_sp(level)``.
    It is defined for trained levels 1 through 4; level 5 has no next level.

    Arguments:
        rank: skill rank, at least 1.
        level: trained skill level, 1 through 4.

    Returns:
        The skill points required to advance from ``level`` to ``level + 1`` on
        a skill of the given rank.

    Raises:
        InvalidSkillLevelError: when ``level`` is below 1 or above 4.
        InvalidSkillRankError: when ``rank`` is below 1.
    """

    if level < 1 or level > 4:
        raise InvalidSkillLevelError(f"level {level} outside 1..4")
    if rank < 1:
        raise InvalidSkillRankError(f"rank {rank} below 1")
    return accumulated_skill_sp(rank=rank, level=level + 1) - accumulated_skill_sp(rank=rank, level=level)
