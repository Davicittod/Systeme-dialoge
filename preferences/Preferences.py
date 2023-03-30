from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List
    from preferences.CriterionName import CriterionName
    from preferences.CriterionValue import CriterionValue
    from preferences.Value import Value

import numpy as np

from preferences.Item import Item


class Preferences:
    """Preferences class.
    This class implements the preferences of an agent.

    attr:
        criterion_name_list: the list of criterion name (ordered by importance)
        criterion_value_list: the list of criterion value
    """

    def __init__(self):
        """Creates a new Preferences object."""
        self.__criterion_name_list: List[CriterionName] = []
        self.__criterion_value_list: List[CriterionValue] = []

    def get_criterion_name_list(self) -> List[CriterionName]:
        """Returns the list of criterion name."""
        return self.__criterion_name_list

    def get_criterion_value_list(self) -> List[CriterionValue]:
        """Returns the list of criterion value."""
        return self.__criterion_value_list

    def set_criterion_name_list(self, criterion_name_list: List[CriterionName]):
        """Sets the list of criterion name."""
        self.__criterion_name_list = criterion_name_list

    def add_criterion_value(self, criterion_value: CriterionValue):
        """Adds a criterion value in the list."""
        self.__criterion_value_list.append(criterion_value)

    def get_value(self, item: Item, criterion_name: CriterionName) -> Value | None:
        """Gets the value for a given item and a given criterion name."""
        for value in self.__criterion_value_list:
            if (
                value.get_item() == item
                and value.get_criterion_name() == criterion_name
            ):
                return value.get_value()
        return None

    def is_preferred_criterion(
        self, criterion_name_1: CriterionName, criterion_name_2: CriterionName
    ) -> bool:
        """Returns if a criterion 1 is preferred to the criterion 2."""
        for criterion_name in self.__criterion_name_list:
            if criterion_name == criterion_name_1:
                return True
            if criterion_name == criterion_name_2:
                return False

    def is_preferred_item(self, item_1: Item, item_2: Item) -> bool:
        """Returns if the item 1 is preferred to the item 2."""
        return item_1.get_score(self) > item_2.get_score(self)

    def most_preferred(self, item_list: List[Item]) -> Item:
        """Returns the most preferred item from a list."""
        best_item_index = np.argmax(map(lambda item: item.get_score(self), item_list))
        return item_list[best_item_index]

    def is_item_among_top_10_percent(self, item: Item, item_list: List[Item]) -> bool:
        """
        Return whether a given item is among the top 10 percent of the preferred items.

        :return: a boolean, True means that the item is among the favourite ones
        """
        item_list_scores = list(map(lambda item: item.get_score(self), item_list))
        max_score = np.max(item_list_scores)
        if item.get_score(self) >= 0.9 * max_score:
            return True
        return False
