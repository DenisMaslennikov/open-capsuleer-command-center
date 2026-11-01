"""Pure domain rules for character skills.

This package holds the shared skill-table logic, the training-speed rule and the
errors its functions raise. It imports nothing from the framework, the database
or the network.
"""

from app.domain.skills.errors import (
    InvalidSkillAttributeError,
    InvalidSkillLevelError,
    InvalidSkillRankError,
)
from app.domain.skills.sp_rate import skill_sp_per_minute
from app.domain.skills.sp_table import accumulated_skill_sp, skill_sp_to_next_level

__all__ = [
    "InvalidSkillAttributeError",
    "InvalidSkillLevelError",
    "InvalidSkillRankError",
    "accumulated_skill_sp",
    "skill_sp_per_minute",
    "skill_sp_to_next_level",
]
