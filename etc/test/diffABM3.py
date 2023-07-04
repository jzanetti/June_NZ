import random

import numpy as np
import scipy.stats as stats
import torch
import torch.nn as nn
import torch.optim as optim
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
