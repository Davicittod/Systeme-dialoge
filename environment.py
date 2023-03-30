from loader import load_json

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
