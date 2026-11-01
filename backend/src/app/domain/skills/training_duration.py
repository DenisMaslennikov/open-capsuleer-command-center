"""Time needed to train a skill level at a given speed.

The estimate is the skill points still missing for the target level divided
by the training speed. The missing points come from the SP table totals, the
speed from the attribute rule; both live in sibling modules of this package.
"""

from datetime import timedelta

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
        InvalidSkillSpeedError: when ``sp_per_minute`` is not positive.
    """

    raise NotImplementedError