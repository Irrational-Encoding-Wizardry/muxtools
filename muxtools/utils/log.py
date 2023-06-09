import logging
from rich.logging import RichHandler
import time
import inspect

__all__ = ["crit", "debug", "error", "exit", "info", "warn", "logger"]

FORMAT = "%(name)s | %(message)s"  #
logging.basicConfig(format=FORMAT, datefmt="[%X]", handlers=[RichHandler(markup=True, omit_repeated_times=False, show_path=False)])

logger = logging.getLogger("muxtools")
logger.setLevel(logging.DEBUG)


def _format_msg(msg: str, caller: any) -> str:
    if caller and not isinstance(caller, str):
        caller = caller.__class__.__qualname__ if hasattr(caller, "__class__") and caller.__class__.__name__ not in ["function", "method"] else caller
        caller = caller.__name__ if not isinstance(caller, str) else caller
    return msg if caller is None else f"[bold]{caller}:[/] {msg}"


def crit(msg: str, caller: any = None) -> Exception:
    message = _format_msg(msg, caller)
    logger.critical(message)
    return Exception(message)


def debug(msg: str, caller: any = None):
    from .env import is_debug

    if not is_debug():
        return
    message = _format_msg(msg, caller)
    logger.debug(message)


def info(msg: str, caller: any = None):
    message = _format_msg(msg, caller)
    logger.info(message)


def warn(msg: str, caller: any = None, sleep: int = 0):
    message = _format_msg(msg, caller)
    logger.warning(message)
    if sleep:
        time.sleep(sleep)


def error(msg: str, caller: any = None) -> Exception:
    message = _format_msg(msg, caller)
    logger.error(message)
    return Exception(message)


def exit(msg: str, caller: any = None):
    message = _format_msg(msg, caller)
    logger.info(message)
    import sys

    sys.exit(0)
