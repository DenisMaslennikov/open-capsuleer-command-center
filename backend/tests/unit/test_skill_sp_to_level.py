"""Unit tests for the skill-point step from one trained level to the next."""

import pytest

from app.domain.skills.errors import InvalidSkillLevelError, InvalidSkillRankError
from app.domain.skills.sp_table import skill_sp_to_next_level

# Steps derived from the game rule ceil(250 * rank * sqrt(32) ** (level - 1)):
# each step is the difference of two accumulated totals.
STEPS = [
    (1, 1, 1165),
    (1, 2, 6585),
    (1, 3, 37255),
    (1, 4, 210745),
    (2, 4, 421490),
    (5, 4, 1053725),
    (8, 4, 1685961),
    (16, 4, 3371922),
]


@pytest.mark.parametrize(("rank", "level", "expected"), STEPS)
def test_step_from_level_to_next_returns_difference_of_accumulated_totals(rank, level, expected):
    assert skill_sp_to_next_level(rank=rank, level=level) == expected


@pytest.mark.parametrize("level", [0, 5])
def test_level_outside_1_through_4_raises_skill_level_error(level):
    with pytest.raises(InvalidSkillLevelError):
        skill_sp_to_next_level(rank=1, level=level)


def test_rank_below_1_raises_skill_rank_error():
    with pytest.raises(InvalidSkillRankError):
        skill_sp_to_next_level(rank=0, level=1)
