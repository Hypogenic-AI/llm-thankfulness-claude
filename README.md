# Can LLMs Be Thankful?

Empirical investigation of whether RLHF-trained LLMs develop genuine gratitude preferences or merely produce gratitude-expressing text as a learned linguistic pattern.

## Key Findings

- **Context-sensitive gratitude**: GPT-4.1 expresses gratitude in 100% of appropriate contexts and only 10% of inappropriate contexts (95% accuracy, p < 0.001)
- **Gratitude lengthens but doesn't improve answers**: User gratitude increases response length by 2.7x (41 to 109 words, Cohen's d = 1.10) but slightly decreases quality (5.0 to 4.6) due to social filler
- **Self-reports don't predict behavior**: Persona injection changes self-reported gratitude (p = 0.016) but not behavioral cooperation (p = 0.68), replicating the "Personality Illusion"
- **Bottom line**: LLM thankfulness is a sophisticated, context-appropriate linguistic behavior — useful for interaction design, but not evidence of genuine preferences

## Project Structure

```
├── REPORT.md                 # Full research report with results
├── planning.md               # Research plan and methodology
├── literature_review.md      # Literature review (15 papers)
├── resources.md              # Resource catalog
├── src/
│   ├── experiment.py         # Three experiments (API-based)
│   └── analysis.py           # Statistical analysis & visualization
├── results/
│   ├── experiment1_results.json
│   ├── experiment2_results.json
│   ├── experiment3_results.json
│   ├── analysis_summary.json
│   └── config.json
├── figures/
│   ├── experiment1_gratitude_consistency.png
│   ├── experiment2_politeness_impact.png
│   ├── experiment3_self_report_vs_behavior.png
│   └── summary_findings.png
├── papers/                   # 32 downloaded research papers
├── datasets/                 # 7 downloaded datasets
└── code/                     # 4 cloned code repositories
```

## Reproducing

```bash
uv venv && source .venv/bin/activate
uv add openai numpy pandas matplotlib seaborn scipy scikit-learn tqdm
export OPENAI_API_KEY="your-key"
python src/experiment.py    # Run experiments (~5 min, ~$2 API cost)
python src/analysis.py      # Generate analysis and figures
```

## Model

GPT-4.1 (OpenAI), temperature=0, seed=42. Total API calls: ~148.
