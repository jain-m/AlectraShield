import os
from functools import lru_cache

DEFAULT_GEMINI_MODEL = "gemini-2.0-flash"

@lru_cache(maxsize=1)
def get_gemini_model() -> str:
    value = os.environ.get("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)
    return value.strip().strip('"')
