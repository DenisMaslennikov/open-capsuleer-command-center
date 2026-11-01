"""Offline behaviour of the training-duration estimate for a skill level."""

import datetime

import pytest

from app.domain.skills import (
    InvalidAccumulatedSkillSpError,
    InvalidSkillLevelError,
    InvalidSkillRankError,
    InvalidSkillSpeedError,
    skill_training_duration,
)

DURATION_CASES = (
    pytest.param(1, 1, 0, 25.0, datetime.timedelta(minutes=10), id="rank1-level1-fresh"),
    pytest.param(1, 1, 100, 25.0, datetime.timedelta(minutes=6), id="rank1-level1-partial"),
    pytest.param(1, 1, 250, 25.0, datetime.timedelta(0), id="rank1-level1-threshold-reached"),
    pytest.param(1, 1, 400, 25.0, datetime.timedelta(0), id="rank1-level1-threshold-exceeded"),
    pytest.param(1, 2, 0, 25.0, datetime.timedelta(seconds=3396), id="rank1-level2-fresh"),
    pytest.param(1, 4, 40000, 25.0, datetime.timedelta(seconds=12612), id="rank1-level4-partial"),
    pytest.param(2, 3, 0, 37.5, datetime.timedelta(seconds=25600), id="rank2-level3-fresh"),
    pytest.param(
        5,
        5,
        0,
        25.0,
        datetime.timedelta(days=35, hours=13, minutes=20),
        id="rank5-level5-fresh",
    ),
)


@pytest.mark.parametrize(
    ("rank", "target_level", "accumulated_sp", "sp_per_minute", "expected"),
    DURATION_CASES,
)
def test_duration_is_the_remaining_skill_points_divided_by_speed(
    rank: int,
    target_level: int,
    accumulated_sp: int,
    sp_per_minute: float,
    expected: datetime.timedelta,
) -> None:
    result = skill_training_duration(
        rank=rank,
        target_level=target_level,
        accumulated_sp=accumulated_sp,
        sp_per_minute=sp_per_minute,
    )

    assert result == expected


@pytest.mark.parametrize("accumulated_sp", [-1, -250])
def test_negative_accumulated_skill_points_are_rejected(accumulated_sp: int) -> None:
    with pytest.raises(InvalidAccumulatedSkillSpError):
        skill_training_duration(
            rank=1,
            target_level=1,
            accumulated_sp=accumulated_sp,
            sp_per_minute=25.0,
        )


@pytest.mark.parametrize("sp_per_minute", [0.0, -5.0])
def test_non_positive_training_speed_is_rejected(sp_per_minute: float) -> None:
    with pytest.raises(InvalidSkillSpeedError):
        skill_training_duration(
            rank=1,
            target_level=1,
            accumulated_sp=0,
            sp_per_minute=sp_per_minute,
        )


def test_invalid_accumulated_skill_points_error_is_a_value_error() -> None:
    assert issubclass(InvalidAccumulatedSkillSpError, ValueError)


def test_invalid_skill_speed_error_is_a_value_error() -> None:
    assert issubclass(InvalidSkillSpeedError, ValueError)


def test_level_above_the_ladder_propagates_the_level_error() -> None:
    with pytest.raises(InvalidSkillLevelError) as excinfo:
        skill_training_duration(
            rank=1,
            target_level=6,
            accumulated_sp=0,
            sp_per_minute=25.0,
        )

    assert excinfo.type is InvalidSkillLevelError


@pytest.mark.parametrize("target_level", [0, -1])
def test_level_below_the_ladder_propagates_the_level_error(target_level: int) -> None:
    with pytest.raises(InvalidSkillLevelError) as excinfo:
        skill_training_duration(
            rank=1,
            target_level=target_level,
            accumulated_sp=0,
            sp_per_minute=25.0,
        )

    assert excinfo.type is InvalidSkillLevelError


@pytest.mark.parametrize("sp_per_minute", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_training_speed_is_rejected(sp_per_minute: float) -> None:
    with pytest.raises(InvalidSkillSpeedError) as excinfo:
        skill_training_duration(
            rank=1,
            target_level=1,
            accumulated_sp=0,
            sp_per_minute=sp_per_minute,
        )

    assert excinfo.type is InvalidSkillSpeedError


def test_rank_below_the_ladder_propagates_the_rank_error() -> None:
    with pytest.raises(InvalidSkillRankError) as excinfo:
        skill_training_duration(
            rank=0,
            target_level=1,
            accumulated_sp=0,
            sp_per_minute=25.0,
        )

    assert excinfo.type is InvalidSkillRankError
