"""Pure domain rules for character skills.

This package holds the shared skill-table logic and the errors its functions
raise. It imports nothing from the framework, the database or the network.
"""

from app.domain.skills.errors import InvalidSkillLevelError, InvalidSkillRankError

__all__ = ["InvalidSkillLevelError", "InvalidSkillRankError"]
