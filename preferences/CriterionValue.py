from preferences.CriterionName import CriterionName
from preferences.Item import Item
from preferences.Value import Value


class CriterionValue:
    """CriterionValue class.
    This class implements the CriterionValue object which associates an item with a CriterionName and a Value.
    """

    def __init__(self, item: Item, criterion_name: CriterionName, value: Value):
        """Creates a new CriterionValue."""
        self.__item = item
        self.__criterion_name = criterion_name
        self.__value = value

    def get_item(self) -> Item:
        """Returns the item."""
        return self.__item

    def get_criterion_name(self) -> CriterionName:
        """Returns the criterion name."""
        return self.__criterion_name

    def get_value(self) -> Value:
        """Returns the value."""
        return self.__value
