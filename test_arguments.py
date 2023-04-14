from arguments.Comparison import Comparison
from arguments.CoupleValue import CoupleValue
from preferences.CriterionName import CriterionName
from preferences.Value import Value

if __name__ == "__main__":
    comp = Comparison(CriterionName.CONSUMPTION, CriterionName.DURABILITY)
    print(comp)

    couple_value = CoupleValue(CriterionName.CONSUMPTION, Value.BAD)
    print(couple_value)
