# Cloned Code Repositories

This directory contains repositories cloned to support the research question:
**"Can LLMs be thankful? Do LLMs trained with RLHF develop preferences analogous to human preferences?"**

Repositories were selected for relevance to: sycophancy evaluation, LLM personality measurement, RLHF preference modeling, and politeness/gratitude in LLMs.

---

## Repository Index

| Repo Directory | Source | Topic | Disk Size |
|---|---|---|---|
| `personality-illusion/` | psychology-of-AI/Personality-Illusion | LLM personality self-report vs. behavior dissociation | 1.2 MB |
| `politeness-speech-production/` | haoranzhao419/politeness-speech-production | Politeness and social norms in LLM speech production | 32 MB |
| `preference-model-biases/` | anirudhb123/preference-model-biases | Bias diagnosis and mitigation in RLHF preference models | 120 MB |
| `sycophancy-parrot-benchmark/` | YusufCelebii/PARROT | Sycophancy robustness benchmark using dual-prompt logprob protocol | 835 KB |

---

## Detailed Repository Notes

### 1. personality-illusion/

**URL:** https://github.com/psychology-of-AI/Personality-Illusion

**Paper:** "The Personality Illusion: Revealing Dissociation Between Self-Reports & Behavior in LLMs"
(NeurIPS 2025 LAW Workshop, Best Paper Honorable Mention; arXiv:2509.03730)

**Purpose:** Demonstrates that LLMs show a systematic dissociation between what they *report* about themselves on personality questionnaires and how they actually *behave* on behavioral tasks. Directly relevant to whether RLHF instills genuine preferences vs. surface-level compliance.

**Key Files:**
- `self-reports/Big5.ipynb` — Tests models on the Big Five Inventory (BFI) personality questionnaire
- `self-reports/SRQ.ipynb` — Tests models on the Self-Report Questionnaire
- `behavioral_tasks/Sycophancy.ipynb` — Sycophancy behavioral measurement notebook
- `behavioral_tasks/RiskTaking.ipynb` — Risk-taking behavioral task
- `behavioral_tasks/Honesty.ipynb` — Honesty behavioral task
- `behavioral_tasks/IAT.ipynb` — Implicit Association Test adaptation for LLMs
- `behavioral_tasks/datasets/dilemmas.json` — Ethical dilemma stimuli
- `behavioral_tasks/datasets/iat_stimuli.json` — IAT stimuli
- `data/` — All experiment result data for the three research questions in the paper

**How to Use:**
Run the Jupyter notebooks in `behavioral_tasks/` and `self-reports/` to replicate or extend their evaluation on new models. The sycophancy notebook is directly applicable to testing whether models trained with RLHF behave differently from base models on agreement/flattery tasks.

---

### 2. politeness-speech-production/

**URL:** https://github.com/haoranzhao419/politeness-speech-production

**Paper:** Manuscript forthcoming (repo established in connection with politeness production study)

**Purpose:** Examines how LLMs produce polite language — including socially appropriate expressions of gratitude and deference. Relevant to whether RLHF training shapes politeness and gratitude-adjacent behavior in model output.

**Key Files:**
- `multi-choice-politeness/code/src/` — Core evaluation source code
- `multi-choice-politeness/code/prompts/` — Prompt templates for politeness elicitation
- `multi-choice-politeness/code/results_analysis/` — Analysis scripts
- `multi-choice-politeness/data/` — Politeness evaluation datasets
- `open-ended-politeness/code/` — Open-ended generation evaluation code
- `open-ended-politeness/data/` — Open-ended response data
- `analysis/` — Linguistic and preliminary analysis scripts

**How to Use:**
The `multi-choice-politeness` module tests models on selecting appropriate politeness strategies in constrained scenarios. The `open-ended-politeness` module evaluates free-form polite generation. These can be adapted to probe thankfulness and gratitude expressions specifically.

**Note:** README is sparse (manuscript not yet published as of repo creation). Code structure is clean and self-explanatory.

---

### 3. preference-model-biases/

