import random
from typing import List

from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative
from communication.message.MessageService import MessageService
from loader import load_json
from preferences.Item import Item
from preferences.Preferences import Preferences


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
            item: Item = message.get_content()
            match message.get_performative():
                case MessagePerformative.PROPOSE:
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
                    self.send_message(
                        Message(
                            self.get_name(),
                            message.get_exp(),
                            MessagePerformative.ARGUE,
                            item,
                        )
                    )

                case _:
                    print("Message not supported:", message)

    def get_preference(self) -> Preferences:
        return self.__preference

    def generate_preferences(self, item_list: List[Item]):
        # see question 3
        # To be completed
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
