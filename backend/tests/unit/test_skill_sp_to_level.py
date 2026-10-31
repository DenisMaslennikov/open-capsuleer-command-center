"""Unit tests for the per-level skill-point step in the sp table."""

import pytest

from app.domain.skills.errors import InvalidSkillLevelError, InvalidSkillRankError
from app.domain.skills.sp_table import skill_sp_to_next_level


@pytest.mark.parametrize(
    ("rank", "level", "expected"),
    [
        (1, 1, 1165),
        (5, 4, 1_152_000),
    ],
)
def test_step_to_next_level_matches_accumulated_difference(rank: int, level: int, expected: int) -> None:
    """The step is accumulated(level + 1) minus accumulated(level)."""
    assert skill_sp_to_next_level(rank=rank, level=level) == expected


@pytest.mark.parametrize(
    ("rank", "level", "error"),
    [
        (1, 0, InvalidSkillLevelError),
        (1, 5, InvalidSkillLevelError),
        (0, 1, InvalidSkillRankError),
    ],
)
def test_out_of_range_arguments_raise_domain_errors(
    rank: int, level: int, error: type[Exception]
) -> None:
    """A level outside 1..4 or a rank below 1 raises its domain error."""
    with pytest.raises(error):
        skill_sp_to_next_level(rank=rank, level=level)


def test_level_error_names_the_level() -> None:
    """The level error message names the invalid level."""
    with pytest.raises(InvalidSkillLevelError, match="5"):
        skill_sp_to_next_level(rank=1, level=5)


def test_rank_error_names_the_rank() -> None:
    """The rank error message names the invalid rank."""
    with pytest.raises(InvalidSkillRankError, match="0"):
        skill_sp_to_next_level(rank=0, level=1)
