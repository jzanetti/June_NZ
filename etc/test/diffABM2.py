import random

import numpy as np
import scipy.stats as stats
import torch
import torch.nn as nn
import torch.optim as optim


# Define the agent class
class Agent:
    def __init__(self, age):
        self.age = age
        self.is_alive = True
        self.alpha = nn.Parameter(torch.tensor(0.1))
        self.beta = nn.Parameter(torch.tensor(0.5))

    def transition_health_to_death(self):
        # Define parameters for the beta distribution based on age

        # Calculate the probability of death based on the beta distribution
        p_death = stats.norm.rvs(self.alpha.item(), self.beta.item())
        p_death = self.alpha.item() + self.beta.item()
        proc_p = np.random.uniform()
        # Randomly determine if the agent transitions to death
        if proc_p > p_death:
            self.is_alive = False
        else:
            self.is_alive = True

    def get_action(self):
        # Return the action for this agent
        return torch.tensor([0.0, 1.0], requires_grad=True)


# Define your agent-based model
class AgentBasedModel:
    def __init__(self):
        # self.agent1 = Agent(age=30)
        # self.agent2 = Agent(age=40)
        # self.agent3 = Agent(age=50)

        self.agents = []
        for _ in range(999):
            age = random.randint(10, 100)
            agent = Agent(age=age)
            self.agents.append(agent)

    def forward(self, actions):
        # Update the state of the environment using the actions of the agents
        num_deaths = []  # Initialize the count of deaths
        actions2 = []

        for agent in self.agents:
            x = []
            for i in range(len(actions)):
                x.append(
                    torch.tensor(
                        [torch.tensor(actions[i][0].item()), torch.tensor(actions[i][1].item())],
                        dtype=torch.float32,
                        requires_grad=True,
                    )
                )

            output = torch.stack([x]).sum()
            # output = actions.sum()
            return output

        for agent, action in zip(self.agents, actions):
            agent.alpha = action[0]
            agent.beta = action[1]
            x = torch.tensor(
                [torch.tensor(action[0].item()), torch.tensor(action[1].item())],
                dtype=torch.float32,
                requires_grad=True,
            )
            actions2.append(x)
            # is_equal1 = torch.all(x == action)
            agent.transition_health_to_death()

            if not agent.is_alive:
                num_deaths.append(torch.tensor(1.0, requires_grad=True))

        # if not agent.is_alive:
        #    num_deaths += 1

        output = torch.stack(num_deaths).sum()
        output = torch.stack(actions2).sum()
        # output = actions.sum()
        return output

        print(output)
        # output = torch.stack(actions).sum()

        # return output
        # total_death = torch.tensor(
        #    num_deaths, dtype=torch.float32, requires_grad=True
        # )  # Convert deaths to a torch.Tensor
        return output


# Define the objective function
def objective_function(actions):
    # Perform a forward pass of the model to get the model output
    num_deaths = model.forward(actions)
    # Define your own error calculation logic
    target = torch.tensor(100.0)  # Set a target value
    error = torch.abs(num_deaths - target)  # Calculate the error

    return error


from torch_geometric.data import HeteroData

n_agents = 10
n_households = 2

data = HeteroData()

data["agent"].id = torch.arange(0, n_agents)
data["agent"].age = torch.randint(18, 100, (n_agents,))
data["household"].id = torch.zeros(n_households)

data["household"].people = torch.tensor([n_agents // n_households])

data["agent", "attends_household", "household"].edge_index = torch.vstack(
    (data["agent"].id, torch.tensor([0, 0, 0, 0, 0, 1, 1, 1, 1, 1], dtype=torch.long))
)

# Create an instance of your agent-based model
model = AgentBasedModel()

actions = []
for agent in model.agents:
    actions.append([agent.alpha, agent.beta])

actions = [torch.tensor(agent_actions, requires_grad=True) for agent_actions in actions]

# Choose an optimization algorithm
optimizer = optim.SGD(actions, lr=0.1)
# Perform optimization for a total of 200 steps
total_steps = 10
for step in range(total_steps):
    # Clear the gradients from the previous iteration
    optimizer.zero_grad()

    # Calculate the number of deaths
    error = objective_function(actions)
    print(actions[0])
    # Perform backpropagation to calculate the gradients
    error.backward()

    # Update the agents' actions
    optimizer.step()

    # Print the number of deaths for monitoring
    print(f"Step {step+1}/{total_steps}: Error = {error.item()}")

# Final actions after optimization
final_actions = [agent.get_action().detach().numpy() for agent in model.agents]
