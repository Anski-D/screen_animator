import logging
from datetime import datetime
from pathlib import Path

LOG_DIR = "logs"
LOG_FILE = f"{__package__}_{datetime.now().strftime('%Y%m%d%H%M')}.log"


def setup_logging(logging_level="WARNING"):
    log = logging.getLogger(__package__)
    log.setLevel(getattr(logging, logging_level.upper()))
    Path(LOG_DIR).mkdir(exist_ok=True)
    file_handler = logging.FileHandler(Path(LOG_DIR, LOG_FILE))
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)
    log.addHandler(stream_handler)

    log.info(50 * "=")
    log.info(
        "Logging to %s at %s level",
        LOG_FILE,
        logging.getLevelName(log.getEffectiveLevel()),
    )
