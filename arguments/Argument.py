from typing import List

from arguments.Comparison import Comparison
from arguments.CoupleValue import CoupleValue
from preferences.CriterionName import CriterionName
from preferences.Item import Item
from preferences.Value import Value


class Argument:
    """Argument class .
    This class implements an argument used during the interaction .

    attr :
    decision :
    item :
    comparison_list :
    couple_values_list :
    """

    def __init__(self, boolean_decision: bool, item: Item):
        """Creates a new Argument ."""
        self.boolean_decision = boolean_decision
        self.item = item
        self.comparison: Comparison = None
        self.couple_value: CoupleValue = None

    def set_premiss_comparison(
        self, best_criterion_name: CriterionName, worst_criterion_name: CriterionName
    ):
        """Adds a premiss comparison in the comparison list ."""
        self.comparison = Comparison(best_criterion_name, worst_criterion_name)

    def set_premiss_couple_value(self, criterion_name: CriterionName, value: Value):
        """Add a premiss couple values in the couple values list ."""
        self.couple_value = CoupleValue(criterion_name, value)

    def __str__(self) -> str:
        neg = "" if self.boolean_decision else "not "

        premises = [self.couple_value]
        if self.comparison != None:
            premises.append(self.comparison)
        premises = ", ".join(map(str, premises))

        return f"{neg}{self.item.get_name()} <= {premises}"

    def __repr__(self) -> str:
        return str(self)
