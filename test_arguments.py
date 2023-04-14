from arguments.Argument import Argument
from arguments.Comparison import Comparison
from arguments.CoupleValue import CoupleValue
from preferences.CriterionName import CriterionName
from preferences.Item import Item
from preferences.Value import Value

if __name__ == "__main__":
    comparaison = Comparison(CriterionName.CONSUMPTION, CriterionName.DURABILITY)
    print(comparaison)

    couple_value = CoupleValue(CriterionName.CONSUMPTION, Value.BAD)
    print(couple_value)

    argument = Argument(False, Item("Item", "Description"))
    argument.add_premiss_comparison(CriterionName.CONSUMPTION, CriterionName.DURABILITY)
    argument.add_premiss_couple_values(CriterionName.CONSUMPTION, Value.BAD)
    print(argument)
