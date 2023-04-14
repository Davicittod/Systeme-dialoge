from preferences.CriterionName import CriterionName
from preferences.Value import Value


class CoupleValue:
    """CoupleValue class .
    This class implements a couple value used in argument object .

    attr :
    criterion_name :
    10 value :
    """

    def __init__(self, criterion_name: CriterionName, value: Value):
        """Creates a new couple value ."""
        self.criterion_name = criterion_name
        self.value = value

    def __str__(self) -> str:
        return f"{self.criterion_name.name} = {self.value.name}"

    def __repr__(self) -> str:
        return str(self)
