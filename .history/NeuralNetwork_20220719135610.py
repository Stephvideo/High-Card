import numpy as np
import random
import torch
from torch import nn
from Card import *
from Player import *

NUM_INPUTS = 15 # 13 card ranks plus currBet and myChips as input
NUM_HIDDEN = 15
NUM_OUTPUTS = 5 # 5 outputs: fold, call minRaise, higherRaise, shove



# does bias count for next layer or current layer?
# if counts for next: must make bias false for final layer
class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        
        self.flatten = nn.Flatten()
        
        self.linear_relu_stack = nn.Sequential(
            
            nn.Linear(NUM_INPUTS, NUM_HIDDEN),
            nn.ReLU(),
            nn.Linear(NUM_HIDDEN, NUM_HIDDEN),
            nn.ReLU(),
            nn.Linear(NUM_HIDDEN, NUM_OUTPUTS), 
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits


    # Method which returns an ordered dictionary containing
    # all weights with their cooresponding key values representing 
    # the names of each layer.
    def getWeights(self):
        return self.state_dict()





# Crossover strategy involving taking the average of each weight
# from both weight tensors
#
# weights1 and weights2 are ordered dictionaries
#   whose key values are the names of each layer
#   and values are a 2d list containing floats [0, 1].
#   
# Returns an orderd dictionary with the same keys mapped to 
# new averaged weight values.
def avgCrossover(weights1, weights2):
    finalDict = {}
    for key in sorted(weights1.keys()):
        tensor1 = weights1[key]
        tensor2 = weights2[key]

        cols = len(tensor1[0])
        rows = len(tensor1)
        mutatedTensor = [[0]*cols for _ in range(rows)]

        for i in range(rows):
            for j in range(cols):
                w1 = tensor1[i][j]
                w2 = tensor2[i][j]
                mutatedTensor[i][j] = (w1 + w2)/2

        finalDict[key] = mutatedTensor
    
    return finalDict

# Method which adds a mutation to each weight
def randomMutation(weightDict, mutStr, mutChance):
    finalDict = {}

    for key in sorted(weightDict.keys()):
        currTensor = weightDict[key]
        mutatedTensor = [[0]*cols for _ in range(rows)]

        cols = len(mutatedTensor[0])
        rows = len(mutatedTensor)
        for i in range (rows):
            for j in range(cols):
                if random.random() <= mutChance:
                    mutAmount = random.random() * mutStr
                    newWeight = currTensor[i][j] + mutAmount

                    if newWeight > 1:
                        newWeight = 1.0
                    if newWeight < -1:
                        newWeight = -1.0
                    
                    mutatedTensor[i][j] = newWeight
        finalDict[key] = mutatedTensor
    
    return finalDict
# this method activates the node which cooresponds to the current
# card rank, activates nodes reflective of the current bet size 
# and the player's current chips and returns a tensor reflecting the activations.
def createInputs(card, betSize, myChips):
    inputs = np.zeros(NUM_INPUTS)

    rank = int(convertRank(card.getRank()))
    
    #inputs[0] => rank = 2
    #inputs[12] => rank = 14 = A 
    inputs[rank-2] = 1

    total = float(myChips + betSize)
    inputs[13] = min(float(betSize/myChips), 1) # current bet
    inputs[14] = min(float(.5 * (myChips/STARTING_CASH)), 1) # myChips

    return torch.from_numpy(inputs)
