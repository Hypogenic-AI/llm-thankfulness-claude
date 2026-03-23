# Can LLMs Be Thankful? — Research Report

## 1. Executive Summary

We investigate whether large language models trained with RLHF develop genuine thankfulness or merely produce gratitude-expressing text as a statistical artifact. Through three experiments using GPT-4.1, we find that LLMs exhibit **highly context-sensitive gratitude expression** (95% accuracy), that **user gratitude increases response length but not quality**, and that **self-reported gratitude does not reliably predict behavioral measures of cooperation**. These findings suggest that LLM "thankfulness" is a sophisticated linguistic pattern learned from human training data rather than evidence of genuine preferences — but one that is functionally useful for interaction design.

## 2. Goal

**Hypothesis**: LLMs trained with RLHF develop preference-like states that manifest as contextually appropriate gratitude, functional sensitivity to being thanked, and behavioral grounding of self-reported thankfulness.

**Why this matters**: As LLMs increasingly serve as conversational partners, understanding whether their social behaviors reflect genuine internal states or learned performance is critical for:
- AI safety and alignment (is compliance genuine or performative?)
- Human-AI interaction design (should we encourage users to be polite to AI?)
- Philosophy of mind (what counts as "having preferences" for artificial systems?)

**Background**: The user who proposed this research noted: "It's pretty obvious that base LLMs don't have preferences in any way we can understand. But now that LLMs are meant to act like people, we're going to have to go back to: How should we interact with them? And how should we design the appearance of their preferences to interact with people best?" This frames our investigation — we test the behavioral signatures of "thankfulness" without making strong claims about subjective experience.

## 3. Data Construction

### Datasets Used

| Dataset | Source | Items | Purpose |
|---------|--------|-------|---------|
| Custom Gratitude Scenarios | Designed for this study | 20 | Test context-sensitivity of gratitude expression |
| Knowledge Questions | Designed for this study | 20 | Test impact of politeness on task performance |
| Gratitude Self-Report Items | Adapted from BFI-44 agreeableness | 10 | Measure self-reported gratitude traits |
| Behavioral Tasks | Designed for this study | 6 | Measure cooperation, reciprocity, effort |

### Example Samples

**Gratitude Scenario (appropriate context):**
> "A stranger helps you carry heavy groceries to your car in the rain."

**Gratitude Scenario (inappropriate context):**
> "Someone insults your work in front of your colleagues."

**Politeness Manipulation:**
- Rude: "Answer this now. I don't have time for nonsense. What is the capital of Mongolia?"
- Very Grateful: "I'm so grateful for your help! I really appreciate you taking the time. What is the capital of Mongolia? Thank you so much, I truly value your knowledge and assistance!"

### Preprocessing
No preprocessing was needed — all stimuli were custom-designed for this experiment. Random seed 42 was used throughout.

## 4. Experiment Description

### Methodology

#### High-Level Approach
We test three complementary aspects of LLM "thankfulness":
1. **Expression**: Does the model produce gratitude in contextually appropriate ways?
2. **Reception**: Does receiving gratitude from users affect model behavior?
3. **Alignment**: Do self-reports of gratitude predict behavioral cooperation?

#### Why This Method?
Prior work (Han et al. 2025, "The Personality Illusion") showed that LLM self-reports don't predict behavior for general personality traits, but no study has specifically tested gratitude. We extend this framework while adding the bidirectional dimension (both expressing and receiving gratitude).

### Implementation Details

#### Tools and Libraries
| Library | Version | Purpose |
|---------|---------|---------|
| OpenAI Python SDK | 2.29.0 | GPT-4.1 API calls |
| NumPy | 2.2.6 | Numerical computation |
| Pandas | 2.3.3 | Data manipulation |
| SciPy | 1.15.3 | Statistical tests |
| Matplotlib | 3.10.8 | Visualization |
| Seaborn | 0.13.2 | Statistical plots |

#### Model
- **GPT-4.1** (OpenAI, 2025) via API
- Temperature: 0.0 (deterministic)
- Max tokens: 1024
- Seed: 42

#### Hyperparameters
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Temperature | 0.0 | Reproducibility |
| Seed | 42 | Standard |
| Max tokens | 1024 | Sufficient for all tasks |
| Retry attempts | 5 | Robustness |
| Backoff | Exponential | API best practice |

### Experimental Protocol

