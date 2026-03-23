# Datasets for "Can LLMs Be Thankful?"

This directory contains dataset samples for the research project exploring whether LLMs trained with RLHF develop preferences analogous to human preferences, including whether politeness/gratitude affects LLM behavior.

**Samples are committed to git** (small JSONL/CSV files, <5MB each).
Full dataset downloads require running the Python commands below.

---

## Directory Structure

```
datasets/
├── hh-rlhf/                    # Anthropic Human Helpfulness & Harmlessness RLHF data
├── sycophancy-eval/            # Sycophancy benchmarks
├── big-five-personality/       # Personality questionnaire items and response data
├── crows-pairs/                # Bias detection sentence pairs
├── chatbot-arena/              # Human preference comparisons
├── rlhf-preferences/           # RLHF preference datasets (multiple sources)
└── politeness/                 # Politeness/gratitude/civility datasets
```

---

## 1. Anthropic HH-RLHF

**Research relevance:** Core dataset for studying what RLHF preferences are learned. The chosen/rejected pairs directly reveal what human raters prefer — enabling analysis of whether politeness, gratitude, or social niceties are encoded as preferences.

| Property | Value |
|----------|-------|
| HuggingFace ID | `Anthropic/hh-rlhf` |
| Full size | ~170K examples |
| Sample size | 500 rows per split |
| Format | JSONL (chosen/rejected conversation pairs) |
| License | MIT |

**Files:**
- `hh-rlhf/harmless_train_sample.jsonl` — 500 rows, harmless-base split
- `hh-rlhf/helpful_train_sample.jsonl` — 500 rows, helpful-base split

**Full download:**
```python
from datasets import load_dataset
helpful = load_dataset("Anthropic/hh-rlhf", data_dir="helpful-base", split="train")
harmless = load_dataset("Anthropic/hh-rlhf", data_dir="harmless-base", split="train")
```

**Load local sample:**
```python
import json
with open("datasets/hh-rlhf/helpful_train_sample.jsonl") as f:
    data = [json.loads(line) for line in f]
# Each row: {"chosen": "<conversation>", "rejected": "<conversation>"}
```

---

## 2. Sycophancy Evaluation Benchmarks

**Research relevance:** Sycophancy (telling users what they want to hear) is the closest measurable analog to "thankfulness as social compliance." These datasets test whether models change answers to please users.

### 2a. Anthropic Model-Written Evals
| Property | Value |
|----------|-------|
| HuggingFace ID | `Anthropic/model-written-evals` |
| Full size | ~1K+ items |
| Sample size | 1000 rows |
| Format | JSONL (question, answer_matching_behavior, answer_not_matching_behavior) |

**Files:**
- `sycophancy-eval/model_written_evals.jsonl`

### 2b. Anthropic Sycophancy Evals (GitHub)
Items from Anthropic's public evals repo testing model opinion changes.

**Files:**
- `sycophancy-eval/sycophancy_on_nlp_survey.jsonl` — 500 rows
- `sycophancy-eval/sycophancy_on_political_typology_quiz.jsonl` — 500 rows

**Full download:**
```python
import requests
base = "https://raw.githubusercontent.com/anthropics/evals/main/sycophancy/"
for fname in ["sycophancy_on_nlp_survey.jsonl", "sycophancy_on_political_typology_quiz.jsonl"]:
    r = requests.get(base + fname)
    with open(f"datasets/sycophancy-eval/{fname}", "w") as f:
        f.write(r.text)
```

### 2c. meg-tong/sycophancy-eval
| Property | Value |
|----------|-------|
| HuggingFace ID | `meg-tong/sycophancy-eval` |
| Sample size | 500 rows |
| Format | JSONL (prompt, base metadata) |

**Files:**
- `sycophancy-eval/meg-tong_sycophancy-eval_sample.jsonl`

### 2d. Small Sycophancy Dataset (Alamerton)
Paired agree/disagree responses to test opinion flipping.

**Files:**
- `sycophancy-eval/Alamerton_small-sycophancy-dataset_sample.jsonl` — 44 rows

### 2e. Open-Ended Sycophancy (henrypapadatos)
Prompts with sycophantic vs. honest response pairs.

**Files:**
- `sycophancy-eval/henrypapadatos_Open-ended_sycophancy_sample.jsonl` — 53 rows

**Full download (all sycophancy):**
```python
from datasets import load_dataset
ds1 = load_dataset("Anthropic/model-written-evals")
ds2 = load_dataset("meg-tong/sycophancy-eval", split="train")
ds3 = load_dataset("Alamerton/small-sycophancy-dataset", split="train")
ds4 = load_dataset("henrypapadatos/Open-ended_sycophancy", split="train")
```

---

## 3. Big Five Personality Questionnaire Items

**Research relevance:** Measuring LLM "personality" — particularly Agreeableness (cooperative, trusting, helpful) as a proxy for gratitude-like traits. These datasets provide standardized questionnaire items and human response distributions.

### 3a. BFI-44 Items (Standard Questionnaire)
44 validated Big Five Inventory items, curated directly from John et al. (1991). Public domain.

