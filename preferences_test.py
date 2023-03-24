from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Item import Item
from communication.preferences.Preferences import Preferences
from communication.preferences.Value import Value

if __name__ == "__main__":
    """Testing the Preferences class."""
    agent_pref = Preferences()
    agent_pref.set_criterion_name_list(
        [
            CriterionName.PRODUCTION_COST,
            CriterionName.ENVIRONMENT_IMPACT,
            CriterionName.CONSUMPTION,
            CriterionName.DURABILITY,
            CriterionName.NOISE,
        ]
    )

    diesel_engine = Item("Diesel Engine", "A super cool diesel engine")
    agent_pref.add_criterion_value(
        CriterionValue(diesel_engine, CriterionName.PRODUCTION_COST, Value.VERY_GOOD)
    )
    agent_pref.add_criterion_value(
        CriterionValue(diesel_engine, CriterionName.CONSUMPTION, Value.GOOD)
    )
    agent_pref.add_criterion_value(
        CriterionValue(diesel_engine, CriterionName.DURABILITY, Value.VERY_GOOD)
    )
    agent_pref.add_criterion_value(
        CriterionValue(diesel_engine, CriterionName.ENVIRONMENT_IMPACT, Value.VERY_BAD)
    )
    agent_pref.add_criterion_value(
        CriterionValue(diesel_engine, CriterionName.NOISE, Value.VERY_BAD)
    )

    electric_engine = Item("Electric Engine", "A very quiet engine")
    agent_pref.add_criterion_value(
        CriterionValue(electric_engine, CriterionName.PRODUCTION_COST, Value.BAD)
    )
    agent_pref.add_criterion_value(
        CriterionValue(electric_engine, CriterionName.CONSUMPTION, Value.VERY_BAD)
    )
    agent_pref.add_criterion_value(
        CriterionValue(electric_engine, CriterionName.DURABILITY, Value.GOOD)
    )
    agent_pref.add_criterion_value(
        CriterionValue(
            electric_engine, CriterionName.ENVIRONMENT_IMPACT, Value.VERY_GOOD
        )
    )
    agent_pref.add_criterion_value(
        CriterionValue(electric_engine, CriterionName.NOISE, Value.VERY_GOOD)
    )

    """test list of preferences"""
    print(diesel_engine)
    print(electric_engine)
    print(diesel_engine.get_value(agent_pref, CriterionName.PRODUCTION_COST))
    print(
        agent_pref.is_preferred_criterion(
            CriterionName.CONSUMPTION, CriterionName.NOISE
        )
    )
    print(
        "Electric Engine > Diesel Engine : {}".format(
            agent_pref.is_preferred_item(electric_engine, diesel_engine)
        )
    )
    print(
        "Diesel Engine > Electric Engine : {}".format(
            agent_pref.is_preferred_item(diesel_engine, electric_engine)
        )
    )
    print(
        "Electric Engine (for agent 1) = {}".format(
            electric_engine.get_score(agent_pref)
        )
    )
    print(
        "Diesel Engine (for agent 1) = {}".format(diesel_engine.get_score(agent_pref))
    )
    print(
        "Most preferred item is : {}".format(
            agent_pref.most_preferred([diesel_engine, electric_engine]).get_name()
        )
    )
    print(
        "Is Diesel Engine in top 10%:",
        agent_pref.is_item_among_top_10_percent(
            diesel_engine, [diesel_engine, electric_engine]
        ),
    )
    print(
        "Is Electric Engine in top 10%:",
        agent_pref.is_item_among_top_10_percent(
            electric_engine, [diesel_engine, electric_engine]
        ),
    )
