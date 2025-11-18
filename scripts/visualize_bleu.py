import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def shorten_model_name(name: str) -> str:
    """
    Extract a shorter, readable model identifier.
    Example:
        student_Qwen_Qwen3-8B → Qwen3-8B
        student_deepseek-ai_DeepSeek-R1-Distill-Qwen-7B → Qwen-7B
    Falls back to the original name if no known token is found.
    """
    parts = name.split("_")
    for part in reversed(parts):
        if any(t in part.lower() for t in ["qwen", "llama", "deepseek"]):
            return part
    return name


def load_summary():
    """
    Load the grouped BLEU summary JSON.
    Expects the file to be located in: <project_root>/results/bleu_summary_grouped.json

    Returns:
        summary (dict): Loaded BLEU data.
        script_dir (Path): Directory containing this script.
    """
    script_dir = Path(__file__).resolve().parent
    summary_path = script_dir.parent / "results" / "bleu_summary_grouped.json"

    with open(summary_path, "r", encoding="utf-8") as f:
        summary = json.load(f)

    return summary, script_dir


def visualize(summary: dict, script_dir: Path):
    """
    Generate a multi-row, multi-column bar chart visualization of BLEU scores.

    Rows correspond to models.
    Columns correspond to language pairs.

    Saves:
        results/bleu_visualization.png
    """
    models = list(summary.keys())
    language_pairs = sorted({lp for m in summary.values() for lp in m.keys()})

    fig, axes = plt.subplots(
        len(models),
        len(language_pairs),
        figsize=(4 * len(language_pairs), 2.5 * len(models)),
        squeeze=False
    )

    for r, model in enumerate(models):
        short = shorten_model_name(model)

        for c, lp in enumerate(language_pairs):
            ax = axes[r][c]

            if lp not in summary[model]:
                ax.axis("off")
                continue

            methods = summary[model][lp]
            labels = list(methods.keys())
            bleu_vals = [methods[m]["average_bleu"] for m in labels]

            x = np.arange(len(labels))
            ax.bar(x, bleu_vals)

            ax.set_xticks(x)
            ax.set_xticklabels(labels, rotation=25, fontsize=7)

            if r == 0:
                ax.set_title(lp, fontsize=10, weight="bold")
            if c == 0:
                ax.set_ylabel(short, fontsize=9, weight="bold")

            max_v = max(bleu_vals)
            ax.set_ylim(0, max_v * 1.2 if max_v > 0 else 1)

    plt.suptitle("BLEU Scores by Method Across Models and Language Pairs", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    out_path = script_dir.parent / "results" / "bleu_visualization.png"
    plt.savefig(out_path, dpi=300)
    print(f"Saved visualization to: {out_path}")

    plt.close(fig)


if __name__ == "__main__":
    summary, script_dir = load_summary()
    visualize(summary, script_dir)
