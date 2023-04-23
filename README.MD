# Argumentation-based interacion Model

Carl RIZK

David DE LA HERA CARRETERO

# Summary

This project simulates the interactions between multiple agents, with the goal of persuading another agent to accept an item according to specific criteria.

During each round of the simulation, agents exchange messages based on the information they have received. Each agent has a unique set of preferences, which they can use to either persuade the other agent or reject their argumentation during these conversations.

# Preferences class

This class implements the preferences of an agent.

## Attributes

Includes two attributes:

- `criterion_name_list`: the list of criterion name (ordered by importance)
- `criterion_value_list`: the list of criterion value

## Methods

The methods implemented are the following:

- `most_preferred`: returns the most preferred criterion of the item list
- `is_item_among_top_10_percent`: Return whether a given item is at least 0.9 times the highest score among the items.

# Argument Model class

## Methods

In the **init** method we initialize the preferences for each agent from a json so we could work with that. You can see the implementation in the code.

# Argument class

This class implements an argument used during the interaction between two agents.

## Methods

- `set_premiss_comparison`: adds a premiss comparison in the comparison list.
- `set_premiss_couple_value`: adds a premiss couple value in the couple value list.

# Auxiliar classes for the Argument class

## Comparison class

Implements the comparison between two criterion.

### Attributes

- `best_criterion_name`: the name of the best criterion
- `worst_criterion_name`: the name of the worst criterion

## CoupleValue class

Implements the class with the couple value used in argument objects

### Attributes

- `criterion_name`: the name of the criterion
- `value`: the value of the criterion

# Argument Agent class

This agent inherits from the ComunicatingAgent class, and implements the argumentation-based interaction model.

## Attributes

- `preferences`: the preferences of the agent
- `item_list`: the list of items that the agent can propose to the other agent
- `agent_to_propose_to`: the agent to whom the agent will propose an item, it is used also to define the agent that will start the conversation.

## Methods

- `get_preferences`: returns the preferences of the agent, arleady implemented in the jdon with the information.
- `step`: the method that is called at each step of the simulation. We had to work with different situations depending on the received messages:
  - `propose`: the agent receives a proposal from the other agent. He can accept or reject it depending on whether this item is in his top 10% or not. If he doesn't accept, he will send an ask_why message.
  - `accept`: the agent receives an accept message from the other agent. He will send back a commit message to confirm the acceptation of the item and will remove the item from his item list so he won't keep commiting later with the other agent.
  - `commit`: the agent receives a commit message from the other agent, checks whether he has yet the item in the list and if the answer is possitive, sends a commit back and removes the item from the list.
  - `ask_why`: the agent receives an ask_why message from the other agent. He will send back an argue message se he can convince him thanks to the `support_proposal` method.
  - `argue`: the agent receives an argue message from the other agent. First, it will check whether the argument is positive or negative towards the item. If it is positive, we will check if the item is in the top 10% of the agent's preferences and we will accept it, otherwise we will send an `argue` message with a counter argument thanks to the `attack_argument` method. If it is negative, the agent checks whether there is another item to propose, otherwise he will send a `cancel` message, finishing the loop of messages.
- `support_proposal`: returns an argument that supports the proposal of the agent, based on the preferences that are good or very good for him.
- `list_supporting_proposal`: returns a list of criterions that can be used as premisses to support the proposal of the agent.
- `attack_argument`: returns an argument that attacks the argument of the other agent, based on the preferences that are bad or very bad for him or if the top criterion of the item is bad for him.
- `list_attacking_argument`: returns a list of criterions that can be used as premisses to attack the item proposed by the other agent.
