# Reasoning project specfic exercise

The code is modular and organized as follows:

- `filter_translations.py` – Filters out empty translations and validates JSONL entries.
- `bleu_eval.py` – Computes sentence-level BLEU and summarizes the best-performing methods.
- `visualize.py` – Generates bar chart visualizations of BLEU scores across models and language pairs.
- `utils.py` – Helper functions for parsing filenames and mapping translation methods to JSON fields.

## Running the Code

> All commands assume execution from the project root. 

### 0. Install Dependencies 
Dependencies: numpy, matplotlib, evaluate, json, pathlib
```bash
pip install -r requirements.txt
```

### 1. Filter Empty Translations

Run the script to filter out entries with missing or empty translations. The script expects data to be in data to be in `data/trace_path/`.  Outputs go to `data/cleaned/`.

```bash
python -m scripts.filter_translations
```

### 2. Compute Bleu Scores
Computes sentence-level BLEU for all cleaned JSONL files and summarize results by model, method, and language pair. Output is saved to `results/bleu_summary_grouped.json.`

```bash
python -m scripts.bleu_eval
```

### 3. Visualize Bleu Scores
Generate bar charts of BLEU scores across models and language pairs. Output figure is saved to `results/bleu_visualization.png.`

```bash
python -m scripts.visualize
```

## Results Analysis

> **Note on data:** Upon inspection, it appears that the source sentences are consistently in French, and the reference translations are in English. This suggests that only the French → English (fr-en) translations provide a reliable evaluation. Other language pairs (e.g., en-es, es-en) may not align properly with what the model expected, which could explain why some BLEU scores are zero or very low. While we cannot be certain that the data is incorrect, this seems to be a reasonable interpretation for analyzing the results.

### Key Observations

1. **French → English (fr-en) is likely the most reliable evaluation:**
   - Across all models, BLEU scores are generally highest for Teacher-CoT.
   - Direct and Self-CoT methods tend to achieve lower BLEU scores.

2. **Model performance trends (fr-en):**
   - **student_Qwen_Qwen3-8B:** Teacher-Synthesized-CoT achieved the highest BLEU (~0.342), slightly better than Teacher-CoT (~0.324) and Direct (~0.323).  
   - **student_deepseek-ai_DeepSeek-R1-Distill-Llama-8B:** The only model where Self-CoT performed the best (~0.320). Teacher-CoT is still close (~0.293), followed by Direct (~0.272).
   - **student_deepseek-ai_DeepSeek-R1-Distill-Qwen-1.5B:** Teacher-CoT performs best (~0.286), while Direct and Self-CoT remain lower (~0.042–0.052).  
   - **student_deepseek-ai_DeepSeek-R1-Distill-Qwen-7B:** Teacher-CoT (~0.344) outperforms Direct (~0.228) and Self-CoT (~0.172).

3. **Other language pairs:**
   - BLEU scores for en-es are very variable, with many at 0. This is likely due to the mismatch in languages in the data, since provided references are in English but the translation is expected to be in Spanish. 
   - Interestingly, Teacher-CoT still achieves the highest BLEU for es-en, although the results may be unreliable (since the provided sources are in French instead of the expected Spanish).

### Visualization

- The BLEU bar chart (`results/bleu_visualization.png`) highlights that Teacher-CoT generally outperforms Direct and Self-CoT for fr-en across all models.
