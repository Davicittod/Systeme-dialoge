from typing import List

from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
from loader import load_json
from preferences.Item import Item
from preferences.Preferences import Preferences


class ArgumentAgent(CommunicatingAgent):
    """ArgumentAgent which inherit from CommunicatingAgent ."""

    def __init__(
        self, unique_id: int, model: Model, name: str, preferences: Preferences
    ):
        super().__init__(unique_id, model, name)
        self.__preference: Preferences = preferences

    def step(self):
        super().step()

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

        for agent_data in agents_data:
            agent = ArgumentAgent(self.next_id(), self, agent_data[0], agent_data[1])
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
