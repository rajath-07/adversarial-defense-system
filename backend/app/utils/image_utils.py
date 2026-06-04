import base64
from io import BytesIO

import torch
from PIL import Image

from torchvision import transforms

def tensor_to_base64(
    tensor,
    mean,
    std
):

    tensor = tensor.detach().cpu()

    tensor = tensor * std.cpu() + mean.cpu()

    tensor = torch.clamp(
        tensor,
        0,
        1
    )

    tensor = tensor.squeeze(0)

    image = transforms.ToPILImage()(tensor)

    buffer = BytesIO()

    image.save(
        buffer,
        format="PNG"
    )

    encoded = base64.b64encode(
        buffer.getvalue()
    ).decode()

    return encoded