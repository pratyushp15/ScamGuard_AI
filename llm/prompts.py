# llm/prompts/prompts.py

from pathlib import Path
from utils import load_file

PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_prompt(filename: str) -> str:
    """Load a prompt template from file."""
    return load_file(PROMPTS_DIR / filename)

PROMPT = load_prompt("react.md") #change the prompt here


def generate_prompt(user_input: str) -> str:
    template = PROMPT
    return f"{template}\n\nUser Input: {user_input.strip()}\n\nResponse:"