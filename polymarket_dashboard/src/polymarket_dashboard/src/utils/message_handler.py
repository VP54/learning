import pkgutil, importlib
from polymarket_dashboard.src.config.types import MessageHandler
from polymarket_dashboard.src.config.paths import MESSAGE_HANDLER_PATH

__all__ = ["register", "get_handler", "init_handlers"]


_HANDLERS: dict[str, MessageHandler] = {}

def register(exchange: str):
    """Decorator to register a handler for a message type.

    Args:
        exchange (str):
    """
    def decorator(fn: MessageHandler):
        _HANDLERS[exchange.upper()] = fn
        print(_HANDLERS)
        return fn
    return decorator


def init_handlers(package: str):
    """Dynamically import all modules in a package to trigger handler registration."""
    pkg = importlib.import_module(package)
    for _, module_name, _ in pkgutil.iter_modules(pkg.__path__):
        importlib.import_module(f"{package}.{module_name}")


def get_handler(exchange: str) -> MessageHandler:
    init_handlers(MESSAGE_HANDLER_PATH)
    return _HANDLERS[exchange.upper()]

