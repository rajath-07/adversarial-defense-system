import torch
import torch.nn as nn
import torch.nn.functional as F


class WideBasic(nn.Module):
    def __init__(self, in_planes, planes, dropout_rate, stride=1):
        super().__init__()

        self.bn1 = nn.BatchNorm2d(in_planes)

        self.conv1 = nn.Conv2d(
            in_planes,
            planes,
            kernel_size=3,
            padding=1,
            bias=False
        )

        self.dropout = nn.Dropout(dropout_rate)

        self.bn2 = nn.BatchNorm2d(planes)

        self.conv2 = nn.Conv2d(
            planes,
            planes,
            kernel_size=3,
            stride=stride,
            padding=1,
            bias=False
        )

        self.shortcut = nn.Sequential()

        if stride != 1 or in_planes != planes:
            self.shortcut = nn.Conv2d(
                in_planes,
                planes,
                kernel_size=1,
                stride=stride,
                bias=False
            )

    def forward(self, x):
        out = self.conv1(F.relu(self.bn1(x)))
        out = self.conv2(F.relu(self.bn2(self.dropout(out))))
        out += self.shortcut(x)
        return out


class WideResNet(nn.Module):
    def __init__(
        self,
        depth=28,
        widen_factor=10,
        dropout_rate=0.3,
        num_classes=10
    ):
        super().__init__()

        assert (depth - 4) % 6 == 0

        n = (depth - 4) // 6
        k = widen_factor

        self.in_planes = 16

        self.conv1 = nn.Conv2d(
            3,
            16,
            kernel_size=3,
            padding=1,
            bias=False
        )

        self.layer1 = self._make_layer(
            16 * k,
            n,
            dropout_rate,
            stride=1
        )

        self.layer2 = self._make_layer(
            32 * k,
            n,
            dropout_rate,
            stride=2
        )

        self.layer3 = self._make_layer(
            64 * k,
            n,
            dropout_rate,
            stride=2
        )

        self.bn = nn.BatchNorm2d(64 * k)

        self.linear = nn.Linear(
            64 * k,
            num_classes
        )

    def _make_layer(
        self,
        planes,
        num_blocks,
        dropout_rate,
        stride
    ):
        strides = [stride] + [1] * (num_blocks - 1)

        layers = []

        for s in strides:
            layers.append(
                WideBasic(
                    self.in_planes,
                    planes,
                    dropout_rate,
                    s
                )
            )

            self.in_planes = planes

        return nn.Sequential(*layers)

    def forward(self, x):

        out = self.conv1(x)

        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)

        out = F.relu(self.bn(out))

        out = F.avg_pool2d(out, 8)

        out = out.view(out.size(0), -1)

        return self.linear(out)


def load_wideresnet(weights_path, device):

    model = WideResNet(
        depth=28,
        widen_factor=10,
        dropout_rate=0.3,
        num_classes=10
    )

    state_dict = torch.load(
        weights_path,
        map_location=device
    )

    model.load_state_dict(state_dict)

    model.to(device)
    model.eval()

    return model