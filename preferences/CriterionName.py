from enum import Enum
from typing import Self


class CriterionName(Enum):
    """CriterionName enum class.
    Enumeration containing the possible CriterionName.
    """

    PRODUCTION_COST = 0
    CONSUMPTION = 1
    DURABILITY = 2
    ENVIRONMENT_IMPACT = 3
    NOISE = 4
