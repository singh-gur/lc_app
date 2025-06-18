from datetime import datetime
from typing import Callable, Awaitable, Any, TypeVar
from asyncio import get_event_loop
T = TypeVar("T")


def hydreate_template(template_str: str, placeholders: dict[str, str]) -> str:
    """
    Hydrate a template string with the provided placeholders.
    """
    placeholders.update(
        {
            "current_time": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "date": datetime.now().strftime("%Y_%m_%d"),
            "time": datetime.now().strftime("%H_%M_%S"),
            "year": datetime.now().strftime("%Y"),
            "month": datetime.now().strftime("%m"),
            "day": datetime.now().strftime("%d"),
            "hour": datetime.now().strftime("%H"),
            "minute": datetime.now().strftime("%M"),
            "second": datetime.now().strftime("%S"),
        }
    )

    return template_str.format(**placeholders)


def run_sync(func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
    """
    Run an async function synchronously.
    """

    loop = get_event_loop()
    return loop.run_until_complete(func(*args, **kwargs))