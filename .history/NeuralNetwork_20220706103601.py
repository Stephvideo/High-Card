import numpy as np
import torch
from torch import nn
from Card import *

NUM_INPUTS = 13
NUM_HIDDEN = 100
NUM_OUTPUTS = 5
device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)

# does bias count for next layer or current layer?
# if counts for next: must make bias false for final layer
class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        
        self.flatten = nn.Flatten()
        
        self.linear_relu_stack = nn.Sequential(
            # 13 card ranks plus currBet, myChips, and opponentsChips as input
            nn.Linear(NUM_INPUTS, NUM_HIDDEN),
            nn.ReLU(),
            nn.Linear(NUM_HIDDEN, NUM_HIDDEN),
            nn.ReLU(),
            nn.Linear(NUM_HIDDEN, NUM_OUTPUTS), # 5 outputs: fold, call minRaise, higherRaise, shove
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits




def createInputs(card):
    inputs = np.zeros(NUM_INPUTS)

    rank = int(convertRank(card.getRank()))

    inputs[rank] = 1

    return torch.from_numpy(inputs)
