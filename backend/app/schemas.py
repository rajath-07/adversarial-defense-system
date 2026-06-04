from pydantic import BaseModel


class PredictionResponse(BaseModel):

    original_prediction: str
    original_confidence: float

    attacked_prediction: str
    attacked_confidence: float

    defended_prediction: str
    defended_confidence: float