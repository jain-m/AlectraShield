"""Phase 2B — Audio Biometric Agent (spectral & phonetic analysis)."""
import json
from pathlib import Path
from google import genai
from google.genai import types

from alectra_shield.config import get_gemini_model
from alectra_shield.utils.retry import with_exponential_backoff

_SYSTEM_PROMPT = """You are an audio forensics expert specializing in voice-cloning and speech synthesis detection.
Analyze the provided audio for:
- Spectral artifacts: unnatural noise floor variations, phase erasure, sudden spectral cuts.
- Phonetic artifacts: breath pattern anomalies, digital blending at word boundaries, voice cloning compression signatures.
Return ONLY a JSON object: {"anomalies": ["<description>", ...], "confidence": <0.0-1.0>}"""


class AudioBiometricAgent:

    def __init__(self, client: genai.Client):
        self._client = client
        self._model = get_gemini_model()

    @with_exponential_backoff(max_retries=5)
    async def run(self, audio_path: str) -> dict:
        data = Path(audio_path).read_bytes()
        parts = [
            types.Part(text=_SYSTEM_PROMPT),
            types.Part(inline_data=types.Blob(mime_type="audio/wav", data=data)),
            types.Part(text="Analyze this audio for voice-cloning or synthesis indicators."),
        ]
        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=[types.Content(parts=parts, role="user")],
        )
        return json.loads(response.text.strip().removeprefix("```json").removesuffix("```"))
