#!/usr/bin/env python3
import numpy as np


class Preferences:
    """Preferences class.
    This class implements the preferences of an agent.

    attr:
        criterion_name_list: the list of criterion name (ordered by importance)
        criterion_value_list: the list of criterion value
    """

    def __init__(self):
        """Creates a new Preferences object."""
        self.__criterion_name_list = []
        self.__criterion_value_list = []

    def get_criterion_name_list(self):
        """Returns the list of criterion name."""
        return self.__criterion_name_list

    def get_criterion_value_list(self):
        """Returns the list of criterion value."""
        return self.__criterion_value_list

    def set_criterion_name_list(self, criterion_name_list):
        """Sets the list of criterion name."""
        self.__criterion_name_list = criterion_name_list

    def add_criterion_value(self, criterion_value):
        """Adds a criterion value in the list."""
        self.__criterion_value_list.append(criterion_value)

    def get_value(self, item, criterion_name):
        """Gets the value for a given item and a given criterion name."""
        for value in self.__criterion_value_list:
            if (
                value.get_item() == item
                and value.get_criterion_name() == criterion_name
            ):
                return value.get_value()
        return None

    def is_preferred_criterion(self, criterion_name_1, criterion_name_2):
        """Returns if a criterion 1 is preferred to the criterion 2."""
        for criterion_name in self.__criterion_name_list:
            if criterion_name == criterion_name_1:
                return True
            if criterion_name == criterion_name_2:
                return False

    def is_preferred_item(self, item_1, item_2):
        """Returns if the item 1 is preferred to the item 2."""
        return item_1.get_score(self) > item_2.get_score(self)

    def most_preferred(self, item_list):
        """Returns the most preferred item from a list."""
        best_item_index = np.argmax(map(lambda item: item.get_score(self), item_list))
        return item_list[best_item_index]

    def is_item_among_top_10_percent(self, item, item_list):
        """
        Return whether a given item is among the top 10 percent of the preferred items.

        :return: a boolean, True means that the item is among the favourite ones
        """
        item_list_scores = list(map(lambda item: item.get_score(self), item_list))
        max_score = np.max(item_list_scores)
        if item.get_score(self) >= 0.9 * max_score:
            return True
        return False
