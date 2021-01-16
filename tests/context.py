# Setup paths for the tests independent of the installation method.
# Based on https://docs.python-guide.org/writing/structure/.

from os import path
import sys
sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '..')))

from LoAFi.log_file_manager import LogFileManager  # noqa: F401
