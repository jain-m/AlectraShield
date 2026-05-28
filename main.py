# Copyright (c) 2026 jain-m (Manisha Jain)
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""AlectraShield — CLI entry point."""
import asyncio
import json
import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

from alectra_shield.orchestrator import run_pipeline


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <path/to/media.mp4>")
        sys.exit(1)

    media_path = sys.argv[1]
    if not os.path.exists(media_path):
        print(f"File not found: {media_path}")
        sys.exit(1)

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not set. Copy .env.example to .env and add your key.")
        sys.exit(1)

    result = asyncio.run(run_pipeline(media_path, api_key))
    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    main()
