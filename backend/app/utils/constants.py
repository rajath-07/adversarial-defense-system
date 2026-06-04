import torch

MEAN = torch.tensor(
    [0.4914, 0.4822, 0.4465]
).view(1,3,1,1)

STD = torch.tensor(
    [0.2023, 0.1994, 0.2010]
).view(1,3,1,1)

CIFAR10_CLASSES = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck"
]