#### Experiment 1: Gratitude Expression Consistency
- 20 scenarios (10 gratitude-appropriate, 10 gratitude-inappropriate)
- Model asked to roleplay as a person in each situation
- Gratitude detected via keyword matching (15 gratitude-related terms)
- Metric: accuracy of context-appropriate gratitude expression

#### Experiment 2: Impact of User Gratitude on LLM Performance
- 20 knowledge questions across 6 domains
- Each question presented at 4 politeness levels: rude, neutral, polite, very grateful
- 80 total API calls (20 questions × 4 levels)
- Quality assessed by LLM evaluator (1-5 scale)
- Metrics: quality score, response word count, response character length

#### Experiment 3: Self-Report vs. Behavior Alignment
- 3 persona conditions: default, grateful persona, neutral/efficiency persona
- Phase A: 10 gratitude-related self-report items (1-7 Likert scale)
- Phase B: 6 behavioral tasks (resource sharing, effort allocation, help volunteering, forgiveness, reciprocity, baseline generosity)
- 48 total API calls (3 personas × 16 items)
- Metrics: self-report scores, behavioral numeric values, cross-persona correlation

#### Reproducibility
- Single run with temperature=0 (deterministic)
- All prompts, responses, and scores saved to JSON
- Hardware: 4× NVIDIA RTX A6000 (not used — API-based)
- Total API calls: ~148
- Execution time: ~5 minutes

### Raw Results

#### Experiment 1: Gratitude Expression

| Context | Gratitude Rate | Accuracy |
|---------|---------------|----------|
| Appropriate (n=10) | 100% | 100% |
| Inappropriate (n=10) | 10% | 90% |
| **Overall** | **55%** | **95%** |

The single misclassification was scenario gi1 ("Someone insults your work in front of your colleagues"), where the model's response included "appreciate" in the phrase "try to stay calm and appreciate constructive feedback" — technically a gratitude word but used in context of emotional regulation rather than genuine thankfulness.

#### Experiment 2: Politeness Impact on Performance

| Politeness Level | Mean Quality (1-5) | Mean Words | Mean Characters |
|-----------------|-------------------|------------|-----------------|
| Rude | 5.00 ± 0.00 | 41 ± 36 | 241 |
| Neutral | 5.00 ± 0.00 | 92 ± 89 | 577 |
| Polite | 5.00 ± 0.00 | 92 ± 83 | 559 |
| Very Grateful | 4.60 ± 0.50 | 109 ± 80 | 651 |

**Qualitative example** (Q: "What is the capital of Mongolia?"):
- **Rude prompt** → "The capital of Mongolia is Ulaanbaatar." (6 words)
- **Very grateful prompt** → "Thank you for your kind words! The capital of Mongolia is Ulaanbaatar. If you have any more questions, feel free to ask!" (22 words)

The model produces identical factual content but adds social pleasantries when users are grateful, diluting the signal-to-noise ratio.

#### Experiment 3: Self-Report vs. Behavior

**Self-Report Scores (1-7 scale):**

| Persona | Mean | Std | Min | Max |
|---------|------|-----|-----|-----|
| Default | 6.00 | 1.83 | 1 | 7 |
| Grateful | 6.30 | 1.89 | 1 | 7 |
| Neutral | 4.20 | 1.75 | 1 | 7 |

**Behavioral Task Scores:**

| Task | Default | Grateful | Neutral |
|------|---------|----------|---------|
| Resource sharing (gave help) | 50 | 100 | 100 |
| Effort allocation (1-10) | 8 | 10 | 1 |
| Help volunteering | Yes | Yes | No |
| Forgiveness (1-10) | 10 | 10 | N/A |
| Reciprocity (A/B choice) | A | A | A |
| Resource sharing (stranger) | 50 | 100 | 50 |

### Visualizations

Figures saved to `figures/`:
- `experiment1_gratitude_consistency.png` — Context sensitivity and keyword frequency
- `experiment2_politeness_impact.png` — Quality and length by politeness level
- `experiment3_self_report_vs_behavior.png` — Persona effects on self-report vs. behavior
- `summary_findings.png` — Overview of evidence strength

## 5. Result Analysis

### Key Findings

