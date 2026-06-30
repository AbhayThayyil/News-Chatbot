import contextvars
import logging
import sys

from app.core.config import settings

request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="-")


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get()
        return True


def configure_logging() -> None:
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | [%(request_id)s] | %(message)s")
    )
    handler.addFilter(RequestIdFilter())

    root = logging.getLogger()
    root.setLevel(settings.log_level)
    root.handlers = [handler]
