import asyncio
import functools
import logging
from typing import Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")

# Retries on transient Google AI Studio rate-limit / server errors.
RETRYABLE_STATUS_CODES = {429, 500, 502, 503}


def with_exponential_backoff(max_retries: int = 5, base_delay: float = 1.0):
    def decorator(fn: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(max_retries):
                try:
                    return await fn(*args, **kwargs)
                except Exception as exc:
                    code = getattr(getattr(exc, "response", None), "status_code", None)
                    if code not in RETRYABLE_STATUS_CODES and attempt == max_retries - 1:
                        raise
                    logger.warning("Attempt %d failed (%s); retrying in %.1fs", attempt + 1, exc, delay)
                    await asyncio.sleep(delay)
                    delay = min(delay * 2, 60.0)
            raise RuntimeError("Exhausted retries")

        return wrapper

    return decorator
