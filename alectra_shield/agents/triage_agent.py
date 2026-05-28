# Copyright (c) 2026 jain-m (Manisha Jain)
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""Phase 1 — Triage & Asset Extraction Agent."""
import os
import tempfile
from google import genai

from alectra_shield.models import TriageAssets
from alectra_shield.utils import extract_keyframes, extract_audio


class TriageAgent:
    def __init__(self, client: genai.Client):
        self._client = client

    async def run(self, media_path: str, work_dir: str) -> TriageAssets:
        frames_dir = os.path.join(work_dir, "keyframes")
        audio_path = os.path.join(work_dir, "audio.wav")

        keyframe_paths = extract_keyframes(media_path, frames_dir)
        extract_audio(media_path, audio_path)

        import cv2
        cap = cv2.VideoCapture(media_path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 1
        total = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        cap.release()
        duration = total / fps

        return TriageAssets(
            keyframe_paths=keyframe_paths,
            audio_path=audio_path,
            media_duration_seconds=duration,
        )
