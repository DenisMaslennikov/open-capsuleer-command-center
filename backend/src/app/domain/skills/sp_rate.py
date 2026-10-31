from typing import final

from app.domain.skills.errors import InvalidSkillAttributeError


def skill_sp_per_minute(*, primary: int, secondary: int) -> float:
    """
    Compute skill SP per minute as (primary + secondary) / 2.

    :param primary: Primary skill attribute value.
    :param secondary: Secondary skill attribute value.
    :return: SP per minute as a float.
    :raises InvalidSkillAttributeError: If either attribute is zero or negative.
    """
    raise NotImplementedError
