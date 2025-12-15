import sys
import os

# Add the parent directory to sys.path to allow imports from backend root
# This is necessary because Vercel Serverless Functions run from the file location
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
