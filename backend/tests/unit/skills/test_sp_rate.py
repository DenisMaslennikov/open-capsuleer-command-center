import pytest

from app.domain.skills.errors import InvalidSkillAttributeError
from app.domain.skills.sp_rate import skill_sp_per_minute


class TestSkillSpPerMinute:
    @pytest.mark.parametrize(
        ("primary", "secondary", "expected"),
        [
            (17, 17, 25.5),
            (27, 21, 37.5),
            (32, 26, 45.0),
            (21, 17, 29.5),
        ],
    )
    def test_returns_correct_sp_per_minute(self, primary: int, secondary: int, expected: float):
        assert skill_sp_per_minute(primary=primary, secondary=secondary) == expected

    @pytest.mark.parametrize(
        ("primary", "secondary"),
        [
            (0, 0),
            (17, -1),
            (-5, 17),
        ],
    )
    def test_raises_invalid_skill_attribute_error(self, primary: int, secondary: int):
        with pytest.raises(InvalidSkillAttributeError):
            skill_sp_per_minute(primary=primary, secondary=secondary)
