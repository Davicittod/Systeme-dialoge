import json
from typing import Dict, List, Tuple

from preferences.CriterionName import CriterionName
from preferences.CriterionValue import CriterionValue
from preferences.Item import Item
from preferences.Preferences import Preferences
from preferences.Value import Value


def load_json(path: str) -> Tuple[List[Item], List[Tuple[str, Preferences]]]:
    with open(path, "r") as f:
        environment_json: Dict = json.load(f)

    items: List[Item] = [
        Item(item_json["name"], item_json["description"])
        for item_json in environment_json["items"]
    ]

    agents = [
        __load_agent(agent_json, items) for agent_json in environment_json["agents"]
    ]

    return (items, agents)


def __load_agent(agent_json: Dict, items: List[Item]) -> Tuple[str, Preferences]:
    name: str = agent_json["name"]

    preferences: Preferences = Preferences()
    preferences.set_criterion_name_list(
        [
            CriterionName[preference_json]
            for preference_json in agent_json["preferences"]
        ]
    )

    performance_json: Dict = agent_json["performance"]
    for item in items:
        item_performance_json: Dict = performance_json[item.get_name()]
        for crit_name, value in item_performance_json.items():
            preferences.add_criterion_value(
                CriterionValue(item, CriterionName[crit_name], Value[value])
            )

    return (name, preferences)


if __name__ == "__main__":
    environment = load_json("./environment.json")

    print("Items:")
    for item in environment[0]:
        print("-", item)

    print()

    print("Agents:")
    for agent in environment[1]:
        print("", "Name:", agent[0])
        print("", "Preferences:")
        preferences = agent[1]
        print("", "", "Criterion Order:")
        for criterion_name in preferences.get_criterion_name_list():
            print("", "", "", "-", criterion_name)
        print("", "", "Criterion Values:")
        for criterion_value in preferences.get_criterion_value_list():
            print(
                "",
                "",
                "",
                "-",
                f"{criterion_value.get_item().get_name(): <10}",
                f"{criterion_value.get_criterion_name(): <40}",
                criterion_value.get_value(),
            )
        print()
