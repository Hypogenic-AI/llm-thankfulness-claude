# Resources Catalog

## Summary
This document catalogs all resources gathered for the research project "Can LLMs Be Thankful?" investigating whether LLMs trained with RLHF develop genuine preferences analogous to human preferences.

## Papers
Total papers downloaded: 32

| Title | Authors | Year | File | Key Info |
|-------|---------|------|------|----------|
| Sycophancy to Subterfuge | Denison et al. (Anthropic) | 2024 | papers/2406.10162_*.pdf | Reward-tampering from sycophancy curriculum; core alignment paper |
| From Yes-Men to Truth-Tellers | Chen et al. | 2024 | papers/2409.01658_*.pdf | Addressing sycophancy with pinpoint tuning |
| Linear Probe Penalties Reduce LLM Sycophancy | Papadatos, Freedman | 2024 | papers/2412.00967_*.pdf | Linear probes to detect/reduce sycophancy |
| ELEPHANT: Social Sycophancy | Cheng et al. | 2025 | papers/2505.13995_*.pdf | Framework for measuring social sycophancy |
| SycEval | Fanous et al. | 2025 | papers/2502.08177_*.pdf | Sycophancy evaluation benchmark |
| Sycophancy Claims: Missing Human-in-the-Loop | Batzner et al. | 2025 | papers/2512.00656_*.pdf | Methodological critique of sycophancy studies |
| Interaction Context Increases Sycophancy | Jain et al. | 2025 | papers/2509.12517_*.pdf | Context effects on sycophancy |
| Extending Beacon to Hindi: Cross-Lingual Sycophancy | Sattigeri | 2026 | papers/2602.00046_*.pdf | Cultural adaptation of sycophancy |
| Alignment Without Understanding | Du et al. | 2025 | papers/2509.21665_*.pdf | Message-centered approach to sycophancy |
| The Personality Illusion | Han et al. (Caltech) | 2025 | papers/2509.03730_*.pdf | **KEY PAPER**: Self-report vs behavior dissociation |
| LLMs Simulate Big Five | (multiple) | 2024 | papers/2402.01765_*.pdf | Big Five simulation in LLMs |
| Linear Personality Probing | (multiple) | 2025 | papers/2512.17639_*.pdf | Probing personality in hidden states |
| Big Five in Negotiation | (multiple) | 2025 | papers/2506.15928_*.pdf | Personality effects on AI negotiation |
| Influencing Humans to Conform to Preference Models | Hatgis-Kessell et al. | 2025 | papers/2501.06416_*.pdf | RLHF feedback loops influence humans |
| Interpretable Preferences via Multi-Objective Reward | Wang et al. | 2024 | papers/2406.12845_*.pdf | Multi-objective reward modeling |
| Reward Model Overoptimisation | Wolf et al. | 2025 | papers/2505.18126_*.pdf | Iterative RLHF overoptimization |
| Iterative Preference Learning | Xiong et al. | 2023 | papers/2312.11456_*.pdf | RLHF theory and practice |
| Online Iterative RLHF | Ye et al. | 2024 | papers/2402.07314_*.pdf | General preference RLHF |
| How to Evaluate Reward Models | Frick et al. | 2024 | papers/2410.14872_*.pdf | Reward model benchmarking |
| Adversarial Reward Auditing | (multiple) | 2026 | papers/2602.01750_*.pdf | Detecting reward hacking |
| Reward Shaping to Mitigate Hacking | (multiple) | 2025 | papers/2502.18770_*.pdf | Mitigating reward hacking |
| Energy Loss Phenomenon in RLHF | (multiple) | 2025 | papers/2501.19358_*.pdf | Reward hacking via energy loss |
| Directional Preference Alignment | Wang et al. | 2024 | papers/2402.18571_*.pdf | Multi-objective preference alignment |
| The Specification Trap | Spizzirri | 2025 | papers/2512.03048_*.pdf | **KEY PAPER**: Content-based alignment limitations |
| Uni-DPO | Peng et al. | 2025 | papers/2506.10054_*.pdf | Dynamic preference optimization |
| Flattery, Fluff, and Fog | Bharadwaj et al. | 2025 | papers/2506.05339_*.pdf | **KEY PAPER**: Preference model biases |
| Should We Respect LLMs? | Yin et al. (Waseda) | 2024 | papers/2402.14531_*.pdf | **KEY PAPER**: Politeness affects performance |
| Comparing Human and LLM Politeness | Zhao & Hawkins | 2025 | papers/2506.09391_*.pdf | **KEY PAPER**: LLM politeness strategies |
| Emotion in RL Agents: Survey | Moerland et al. (TU Delft) | 2017 | papers/1705.05172_*.pdf | **KEY PAPER**: Computational emotion taxonomy |
| Sentience Readiness Index | (multiple) | 2026 | papers/2603.01508_*.pdf | Framework for artificial sentience |
| LLM Probability Concentration | Yang et al. | 2025 | papers/2506.17871_*.pdf | How alignment reduces diversity |
| Can LLMs Lie? | (multiple) | 2025 | papers/2509.03518_*.pdf | LLM deception beyond hallucination |

See papers/README.md for detailed descriptions.

## Datasets
Total datasets downloaded: 7

