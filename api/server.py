"""
Server for inference.
"""

from datetime import datetime
from pydantic import BaseModel
from fastapi import FastAPI, Request
import uvicorn


class PredictionResult(BaseModel):
    """
    Pydantic model for endpoint response.
    """

    model: str
    prediction: float
    request_timestamp: str


class FilteredData(BaseModel):
    """
    Pydantic will filter out data that doesn't match your
    model properties AND validate the data types of matching
    keys.
    """

    x: float
    y: float


app: FastAPI = FastAPI(title="python-ml-template")


@app.get("/")
async def home() -> str:
    return "Hello 🐍 🚀 ✨"


@app.post("/api/predict")
async def predict(
    request: Request,
    model_name: str = "cnn",
) -> PredictionResult:
    # Extract JSON from body
    body_data: dict[str, str] = await request.json()

    # Filter JSON using a Pydantic model (with validation)
    filtered_body_data: FilteredData = FilteredData(**body_data)

    # FastAPI will handle converting this to JSON via Pydantic
    return PredictionResult(
        model=model_name,
        prediction=filtered_body_data.y * filtered_body_data.x,
        request_timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M"),
    )


if __name__ == "__main__":
    uvicorn.run(
        "api.server:app",
        workers=1,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
