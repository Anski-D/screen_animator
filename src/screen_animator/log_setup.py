import logging
import logging.handlers

LOG_FILE = "screen_animator.log"


def setup_logging(logging_level="WARNING"):
    log = logging.getLogger(__package__)
    log.setLevel(getattr(logging, logging_level.upper()))
    file_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=2000000, backupCount=5)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)
    log.addHandler(stream_handler)

    log.info(50 * "=")
    log.info("Logging to %s at %s level", LOG_FILE, logging.getLevelName(log.getEffectiveLevel()))
