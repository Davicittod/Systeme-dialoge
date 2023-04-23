import random
from typing import List, Tuple

from mesa import Model
from mesa.time import RandomActivation

from arguments.Argument import Argument
from arguments.CoupleValue import CoupleValue
from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative
from communication.message.MessageService import MessageService
from loader import load_json
from preferences.Item import Item
from preferences.Preferences import Preferences
from preferences.Value import Value


class ArgumentAgent(CommunicatingAgent):
    """ArgumentAgent which inherit from CommunicatingAgent ."""

    def __init__(
        self,
        unique_id: int,
        model: Model,
        name: str,
        preferences: Preferences,
        item_list: List[Item],
        agent_to_propose_to: str | None = None,
    ):
        super().__init__(unique_id, model, name)
        self.__preference: Preferences = preferences
        self.__item_list = item_list
        self.__agent_to_propose_to = agent_to_propose_to

    def send_message(self, message: Message):
        print(message)
        return super().send_message(message)

    def step(self):
        super().step()

        if self.__agent_to_propose_to != None:
            # Propose an item that is acceptable to the agent
            item_choices = list(
                filter(
                    lambda item: self.get_preference().is_item_among_top_10_percent(
                        item, self.__item_list
                    ),
                    self.__item_list,
                )
            )
            print(item_choices)
            self.send_message(
                Message(
                    self.get_name(),
                    self.__agent_to_propose_to,
                    MessagePerformative.PROPOSE,
                    random.choice(item_choices),
                )
            )
            self.__agent_to_propose_to = None

        messages = self.get_new_messages()
        for message in messages:
            match message.get_performative():
                case MessagePerformative.PROPOSE:
                    item: Item = message.get_content()
                    # We check wether is of the 10% preferred item
                    if self.get_preference().is_item_among_top_10_percent(
                        item, self.__item_list
                    ):
                        self.send_message(
                            Message(
                                self.get_name(),
                                message.get_exp(),
                                MessagePerformative.ACCEPT,
                                item,
                            )
                        )
                    else:
                        self.send_message(
                            Message(
                                self.get_name(),
                                message.get_exp(),
                                MessagePerformative.ASK_WHY,
                                item,
                            )
                        )
                case MessagePerformative.ACCEPT:
                    item: Item = message.get_content()
                    self.send_message(
                        Message(
                            self.get_name(),
                            message.get_exp(),
                            MessagePerformative.COMMIT,
                            item,
                        )
                    )
                    self.__item_list.remove(item)

                case MessagePerformative.COMMIT:
                    item: Item = message.get_content()
                    if item in self.__item_list:
                        self.send_message(
                            Message(
                                self.get_name(),
                                message.get_exp(),
                                MessagePerformative.COMMIT,
                                item,
                            )
                        )
                        self.__item_list.remove(item)

                case MessagePerformative.ASK_WHY:
                    item: Item = message.get_content()
                    self.send_message(
                        Message(
                            self.get_name(),
                            message.get_exp(),
                            MessagePerformative.ARGUE,
                            (item, self.support_proposal(item)),
                        )
                    )

                case MessagePerformative.CANCEL:
                    pass

                case MessagePerformative.ARGUE:
                    message_content: Tuple[Item, Argument] = message.get_content()
                    item, argument = message_content

                    # If the argument is positive toward the item
                    if argument.boolean_decision:
                        # Check if the item is acceptable
                        if self.get_preference().is_item_among_top_10_percent(
                            item, self.__item_list
                        ):
                            # Accept the item
                            self.send_message(
                                Message(
                                    self.get_name(),
                                    message.get_exp(),
                                    MessagePerformative.ACCEPT,
                                    item,
                                )
                            )
                        else:
                            # The item is not acceptable, create a counter argument
                            counter_argument = self.attack_argument(argument)
                            self.send_message(
                                Message(
                                    self.get_name(),
                                    message.get_exp(),
                                    MessagePerformative.ARGUE,
                                    (counter_argument.item, counter_argument),
                                )
                            )

                    # The received argument is a counter argument against the item
                    else:
                        # The other agent doesnt want this item,
                        # Check if another item is acceptable by this agent to propose it
                        item_choices = filter(
                            lambda item: item != argument.item, self.__item_list
                        )
                        item_choices = filter(
                            lambda item: self.get_preference().is_item_among_top_10_percent(
                                item, self.__item_list
                            ),
                            item_choices,
                        )

                        item_choices = list(item_choices)
                        if len(item_choices) == 0:
                            # If there are no valid items, CANCEL the argumentation
                            self.send_message(
                                Message(
                                    self.get_name(),
                                    message.get_exp(),
                                    MessagePerformative.CANCEL,
                                    "",
                                )
                            )
                        else:
                            new_item = random.choice(item_choices)
                            self.send_message(
                                Message(
                                    self.get_name(),
                                    message.get_exp(),
                                    MessagePerformative.PROPOSE,
                                    new_item,
                                )
                            )

                case _:
                    print("Message not supported:", message)

    def get_preference(self) -> Preferences:
        return self.__preference

    def list_supporting_proposal(self, item: Item) -> List[CoupleValue]:
        result = []
        for criterion in self.get_preference().get_criterion_name_list():
            value = self.get_preference().get_value(item, criterion)
            if value == Value.GOOD or value == Value.VERY_GOOD:
                result.append(CoupleValue(criterion, value))
        return result

    def list_attacking_proposal(self, item: Item) -> List[CoupleValue]:
        result = []
        for criterion in self.get_preference().get_criterion_name_list():
            value = self.get_preference().get_value(item, criterion)
            if value == Value.BAD or value == Value.VERY_BAD:
                result.append(CoupleValue(criterion, value))
        return result

    def support_proposal(self, item: Item) -> Argument:
        argument = Argument(True, item)
        premise: CoupleValue = self.list_supporting_proposal(item)[0]
        argument.set_premiss_couple_value(premise.criterion_name, premise.value)
        return argument

    def attack_argument(self, argument: Argument) -> Argument:
        argument_criterion = argument.couple_value.criterion_name
        argument_value = argument.couple_value.value
        argument_item = argument.item

        value = self.get_preference().get_value(argument_item, argument_criterion)

        # Only the top criterion is considered important
        top_priority_criterion = self.get_preference().get_criterion_name_list()[0]
        top_priority_criterion_value = self.get_preference().get_value(
            argument_item, top_priority_criterion
        )

        # If the criterion is important for him
        if argument_criterion == top_priority_criterion:
            # Check if the criterion value is bad
            if value == Value.BAD or value == Value.VERY_BAD:
                argument = Argument(False, argument_item)
                argument.set_premiss_couple_value(argument_criterion, value)
                return argument

        # Check if the top criterion is bad
        if (
            top_priority_criterion_value == Value.VERY_BAD
            or top_priority_criterion_value == Value.BAD
        ):
            argument = Argument(False, argument_item)
            argument.set_premiss_couple_value(
                top_priority_criterion, top_priority_criterion_value
            )
            argument.set_premiss_comparison(top_priority_criterion, argument_criterion)
            return argument


class ArgumentModel(Model):
    """ArgumentModel which inherit from Model ."""

    def __init__(self, path: str):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)

        (items, agents_data) = load_json(path)

        start_index = random.randint(0, 1)

        names = [agent_data[0] for agent_data in agents_data]
        agent_to_propose = names[start_index]
        agent_to_propose_to = names[1 - start_index]

        agents = [
            ArgumentAgent(
                self.next_id(),
                self,
                names[index],
                agent_data[1],
                items.copy(),
                agent_to_propose_to if names[index] == agent_to_propose else None,
            )
            for index, agent_data in enumerate(agents_data)
        ]

        # Add to schedule
        for agent in agents:
            self.schedule.add(agent)

        self.running = True

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()


if __name__ == "__main__":
    NUMBER_OF_STEPS = 10

    argument_model = ArgumentModel("./environment.json")
    for i in range(NUMBER_OF_STEPS):
        argument_model.step()
