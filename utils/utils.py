from pathlib import Path

# Maps method → translation field name in JSON
TRANSLATION_KEY_MAP = {
    "Teacher-Synthesized-CoT": "teacher-Synthesized-CoT-translation",
    "Teacher-CoT": "teacher-CoT-translation",
    "Direct": "direct_translation",
    "Self-CoT": "self-CoT-translation",
}

def parse_filename(filename):
    """
    Parse a cleaned JSONL filename of the form:
        model__method__extra_langpair.jsonl

    Returns:
        model, method, lang_pair

    Raises:
        ValueError if parsing fails
    """
    stem = Path(filename).stem
    parts = stem.split("__")

    if len(parts) != 3:
        raise ValueError(f"Unexpected filename format: {filename}")

    model = parts[0]
    method = parts[1]
    last_part = parts[2]

    if "_" not in last_part:
        raise ValueError(f"Cannot extract language pair from: {filename}")

    _, lang_pair = last_part.rsplit("_", 1)

    return model, method, lang_pair
