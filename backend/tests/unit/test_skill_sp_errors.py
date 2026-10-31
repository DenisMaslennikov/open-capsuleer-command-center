"""Unit tests for the shared skill domain errors."""

import pytest

from app.domain.skills import InvalidSkillLevelError, InvalidSkillRankError
from app.domain.skills.errors import (
    InvalidSkillLevelError as ErrorsInvalidSkillLevelError,
)
from app.domain.skills.errors import (
    InvalidSkillRankError as ErrorsInvalidSkillRankError,
)


@pytest.mark.parametrize(
    ("error_class", "message"),
    [
        pytest.param(
            InvalidSkillLevelError,
            "level 6 outside 0..5",
            id="level-outside-range",
        ),
        pytest.param(
            InvalidSkillRankError,
            "rank 0 below 1",
            id="rank-below-one",
        ),
        pytest.param(
            ErrorsInvalidSkillLevelError,
            "level 6 outside 0..5",
            id="level-error-reachable-through-errors-module",
        ),
        pytest.param(
            ErrorsInvalidSkillRankError,
            "rank 0 below 1",
            id="rank-error-reachable-through-errors-module",
        ),
    ],
)
def test_skill_error_subclasses_valueerror_and_keeps_message(error_class, message):
    error = error_class(message)

    assert isinstance(error, ValueError)
    assert str(error) == message
