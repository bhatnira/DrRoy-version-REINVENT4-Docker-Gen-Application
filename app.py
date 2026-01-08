"""
Hugging Face Spaces entry point for REINVENT4 Drug Generation Application
This file serves as the main entry point for Hugging Face Spaces deployment.
"""

import sys
import os

# Add streamlit_app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'streamlit_app'))

# Import and run the main Streamlit app
from streamlit_app.app import main

if __name__ == "__main__":
    main()
