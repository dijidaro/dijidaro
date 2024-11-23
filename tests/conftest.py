# tests/conftest.py
import sys
from os.path import abspath, dirname

# Add the project root directory to sys.path
sys.path.insert(0, dirname(dirname(abspath(__file__))))
