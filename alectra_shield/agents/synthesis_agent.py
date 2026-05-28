# Copyright (c) 2026 jain-m (Manisha Jain)
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""Phase 4 — Synthesis & Consensual Verifier (final risk aggregation)."""
import json
from google import genai
from google.genai import types

from alectra_shield.config import get_gemini_model
from alectra_shield.models import DetectionResult, Telemetry
from alectra_shield.utils.retry import with_exponential_backoff

_SYSTEM_PROMPT = """You are the final arbiter in a deepfake detection pipeline.
You receive independent telemetry from three specialist sub-agents:
- Visual Forensic Agent (spatial/temporal analysis)
- Audio Biometric Agent (spectral/phonetic analysis)
- Contextual Cross-Referencing Agent (provenance grounding)

Synthesize this data using a weighted confidence framework:
- Visual: 40% weight  |  Audio: 35% weight  |  Contextual: 25% weight

Return ONLY a valid JSON object matching this exact schema:
{
  "deepfake_detected": <true|false>,
  "confidence_score": <0.0-1.0>,
  "analysis_summary": "<1-2 sentence conclusion>",
  "telemetry": {
    "visual_anomalies": ["<item>", ...],
    "audio_anomalies": ["<item>", ...],
    "contextual_grounding": "<text>"
  }
}"""


class SynthesisAgent:

    def __init__(self, client: genai.Client):
        self._client = client
        self._model = get_gemini_model()

    @with_exponential_backoff(max_retries=5)
    async def run(
        self,
        visual_result: dict,
        audio_result: dict,
        context_result: dict,
    ) -> DetectionResult:
        telemetry_text = json.dumps({
            "visual": visual_result,
            "audio": audio_result,
            "contextual": context_result,
        }, indent=2)

        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=[
                types.Content(
                    parts=[
                        types.Part(text=_SYSTEM_PROMPT),
                        types.Part(text=f"Telemetry data:\n{telemetry_text}"),
                        types.Part(text="Produce the final detection verdict."),
                    ],
                    role="user",
                )
            ],
        )
        raw = json.loads(response.text.strip().removeprefix("```json").removesuffix("```"))
        return DetectionResult(
            deepfake_detected=raw["deepfake_detected"],
            confidence_score=raw["confidence_score"],
            analysis_summary=raw["analysis_summary"],
            telemetry=Telemetry(**raw["telemetry"]),
        )
