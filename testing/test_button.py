import buttonup
import unittest
import logging
import colorama


class Formatter(logging.Formatter):
    colors = {
        logging.DEBUG: f"{colorama.Fore.LIGHTBLACK_EX}",
        logging.INFO: f"{colorama.Fore.LIGHTWHITE_EX}",
        logging.WARNING: f"{colorama.Fore.YELLOW}",
        logging.ERROR: f"{colorama.Fore.RED}",
        logging.CRITICAL: f"{colorama.Fore.RED}{colorama.Style.BRIGHT}"
    }

    def __init__(self, fmt: str = None, datefmt: str = None, style: str = "%") -> None:
        super().__init__(fmt, datefmt, style)

    def format(self, record: logging.LogRecord) -> str:
        color = self.colors.get(record.levelno, f"{colorama.Fore.WHITE}")
        record.msg = f"{color}{record.msg}{colorama.Style.RESET_ALL}"
        return super().format(record)


# Create a separate logger for the module
_log = logging.getLogger(__name__)
_log_format = "%(name)-14s : %(levelname)-10s : %(message)s"
_log_formatter = Formatter(_log_format)
_log_handler = logging.StreamHandler()
_log_handler.setFormatter(_log_formatter)
_log.addHandler(_log_handler)
_log.setLevel(logging.DEBUG)


class ButtonInitTest(unittest.TestCase):
    def test_init(self) -> None:
        _log.info("Testing DefaultButton test_init()...")
        _ = buttonup.button.DefaultButton(0, 0)
        _log.info(" - Passed all.\n")

    def test_position_init(self) -> None:
        _log.info("Testing DefaultButton test_position_init()...")
        casesArgsError = {
            (0, 0): None,
            (-1, 0): ValueError,
            (0, -1): None,
            (-1, -1): None,
            (0, 0.1): None,  # button will try and convert to int
            ("0", 0): None,  # button will try and convert to int
            (0, "adasd"): TypeError,
            (3.0, 0.0): None
        }

        for i, argsErrors in enumerate(casesArgsError.items()):
            try:
                args, error = argsErrors
                _log.debug(f"{i + 1}/{len(casesArgsError)} testing '{args}' with error '{error}'... ")
                if error is None:
                    _ = buttonup.button.DefaultButton(*args)
                else:
                    with self.assertRaises(error):
                        _ = buttonup.button.DefaultButton(*args)

            except Exception as e:
                _log.fatal(f"Error: {e}")
                raise e

            _log.debug(f"- passed.")

        _log.info(" - Passed all.\n")

    def test_width_height_init(self) -> None:
        _log.info("Testing DefaultButton test_width_height_init()...")
        casesArgsError = {
            (0, 0): None,
            (-1, 0): None,
            (0, -1): None,
            (-1, -1): None,
            (0, 0.1): None,  # button will try and convert to int
            ("0", 0): None,  # button will try and convert to int
            (0, "adasd"): TypeError,
            (3.0, 0.0): None
        }

        for i, argsErrors in enumerate(casesArgsError.items()):
            args, error = argsErrors
            _log.debug(f"{i + 1}/{len(casesArgsError)} testing '{args}' with error '{error}'... ")
            if error is None:
                _ = buttonup.button.DefaultButton(0, 0, width=args[0], height=args[1])
            else:
                with self.assertRaises(error):
                    _ = buttonup.button.DefaultButton(0, 0, width=args[0], height=args[1])

            _log.debug(f"- passed.")

        _log.info(" - Passed all.\n")

    def test_theme_init(self) -> None:
        _log.info("Testing DefaultButton test_theme_init()...")
        casesArgsError = {
            buttonup.themes.Theme: TypeError,
            buttonup.themes.get_theme("default"): None,
            "default": None,
            0: TypeError,
            None: None
        }

        for i, argsErrors in enumerate(casesArgsError.items()):
            args, error = argsErrors
            _log.debug(f"{i + 1}/{len(casesArgsError)} testing '{args}' with error '{error}'... ")
            if error is None:
                _ = buttonup.button.DefaultButton(0, 0, theme=args)
            else:
                with self.assertRaises(error):
                    _ = buttonup.button.DefaultButton(0, 0, theme=args)

            _log.debug(f"- passed.")

        _log.info(" - Passed all.\n")

    def test_text_init(self) -> None:
        _log.info("Testing DefaultButton test_text_init()...")
        casesArgsError = {
            "": None,
            " ": None,
            "Hello": None,
            0: TypeError,
            None: None,
            True: TypeError
        }

        for i, argsErrors in enumerate(casesArgsError.items()):
            args, error = argsErrors
            _log.debug(f"{i + 1}/{len(casesArgsError)} testing '{args}' with error '{error}'... ")
            if error is None:
                _ = buttonup.button.DefaultButton(0, 0, text=args)
            else:
                with self.assertRaises(error):
                    _ = buttonup.button.DefaultButton(0, 0, text=args)

            _log.debug(f"- passed.")

        _log.info(" - Passed all.\n")

    def test_text_size_init(self) -> None:
        _log.info("Testing DefaultButton test_text_size_init()...")
        casesArgsError = {
            0: None,
            1: None,
            100: None,
            -1: ValueError,
            0.1: None,  # button will try and convert to int
            "0": None,  # button will try and convert to int
            "adasd": TypeError,
            3.0: None
        }

        for i, argsErrors in enumerate(casesArgsError.items()):
            args, error = argsErrors
            _log.debug(f"{i + 1}/{len(casesArgsError)} testing '{args}' with error '{error}'... ")
            if error is None:
                _ = buttonup.button.DefaultButton(0, 0, text_size=args)
            else:
                with self.assertRaises(error):
                    _ = buttonup.button.DefaultButton(0, 0, text_size=args)

            _log.debug(f"- passed.")

        _log.info(" - Passed all.\n")
