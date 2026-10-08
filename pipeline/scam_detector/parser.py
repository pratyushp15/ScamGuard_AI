# pipeline/scam_detector/parser.py

from typing import Dict, Any
from utils import get_logger, extract_json_from_text

logger = get_logger(__name__)

class OutputParser:
    """Parses LLM output into structured format."""
    
    def parse_llm_output(self, llm_output: str) -> Dict[str, Any]:
        """
        Extract and parse JSON structure from LLM response.
        
        Args:
            llm_output: Raw text output from the LLM
            
        Returns:
            Dictionary containing structured detection results with keys:
            - label: str - Classification result ("Scam", "Not Scam", "Uncertain")
            - reasoning: str - Step-by-step analysis
            - intent: str - Description of user intent
            - risk_factors: List[str] - List of identified red flags
            
        Raises:
            ValueError: If the response is invalid JSON or does not match the output schema.
        """
        logger.info(f"Parsing LLM output of length: {len(llm_output)}")
        
        # Try to extract JSON using utils function
        parsed_json = extract_json_from_text(llm_output)
        
        required_fields = {"label", "reasoning", "intent", "risk_factors"}
        if not isinstance(parsed_json, dict):
            raise ValueError("Model response did not contain a JSON object")
        if set(parsed_json) != required_fields:
            raise ValueError("Model response JSON does not match the required schema")
        if parsed_json["label"] not in {"Scam", "Not Scam", "Uncertain"}:
            raise ValueError("Model response contains an invalid label")
        if not isinstance(parsed_json["reasoning"], str) or not isinstance(parsed_json["intent"], str):
            raise ValueError("Model response reasoning and intent must be strings")
        if not isinstance(parsed_json["risk_factors"], list) or not all(
            isinstance(factor, str) for factor in parsed_json["risk_factors"]
        ):
            raise ValueError("Model response risk_factors must be a list of strings")

        logger.info("Successfully parsed LLM output to JSON.")
        return parsed_json