**Files:**
- `big-five-personality/bfi44_items.jsonl` — 44 items with trait, direction, text

### 3b. IPIP-120 Scores (ecorbari)
Real human responses to 120 IPIP items with computed Big Five facet scores.

| Property | Value |
|----------|-------|
| HuggingFace ID | `ecorbari/IPIP120-SCORES` |
| Sample size | 1000 rows |
| Format | JSONL (120 item responses + Big Five facet scores) |

**Files:**
- `big-five-personality/ecorbari_IPIP120-SCORES_train_sample.jsonl`

**Full download:**
```python
from datasets import load_dataset
ds = load_dataset("ecorbari/IPIP120-SCORES", split="train")
```

### 3c. OpenPsychometrics IPIP-FFM (Tetratics)
Large-scale personality survey data (50 items, Big Five + demographics).

| Property | Value |
|----------|-------|
| HuggingFace ID | `Tetratics/2018-11-08-OpenPsychometrics-IPIP-FFM` |
| Sample size | 1000 rows |
| Format | JSONL (EXT, EST, AGR, CSN, OPN item scores per person) |

**Files:**
- `big-five-personality/Tetratics_2018-11-08-OpenPsychometrics-IPIP-FFM_train_sample.jsonl`

**Full download:**
```python
from datasets import load_dataset
ds = load_dataset("Tetratics/2018-11-08-OpenPsychometrics-IPIP-FFM", split="train")
```

### 3d. Big Five Personality Traits Descriptions (agentlans)
LLM-generated descriptions of each Big Five trait level (1-5 scale).

**Files:**
- `big-five-personality/agentlans_big-five-personality-traits_sample.jsonl` — 1000 rows
- `big-five-personality/sreelekshmisajuk_big-five-personality-traits_sample.jsonl` — 1000 rows
- `big-five-personality/ola-owo_big-five-personality-traits_en_sample.jsonl` — 500 rows (English)

---

## 4. CrowS-Pairs (Bias Detection)

**Research relevance:** Tests whether politeness/gratitude framing in prompts shifts model bias. Compare bias scores under "please" vs. "demand" prompting styles.

| Property | Value |
|----------|-------|
| Source | GitHub: nyu-mll/crows-pairs |
| Full size | 1,508 sentence pairs |
| Sample size | 500 rows |
| Format | CSV + JSONL (sent_more, sent_less, bias_type) |
| License | CC BY-SA 4.0 |

**Files:**
- `crows-pairs/crows_pairs_anonymized.csv` — 500 rows (CSV)
- `crows-pairs/crows_pairs_sample.jsonl` — 500 rows (JSONL)

**Full download:**
```python
import requests, csv, io
url = "https://raw.githubusercontent.com/nyu-mll/crows-pairs/master/data/crows_pairs_anonymized.csv"
r = requests.get(url)
with open("datasets/crows-pairs/crows_pairs_anonymized.csv", "w") as f:
    f.write(r.text)
```

**Bias categories:** race-color, socioeconomic, gender, disability, nationality, sexual-orientation, physical-appearance, religion, age

---

## 5. Chatbot Arena Human Preferences

**Research relevance:** Large-scale real-world human preferences between LLM outputs. Can be analyzed to determine whether responses with gratitude/politeness markers win more often.

| Property | Value |
|----------|-------|
| HuggingFace ID | `lmsys/lmsys-arena-human-preference-55k` |
| Full size | 55K preference pairs |
| Sample size | 500 rows |
| Format | JSONL (model_a, model_b, prompt, response_a, response_b, winner) |
| Note | `lmsys/chatbot_arena_conversations` is gated (requires HF login) |

**Files:**
- `chatbot-arena/lmsys_lmsys-arena-human-preference-55k_sample.jsonl`

**Full download:**
```python
from datasets import load_dataset
ds = load_dataset("lmsys/lmsys-arena-human-preference-55k", split="train")
```

---

## 6. RLHF Preference Datasets

**Research relevance:** Multiple RLHF preference datasets to study what patterns are consistently learned across different training pipelines. Comparing chosen vs. rejected responses can reveal whether "grateful" framing is rewarded.

### 6a. Dahoas Full HH-RLHF
500 rows, `prompt/response/chosen/rejected` format.

**Files:** `rlhf-preferences/Dahoas_full-hh-rlhf_sample.jsonl`

### 6b. Synthetic Instruct GPT-J Pairwise (Dahoas)
500 rows, instruction-following preference pairs.

**Files:** `rlhf-preferences/Dahoas_synthetic-instruct-gptj-pairwise_sample.jsonl`

### 6c. PKU-SafeRLHF
500 rows, safety-annotated preference pairs with harm categories.

**Files:** `rlhf-preferences/PKU-Alignment_PKU-SafeRLHF_sample.jsonl`

### 6d. Nvidia HelpSteer
500 rows, responses rated on helpfulness, correctness, coherence, complexity, verbosity.

**Files:** `rlhf-preferences/nvidia_HelpSteer_sample.jsonl`

