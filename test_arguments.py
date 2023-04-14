from arguments.Argument import Argument
from arguments.Comparison import Comparison
from arguments.CoupleValue import CoupleValue
from preferences.CriterionName import CriterionName
from preferences.CriterionValue import CriterionValue
from preferences.Item import Item
from preferences.Preferences import Preferences
from preferences.Value import Value
from pw_argumentation import ArgumentAgent

if __name__ == "__main__":
    comparaison = Comparison(CriterionName.CONSUMPTION, CriterionName.DURABILITY)
    print(comparaison)

    couple_value = CoupleValue(CriterionName.CONSUMPTION, Value.BAD)
    print(couple_value)

    argument = Argument(False, Item("Item", "Description"))
    argument.set_premiss_couple_value(CriterionName.CONSUMPTION, Value.BAD)
    argument.set_premiss_comparison(CriterionName.CONSUMPTION, CriterionName.DURABILITY)
    print(argument)

    argument = Argument(True, Item("Item", "Description"))
    argument.set_premiss_couple_value(CriterionName.CONSUMPTION, Value.BAD)
    print(argument)

    item = Item("item", "desc")
    preferences = Preferences()
    preferences.set_criterion_name_list(
        [
            CriterionName.ENVIRONMENT_IMPACT,
            CriterionName.NOISE,
            CriterionName.CONSUMPTION,
            CriterionName.DURABILITY,
            CriterionName.PRODUCTION_COST,
        ]
    )
    preferences.add_criterion_value(
        CriterionValue(item, CriterionName.ENVIRONMENT_IMPACT, Value.VERY_GOOD)
    )
    preferences.add_criterion_value(
        CriterionValue(item, CriterionName.NOISE, Value.VERY_BAD)
    )
    preferences.add_criterion_value(
        CriterionValue(item, CriterionName.CONSUMPTION, Value.GOOD)
    )
    preferences.add_criterion_value(
        CriterionValue(item, CriterionName.DURABILITY, Value.BAD)
    )
    agent = ArgumentAgent(0, None, "Agent", preferences, [item])
    print(agent.list_supporting_proposal(item))
    print(agent.list_attacking_proposal(item))
