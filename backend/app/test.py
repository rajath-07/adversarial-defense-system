import torch

from pipeline import InferencePipeline
from utils.image_utils import tensor_to_base64

device = torch.device(
    "cuda" if torch.cuda.is_available()
    else "cpu"
)

pipeline = InferencePipeline(device)

dummy = torch.randn(
    1, 3, 32, 32
)

encoded = tensor_to_base64(
    dummy,
    pipeline.mean,
    pipeline.std
)

print(type(encoded))
print(len(encoded))