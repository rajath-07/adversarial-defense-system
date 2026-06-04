import torch
from PIL import Image
from torchvision import transforms


transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=(0.4914, 0.4822, 0.4465),
        std=(0.2023, 0.1994, 0.2010)
    )
])


def preprocess_image(image_path):

    image = Image.open(
        image_path
    ).convert("RGB")

    image = transform(
        image
    )

    image = image.unsqueeze(0)

    return image


def denormalize(
    tensor,
    mean,
    std
):

    tensor = (
        tensor * std +
        mean
    )

    return torch.clamp(
        tensor,
        0,
        1
    )

def preprocess_pil_image(image):

    image = image.convert("RGB")

    image = transform(
        image
    )

    image = image.unsqueeze(0)

    return image