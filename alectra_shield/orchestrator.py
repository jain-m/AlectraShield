# Copyright (c) 2026 jain-m (Manisha Jain)
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""Main pipeline orchestrator — runs all four phases."""
import asyncio
import logging
import tempfile
from google import genai

from alectra_shield.agents import (
    TriageAgent,
    VisualForensicAgent,
    AudioBiometricAgent,
    ContextualAgent,
    SynthesisAgent,
)
from alectra_shield.models import DetectionResult

logger = logging.getLogger(__name__)


async def run_pipeline(media_path: str, api_key: str) -> DetectionResult:
    client = genai.Client(api_key=api_key)

    with tempfile.TemporaryDirectory(prefix="alectra_") as work_dir:
        # Phase 1 — sequential: must complete before Phase 2 can start
        logger.info("Phase 1: Triage & asset extraction")
        triage = TriageAgent(client)
        assets = await triage.run(media_path, work_dir)
        logger.info("Extracted %d keyframes, audio at %s", len(assets.keyframe_paths), assets.audio_path)

        # Phase 2A + 2B — parallel
        logger.info("Phase 2: Visual + Audio analysis (parallel)")
        visual_agent = VisualForensicAgent(client)
        audio_agent = AudioBiometricAgent(client)
        visual_result, audio_result = await asyncio.gather(
            visual_agent.run(assets.keyframe_paths),
            audio_agent.run(assets.audio_path),
        )
        logger.info("Visual confidence: %.2f | Audio confidence: %.2f",
                    visual_result.get("confidence", 0), audio_result.get("confidence", 0))

        # Phase 3 — sequential: needs Phase 2 results
        logger.info("Phase 3: Contextual cross-referencing")
        context_agent = ContextualAgent(client)
        context_result = await context_agent.run(visual_result, audio_result)

        # Phase 4 — sequential: aggregates all three
        logger.info("Phase 4: Synthesis & final verdict")
        synthesis_agent = SynthesisAgent(client)
        result = await synthesis_agent.run(visual_result, audio_result, context_result)

    return result
