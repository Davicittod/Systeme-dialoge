# Argumentation-based interaction Model

Carl RIZK

David DE LA HERA CARRETERO

# Summary

This project simulates the interactions between 2 agents, with the goal of persuading another agent to accept an item according to specific criteria.

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

In the **init** method we initialize the preferences for each agent from a JSON file. A file named `environment.json` is provided with a working example containing:

- 3 items Electic Engine(E), Internal Combustion Engine (ICED) and Gas Engine (GNS)
- 2 agents: A1 prefers items E and ICED, A2 prefers items ICED and GNS
- The agents will always converge on the ICED engine

A random agent is chosen to start the propositions. An agent will never propose or accept an item that is not in his list of most prefered items (see `is_item_among_top_10_percent`).

# Argument class

This class implements an argument used during the interaction between two agents.

## Methods

- `set_premiss_comparison`: sets the premiss comparison.
- `set_premiss_couple_value`: sets the premiss couple.

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
  - `PROPOSE`: the agent receives a proposal from the other agent.
    If the item is in his top 10%, he responds with an `ACCEPT` message, otherwise, he responds with an `ASK_WHY` message.
  - `ACCEPT`: the agent receives an acceptance to a proposition from the other agent. He will send back a `COMMIT` message to confirm the acceptation of the item and will remove the item from his item list so he won't keep commiting later with the other agent.
  - `COMMIT`: the agent receives a commitment to the trade from the other agent, checks whether he has yet the item in the list and if the answer is possitive, sends a commit back and removes the item from the list.
  - `ASK_WHY`: the agent is asked by the other agent why to choose this item. The agent will respond with an `ARGUE` message containing the criterion with the highest order that has a value of `GOOD` or `VERY_GOOD`.
  - `ARGUE`: the agent receives an argument from the other agent. First, it will check whether the argument is positive or negative towards the item:
    - If it is positive, we will check if the item is in the top 10% of the agent's preferences and we will accept it, otherwise he will respond as bellow (checks done in order):
      - If the received argument criterion is his top priority and it's value is `BAD` or `VERY_BAD`, respond with an `ARGUE` message with an argument that is negative toward the item listing the criterion and it's value as a reason.
      - If the received argument criterion is not his top priority, and his most important criterion's value is `BAD` or `VERY_BAD`, respond with an `ARGUE` message with an argument that is negative toward the item listing his best criterion and it's value as a reason and that his criterion is more important than the received criterion.
      - Send a `CANCEL` message.
    - If it is negative, the agent checks whether there is another item in the top 10% to `PROPOSE`, otherwise he will send a `CANCEL` message.
  - `CANCEL`: Ends the conversation.
- `support_proposal`: returns an argument that supports the proposal of the agent, based on the preferences that are good or very good for him.
- `list_supporting_proposal`: returns a list of criterions that can be used as premisses to support the proposal of the agent.
- `attack_argument`: returns an argument that attacks the argument of the other agent (see section on `step`-`ARGUE`)
- `list_attacking_argument`: returns a list of criterions that can be used as premisses to attack the item proposed by the other agent.

# Examples

```
From A1 to A2 (PROPOSE) E (E description)
From A2 to A1 (ASK_WHY) E (E description)
From A1 to A2 (ARGUE) (E, E <= CONSUMPTION = GOOD)
From A2 to A1 (ARGUE) (E, not E <= PRODUCTION_COST = VERY_BAD, PRODUCTION_COST > CONSUMPTION)
From A1 to A2 (PROPOSE) ICED (ICED description)
From A2 to A1 (ACCEPT) ICED (ICED description)
From A1 to A2 (COMMIT) ICED (ICED description)
From A2 to A1 (COMMIT) ICED (ICED description)
```

```
From A2 to A1 (PROPOSE) CNG (CNG description)
From A1 to A2 (ASK_WHY) CNG (CNG description)
From A2 to A1 (ARGUE) (CNG, CNG <= PRODUCTION_COST = VERY_GOOD)
From A1 to A2 (ARGUE) (CNG, not CNG <= CONSUMPTION = VERY_BAD, CONSUMPTION > PRODUCTION_COST)
From A2 to A1 (PROPOSE) ICED (ICED description)
From A1 to A2 (ACCEPT) ICED (ICED description)
From A2 to A1 (COMMIT) ICED (ICED description)
From A1 to A2 (COMMIT) ICED (ICED description)
```
