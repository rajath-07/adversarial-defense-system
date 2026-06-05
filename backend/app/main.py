from download_weights import *
from fastapi import FastAPI
from fastapi import UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

import torch

from pipeline import InferencePipeline

from PIL import Image

from utils.preprocessing import (
    preprocess_pil_image
)
from utils.image_utils import tensor_to_base64

app = FastAPI(
    title="Adversarial Defense API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)

device = torch.device(
    "cuda" if torch.cuda.is_available()
    else "cpu"
)

pipeline = InferencePipeline(device)


@app.get("/")
def home():

    return {
        "message": "Adversarial Defense API Running"
    }


@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    model_name: str = Form(...),
    attack_name: str = Form(...)
):

    image = Image.open(file.file)

    image_tensor = preprocess_pil_image(
        image
    )

    result = pipeline.run(
        image=image_tensor,
        model_name=model_name,
        attack_name=attack_name
    )

    adv_base64 = tensor_to_base64(
        result["adv_image"],
        pipeline.mean,
        pipeline.std
    )

    purified_base64 = tensor_to_base64(
        result["purified_image"],
        pipeline.mean,
        pipeline.std
    )
    original_base64 = tensor_to_base64(
        image_tensor,
        pipeline.mean,
        pipeline.std
    )

    response = {

        "original_prediction":
            result["original_prediction"],

        "original_confidence":
            result["original_confidence"],

        "attacked_prediction":
            result["attacked_prediction"],

        "attacked_confidence":
            result["attacked_confidence"],

        "defended_prediction":
            result["defended_prediction"],

        "defended_confidence":
            result["defended_confidence"],

        "model": model_name,
        "attack": attack_name,
        "defense": "Dual-Pass IDAE",

        "original_image": original_base64,
        "adversarial_image": adv_base64,
        "denoised_image": purified_base64,

        "adversarial_image":
            adv_base64,

        "denoised_image":
            purified_base64,

        "original_image":
            original_base64
    }

    return response