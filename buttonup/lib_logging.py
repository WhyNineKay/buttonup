import logging
import sys

LOGGING_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s"


def setup_logging(debug: bool = False) -> None:
    level = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(
        level=level,
        format=LOGGING_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ],
    )


