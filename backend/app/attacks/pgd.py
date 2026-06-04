import torch
import torch.nn.functional as F


def pgd_attack(
    model,
    images,
    labels,
    epsilon,
    alpha,
    steps,
    mean,
    std
):

    adv = images.clone().detach()

    for _ in range(steps):

        adv.requires_grad_(True)

        outputs = model(adv)

        loss = F.cross_entropy(
            outputs,
            labels
        )

        model.zero_grad()

        loss.backward()

        adv = adv + alpha * adv.grad.sign()

        # Projection to epsilon ball
        adv = torch.max(
            torch.min(
                adv,
                images + epsilon
            ),
            images - epsilon
        )

        # Clamp normalized range
        adv = torch.max(
            torch.min(
                adv,
                (1 - mean) / std
            ),
            (-mean / std)
        )

        adv = adv.detach()

    return adv