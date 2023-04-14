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
        agent_to_propose: str | None = None,
    ):
        super().__init__(unique_id, model, name)
        self.__preference: Preferences = preferences
        self.__item_list = item_list
        self.__agent_to_propose = agent_to_propose

    def send_message(self, message: Message):
        print(message)
        return super().send_message(message)

    def step(self):
        super().step()

        if self.__agent_to_propose != None:
            self.send_message(
                Message(
                    self.get_name(),
                    self.__agent_to_propose,
                    MessagePerformative.PROPOSE,
                    random.choice(self.__item_list),
                )
            )
            self.__agent_to_propose = None

        messages = self.get_new_messages()
        for message in messages:
            match message.get_performative():
                case MessagePerformative.PROPOSE:
                    item: Item = message.get_content()
                    # We check wether is of the 10% preferred item
                    if self.__preference.is_item_among_top_10_percent(
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

                case MessagePerformative.ARGUE:
                    message_content: Tuple[Item, Argument] = message.get_content()
                    item, argument = message_content
                    counter_argument = self.attack_argument(argument)
                    self.send_message(
                        Message(
                            self.get_name(),
                            message.get_exp(),
                            MessagePerformative.ARGUE,
                            (item, counter_argument),
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

    def attack_argument(self, argument: Argument) -> Argument | None:
        argument_criterion = argument.couple_value.criterion_name
        argument_value = argument.couple_value.value
        argument_item = argument.item
        argument_boolean_decision = argument.boolean_decision

        value = self.get_preference().get_value(argument_item, argument_criterion)

        if value == Value.BAD or value == Value.VERY_BAD:
            argument = Argument(not argument_boolean_decision, argument_item)
            argument.set_premiss_couple_value(argument_criterion, value)
            return argument

        pass


class ArgumentModel(Model):
    """ArgumentModel which inherit from Model ."""

    def __init__(self, path: str):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)

        (items, agents_data) = load_json(path)

        for index, agent_data in enumerate(agents_data):
            other_agent = None
            if index == 0:
                other_agent = random.choice(agents_data[1:])[0]
            agent = ArgumentAgent(
                self.next_id(),
                self,
                agent_data[0],
                agent_data[1],
                items.copy(),
                other_agent,
            )
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
