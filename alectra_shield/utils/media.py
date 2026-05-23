import os
import cv2
import librosa
import soundfile as sf
import numpy as np
from pathlib import Path


def extract_keyframes(video_path: str, output_dir: str, max_frames: int = 30) -> list[str]:
    """Extract evenly-spaced keyframes from a video, targeting motion-rich segments."""
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    indices = np.linspace(0, total_frames - 1, min(max_frames, total_frames), dtype=int)

    saved: list[str] = []
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(idx))
        ret, frame = cap.read()
        if not ret:
            continue
        out_path = os.path.join(output_dir, f"frame_{idx:06d}.jpg")
        cv2.imwrite(out_path, frame)
        saved.append(out_path)

    cap.release()
    return saved


def extract_audio(video_path: str, output_path: str) -> str:
    """Extract audio track from a video file and save as WAV."""
    os.makedirs(Path(output_path).parent, exist_ok=True)
    y, sr = librosa.load(video_path, sr=None, mono=False)
    if y.ndim > 1:
        y = y.T
    sf.write(output_path, y, sr)
    return output_path
