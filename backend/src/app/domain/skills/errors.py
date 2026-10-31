"""Shared domain errors for invalid skill levels and ranks.

The SP table functions raise these when called with values the game rules
reject: a trained level outside the function's valid range (0..5, or 1..4 for
the step function) and a skill rank below 1. Both subclass ValueError so
callers can catch the whole family with a single except clause.
"""

__all__ = ["InvalidSkillLevelError", "InvalidSkillRankError"]


class InvalidSkillLevelError(ValueError):
    """Raised when a skill level is outside the valid range for the calling function.

    The message names the invalid argument (the level) so a caller can surface
    it verbatim to the user.
    """

    def __init__(self, message: str) -> None:
        """Create the error.

        Arguments:
            message: human-readable text naming the invalid level, shown verbatim
                to downstream callers.

        Raises:
            Nothing; this is the error itself.
        """

        raise NotImplementedError


class InvalidSkillRankError(ValueError):
    """Raised when a skill rank is below 1.

    The message names the invalid argument (the rank) so a caller can surface it
    verbatim to the user.
    """

    def __init__(self, message: str) -> None:
        """Create the error.

        Arguments:
            message: human-readable text naming the invalid rank, shown verbatim
                to downstream callers.

        Raises:
            Nothing; this is the error itself.
        """

        raise NotImplementedError
