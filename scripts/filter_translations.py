import json
from pathlib import Path

from utils.utils import parse_filename, TRANSLATION_KEY_MAP


def validate_entry(entry, translation_key):
    """
    Validate a single JSON entry.
    Required fields: 'source', 'reference', 'reference2', and the expected translation field.
    """

    for field in ["source", "reference", "reference2"]:
        if field not in entry or not isinstance(entry[field], str) or not entry[field].strip():
            return False

    if translation_key not in entry or not isinstance(entry[translation_key], str) or not entry[translation_key].strip():
        return False

    return True


def process_file(input_path, output_path):
    """
    Process a single JSONL file using filename-based translation key.
    Returns (empty_count, kept_count).
    """
    filename = input_path.name
    model, method, langpair = parse_filename(filename)

    if method not in TRANSLATION_KEY_MAP:
        raise ValueError(f"Unknown method: {method} in file {filename}")

    translation_key = TRANSLATION_KEY_MAP[method]

    filtered = []
    empty_count = 0

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)

            if validate_entry(entry, translation_key):
                filtered.append(entry)
            else:
                empty_count += 1

    with open(output_path, "w", encoding="utf-8") as f:
        for item in filtered:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    return empty_count, len(filtered)


def process_directory(input_dir, cleaned_dir):
    """
    Process all JSONL files in a directory.
    Saves cleaned versions to output.
    Returns results dict.
    """
    input_dir = Path(input_dir)
    cleaned_dir = Path(cleaned_dir)
    cleaned_dir.mkdir(parents=True, exist_ok=True)

    results = {}

    for file in sorted(input_dir.glob("*.jsonl")):
        output_file = cleaned_dir / file.name
        empty_count, kept_count = process_file(file, output_file)
        results[file.name] = (empty_count, kept_count)
        print(f"{file.name}: filtered {empty_count}, kept {kept_count}")

    return results


if __name__ == "__main__":
    input_dir = "data/trace_path/"
    cleaned_dir = "data/cleaned/"
    results = process_directory(input_dir, cleaned_dir)

    print("\n=== Summary ===")
    for filename, (empty, kept) in results.items():
        print(f"{filename}: empty={empty}, kept={kept}")
