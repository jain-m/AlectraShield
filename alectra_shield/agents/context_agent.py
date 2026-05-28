# Copyright (c) 2026 jain-m (Manisha Jain)
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""Phase 3 — Contextual Cross-Referencing Agent (Google Search grounding)."""
import json
from google import genai
from google.genai import types

from alectra_shield.config import get_gemini_model
from alectra_shield.utils.retry import with_exponential_backoff

_SYSTEM_PROMPT = """You are a fact-checking and digital provenance specialist.
Given a summary of visual and audio analysis from a media clip:
1. Extract key claims, names, locations, or events mentioned or depicted.
2. Use Google Search to find reputable sources that either confirm or deny these claims.
3. Determine whether the depicted event/speech has a verified origin.
Return ONLY a JSON object: {"grounding_summary": "<text>", "source_found": <true|false>, "confidence": <0.0-1.0>}"""


class ContextualAgent:

    def __init__(self, client: genai.Client):
        self._client = client
        self._model = get_gemini_model()

    @with_exponential_backoff(max_retries=5)
    async def run(self, visual_result: dict, audio_result: dict) -> dict:
        context_text = (
            f"Visual anomalies: {visual_result.get('anomalies', [])}\n"
            f"Audio anomalies: {audio_result.get('anomalies', [])}"
        )
        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=[
                types.Content(
                    parts=[
                        types.Part(text=_SYSTEM_PROMPT),
                        types.Part(text=context_text),
                        types.Part(text="Cross-reference the above indicators and verify the media's claimed origin."),
                    ],
                    role="user",
                )
            ],
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            ),
        )
        return json.loads(response.text.strip().removeprefix("```json").removesuffix("```"))
