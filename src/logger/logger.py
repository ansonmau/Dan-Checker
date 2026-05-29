from pathlib import Path
import logging

class MyLogger():
    __loggers               = []
    _file_output_format     = "%(name)s | %(levelname)s >> %(message)s"
    _terminal_output_format = "%(name)s | %(levelname)s >> %(message)s"

    def __init__(self, name: str):
        self._name = name 
        self._logger = logging.Logger(name) 
        self.__loggers.append(self)

    def info(self, msg):
        self._logger.info(msg)

    def debug(self, msg):
        self._logger.debug(msg)

    def critical(self, msg):
        self._logger.critical(msg)

    def warning(self, msg):
        self._logger.debug(msg)

    def set_level(self, level):
        level_dict = {
                "warning": logging.WARNING,
                "debug": logging.DEBUG,
                "critical": logging.CRITICAL,
                "info": logging.INFO,
                }
        
        if level not in level_dict:
            raise ValueError(f"Cannot set logger ({self._name}) to unknown level: {level}")
        
        self._logger.setLevel(level_dict[level])

    @staticmethod
    def set_global_level(level):
        for l in MyLogger.__loggers:
            l.set_level(level)

    @staticmethod
    def add_stream_handler():
        h = logging.StreamHandler()
        h.setFormatter(logging.Formatter(MyLogger._terminal_output_format))
        for l in MyLogger.__loggers:
            l._logger.addHandler(h)

    @staticmethod
    def add_file_handler(file_path: Path):
        # ── value checking ────────────────────────────────────────────────────
        if not(file_path.exists()):
            file_path.touch()

        # ── set handlers ──────────────────────────────────────────────────────
        h = logging.FileHandler(file_path, encoding="utf-8")
        h.setFormatter(logging.Formatter(MyLogger._file_output_format))
        for l in MyLogger.__loggers:
            l._logger.addHandler(h)


def get_logger(name):
    return MyLogger(name)

