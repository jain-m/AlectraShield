# Copyright (c) 2026 jain-m (Manisha Jain)
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""Smoke tests for the AlectraShield pipeline."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from alectra_shield.models import DetectionResult, Telemetry
from alectra_shield.orchestrator import run_pipeline


MOCK_VISUAL = {"anomalies": ["Asymmetric pupillary reflections"], "confidence": 0.85}
MOCK_AUDIO = {"anomalies": ["Inconsistent noise floor"], "confidence": 0.78}
MOCK_CONTEXT = {"grounding_summary": "No verified source found.", "source_found": False, "confidence": 0.70}
MOCK_RESULT = DetectionResult(
    deepfake_detected=True,
    confidence_score=0.82,
    analysis_summary="Synthetic media indicators detected.",
    telemetry=Telemetry(
        visual_anomalies=MOCK_VISUAL["anomalies"],
        audio_anomalies=MOCK_AUDIO["anomalies"],
        contextual_grounding=MOCK_CONTEXT["grounding_summary"],
    ),
)


@pytest.mark.asyncio
async def test_pipeline_returns_detection_result(tmp_path):
    fake_video = tmp_path / "test.mp4"
    fake_video.touch()

    with (
        patch("alectra_shield.orchestrator.TriageAgent") as MockTriage,
        patch("alectra_shield.orchestrator.VisualForensicAgent") as MockVisual,
        patch("alectra_shield.orchestrator.AudioBiometricAgent") as MockAudio,
        patch("alectra_shield.orchestrator.ContextualAgent") as MockContext,
        patch("alectra_shield.orchestrator.SynthesisAgent") as MockSynth,
        patch("alectra_shield.orchestrator.genai"),
    ):
        from alectra_shield.models import TriageAssets

        MockTriage.return_value.run = AsyncMock(return_value=TriageAssets(
            keyframe_paths=[], audio_path=str(tmp_path / "audio.wav"), media_duration_seconds=5.0
        ))
        MockVisual.return_value.run = AsyncMock(return_value=MOCK_VISUAL)
        MockAudio.return_value.run = AsyncMock(return_value=MOCK_AUDIO)
        MockContext.return_value.run = AsyncMock(return_value=MOCK_CONTEXT)
        MockSynth.return_value.run = AsyncMock(return_value=MOCK_RESULT)

        result = await run_pipeline(str(fake_video), api_key="test-key")

    assert isinstance(result, DetectionResult)
    assert result.deepfake_detected is True
    assert 0.0 <= result.confidence_score <= 1.0