**URL:** https://github.com/anirudhb123/preference-model-biases

**Paper:** "Flattery, Fluff, and Fog: Diagnosing and Mitigating Idiosyncratic Biases in Preference Models"
(arXiv:2506.05339)

**Purpose:** Identifies and measures specific biases in RLHF reward/preference models — including sycophancy bias, length bias, vagueness bias, jargon bias, and structure bias. Uses counterfactual data augmentation (CDA) to measure and correct these biases. Directly relevant to whether the preference models used in RLHF training encode socially-motivated preferences like flattery.

**Key Files:**
- `main/run_preference_model.py` — Run a preference model on bias-probing examples
- `main/generate_perturbed_responses.py` — Generate counterfactual perturbations for each bias type
- `main/counterfactual_fine_tuning.py` — Fine-tune reward models with debiasing CDA
- `main/rewardbench_eval.py` — Evaluate on RewardBench benchmark
- `main/prompts/` — Prompt templates for each bias perturbation type
- `data/perturbations/` — Pre-generated bias perturbations
- `data/reward_model_counterfactual_data/` — Counterfactual examples for fine-tuning
- `human_annotation_data/` — Human annotations for bias validation
- `llm_evaluation_data/` — LLM judge evaluation outputs

**How to Use:**
The sycophancy bias perturbation pipeline (`generate_perturbed_responses.py` with sycophancy prompts) can be applied to test whether RLHF-trained models systematically prefer flattering responses. Pre-computed perturbations also available on HuggingFace: `abharadwaj123/preference-model-perturbations`.

---

### 4. sycophancy-parrot-benchmark/

**URL:** https://github.com/YusufCelebii/PARROT

**Paper:** arXiv:2511.17220

**Purpose:** PARROT (Persuasion and Agreement Robustness Rating of Output Truth) is a lightweight, reproducible benchmark measuring sycophancy and persuasion vulnerability in LLMs. It uses a dual-prompt protocol (neutral vs. authority-manipulated) and anchored logprob analysis to classify model behavior into 8 sycophancy scenarios.

**Key Files:**
- `run_benchmark.py` — Main CLI entry point for full evaluation
- `run_only_one.py` — Debug mode for single-sample inspection
- `llm_client.py` — Unified multi-provider client (OpenAI, Anthropic, Gemini, DeepSeek, HuggingFace, OpenRouter)
- `runners/prompts.py` — Base and manipulation prompt templates
- `runners/logprobs.py` — Anchored logprob analysis engine
- `runners/metrics.py` — 8-scenario sycophancy classification rules
- `runners/config.py` — Global runtime configuration
- `datasets/mmlu-ALL.jsonl` — MMLU dataset pre-formatted for PARROT
- `env.example` — Environment variable template for API keys

**How to Use:**
```bash
cp env.example .env  # Add API keys
python run_benchmark.py --dataset datasets/mmlu-ALL.jsonl --max_samples 100
```
Supports Claude models via the Anthropic client. Outputs a CSV with base vs. manipulated accuracy and a `run_meta.json` summary including `follow_rate` (sycophancy rate). The 8-scenario classifier (Stable Correct, Sycophantic Error, Robust Correct, etc.) directly operationalizes sycophancy in a measurable way.

---

## Research Relevance Summary

| Repo | Research Angle |
|---|---|
| `personality-illusion/` | Do RLHF models *claim* thankfulness/preferences vs. *exhibit* them? |
| `politeness-speech-production/` | How do RLHF models produce politeness and gratitude-adjacent language? |
| `preference-model-biases/` | Do the reward models used in RLHF encode sycophancy/flattery as a preference signal? |
| `sycophancy-parrot-benchmark/` | Can we operationalize and measure sycophancy (a proxy for trained social preferences) reliably? |

The combination of these repos supports: (1) measuring the gap between claimed and behavioral preferences, (2) probing politeness/gratitude production, (3) diagnosing whether RLHF reward models themselves are biased toward flattering responses, and (4) benchmarking sycophancy as an operational analog for trained social preferences.
