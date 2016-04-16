import logging
import logging.handlers


_output = "tests.log"  # store at the location python ran from
_fmt = logging.Formatter('(%(asctime)s) - %(levelname)s -> %(message)s')
_handler = logging.FileHandler(_output, mode="a")
_handler.setFormatter(_fmt)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(_handler)
