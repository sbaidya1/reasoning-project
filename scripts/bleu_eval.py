import json
from pathlib import Path
import evaluate

from utils.utils import parse_filename, TRANSLATION_KEY_MAP


bleu = evaluate.load("bleu")

def compute_sentence_bleu(file_path, translation_key):
    """
    Compute sentence-level BLEU for a single JSONL file.
    Returns (list of BLEU scores, average BLEU).
    """
    scores = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)

            if translation_key not in entry:
                continue

            prediction = entry[translation_key]
            references = [entry["reference"], entry["reference2"]]

            result = bleu.compute(predictions=[prediction], references=[references])
            scores.append(result["bleu"])

    avg_bleu = sum(scores) / len(scores) if scores else 0
    return scores, avg_bleu


def process_cleaned_directory(cleaned_dir):
    """
    Process all cleaned JSONL files and compute BLEU grouped by:
    model → language pair → method.
    """
    cleaned_dir = Path(cleaned_dir)
    summary = {}

    for file in sorted(cleaned_dir.glob("*.jsonl")):

        try:
            model, method, lang_pair = parse_filename(file.name)
        except ValueError as e:
            print(f"Warning: {e}")
            continue

        if method not in TRANSLATION_KEY_MAP:
            print(f"Warning: No translation key for method '{method}' in {file.name}")
            continue

        translation_key = TRANSLATION_KEY_MAP[method]
        scores, avg_bleu = compute_sentence_bleu(file, translation_key)

        summary.setdefault(model, {}).setdefault(lang_pair, {})[method] = {
            "average_bleu": avg_bleu,
            "num_sentences": len(scores),
        }

        print(f"{file.name}: {method}, {lang_pair}, average BLEU = {avg_bleu:.2f}")

    return summary


def report_best_methods(summary):
    """
    Print the best-performing method per model and language pair.
    """
    print("\n=== Best Method per Model / Language Pair ===")
    for model, lang_data in summary.items():
        for lang_pair, methods in lang_data.items():
            if not methods:
                continue

            best_method = max(methods.items(), key=lambda x: x[1]["average_bleu"])
            print(
                f"{model} | {lang_pair} → Best: {best_method[0]}, "
                f"BLEU={best_method[1]['average_bleu']:.2f}"
            )


if __name__ == "__main__":
    cleaned_dir = "data/cleaned/"
    results_dir = Path("results/")
    results_dir.mkdir(parents=True, exist_ok=True)

    summary = process_cleaned_directory(cleaned_dir)

    output_path = results_dir / "bleu_summary_grouped.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\nSaved BLEU summary to {output_path}")
    report_best_methods(summary)
