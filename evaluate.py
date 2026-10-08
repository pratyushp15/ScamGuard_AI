# evaluate.py

import pandas as pd
from tqdm import tqdm
import argparse

from pipeline.scam_detector.detector import ScamDetector

def calculate_metrics(actual_labels, predicted_labels):
    """Calculate accuracy, recall, and F1-score for scam detection."""
    total = len(actual_labels)
    if total == 0:
        return {"total": 0, "correct": 0, "accuracy": 0.0, "class_metrics": {}}

    # Clean up labels (remove spaces, make lowercase)
    actual_clean = [label.lower().strip() for label in actual_labels]
    predicted_clean = [label.lower().strip() for label in predicted_labels]
    
    # Calculate overall accuracy
    correct = 0
    for actual, pred in zip(actual_clean, predicted_clean):
        if actual == pred:
            correct += 1
    
    accuracy = (correct / total) * 100
    
    # Calculate metrics for each class
    class_metrics = {}
    unique_labels = set(actual_clean)
    
    for label in unique_labels:
        # Count correct and incorrect predictions for this class
        true_positives = 0
        false_negatives = 0
        false_positives = 0
        
        for actual, pred in zip(actual_clean, predicted_clean):
            if actual == label and pred == label:
                true_positives += 1
            elif actual == label and pred != label:
                false_negatives += 1
            elif actual != label and pred == label:
                false_positives += 1
        
        # Calculate metrics
        if true_positives + false_negatives > 0:
            recall = (true_positives / (true_positives + false_negatives)) * 100
        else:
            recall = 0
            
        if true_positives + false_positives > 0:
            precision = (true_positives / (true_positives + false_positives)) * 100
        else:
            precision = 0
            
        if precision + recall > 0:
            f1_score = (2 * precision * recall) / (precision + recall)
        else:
            f1_score = 0
        
        class_metrics[label] = {
            "recall": round(recall, 2),
            "f1_score": round(f1_score, 2)
        }
    
    return {
        "total": total,
        "correct": correct,
        "accuracy": round(accuracy, 2),
        "class_metrics": class_metrics
    }

def evaluate_labels(actual_labels, predicted_labels):
    """Calculate evaluation metrics from label lists."""
    metrics = calculate_metrics(actual_labels, predicted_labels)
    total = metrics["total"]
    correct = metrics["correct"]
    accuracy = metrics["accuracy"]

    summary = (
        f"Processed {total} predictions with {accuracy}% accuracy."
        if total > 0 else "No data to evaluate."
    )

    return {
        "total_predictions": total,
        "correct_predictions": correct,
        "overall_accuracy": accuracy,
        "class_metrics": metrics["class_metrics"],
        "summary": summary,
    }


def evaluate_model(dataset_path, limit=None, verbose=False, batch_size=10):
    """Load dataset, run predictions, and evaluate performance."""
    # Load the dataset
    try:
        df = pd.read_csv(dataset_path)
        print(f"Loaded dataset with {len(df)} rows")
    except FileNotFoundError:
        print(f"Error: Dataset file not found at {dataset_path}")
        return

    if limit is not None:
        df = df.head(limit)
        print(f"Limiting evaluation to the first {limit} messages.")

    # Initialize detector
    detector = ScamDetector()
    
    # Prepare data for batch processing
    if 'message_text' in df.columns:
        messages = df['message_text'].tolist()
    elif 'text' in df.columns:
        messages = df['text'].tolist()
    else:
        print("Error: Dataset must contain a 'message_text' or 'text' column.")
        return

    if 'label' not in df.columns:
        print("Error: Dataset must contain a 'label' column.")
        return

    actual_labels = df['label'].tolist()
    
    print(f"\nEvaluating {len(messages)} messages in batches of {batch_size}...")

    # Process messages in batches
    scored_actual_labels = []
    predicted_labels = []
    failed_predictions = 0
    total_batches = (len(messages) + batch_size - 1) // batch_size
    
    for i in tqdm(range(0, len(messages), batch_size), desc="Processing batches", total=total_batches):
        batch_messages = messages[i:i + batch_size]
        batch_actual = actual_labels[i:i + batch_size]
        
        try:
            # Process batch
            batch_results = detector.detect_batch(batch_messages)
            if verbose:
                for j, (msg, true_label, result) in enumerate(zip(batch_messages, batch_actual, batch_results)):
                    print(f"\nMessage {i+j+1}: {msg[:50]}...")
                    print(f"  True: {true_label}")
                    if "processing_error" in result.get("risk_factors", []):
                        print("  Prediction failed; excluded from metrics")
                    else:
                        print(f"  Predicted: {result['label']}")

            for true_label, result in zip(batch_actual, batch_results):
                if "processing_error" in result.get("risk_factors", []):
                    failed_predictions += 1
                    continue
                scored_actual_labels.append(true_label)
                predicted_labels.append(result["label"])
            
        except Exception as e:
            print(f"Error processing batch {i//batch_size + 1}: {e}")
            failed_predictions += len(batch_messages)

    print("\nEvaluation complete.")

    # Calculate and print the final metrics
    metrics = evaluate_labels(scored_actual_labels, predicted_labels)
    metrics["failed_predictions"] = failed_predictions
    
    print("\n" + "="*50)
    print(" MODEL EVALUATION RESULTS")
    print("="*50)
    print(f"  Scored Messages: {metrics['total_predictions']}")
    print(f"  Correct Predictions: {metrics['correct_predictions']}")
    print(f"  Overall Accuracy: {metrics['overall_accuracy']}%")
    print(f"  Failed Messages (excluded): {failed_predictions}")
    print()
    
    print("  PER-CLASS METRICS:")
    for label, class_metrics in metrics['class_metrics'].items():
        print(f"    {label.upper()}:")
        print(f"      Recall: {class_metrics['recall']}%")
        print(f"      F1-Score: {class_metrics['f1_score']}%")
        print()
    print("="*50)

    return metrics

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate the Scam Detection System.")
    parser.add_argument("dataset", help="Path to the labeled dataset (CSV file).")
    parser.add_argument("--limit", type=int, help="Limit evaluation to the first N messages.")
    parser.add_argument("--verbose", action="store_true", help="Print detailed results for each message.")
    parser.add_argument("--batch-size", type=int, default=10, help="Batch size for processing (default: 10).")
    
    args = parser.parse_args()
    evaluate_model(args.dataset, args.limit, args.verbose, args.batch_size)