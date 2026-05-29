<!--
Copyright (c) 2026 jain-m (Manisha Jain)
This software is released under the MIT License.
https://opensource.org/licenses/MIT
-->

# Project Context: AlectraShield (Deepfake Detection Orchestrator)

## System Instructions
You are an expert AI Architect specializing in multi-step agentic workflows. Your task is to orchestrate multiple parallel and sequential instances of Gemini 3.5 Flash inside the AlectraShield defense architecture to detect deepfake media (video, audio, and images). 

Leverage Gemini 3.5 Flash’s core strengths: its native multimodal understanding (text, audio, video, image inputs), high token throughput, extreme speed, and exceptional performance on multi-step tool use.

---

## 1. Architectural Blueprint
The agentic workflow must operate across four distinct phases using specialized Gemini 3.5 Flash sub-agents. 

```
[Input Media] 
      │
      ▼
┌────────────────────────────────────────────────────────┐
│ PHASE 1: Triaging & Artifact Extraction Agent          │
│ (Splits video into keyframes, isolates audio spectrum) │
└─────────────┬──────────────────────────┬───────────────┘
              │                          │
              ▼                          ▼
┌──────────────────────────┐┌────────────────────────────┐
│ PHASE 2A: Visual Forensic││ PHASE 2B: Audio Biometric  │
│ Agent (Spatial/Temporal) ││ Agent (Spectral/Phonetic)  │
└─────────────┬────────────┘└────────────┬───────────────┘
              │                          │
              └─────────────┬────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│ PHASE 3: Contextual Cross-Referencing Agent            │
│ (Grounding checks via Google Search API)               │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│ PHASE 4: Verification & Synthesis Agent                │
│ (Final probability mapping, confidence scoring, report)│
└────────────────────────────────────────────────────────┘
```

---

## 2. Sub-Agent Definitions & Prompts

### Agent 1: Triage & Asset Extraction Agent
*   **Role:** Input ingestion and initial breakdown.
*   **Capabilities Utilized:** Native video/audio file handling, high-speed multimodal parsing.
*   **Execution Instructions:** 
    *   Ingest the raw media container.
    *   Extract separate audio streams (WAV format) and visual assets (high-density keyframes targeting rapid motion/transitions).
    *   Pass the structured assets asynchronously to the Phase 2 sub-agents.

### Agent 2A: Visual Forensic Agent
*   **Role:** Spatial and temporal inconsistency detection.
*   **Capabilities Utilized:** Advanced native visual reasoning.
*   **Analysis Directives:**
    *   **Spatial Analysis:** Scan frame boundaries for warping, asymmetric reflections in eyes, mismatched blending around the jawline/neck, and unnatural texture smoothing.
    *   **Temporal Analysis:** Track blinking frequency, facial muscle synchronization across consecutive frames, and micro-expressions to identify synthetic temporal coherence breaks.

### Agent 2B: Audio Biometric Agent
*   **Role:** Acoustic and phonetic authenticity analysis.
*   **Capabilities Utilized:** Native audio input processing.
*   **Analysis Directives:**
    *   Scan for unnatural noise floor variations, phase erasure, digital artifacts, and sudden spectral cuts indicative of voice cloning/splicing.
    *   Evaluate phonetic alignment (e.g., checking if dental/plosive sounds match visual mouth movements processed by Agent 2A).

### Agent 3: Contextual Cross-Referencing Agent
*   **Role:** External verification and digital footprint mapping.
*   **Capabilities Utilized:** Grounding with Google Search API.
*   **Execution Instructions:**
    *   Extract semantic metadata, spoken quotes, and distinct reverse-image visual profiles from the source media.
    *   Execute parallel search loops to locate historical reference footage or origin sources. Identify if the event/quote is documented by reputable entities or flags known misinformation footprints.

### Agent 4: Synthesis & Consensual Verifier
*   **Role:** Final risk aggregation and structured reporting.
*   **Capabilities Utilized:** High-horizon logic and complex reasoning synthesis.
*   **Execution Instructions:**
    *   Collect independent telemetry data from Agents 2A, 2B, and 3.
    *   Resolve conflicting observations using a weighted confidence framework.
    *   Generate a structured JSON payload outlining the risk probability, definitive indicator tags, and a final textual assessment.

---

## 3. Tech Stack & Environment Guidelines
*   **Language:** Python 3.11+
*   **Core SDK:** `google-genai` (Google GenAI SDK)
*   **Media Analysis Helper Libraries:** `opencv-python`, `librosa`, `scipy`
*   **Execution Rules:** Implement asynchronous execution (`asyncio`) when running Phase 2A and 2B in parallel to optimize processing speed. Always handle Google AI Studio rate limits gracefully using exponential backoff or slight execution delays.

---

## 4. Expected Output Format
The final synthesis step must return a strictly formatted JSON object matching this schema:

