import torch


def dual_pass_denoise(
    image,
    autoencoder,
    mean,
    std
):
    """
    image: normalized image tensor
    shape: (B,3,32,32)
    """

    # convert normalized → pixel space
    image_pixel = image * std + mean

    # Pass 1
    first_pass = autoencoder(image_pixel)

    # Controlled residual noise
    first_pass = torch.clamp(
        first_pass +
        0.02 * torch.randn_like(first_pass),
        0.0,
        1.0
    )

    # Pass 2
    second_pass = autoencoder(first_pass)

    # pixel → normalized
    purified = (
        second_pass - mean
    ) / std

    return purified