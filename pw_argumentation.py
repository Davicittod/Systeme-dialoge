import random
from typing import List, Self

from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative
from communication.message.MessageService import MessageService
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
        other_agent: Self = None,
        start_propose: bool=False, 
    ):
        super().__init__(unique_id, model, name, preferences)
        self.preference: Preferences = preferences
        self.start_propose = start_propose
        self.item_list = item_list
        self.other_agent = other_agent
        self.has_proposed = False

    def step(self):
        super().step()
        if self.start_propose:
            message = Message(self.get_name(), 
                              self.other_agent.get_name(), 
                              MessagePerformative.PROPOSE, 
                              random.choice(self.item_list))
            self.send_message(Message)
            print(message)
            self.start_propose = False

        messages = self.get_new_messages()
        for message in messages:
            match message.get_performative():
                case MessagePerformative.PROPOSE:
                    self.other_agent = message.get_exp()
                    item = message[0].get_content()
                    message = Message(self.get_name(), 
                                        self.other_agent.get_name(), 
                                        MessagePerformative.ACCEPT, 
                                        item)
                    self.send_message(message)
                    print(Message)
                case _:
                    print("Message not supported")

    def get_preference(self) -> Preferences:
        return self.preference

    def generate_preferences(self, item_list: List[Item]):
        # see question 3
        # To be completed
        pass


class ArgumentModel(Model):
    """ArgumentModel which inherit from Model ."""

    def __init__(self):
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)
        # To be completed
        #
        # a = ArgumentAgent ( id , " agent_name ")
        # a . generate_preferences ( preferences )
        # self . schedule . add ( a )
        # ...
        self.running = True

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()


if __name__ == "__main__":
    argument_model = ArgumentModel()
# To be completed
