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
        self.comparison_list: List[Comparison] = []
        self.couple_values_list: List[CoupleValue] = []

    def add_premiss_comparison(
        self, best_criterion_name: CriterionName, worst_criterion_name: CriterionName
    ):
        """Adds a premiss comparison in the comparison list ."""
        self.comparison_list.append(
            Comparison(best_criterion_name, worst_criterion_name)
        )

    def add_premiss_couple_values(self, criterion_name: CriterionName, value: Value):
        """Add a premiss couple values in the couple values list ."""
        self.couple_values_list.append(CoupleValue(criterion_name, value))

    def __str__(self) -> str:
        neg = "" if self.boolean_decision else "not"
        couple_values = ", ".join(map(str, self.couple_values_list))
        comparaisons = ", ".join(map(str, self.comparison_list))
        return f"{neg} {self.item.get_name()} <= {couple_values}, {comparaisons}"

    def __repr__(self) -> str:
        return str(self)
