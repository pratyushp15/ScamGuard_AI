import json
import unittest
from unittest.mock import patch

import pandas as pd

import evaluate
from pipeline.scam_detector.detector import ScamDetector
from pipeline.scam_detector.parser import OutputParser


VALID_RESULT = {
    "label": "Scam",
    "reasoning": "The message asks for credentials through a suspicious link.",
    "intent": "Steal credentials",
    "risk_factors": ["credential request", "suspicious link"],
}


class OutputParserTests(unittest.TestCase):
    def setUp(self):
        self.parser = OutputParser()

    def test_parses_valid_output(self):
        self.assertEqual(self.parser.parse_llm_output(json.dumps(VALID_RESULT)), VALID_RESULT)

    def test_rejects_malformed_json(self):
        with self.assertRaises(ValueError):
            self.parser.parse_llm_output("not JSON")

    def test_rejects_invalid_label(self):
        invalid_result = {**VALID_RESULT, "label": "Maybe"}
        with self.assertRaises(ValueError):
            self.parser.parse_llm_output(json.dumps(invalid_result))


class DetectorBatchTests(unittest.TestCase):
    def test_processing_failure_is_not_a_prediction(self):
        with patch("pipeline.scam_detector.detector.LLMExecutor") as executor_class:
            executor_class.return_value.execute.side_effect = RuntimeError("provider unavailable")
            result = ScamDetector().detect_batch(["test message"])[0]

        self.assertIsNone(result["label"])
        self.assertIn("processing_error", result["risk_factors"])

    def test_valid_uncertain_result_is_not_marked_as_failure(self):
        uncertain_result = {**VALID_RESULT, "label": "Uncertain"}
        with patch("pipeline.scam_detector.detector.LLMExecutor") as executor_class:
            executor_class.return_value.execute.return_value = json.dumps(uncertain_result)
            result = ScamDetector().detect_batch(["ambiguous message"])[0]

        self.assertEqual(result["label"], "Uncertain")
        self.assertNotIn("processing_error", result["risk_factors"])


class EvaluationTests(unittest.TestCase):
    def test_failed_rows_are_excluded_from_metrics(self):
        frame = pd.DataFrame(
            {
                "message_text": ["clear scam", "failed request"],
                "label": ["Scam", "Not Scam"],
            }
        )
        results = [
            VALID_RESULT,
            {
                "label": None,
                "reasoning": "Prediction failed due to an analysis error.",
                "intent": "Could not determine",
                "risk_factors": ["processing_error"],
            },
        ]
        with patch("evaluate.pd.read_csv", return_value=frame), patch("evaluate.ScamDetector") as detector_class:
            detector_class.return_value.detect_batch.return_value = results
            metrics = evaluate.evaluate_model("unused.csv", batch_size=2)

        self.assertEqual(metrics["total_predictions"], 1)
        self.assertEqual(metrics["failed_predictions"], 1)
        self.assertEqual(metrics["overall_accuracy"], 100.0)


if __name__ == "__main__":
    unittest.main()