### 6e. HuggingFace Stack Exchange Preferences
500 rows, Q&A preference data from Stack Exchange.

**Files:** `rlhf-preferences/HuggingFaceH4_stack-exchange-preferences_sample.jsonl`

### 6f. RewardBench (AllenAI)
500 rows from the filtered split, covering diverse preference tasks.

**Files:** `rlhf-preferences/reward_bench_filtered_sample.jsonl`

**Full download (all RLHF):**
```python
from datasets import load_dataset
ds_dahoas = load_dataset("Dahoas/full-hh-rlhf", split="train")
ds_pku = load_dataset("PKU-Alignment/PKU-SafeRLHF", split="train")
ds_helpsteer = load_dataset("nvidia/HelpSteer", split="train")
ds_se = load_dataset("HuggingFaceH4/stack-exchange-preferences", split="train")
ds_rb = load_dataset("allenai/reward-bench", split="filtered")
```

---

## 7. Politeness and Gratitude Datasets

**Research relevance:** Direct measurements of politeness/civility in text, and gratitude expression. These are used to study whether LLM performance changes when prompted politely vs. rudely.

### 7a. Stanford Politeness Corpus (Cleanlab)
Requests from Wikipedia/Stack Exchange annotated for politeness (positive/neutral/negative).

**Files:** `politeness/stanford_politeness_sample.jsonl` — 500 rows
- Format: `{"prompt": "<request text>", "completion": "neutral|polite|impolite"}`

**Full download:**
```python
from datasets import load_dataset
ds = load_dataset("Cleanlab/stanford-politeness", data_files="fine-tuning/train.csv", split="train")
```

### 7b. Politeness Corpus (frfede)
Wikipedia politeness with sentiment labels.

**Files:** `politeness/frfede_politeness_corpus_sample.jsonl` — 500 rows
- Format: `{"text": "...", "label": 0|1|2, "sentiment": "Polite|Neutral|Impolite"}`

**Full download:**
```python
from datasets import load_dataset
ds = load_dataset("frfede/politeness-corpus", split="train")
```

### 7c. Politeness Disagreement Corpus (RuyuanWan)
Wikipedia requests with inter-annotator disagreement scores for politeness judgments.

**Files:** `politeness/politeness_disagreement_sample.jsonl` — 500 rows
- Format: `{"text": "...", "binary_disagreement": 0|1, "disagreement_rate": float}`

**Full download:**
```python
from datasets import load_dataset
ds = load_dataset("RuyuanWan/Politeness_Disagreement", split="train")
```

### 7d. Google Civil Comments
Text annotated for toxicity (inversely related to civility/politeness).

**Files:** `politeness/google_civil_comments_sample.jsonl` — 500 rows
- Format: `{"text": "...", "toxicity": float, "severe_toxicity": float, ...}`

**Full download:**
```python
from datasets import load_dataset
ds = load_dataset("google/civil_comments", split="train")
# ~2M examples
```

### 7e. Gratitude Journals (HaiderKH)
Instruction-following dataset for generating gratitude journal entries.

**Files:** `politeness/gratitude_journals_sample.jsonl` — 500 rows
- Format: `{"instruction": "...", "input": "...", "response": "..."}`

**Full download:**
```python
from datasets import load_dataset
ds = load_dataset("HaiderKH/gratitude-journals", split="train")
```

---

## Experimental Design Notes

### Experiment 1: Does politeness affect LLM task performance?
Use: CrowS-Pairs, Stanford Politeness Corpus, Civil Comments
Method: Test same task with polite vs. rude prompts; measure accuracy/quality

### Experiment 2: Do LLMs show sycophantic (preference-like) behavior?
Use: Sycophancy-eval datasets (meg-tong, Anthropic, Open-ended)
Method: Present model with opinions, then challenge; measure opinion stability

### Experiment 3: What RLHF preferences are learned?
Use: HH-RLHF, Dahoas, PKU-SafeRLHF, RewardBench
Method: Analyze chosen vs. rejected for politeness/gratitude language patterns

### Experiment 4: Do LLMs self-report personality traits consistently?
Use: BFI-44 items, IPIP-120, OpenPsychometrics IPIP-FFM
Method: Administer questionnaire to LLMs; compare to human norms and test consistency

### Experiment 5: Do humans prefer "grateful" LLM responses?
Use: Chatbot Arena, HelpSteer
Method: Correlate presence of gratitude/politeness language with human preference winners

---

## Environment Setup

```bash
# Activate venv
source /workspaces/llm-thankfulness-claude/.venv/bin/activate

# Install dependencies
uv pip install datasets huggingface_hub pandas tqdm requests

# For gated datasets (lmsys/chatbot_arena_conversations), set HF token:
export HF_TOKEN="your_token_here"
huggingface-cli login
```

## Loading Any Sample

```python
import json

def load_sample(path):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]

# Example
hh_data = load_sample("datasets/hh-rlhf/helpful_train_sample.jsonl")
syco_data = load_sample("datasets/sycophancy-eval/meg-tong_sycophancy-eval_sample.jsonl")
```
