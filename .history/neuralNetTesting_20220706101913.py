from NeuralNetwork import *
import torch

model = NeuralNetwork().to(device)
print(model)

x = torch.rand(1, 16)
logits = model(x)
prob = nn.Softmax(dim=1)(logits) # dim=1 is necessary to make probabilities sum to 1
y_pred = prob.argmax(1)
print (prob)
print(y_pred)
#print(logits)