import torch
import torch.nn.functional as F


def fgsm_attack(
    model,
    images,
    labels,
    epsilon,
    mean,
    std
):

    images = images.clone().detach()
    images.requires_grad = True

    outputs = model(images)

    loss = F.cross_entropy(outputs, labels)

    model.zero_grad()
    loss.backward()

    adv_images = (
        images +
        epsilon * images.grad.sign()
    )

    adv_images = torch.max(
        torch.min(
            adv_images,
            (1 - mean) / std
        ),
        (-mean / std)
    )

    return adv_images.detach()