import torch
from pathlib import Path

from models.mobilenet import load_mobilenet
from models.wideresnet import load_wideresnet
from models.autoencoder import load_autoencoder

from attacks.fgsm import fgsm_attack
from attacks.pgd import pgd_attack

from services.denoise_service import dual_pass_denoise

from utils.constants import (
    MEAN,
    STD,
    CIFAR10_CLASSES
)


class InferencePipeline:

    def __init__(self, device):

        self.device = device

        self.mean = MEAN.to(device)
        self.std = STD.to(device)

        base_dir = Path(__file__).resolve().parent

        self.mobilenet = load_mobilenet(
            base_dir / "weights" / "mobilenet_cifar10.pth",
            device
        )

        self.wideresnet = load_wideresnet(
            base_dir / "weights" / "wideresnet_cifar10.pth",
            device
        )

        self.autoencoder = load_autoencoder(
            base_dir / "weights" / "dual_pass_idae_cifar10.pth",
            device
        )

    def get_model(self, model_name):

        if model_name.lower() == "mobilenet":
            return self.mobilenet

        elif model_name.lower() == "wideresnet":
            return self.wideresnet

        raise ValueError(
            f"Unsupported model: {model_name}"
        )

    def predict(self, model, image):

        with torch.no_grad():

            logits = model(image)

            probs = torch.softmax(
                logits,
                dim=1
            )

            confidence, prediction = torch.max(
                probs,
                dim=1
            )

        return (
            prediction.item(),
            confidence.item()
        )

    def generate_attack(
        self,
        model,
        image,
        label,
        attack_name
    ):

        if attack_name.lower() == "fgsm":

            return fgsm_attack(
                model=model,
                images=image,
                labels=label,
                epsilon=8 / 255,
                mean=self.mean,
                std=self.std
            )

        elif attack_name.lower() == "pgd":

            return pgd_attack(
                model=model,
                images=image,
                labels=label,
                epsilon=8 / 255,
                alpha=2 / 255,
                steps=10,
                mean=self.mean,
                std=self.std
            )

        raise ValueError(
            f"Unsupported attack: {attack_name}"
        )

    def run(
        self,
        image,
        model_name,
        attack_name
    ):

        image = image.to(self.device)

        model = self.get_model(
            model_name
        )
        with torch.no_grad():
             label = model(image).argmax(dim=1)

        # Original prediction
        original_pred, original_conf = self.predict(
            model,
            image
        )

        # Generate attack
        adv_image = self.generate_attack(
            model,
            image,
            label,
            attack_name
        )

        # Prediction after attack
        attacked_pred, attacked_conf = self.predict(
            model,
            adv_image
        )

        # Dual-pass denoising
        purified_image = dual_pass_denoise(
            adv_image,
            self.autoencoder,
            self.mean,
            self.std
        )

        # Prediction after defense
        defended_pred, defended_conf = self.predict(
            model,
            purified_image
        )

        return {

            "original_prediction":
                CIFAR10_CLASSES[original_pred],

            "original_confidence":
                round(original_conf * 100, 2),

            "attacked_prediction":
                CIFAR10_CLASSES[attacked_pred],

            "attacked_confidence":
                round(attacked_conf * 100, 2),

            "defended_prediction":
                CIFAR10_CLASSES[defended_pred],

            "defended_confidence":
                round(defended_conf * 100, 2),

            "adv_image":
                adv_image,

            "purified_image":
                purified_image
        }