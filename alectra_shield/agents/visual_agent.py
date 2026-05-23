"""Phase 2A — Visual Forensic Agent (spatial & temporal analysis)."""
import base64
import json
from pathlib import Path
from google import genai
from google.genai import types

from alectra_shield.config import get_gemini_model
from alectra_shield.utils.retry import with_exponential_backoff

_SYSTEM_PROMPT = """You are a visual forensics expert specializing in deepfake detection.
Analyze the provided video keyframes for:
- Spatial artifacts: boundary blending at jawline/neck, asymmetric eye reflections, unnatural skin texture smoothing.
- Temporal artifacts: irregular blink frequency, facial muscle desynchronization, micro-expression discontinuities.
Return ONLY a JSON object: {"anomalies": ["<description>", ...], "confidence": <0.0-1.0>}"""


class VisualForensicAgent:

    def __init__(self, client: genai.Client):
        self._client = client
        self._model = get_gemini_model()

    @with_exponential_backoff(max_retries=5)
    async def run(self, keyframe_paths: list[str]) -> dict:
        parts: list[types.Part] = [types.Part(text=_SYSTEM_PROMPT)]
        for path in keyframe_paths:
            data = Path(path).read_bytes()
            parts.append(types.Part(inline_data=types.Blob(mime_type="image/jpeg", data=data)))
        parts.append(types.Part(text="Analyze these keyframes for deepfake indicators."))

        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=[types.Content(parts=parts, role="user")],
        )
        return json.loads(response.text.strip().removeprefix("```json").removesuffix("```"))
