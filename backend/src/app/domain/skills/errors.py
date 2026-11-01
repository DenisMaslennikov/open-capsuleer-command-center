"""Shared domain errors for invalid skill levels, ranks and training inputs.

The SP table and training-duration functions raise these when called with
values the game rules reject: a trained level outside the function's valid
range (0..5, or 1..4 for the step function), a skill rank below 1, an
accumulated SP amount that is negative and a training speed that is not
positive. All subclass ValueError so callers can catch the whole family with
a single except clause.
"""

__all__ = [
    "InvalidAccumulatedSkillSpError",
    "InvalidSkillAttributeError",
    "InvalidSkillLevelError",
    "InvalidSkillRankError",
    "InvalidSkillSpeedError",
]


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
        """

        super().__init__(message)


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
        """

        super().__init__(message)


class InvalidSkillAttributeError(ValueError):
    """Raised when a skill attribute is zero or negative.

    The message names the offending attribute so a caller can surface it verbatim
    to the user.
    """

    def __init__(self, message: str) -> None:
        """Create the error.

        Arguments:
            message: human-readable text naming the invalid attribute, shown verbatim
                to downstream callers.
        """

        super().__init__(message)


class InvalidAccumulatedSkillSpError(ValueError):
    """Raised when the accumulated skill points already trained are negative.

    The message names the invalid argument (the accumulated SP) so a caller can
    surface it verbatim to the user.
    """

    def __init__(self, message: str) -> None:
        """Create the error.

        Arguments:
            message: human-readable text naming the invalid accumulated SP,
                shown verbatim to downstream callers.
        """

        super().__init__(message)


class InvalidSkillSpeedError(ValueError):
    """Raised when the training speed is not positive.

    The message names the invalid argument (the training speed) so a caller can
    surface it verbatim to the user.
    """

    def __init__(self, message: str) -> None:
        """Create the error.

        Arguments:
            message: human-readable text naming the invalid training speed,
                shown verbatim to downstream callers.
        """

        super().__init__(message)