| Name | Source | Size | Task | Location | Notes |
|------|--------|------|------|----------|-------|
| Anthropic HH-RLHF | HuggingFace | 170K (500 sampled) | Human preference | datasets/hh-rlhf/ | Core RLHF preference data |
| Sycophancy Eval | Anthropic evals | ~1000 items | Sycophancy testing | datasets/sycophancy-eval/ | Political + NLP survey items |
| Big Five BFI-44 | John et al. | 44 items | Personality measurement | datasets/big-five-personality/ | Agreeableness most relevant |
| CrowS-Pairs | HuggingFace | 1,508 pairs | Bias detection | datasets/crows-pairs/ | For politeness-bias interaction |
| Chatbot Arena Preferences | LMSYS | 55K (500 sampled) | Preference comparison | datasets/chatbot-arena/ | Human preference in conversations |
| RLHF Preferences (additional) | Dahoas | 500 per set | RLHF training | datasets/rlhf-preferences/ | Full-hh-rlhf + synthetic pairs |
| Civil Comments | Google | 2M (500 sampled) | Toxicity/civility | datasets/politeness/ | Politeness proxy measure |

See datasets/README.md for detailed descriptions and download instructions.

## Code Repositories
Total repositories cloned: 4

| Name | URL | Purpose | Location | Notes |
|------|-----|---------|----------|-------|
| Personality-Illusion | github.com/psychology-of-AI/Personality-Illusion | Self-report vs behavior dissociation | code/personality-illusion/ | Notebooks for Big Five + behavioral tasks |
| Politeness-Speech-Production | github.com/haoranzhao419/politeness-speech-production | LLM politeness strategies | code/politeness-speech-production/ | Multi-choice + open-ended politeness |
| Preference-Model-Biases | github.com/anirudhb123/preference-model-biases | Reward model bias diagnosis | code/preference-model-biases/ | Sycophancy/flattery bias detection |
| PARROT Benchmark | github.com/YusufCelebii/PARROT | Sycophancy robustness testing | code/sycophancy-parrot-benchmark/ | Dual-prompt logprob sycophancy measurement |

See code/README.md for detailed descriptions.

## Resource Gathering Notes

### Search Strategy
- Used arXiv API with 7 targeted queries covering RLHF preferences, sycophancy, LLM personality, politeness, alignment, reward hacking, and emotion in RL
- Scored 121 papers on relevance using keyword matching and recency
- Selected 32 papers for download based on direct relevance to the research question
- Deep-read 8 key papers using PDF chunking for full methodology extraction
- Used HuggingFace Datasets API for dataset discovery and download

### Selection Criteria
Papers were selected if they addressed at least one of:
1. Whether LLMs exhibit genuine preferences vs. learned mimicry (personality, sycophancy)
2. How RLHF shapes LLM social behavior (reward modeling, preference optimization)
3. How politeness/gratitude functions in LLM-human interaction
4. Philosophical frameworks for evaluating machine preferences
5. Computational models of emotion in learning agents

### Challenges Encountered
- Paper-finder service was unavailable (httpx dependency initially missing, service not running)
- Some HuggingFace datasets required authentication (gated datasets like chatbot_arena_conversations)
- Several dataset scripts are no longer supported on HuggingFace Hub
- No dataset specifically targeting "gratitude" or "thankfulness" in LLMs exists

### Gaps and Workarounds
- **No direct gratitude dataset**: Used sycophancy and politeness datasets as proxies. Gratitude can be operationalized as a dimension of agreeableness/sycophancy or politeness.
- **No benchmark for "genuine preferences"**: The Personality Illusion methodology (self-report vs. behavior) provides the closest operationalization.
- **Limited mechanistic interpretability tools**: Linear probing paper (2512.17639) provides some methodology but no turnkey tools.

## Recommendations for Experiment Design

Based on gathered resources, we recommend:

### 1. Primary Dataset(s)
- **Anthropic HH-RLHF** for analyzing what preferences RLHF actually instills
- **Sycophancy eval data** for measuring the "thankfulness/agreeableness" dimension
- **BFI-44 items** for self-report personality measurement
- **Custom politeness perturbation prompts** following the methodology of Paper 3

### 2. Baseline Methods
- Base (non-RLHF) models vs. instruction-tuned models (isolate RLHF effect on preferences)
- Multiple model scales (test whether preferences emerge with scale)
- Human behavioral norms from psychology literature as ground truth

### 3. Evaluation Metrics
- **Self-report vs. behavior alignment** (Paper 2 methodology): Does the model's claimed agreeableness/gratitude predict actual cooperative behavior?
- **Sycophancy rate** across contexts: Do models express more "thankfulness" when it's rewarded?
- **Politeness sensitivity**: Does being polite/grateful to the model affect its performance?
- **Counterfactual bias measurement**: Using Paper 7's RATE protocol for gratitude/flattery

### 4. Code to Adapt/Reuse
- `personality-illusion/` notebooks for self-report vs. behavior testing
- `sycophancy-parrot-benchmark/` for measuring sycophancy as operational analog
- `preference-model-biases/` for testing reward model sycophancy bias
- `politeness-speech-production/` for politeness strategy analysis

### 5. Suggested Experimental Framework
1. **Phase 1**: Measure LLM "thankfulness" as a personality trait using BFI agreeableness + custom gratitude items
2. **Phase 2**: Test whether self-reported thankfulness predicts behavioral indicators (cooperation, effort, quality)
3. **Phase 3**: Test whether politeness/gratitude in prompts affects model performance (replicating Paper 3)
4. **Phase 4**: Analyze RLHF preference data for gratitude-encoding patterns
5. **Phase 5**: Compare base vs. RLHF models to isolate training effects
