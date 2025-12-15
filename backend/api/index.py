import sys
import os

# Add the project root to sys.path to allow imports from backend package
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from main import app
