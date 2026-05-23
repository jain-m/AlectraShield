from pydantic import BaseModel, Field
from typing import Optional


class TriageAssets(BaseModel):
    keyframe_paths: list[str]
    audio_path: str
    media_duration_seconds: float


class Telemetry(BaseModel):
    visual_anomalies: list[str] = Field(default_factory=list)
    audio_anomalies: list[str] = Field(default_factory=list)
    contextual_grounding: str = ""


class DetectionResult(BaseModel):
    deepfake_detected: bool
    confidence_score: float = Field(ge=0.0, le=1.0)
    analysis_summary: str
    telemetry: Telemetry
