import logging
import sys

def custom_logger(file_level=logging.INFO, console_level=logging.INFO):
    logger = logging.getLogger()  # root logger
    logger.setLevel(logging.DEBUG)

    # Изчистване на стари handler-и
    if logger.hasHandlers():
        logger.handlers.clear()

    # Console handler (stdout)
    if console_level is not None:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(console_level)
        ch_format = logging.Formatter('%(asctime)s - %(message)s')
        ch.setFormatter(ch_format)
        logger.addHandler(ch)

    # File handler (с UTF-8)
    fh = logging.FileHandler("test.log", encoding='utf-8')
    fh.setLevel(file_level)
    fh_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s: %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    fh.setFormatter(fh_format)
    logger.addHandler(fh)

    return logger
