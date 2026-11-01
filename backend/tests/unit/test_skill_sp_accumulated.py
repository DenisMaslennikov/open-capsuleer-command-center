"""Behaviour of accumulated skill points per trained level and rank."""

import pytest

from app.domain.skills.errors import InvalidSkillLevelError, InvalidSkillRankError
from app.domain.skills.sp_table import accumulated_skill_sp


@pytest.mark.parametrize(
    ("level", "expected"),
    [(1, 250), (2, 1415), (3, 8000), (4, 45255), (5, 256000)],
)
def test_rank_1_levels_1_to_5_accumulate_to_table(level, expected):
    assert accumulated_skill_sp(rank=1, level=level) == expected


def test_rank_5_level_5_is_1280000():
    assert accumulated_skill_sp(rank=5, level=5) == 1280000


def test_untrained_level_0_costs_zero_points():
    assert accumulated_skill_sp(rank=16, level=0) == 0


@pytest.mark.parametrize("level", [6, -1])
def test_level_outside_0_to_5_raises(level):
    with pytest.raises(InvalidSkillLevelError):
        accumulated_skill_sp(rank=1, level=level)


def test_rank_below_1_raises():
    with pytest.raises(InvalidSkillRankError):
        accumulated_skill_sp(rank=0, level=1)
