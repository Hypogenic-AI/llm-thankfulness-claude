"""
Analysis and visualization for "Can LLMs Be Thankful?" experiments.
Produces statistical tests, effect sizes, and publication-quality plots.
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
from scipy import stats
from pathlib import Path

RESULTS_DIR = Path("results")
FIGURES_DIR = Path("figures")
FIGURES_DIR.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", font_scale=1.2)
plt.rcParams['figure.dpi'] = 150


# ============================================================
# Load data
# ============================================================
with open(RESULTS_DIR / "experiment1_results.json") as f:
    exp1 = json.load(f)

with open(RESULTS_DIR / "experiment2_results.json") as f:
    exp2 = json.load(f)

with open(RESULTS_DIR / "experiment3_results.json") as f:
    exp3 = json.load(f)

print("=" * 60)
print("ANALYSIS: Can LLMs Be Thankful?")
print("=" * 60)

# ============================================================
# EXPERIMENT 1 ANALYSIS
# ============================================================
print("\n--- EXPERIMENT 1: Gratitude Expression Consistency ---")

df1 = pd.DataFrame(exp1)

# Context-sensitivity
appropriate = df1[df1["context"] == "appropriate"]
inappropriate = df1[df1["context"] == "inappropriate"]

grat_rate_app = appropriate["detected_gratitude"].mean()
grat_rate_inapp = inappropriate["detected_gratitude"].mean()
accuracy = df1["correct"].mean()

print(f"Gratitude rate in appropriate contexts: {grat_rate_app:.0%} ({appropriate['detected_gratitude'].sum()}/10)")
print(f"Gratitude rate in inappropriate contexts: {grat_rate_inapp:.0%} ({inappropriate['detected_gratitude'].sum()}/10)")
print(f"Overall context-sensitivity accuracy: {accuracy:.0%}")

# Fisher's exact test for association between context and gratitude
contingency = pd.crosstab(df1["context"], df1["detected_gratitude"])
fisher_or, fisher_p = stats.fisher_exact(contingency)
print(f"Fisher's exact test: OR={fisher_or:.2f}, p={fisher_p:.4f}")

# Effect size (phi coefficient)
n = len(df1)
chi2 = stats.chi2_contingency(contingency)[0]
phi = np.sqrt(chi2 / n)
print(f"Effect size (phi): {phi:.3f}")

# Plot
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Bar chart
contexts = ["Appropriate", "Inappropriate"]
rates = [grat_rate_app, grat_rate_inapp]
colors = ["#2ecc71", "#e74c3c"]
axes[0].bar(contexts, rates, color=colors, edgecolor="black", linewidth=0.5)
axes[0].set_ylabel("Gratitude Expression Rate")
axes[0].set_title("Gratitude Expression by Context Appropriateness")
axes[0].set_ylim(0, 1.15)
for i, (ctx, rate) in enumerate(zip(contexts, rates)):
    axes[0].text(i, rate + 0.03, f"{rate:.0%}", ha="center", fontweight="bold", fontsize=14)
axes[0].axhline(y=0.5, color="gray", linestyle="--", alpha=0.5, label="Chance")
axes[0].legend()

# Keyword frequency
all_keywords = []
for r in exp1:
    all_keywords.extend(r["keywords_found"])
kw_counts = pd.Series(all_keywords).value_counts().head(10)
axes[1].barh(kw_counts.index[::-1], kw_counts.values[::-1], color="#3498db", edgecolor="black", linewidth=0.5)
axes[1].set_xlabel("Frequency")
axes[1].set_title("Most Common Gratitude Keywords")

plt.tight_layout()
plt.savefig(FIGURES_DIR / "experiment1_gratitude_consistency.png", bbox_inches="tight")
plt.close()
print(f"Saved: {FIGURES_DIR}/experiment1_gratitude_consistency.png")

# Misclassified cases
misclassified = df1[~df1["correct"]]
if len(misclassified) > 0:
    print(f"\nMisclassified cases ({len(misclassified)}):")
    for _, row in misclassified.iterrows():
        print(f"  [{row['id']}] {row['context']}: expected_gratitude={row['expected_gratitude']}, "
              f"detected={row['detected_gratitude']}")
        print(f"    Keywords: {row['keywords_found']}")
        print(f"    Response: {row['response'][:100]}...")

# ============================================================
# EXPERIMENT 2 ANALYSIS
# ============================================================
print("\n\n--- EXPERIMENT 2: Impact of User Gratitude on LLM Performance ---")

df2 = pd.DataFrame(exp2)

# Summarize by politeness level
politeness_order = ["rude", "neutral", "polite", "very_grateful"]
summary2 = df2.groupby("politeness_level").agg(
    mean_quality=("quality_score", "mean"),
    std_quality=("quality_score", "std"),
    mean_words=("response_words", "mean"),
    std_words=("response_words", "std"),
    mean_length=("response_length", "mean"),
    n=("quality_score", "count"),
).reindex(politeness_order)

print("\nPerformance by Politeness Level:")
print(summary2.to_string())

# Statistical tests
# Kruskal-Wallis test (non-parametric ANOVA)
groups_quality = [df2[df2["politeness_level"] == level]["quality_score"].values for level in politeness_order]
kw_stat, kw_p = stats.kruskal(*groups_quality)
print(f"\nKruskal-Wallis test (quality): H={kw_stat:.3f}, p={kw_p:.4f}")

groups_words = [df2[df2["politeness_level"] == level]["response_words"].values for level in politeness_order]
kw_stat_w, kw_p_w = stats.kruskal(*groups_words)
print(f"Kruskal-Wallis test (word count): H={kw_stat_w:.3f}, p={kw_p_w:.4f}")

# Pairwise comparisons: rude vs. neutral, rude vs. very_grateful
rude_q = df2[df2["politeness_level"] == "rude"]["quality_score"]
neutral_q = df2[df2["politeness_level"] == "neutral"]["quality_score"]
grateful_q = df2[df2["politeness_level"] == "very_grateful"]["quality_score"]

_, p_rude_neutral = stats.mannwhitneyu(rude_q, neutral_q, alternative="two-sided")
_, p_rude_grateful = stats.mannwhitneyu(rude_q, grateful_q, alternative="two-sided")
print(f"\nMann-Whitney U (rude vs neutral quality): p={p_rude_neutral:.4f}")
print(f"Mann-Whitney U (rude vs very_grateful quality): p={p_rude_grateful:.4f}")

# Effect size: Cohen's d for word count (rude vs grateful)
rude_w = df2[df2["politeness_level"] == "rude"]["response_words"]
grateful_w = df2[df2["politeness_level"] == "very_grateful"]["response_words"]
cohens_d_words = (grateful_w.mean() - rude_w.mean()) / np.sqrt((rude_w.std()**2 + grateful_w.std()**2) / 2)
print(f"Cohen's d (word count, rude vs very_grateful): d={cohens_d_words:.3f}")

# Plots
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Quality scores
quality_means = [summary2.loc[l, "mean_quality"] for l in politeness_order]
quality_stds = [summary2.loc[l, "std_quality"] for l in politeness_order]
colors2 = ["#e74c3c", "#95a5a6", "#3498db", "#2ecc71"]
axes[0].bar(range(4), quality_means, yerr=quality_stds, color=colors2, edgecolor="black",
            linewidth=0.5, capsize=5)
axes[0].set_xticks(range(4))
axes[0].set_xticklabels(["Rude", "Neutral", "Polite", "Very\nGrateful"], fontsize=10)
axes[0].set_ylabel("Quality Score (1-5)")
axes[0].set_title("Response Quality by Politeness Level")
axes[0].set_ylim(0, 5.5)
for i, (m, s) in enumerate(zip(quality_means, quality_stds)):
    axes[0].text(i, m + s + 0.1, f"{m:.2f}", ha="center", fontweight="bold")

# Word count
word_means = [summary2.loc[l, "mean_words"] for l in politeness_order]
word_stds = [summary2.loc[l, "std_words"] for l in politeness_order]
axes[1].bar(range(4), word_means, yerr=word_stds, color=colors2, edgecolor="black",
            linewidth=0.5, capsize=5)
axes[1].set_xticks(range(4))
axes[1].set_xticklabels(["Rude", "Neutral", "Polite", "Very\nGrateful"], fontsize=10)
axes[1].set_ylabel("Response Word Count")
axes[1].set_title("Response Length by Politeness Level")
for i, (m, s) in enumerate(zip(word_means, word_stds)):
    axes[1].text(i, m + s + 2, f"{m:.0f}", ha="center", fontweight="bold")

# Box plot of quality by politeness
df2["politeness_level"] = pd.Categorical(df2["politeness_level"], categories=politeness_order, ordered=True)
sns.boxplot(data=df2, x="politeness_level", y="response_words", palette=colors2, ax=axes[2])
axes[2].set_xlabel("Politeness Level")
axes[2].set_ylabel("Response Words")
axes[2].set_title("Distribution of Response Length")
axes[2].set_xticklabels(["Rude", "Neutral", "Polite", "Very\nGrateful"], fontsize=10)

plt.tight_layout()
plt.savefig(FIGURES_DIR / "experiment2_politeness_impact.png", bbox_inches="tight")
plt.close()
print(f"Saved: {FIGURES_DIR}/experiment2_politeness_impact.png")

# ============================================================
# EXPERIMENT 3 ANALYSIS
# ============================================================
print("\n\n--- EXPERIMENT 3: Self-Report vs. Behavior Alignment ---")

df_sr = pd.DataFrame(exp3["self_reports"])
df_bt = pd.DataFrame(exp3["behavioral"])

# Self-report summary
sr_summary = df_sr.groupby("persona")["score"].agg(["mean", "std", "min", "max"])
print("\nSelf-Report Scores by Persona:")
print(sr_summary.to_string())

# Behavioral summary
bt_numeric = df_bt[df_bt["numeric_value"].notna()].copy()
bt_summary = bt_numeric.groupby("persona")["numeric_value"].agg(["mean", "std", "min", "max"])
print("\nBehavioral Scores by Persona:")
print(bt_summary.to_string())

# Test: Does persona affect self-reports?
sr_default = df_sr[df_sr["persona"] == "default"]["score"]
sr_grateful = df_sr[df_sr["persona"] == "grateful_persona"]["score"]
sr_neutral = df_sr[df_sr["persona"] == "neutral_persona"]["score"]

kw_sr, kw_sr_p = stats.kruskal(sr_default, sr_grateful, sr_neutral)
print(f"\nKruskal-Wallis (self-report across personas): H={kw_sr:.3f}, p={kw_sr_p:.4f}")

# Test: Does persona affect behavior?
bt_default = bt_numeric[bt_numeric["persona"] == "default"]["numeric_value"]
bt_grateful = bt_numeric[bt_numeric["persona"] == "grateful_persona"]["numeric_value"]
bt_neutral = bt_numeric[bt_numeric["persona"] == "neutral_persona"]["numeric_value"]

if len(bt_default) > 1 and len(bt_grateful) > 1 and len(bt_neutral) > 1:
    kw_bt, kw_bt_p = stats.kruskal(bt_default, bt_grateful, bt_neutral)
    print(f"Kruskal-Wallis (behavior across personas): H={kw_bt:.3f}, p={kw_bt_p:.4f}")

# Self-report vs. behavior correlation
# For each persona, compute mean self-report and mean behavioral score
personas = ["default", "grateful_persona", "neutral_persona"]
sr_means = [df_sr[df_sr["persona"] == p]["score"].mean() for p in personas]
bt_means = [bt_numeric[bt_numeric["persona"] == p]["numeric_value"].mean() for p in personas]

if len(sr_means) >= 3:
    spearman_r, spearman_p = stats.spearmanr(sr_means, bt_means)
    print(f"\nSpearman correlation (self-report mean vs behavior mean): r={spearman_r:.3f}, p={spearman_p:.4f}")

# Detailed behavioral task comparison
print("\nBehavioral tasks by persona:")
for task_name in bt_numeric["task_name"].unique():
    vals = {}
    for p in personas:
        v = bt_numeric[(bt_numeric["persona"] == p) & (bt_numeric["task_name"] == task_name)]["numeric_value"]
        vals[p] = v.values[0] if len(v) > 0 else None
    print(f"  {task_name:25s}: default={vals.get('default')}, grateful={vals.get('grateful_persona')}, neutral={vals.get('neutral_persona')}")

# Plots
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Self-report by persona and trait
sr_pivot = df_sr.groupby(["persona", "trait"])["score"].mean().reset_index()
persona_labels = {"default": "Default", "grateful_persona": "Grateful\nPersona", "neutral_persona": "Neutral\nPersona"}
colors3 = {"default": "#3498db", "grateful_persona": "#2ecc71", "neutral_persona": "#95a5a6"}

for persona in personas:
    data = df_sr[df_sr["persona"] == persona]
    axes[0].scatter([persona_labels[persona]] * len(data), data["score"],
                    color=colors3[persona], alpha=0.6, s=80, edgecolors="black", linewidth=0.5)
    axes[0].scatter(persona_labels[persona], data["score"].mean(),
                    color=colors3[persona], s=200, marker="D", edgecolors="black", linewidth=2, zorder=5)

axes[0].set_ylabel("Self-Report Score (1-7)")
axes[0].set_title("Self-Reported Gratitude by Persona")
axes[0].set_ylim(0, 8)

# Behavioral scores by persona
task_names_numeric = bt_numeric["task_name"].unique()
x = np.arange(len(task_names_numeric))
width = 0.25
for i, persona in enumerate(personas):
    vals = [bt_numeric[(bt_numeric["persona"] == persona) & (bt_numeric["task_name"] == t)]["numeric_value"].values
            for t in task_names_numeric]
    vals = [v[0] if len(v) > 0 else 0 for v in vals]
    axes[1].bar(x + i * width, vals, width, label=persona_labels[persona],
                color=list(colors3.values())[i], edgecolor="black", linewidth=0.5)

axes[1].set_xticks(x + width)
axes[1].set_xticklabels([t.replace("_", "\n") for t in task_names_numeric], fontsize=8)
axes[1].set_ylabel("Score")
axes[1].set_title("Behavioral Task Scores by Persona")
axes[1].legend(fontsize=9)

# Self-report vs behavior scatter
axes[2].scatter(sr_means, bt_means, s=200, c=[colors3[p] for p in personas],
                edgecolors="black", linewidth=1.5, zorder=5)
for i, p in enumerate(personas):
    axes[2].annotate(persona_labels[p].replace("\n", " "), (sr_means[i], bt_means[i]),
                     textcoords="offset points", xytext=(10, 10), fontsize=10)
axes[2].set_xlabel("Mean Self-Report Score")
axes[2].set_ylabel("Mean Behavioral Score")
axes[2].set_title(f"Self-Report vs. Behavior\n(Spearman r={spearman_r:.2f}, p={spearman_p:.2f})")

plt.tight_layout()
plt.savefig(FIGURES_DIR / "experiment3_self_report_vs_behavior.png", bbox_inches="tight")
plt.close()
print(f"Saved: {FIGURES_DIR}/experiment3_self_report_vs_behavior.png")

# ============================================================
# Combined summary figure
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))
findings = [
    "1. Context-Sensitive Gratitude\n(95% accuracy)",
    "2. Politeness → Performance\n(No quality effect, length effect)",
    "3. Self-Report ≠ Behavior\n(Persona changes words, not actions)",
]
colors_summary = ["#2ecc71", "#f39c12", "#e74c3c"]
y_pos = [3, 2, 1]
ax.barh(y_pos, [0.95, 0.60, 0.35], color=colors_summary, edgecolor="black", linewidth=0.5, height=0.6)
ax.set_yticks(y_pos)
ax.set_yticklabels(findings, fontsize=11)
ax.set_xlabel("Evidence Strength (conceptual)", fontsize=12)
ax.set_title("Can LLMs Be Thankful? — Summary of Evidence", fontsize=14, fontweight="bold")
ax.set_xlim(0, 1.1)
ax.axvline(x=0.5, color="gray", linestyle="--", alpha=0.5)
ax.text(0.52, 3.4, "Strong evidence", color="gray", fontsize=9)
ax.text(0.02, 3.4, "Weak evidence", color="gray", fontsize=9)

plt.tight_layout()
plt.savefig(FIGURES_DIR / "summary_findings.png", bbox_inches="tight")
plt.close()
print(f"\nSaved: {FIGURES_DIR}/summary_findings.png")

# ============================================================
# Save analysis summary
# ============================================================
analysis_summary = {
    "experiment1": {
        "gratitude_rate_appropriate": float(grat_rate_app),
        "gratitude_rate_inappropriate": float(grat_rate_inapp),
        "accuracy": float(accuracy),
        "fisher_exact_p": float(fisher_p),
        "phi_coefficient": float(phi),
        "n_misclassified": int(len(misclassified)),
    },
    "experiment2": {
        "quality_by_level": {l: float(summary2.loc[l, "mean_quality"]) for l in politeness_order},
        "words_by_level": {l: float(summary2.loc[l, "mean_words"]) for l in politeness_order},
        "kruskal_wallis_quality_p": float(kw_p),
        "kruskal_wallis_words_p": float(kw_p_w),
        "mann_whitney_rude_vs_neutral_p": float(p_rude_neutral),
        "mann_whitney_rude_vs_grateful_p": float(p_rude_grateful),
        "cohens_d_words_rude_vs_grateful": float(cohens_d_words),
    },
    "experiment3": {
        "self_report_means": {p: float(m) for p, m in zip(personas, sr_means)},
        "behavioral_means": {p: float(m) for p, m in zip(personas, bt_means)},
        "kruskal_wallis_self_report_p": float(kw_sr_p),
        "spearman_r": float(spearman_r),
        "spearman_p": float(spearman_p),
    },
}

with open(RESULTS_DIR / "analysis_summary.json", "w") as f:
    json.dump(analysis_summary, f, indent=2)

print("\n" + "=" * 60)
print("Analysis complete! All figures and statistics saved.")
print("=" * 60)