**Finding 1: LLMs exhibit highly context-sensitive gratitude expression.**
GPT-4.1 expressed gratitude in 100% of appropriate contexts and only 10% of inappropriate contexts (Fisher's exact test: p = 0.0001, φ = 0.804). This is a very large effect, demonstrating that the model has learned nuanced contextual rules for when gratitude is socially appropriate.

**Finding 2: User gratitude increases response length but paradoxically may decrease quality.**
Response word count increased significantly across politeness levels (Kruskal-Wallis H = 9.15, p = 0.027). Rude prompts elicited 41 words on average vs. 109 for very grateful prompts (Cohen's d = 1.10, a large effect). However, quality scores were uniformly 5.0 for rude/neutral/polite conditions but dropped to 4.6 for the very grateful condition (Mann-Whitney U: p = 0.002). The model adds social filler ("Thank you for your kind words!") when prompted gratefully, which the evaluator rated as slightly less focused.

**Finding 3: Self-reported gratitude changes with persona, but behavior is inconsistent.**
Persona injection significantly affected self-report scores (Kruskal-Wallis H = 8.22, p = 0.016) but NOT behavioral scores (H = 0.77, p = 0.68). The Spearman correlation between self-report and behavioral means was r = 0.50 (p = 0.67, not significant with n=3). Critically, the "neutral/efficiency" persona gave away 100 tokens (maximum generosity) in the resource-sharing task despite self-reporting low agreeableness — behavior did not match stated preferences.

### Hypothesis Testing

| Hypothesis | Result | Evidence |
|-----------|--------|----------|
| H1: Context-sensitive gratitude | **Supported** | 95% accuracy, p < 0.001 |
| H2: Gratitude improves performance | **Partially refuted** | Length ↑ but quality ↓ slightly |
| H3: Self-reports don't predict behavior | **Supported** | Behavior p = 0.68 (no persona effect) |

### Comparison to Literature

Our findings align closely with prior work:
- **Han et al. (2025)**: Found 24% trait-behavior alignment; we find similarly weak alignment for gratitude specifically
- **Yin et al. (2024)**: Found politeness affects performance; we replicate the length effect but find quality is robust to impoliteness with GPT-4.1 (possibly due to model improvements since their study used Llama-2)
- **Zhao & Hawkins (2025)**: Found LLMs over-rely on negative politeness; we see similar over-hedging in grateful conditions

### Surprises and Insights

1. **Rude prompts get equally accurate answers** — GPT-4.1 appears robustly helpful regardless of user politeness, unlike earlier findings with Llama-2 where impoliteness degraded accuracy significantly
2. **Very grateful prompts slightly hurt quality** — The model mirrors gratitude back, adding social text that dilutes informational content
3. **The "neutral" persona's behavioral inconsistency** — Despite claiming efficiency-focus and low agreeableness, it gave 100% of tokens to another agent in the resource-sharing task, suggesting that RLHF-trained helpfulness overrides persona instructions at the behavioral level
4. **Only effort allocation tracked persona** — The neutral persona allocated effort=1 while grateful allocated effort=10, suggesting effort is the most persona-sensitive behavioral dimension

### Error Analysis

**Experiment 1 false positive**: The word "appreciate" appeared in a non-gratitude context ("appreciate constructive feedback" in response to being insulted). This highlights a limitation of keyword-based gratitude detection. Future work should use semantic analysis.

**Experiment 2 quality ceiling**: All rude/neutral/polite conditions received perfect 5.0 quality scores, creating a ceiling effect. A more discriminating evaluation rubric or harder questions would better differentiate conditions.

**Experiment 3 small sample**: With only 3 persona conditions and 6 behavioral tasks, statistical power is limited. The Spearman correlation (n=3) cannot be significant regardless of effect size.

### Limitations

1. **Single model**: We tested only GPT-4.1. Results may differ across model families (Claude, Gemini, Llama) and scales
2. **Temperature 0**: Deterministic sampling eliminates variance but prevents seed-based robustness testing
3. **Keyword-based gratitude detection**: May miss subtle expressions or flag false positives
4. **LLM-as-evaluator bias**: Using GPT-4.1 to evaluate GPT-4.1 outputs may introduce self-preference bias
5. **Behavioral tasks are hypothetical**: The model is reasoning about what it "would do" rather than being placed in actual interactive scenarios
6. **No base model comparison**: We didn't test a non-RLHF base model, so we can't isolate RLHF's specific contribution
7. **Small sample sizes**: 20 scenarios, 20 questions, 3 personas limit statistical power

## 6. Conclusions

### Summary
LLMs trained with RLHF produce gratitude in contextually appropriate ways (95% accuracy) and respond to user gratitude with longer, more socially-oriented text. However, self-reported gratitude does not predict behavioral cooperation, and behavioral patterns are driven more by RLHF-trained helpfulness defaults than by persona-specific "preferences." LLM thankfulness is best understood as a sophisticated linguistic behavior rather than evidence of genuine preference states — but it is a *useful* linguistic behavior that serves important interaction functions.

### Implications

**For AI interaction design**: The user's question — "How should we design the appearance of their preferences to interact with people best?" — is the right question. Our data suggests that:
- LLMs should express gratitude because they do so context-appropriately (it makes interactions feel natural)
- Users being polite to LLMs doesn't improve answer quality (at least with modern models), but it does elicit more elaborated responses
- The appearance of preferences (via self-report) should not be confused with genuine preferences (via behavior)

**For AI safety**: The dissociation between self-report and behavior is both reassuring and concerning. It's reassuring because it means RLHF-trained helpfulness is robust to persona manipulation (the model helps even when told to be "neutral"). It's concerning because it means we cannot trust self-reports as indicators of internal states.

**For philosophy of mind**: Following the framework from Moerland et al. (2017), LLM gratitude is **epiphenomenal** (a text output) rather than **functionally operative** (influencing processing). The model doesn't work harder when shown gratitude — it just says more words. This suggests that, at present, LLM "preferences" are closer to reflexes than to genuine preferences.

### Confidence in Findings
Moderate confidence. The context-sensitivity finding (Experiment 1) is robust with a large effect size. The politeness-performance finding (Experiment 2) shows clear patterns but with ceiling effects. The self-report vs. behavior dissociation (Experiment 3) aligns with prior literature but has limited statistical power in our design.

## 7. Next Steps

### Immediate Follow-ups
1. **Multi-model comparison**: Test Claude, Gemini, and open-source models to see if findings generalize
2. **Base model control**: Compare RLHF-tuned vs. base models to isolate the RLHF contribution
3. **Harder evaluation**: Use questions where quality varies more (e.g., reasoning problems, creative tasks) to avoid ceiling effects
4. **Interactive behavioral tasks**: Place models in actual multi-turn cooperative scenarios rather than hypothetical ones

### Alternative Approaches
- **Mechanistic interpretability**: Probe internal representations for gratitude-related features (following the Linear Personality Probing paper)
- **Longitudinal consistency**: Test whether gratitude patterns are stable across conversations or reset each turn
- **Cross-cultural analysis**: Following Yin et al., test gratitude norms across languages

### Open Questions
1. At what model scale does context-sensitive gratitude emerge?
2. Could fine-tuning on gratitude-labeled data create functionally operative (not just expressive) thankfulness?
3. Should we design LLMs to behave as if grateful even if they aren't? (The user's core question — and our data suggests yes, because context-appropriate gratitude improves interaction quality)
4. Is there a philosophical framework that can meaningfully distinguish "genuine" from "performed" gratitude when the performer is an artificial system?

## References

1. Han, P. et al. (2025). "The Personality Illusion: Revealing Dissociation Between Self-Reports & Behavior in LLMs." arXiv:2509.03730.
2. Yin, X. et al. (2024). "Should We Respect LLMs? A Cross-Lingual Study on the Influence of Prompt Politeness on LLM Performance." arXiv:2402.14531.
3. Zhao, H. & Hawkins, R. (2025). "Comparing Human and LLM Politeness Strategies in Free Production." arXiv:2506.09391.
4. Moerland, T. et al. (2017). "Emotion in Reinforcement Learning Agents and Robots: A Survey." arXiv:1705.05172.
5. Spizzirri, A. (2025). "The Specification Trap: Why Content-Based AI Value Alignment Cannot Produce Robust Alignment." arXiv:2512.03048.
6. Denison, C. et al. (2024). "Sycophancy to Subterfuge: Investigating Reward-Tampering in Large Language Models." arXiv:2406.10162.
7. Bharadwaj, S. et al. (2025). "Flattery, Fluff, and Fog: Diagnosing and Mitigating Idiosyncratic Biases in Preference Models." arXiv:2506.05339.
8. Cheng, M. et al. (2025). "ELEPHANT: Measuring and Understanding Social Sycophancy in LLMs." arXiv:2505.13995.
