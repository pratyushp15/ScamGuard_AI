# Configuration file for the Scam Detection project.

"""
Minimal configuration file for the Scam Detection project.
Contains only the essential settings required for the application to run.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Get project root directory
PROJECT_ROOT = Path(__file__).parent

load_dotenv(PROJECT_ROOT / ".env")

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# LLM Configuration
DEFAULT_MODEL = "gemini-3.5-flash-lite"  # Default Gemini model for LLM interactions
MAX_RETRIES = 3  # Maximum number of retries for API calls
RETRY_DELAY = 2  # Delay in seconds between retries

# Dataset Configuration
DATASET_PATH = PROJECT_ROOT / "scam_detection_dataset.csv"  # Path to the scam detection dataset
TEST_DATASET_PATH = PROJECT_ROOT / "test_scam_dataset.csv"  # Path to the test dataset

# Text column names to look for in the dataset
TEXT_COLUMN_NAMES = ["text", "message", "content", "body", "description"]
LABEL_COLUMN_NAMES = ["label", "is_scam", "target", "category", "class"]

# Paths for saving models and logs
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create output directories if they don't exist
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

def get_dataset_path(filename: str) -> Path:
    """
    Find dataset file in project directory.
    
    Args:
        filename: Name of the dataset file
        
    Returns:
        Path to the dataset file
        
    Raises:
        FileNotFoundError: If file not found
    """
    # Try direct path first
    if Path(filename).exists():
        return Path(filename)
    
    # Try project root
    project_path = PROJECT_ROOT / filename
    if project_path.exists():
        return project_path
    
    raise FileNotFoundError(f"Dataset '{filename}' not found")