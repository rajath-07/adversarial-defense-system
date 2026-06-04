import torch
import torch.nn as nn
from torchvision import models


def build_mobilenet(num_classes=10):

    model = models.mobilenet_v2(weights=None)

    model.features[0][0] = nn.Conv2d(
        3,
        32,
        kernel_size=3,
        stride=1,
        padding=1,
        bias=False
    )

    model.classifier[1] = nn.Linear(
        model.last_channel,
        num_classes
    )

    return model


def load_mobilenet(weights_path, device):

    model = build_mobilenet()

    model.load_state_dict(
        torch.load(
            weights_path,
            map_location=device
        )
    )

    model.eval()

    return model.to(device)