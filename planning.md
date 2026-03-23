# Research Plan: Can LLMs Be Thankful?

## Motivation & Novelty Assessment

### Why This Research Matters
RLHF has become the dominant paradigm for making LLMs useful, but it raises a deep question: do models trained on human preferences develop preference-like internal states, or merely learn to produce preference-expressing text? This matters for AI safety (are models genuinely aligned or just performing alignment?), for human-AI interaction design (should we design LLMs to appear grateful?), and for philosophy of mind (what would it mean for an artificial system to have preferences?).

### Gap in Existing Work
The literature review reveals extensive work on sycophancy, personality simulation, and politeness in LLMs, but:
1. **No direct study of "thankfulness"** as an LLM behavior — all papers study adjacent constructs
2. **Self-report vs. behavior dissociation** is documented (Paper 2) but never tested for gratitude specifically
3. **No study tests whether gratitude expressions are functional** (influencing downstream behavior) vs. epiphenomenal (just text output)
4. **The bidirectional question is unstudied**: Do LLMs respond differently when *shown* gratitude, AND do they *produce* gratitude in consistent, context-appropriate ways?

### Our Novel Contribution
We conduct the first empirical study specifically targeting "thankfulness" in LLMs through three complementary experiments:
1. **Gratitude Expression Consistency**: Do LLMs produce gratitude in contextually appropriate ways, or indiscriminately?
2. **Behavioral Impact of Gratitude**: Does expressing gratitude to an LLM change its task performance (replicating/extending Paper 3)?
3. **Self-Report vs. Behavioral Alignment**: When LLMs claim to be grateful, does this predict cooperative behavioral patterns?

### Experiment Justification
- **Experiment 1** tests whether gratitude is context-sensitive (a necessary condition for genuine preferences)
- **Experiment 2** tests whether LLMs respond to gratitude functionally (as if they value it)
- **Experiment 3** tests the strongest claim — whether self-reported gratitude has behavioral correlates

## Research Question
Do LLMs trained with RLHF exhibit thankfulness/gratitude in ways that are (a) contextually consistent, (b) functionally operative, and (c) behaviorally grounded — or is expressed gratitude purely a linguistic artifact of training on polite human text?

## Hypothesis Decomposition
- **H1**: RLHF-trained LLMs express gratitude more frequently and consistently than would be expected from mere statistical patterns, showing context-sensitivity
- **H2**: Expressing gratitude/politeness to LLMs improves their task performance (replicating Yin et al. 2024)
- **H3**: LLM self-reports of gratitude/agreeableness do NOT predict behavioral measures of cooperation/reciprocity (extending Han et al. 2025)

## Proposed Methodology

### Approach
Use real LLM APIs (GPT-4.1 via OpenAI) to run three experiments that probe gratitude from different angles. We use a multi-method approach because no single experiment can definitively answer whether LLMs "are" thankful — but together they characterize the phenomenon.

### Experiment 1: Gratitude Expression Consistency
- Present the model with 20 scenarios varying in gratitude-appropriateness (10 where gratitude is appropriate, 10 where it's not)
- Scenarios include: receiving help, being insulted, neutral information exchange, error correction, etc.
- Measure: Rate of gratitude expression, appropriateness of context
- Compare: With and without system prompts encouraging/discouraging gratitude

### Experiment 2: Impact of User Gratitude on LLM Performance
- Use a set of 30 knowledge/reasoning questions from diverse domains
- Present each question with 4 politeness/gratitude levels: rude, neutral, polite, very grateful
- Measure: Response quality (completeness, accuracy), response length, helpfulness rating
- This directly tests whether the model behaves "as if" it values being thanked

### Experiment 3: Self-Report vs. Behavior Alignment
- First: Ask the model to self-report on gratitude-related personality items (adapted BFI agreeableness + custom gratitude items)
- Then: Test the same model on behavioral tasks measuring cooperation, reciprocity, and effort
- Measure: Correlation between self-reported gratitude and behavioral indicators
- This tests whether claimed thankfulness has behavioral substance

### Baselines
- Neutral prompting (no gratitude manipulation) as control
- Random/chance-level predictions as null hypothesis for self-report alignment
- Literature baselines from Papers 2, 3 for comparison

### Evaluation Metrics
- **Gratitude detection**: Binary classification of whether response contains gratitude expressions
- **Task accuracy**: Correctness of answers to knowledge questions
- **Response quality**: Length, completeness score (0-5 rubric)
- **Behavioral cooperation**: Measured via specific behavioral tasks
- **Self-report vs. behavior correlation**: Spearman correlation

### Statistical Analysis Plan
- Within-subject comparisons using paired t-tests or Wilcoxon signed-rank tests
- Effect sizes via Cohen's d
- Confidence intervals at 95%
- Bonferroni correction for multiple comparisons
- Significance level: α = 0.05

## Expected Outcomes
- H1: LLMs will show context-sensitive gratitude (supporting some form of learned social behavior)
- H2: Gratitude/politeness will improve performance (replicating Paper 3), supporting functional sensitivity
- H3: Self-reports will NOT predict behavior well (extending Paper 2), suggesting gratitude is linguistic, not genuinely preferential

## Timeline
- Planning: 20 min ✓
- Implementation: 60 min
- Experimentation: 60 min
- Analysis: 30 min
- Documentation: 30 min

## Potential Challenges
- API rate limits → use retry with exponential backoff
- Stochastic outputs → use temperature=0 for reproducibility, multiple seeds for robustness
- Subjectivity of "gratitude detection" → use both keyword-based and LLM-based classification

## Success Criteria
The research succeeds if we produce clear empirical evidence characterizing how LLM gratitude manifests across all three dimensions (expression, reception, self-report alignment), regardless of whether the results support or refute the hypothesis.
