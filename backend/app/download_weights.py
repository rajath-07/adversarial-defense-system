from pathlib import Path
import urllib.request

WEIGHTS_DIR = Path(__file__).parent / "weights"
WEIGHTS_DIR.mkdir(exist_ok=True)

FILES = {
    "mobilenet_cifar10.pth":
    "https://huggingface.co/rajzzzzzzzz/adversarial-defense-weights/resolve/main/mobilenet_cifar10.pth",

    "wideresnet_cifar10.pth":
    "https://huggingface.co/rajzzzzzzzz/adversarial-defense-weights/resolve/main/wideresnet_cifar10.pth",

    "dual_pass_idae_cifar10.pth":
    "https://huggingface.co/rajzzzzzzzz/adversarial-defense-weights/resolve/main/dual_pass_idae_cifar10.pth"
}

for filename, url in FILES.items():

    filepath = WEIGHTS_DIR / filename

    if not filepath.exists():

        print(f"Downloading {filename}...")

        urllib.request.urlretrieve(
            url,
            filepath
        )

        print(f"{filename} downloaded.")

    else:

        print(f"{filename} already exists.")