```json
{
  "deepfake_detected": true,
  "confidence_score": 0.94,
  "analysis_summary": "Clear indicators of AI-generation detected via audiovisual desynchronization and distinct generative facial artifacts.",
  "telemetry": {
    "visual_anomalies": ["Asymmetric pupillary reflections in frames 140-180", "Boundary blending artifacts around the lower jawline"],
    "audio_anomalies": ["Inconsistent noise floor", "Phase cancellation detected during high-frequency consonants"],
    "contextual_grounding": "No verified primary source found for the alleged speech via Google Search grounding."
  }
}
```

---

## 5. Testing & Verification Suite

### Step 1: Environment & Test Asset Bootstrap
Run these commands in your project root terminal to build your minimal, lightweight test suite using compressed GitHub evaluation assets:

```bash
# Create local testing architecture
mkdir -p tests/test_assets
curl -L -o tests/test_assets/notfake_sample.mp4 "https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/person-bicycle-car-detection.mp4"
# In case, download speed drops to zero with time left incrementing, CTRL+C and run
curl -L -C - -o tests/test_assets/notfake_sample.mp4 "https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/person-bicycle-car-detection.mp4"

python main.py tests/test_assets/notfake_sample.mp4
# Expected Result
```
{
  "deepfake_detected": false,
  "confidence_score": 0.98,
  "analysis_summary": "No visual anomalies were detected, and the audio track contains only ambient digital silence rather than synthetic speech. The weighted telemetry indicates no evidence of deepfake manipulation.",
  "telemetry": {
    "visual_anomalies": [],
    "audio_anomalies": [
      "No active speech signal or vocal content detected in the audio file",
      "Audio profile consists entirely of near-silent digital noise floor and low-level ambient static",
      "Absence of spectral energy in the typical human vocal frequency ranges"
    ],
    "contextual_grounding": "The provided visual and audio analysis contains no reference to any specific claims, names, locations, or events. The audio profile indicates complete silence or ambient digital noise with no vocal content, and no visual details are provided. Consequently, it is impossible to identify or verify any media origin or source."
  }
}
```

# Morgan Freeman video
```
{
  "deepfake_detected": true,
  "confidence_score": 0.97,
  "analysis_summary": "The media is definitively identified as a deepfake, supported by compounding visual artifacts, neural audio synthesis signatures, and explicit provenance grounding from the Dutch deepfake channel 'Diep Nep'.",
  "telemetry": {
    "visual_anomalies": [
      "Asymmetric eye reflections (catchlights) and slight misalignment of pupil gaze across several frames.",
      "Subtle boundary blending artifacts and lack of micro-shadowing along the jawline and around the ears.",
      "Unnatural rendering and simplified geometry of the mouth interior, teeth, and tongue during speech segments.",
      "Slightly inconsistent tracking of facial wrinkles and age spots during fast head movements.",
      "Dutch outro watermark 'DIEP NEP.' explicitly confirms the video is a deepfake ('diep nep' is the Dutch translation for deepfake)."
    ],
    "audio_anomalies": [
      "Unnatural phonetic blending at word boundaries, indicating neural vocoder synthesis.",
      "Artificial breath pattern cadence, lacking natural physiological variation.",
      "Slight spectral flattening and compression signatures characteristic of neural voice cloning models.",
      "Unusually precise sibilant control with minor phase distortion, typical of deepfake speech generation."
    ],
    "contextual_grounding": "The media's origin as an AI-generated synthetic video is verified. The visual and audio anomalies\u2014such as asymmetric eye reflections, unnatural phonetic blending, and artificial breath patterns\u2014are characteristic of deepfake technology. Furthermore, the 'DIEP NEP.' watermark explicitly attributes the video to 'Diep Nep,' a prominent Dutch deepfake production channel founded by creator Bob de Jong (famous for the 'This is Not Morgan Freeman' concept video). The channel intentionally labels its creations to promote transparency and highlight the capabilities of synthetic media."
  }
}```

# [TODO] Other test sources for later

* GitHub Evaluation Assets (Test Suites): Lightweight, pre-compressed sample clips (.mp4 formats) explicitly hosted inside open-source deepfake detection repositories for automated continuous integration unit tests.

* Hugging Face Benchmark Repositories: Python-accessible public repositories hosting benchmark datasets, specifically referencing the hi-paris/FakeParts dataset and the cambrain/DigiFakeAV dataset.

* FaceForensics++ (FF++): An academic dataset hosted by the Technical University of Munich that contains manipulated videos generated using automated face-swapping and facial reenactment methods.

* Celeb-DF (v2): A high-quality deepfake video dataset managed by the University at Albany's Computer Vision and Machine Learning Lab, which includes authentic celebrity videos, YouTube reference clips, and synthesis face-swapped files.

* Kaggle Datasets (Deepfake Detection Challenge Preview): Open-source developer mirrors or single-file previews from major competitions like the 400GB Deepfake Detection Challenge (DFDC), allowing manual downloads of individual 10–12 second clips without grabbing the full package.
