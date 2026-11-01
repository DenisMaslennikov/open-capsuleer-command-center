from app.domain.skills.errors import InvalidSkillAttributeError


def skill_sp_per_minute(*, primary: int, secondary: int) -> float:
    """
    Compute skill SP per minute as ``primary + secondary / 2``.

    Uses true division, so the result is always a float; no rounding is applied.

    :param primary: Primary skill attribute value.
    :param secondary: Secondary skill attribute value.
    :return: SP per minute as a float.
    :raises InvalidSkillAttributeError: If either attribute is zero or negative.
    """
    if primary <= 0:
        raise InvalidSkillAttributeError(f"primary attribute must be positive, got {primary}")
    if secondary <= 0:
        raise InvalidSkillAttributeError(f"secondary attribute must be positive, got {secondary}")
    return primary + secondary / 2
