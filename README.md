# DeepShield: Adversarial Defense System using Dual-Pass IDAE

# Adversarial Defense System

🚀 Live Demo: https://adversarial-defense-system.vercel.app/

🔗 Backend API: https://adversarial-defense-api.onrender.com

📦 Model Weights: https://huggingface.co/rajzzzzzzzz/adversarial-defense-weights

> Note: The backend is hosted on Render Free Tier. The first prediction request may take 30–60 seconds due to cold start.

> Important: For best results, upload images belonging to CIFAR-10 classes only. The system was trained and evaluated on the CIFAR-10 dataset.

Supported Classes:
- Airplane
- Automobile
- Bird
- Cat
- Deer
- Dog
- Frog
- Horse
- Ship
- Truck

## Overview

Adversarial Defense System is a deep learning security project that demonstrates how adversarial attacks can fool image classification models and how a dual-pass autoencoder defense can recover the original prediction.

The system allows users to upload an image, select a classification model, apply an adversarial attack, and observe the effectiveness of the defense mechanism in real time.

---

## Features

* Upload and classify images through a modern React interface
* Support for multiple image classifiers:

  * MobileNetV2
  * WideResNet-28-10
* Adversarial attack simulation:

  * FGSM (Fast Gradient Sign Method)
  * PGD (Projected Gradient Descent)
* Dual-Pass Improved Denoising Autoencoder (IDAE) defense
* Real-time visualization of:

  * Original image
  * Adversarial image
  * Denoised image
* Confidence score comparison before and after attack/defense
* FastAPI backend for inference
* React frontend for interactive visualization

---

## Tech Stack

### Frontend

* React
* Vite
* Axios
* CSS3

### Backend

* FastAPI
* Python
* Uvicorn

### Deep Learning

* PyTorch
* Torchvision

### Models

* MobileNetV2
* WideResNet-28-10
* Dual-Pass Autoencoder

### Adversarial Attacks

* FGSM
* PGD

### Deployment

* Frontend: Vercel
* Backend: Render
* Model Hosting: Hugging Face
* Inference Engine: FastAPI + PyTorch
---

## Example Results

### MobileNetV2 + FGSM

| Stage    | Prediction | Confidence |
| -------- | ---------- | ---------- |
| Original | Cat        | 98.31%     |
| Attacked | Frog       | 96.85%     |
| Defended | Cat        | 94.95%     |

### WideResNet + PGD

| Stage    | Prediction | Confidence |
| -------- | ---------- | ---------- |
| Original | Cat        | 100.00%    |
| Attacked | Frog       | 99.99%     |
| Defended | Cat        | 100.00%    |

---

## Installation

### Clone Repository

```bash
git clone https://github.com/rajath-07/adversarial-defense-system.git
cd adversarial-defense-system
```

### Backend Setup

```bash
cd backend

pip install -r requirements.txt

cd app

uvicorn main:app --reload
```

Backend runs at:

```text
http://localhost:8000
```

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

## API Endpoint

### Predict

```http
POST /predict
```

Parameters:

* file
* model_name
* attack_name

Response:

```json
{
  "original_prediction": "dog",
  "original_confidence": 99.96,
  "attacked_prediction": "cat",
  "attacked_confidence": 63.98,
  "defended_prediction": "dog",
  "defended_confidence": 99.74
}
```

---

## Future Enhancements

* CW (Carlini-Wagner) Attack
* Docker containerization
* Kubernetes deployment
* DeepFool integration
* Explainable AI visualizations
* Model robustness benchmarking

---

## Author

Rajath Gupta

Machine Learning | Deep Learning | Frontend Development

GitHub: https://github.com/rajath-07
