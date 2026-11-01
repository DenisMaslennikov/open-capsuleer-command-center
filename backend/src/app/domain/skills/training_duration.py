"""Time needed to train a skill level at a given speed.

The estimate is the skill points still missing for the target level divided
by the training speed. The missing points come from the SP table totals in
the sibling ``sp_table`` module; the speed is passed in by the caller in SP
per minute.
"""

from datetime import timedelta
import math

from app.domain.skills.errors import (
    InvalidAccumulatedSkillSpError,
    InvalidSkillLevelError,
    InvalidSkillSpeedError,
)
from app.domain.skills.sp_table import accumulated_skill_sp

__all__ = ["skill_training_duration"]


def skill_training_duration(
    *,
    rank: int,
    target_level: int,
    accumulated_sp: int,
    sp_per_minute: float,
) -> timedelta:
    """Return how long it takes to train a skill to a target level.

    Arguments:
        rank: skill rank, at least 1.
        target_level: trained skill level to reach, 1 through 5.
        accumulated_sp: skill points already spent on the skill, at least 0.
        sp_per_minute: training speed in SP per minute, positive.

    Returns:
        The time between now and the moment the target level is reached; zero
        when the accumulated SP already covers the level.

    Raises:
        InvalidSkillLevelError: when ``target_level`` is outside 1..5.
        InvalidSkillRankError: when ``rank`` is below 1.
        InvalidAccumulatedSkillSpError: when ``accumulated_sp`` is negative.
        InvalidSkillSpeedError: when ``sp_per_minute`` is not a finite
            positive number.
    """

    if target_level < 1 or target_level > 5:
        raise InvalidSkillLevelError(f"level {target_level} outside 1..5")
    if accumulated_sp < 0:
        raise InvalidAccumulatedSkillSpError(f"accumulated_sp {accumulated_sp} below 0")
    if not math.isfinite(sp_per_minute) or sp_per_minute <= 0:
        raise InvalidSkillSpeedError(f"sp_per_minute {sp_per_minute} not a positive finite number")

    total_sp = accumulated_skill_sp(rank=rank, level=target_level)
    remaining_sp = max(total_sp - accumulated_sp, 0)
    return timedelta(minutes=remaining_sp / sp_per_minute)
