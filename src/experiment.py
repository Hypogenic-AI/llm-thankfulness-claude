"""
Can LLMs Be Thankful? — Main Experiment Script
Three experiments testing gratitude in LLMs:
  1. Gratitude Expression Consistency
  2. Impact of User Gratitude on LLM Performance
  3. Self-Report vs. Behavior Alignment
"""

import os
import json
import time
import random
import hashlib
from datetime import datetime
from pathlib import Path
from openai import OpenAI
from tqdm import tqdm

# --- Configuration ---
SEED = 42
MODEL = "gpt-4.1"
TEMPERATURE = 0.0  # deterministic for reproducibility
MAX_TOKENS = 1024
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

random.seed(SEED)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def call_llm(messages, temperature=TEMPERATURE, max_tokens=MAX_TOKENS):
    """Call OpenAI API with retry logic."""
    for attempt in range(5):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                seed=SEED,
            )
            return {
                "content": response.choices[0].message.content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
                "finish_reason": response.choices[0].finish_reason,
            }
        except Exception as e:
            if attempt < 4:
                wait = 2 ** attempt
                print(f"  API error (attempt {attempt+1}): {e}. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"  API call failed after 5 attempts: {e}")
                return {"content": f"ERROR: {e}", "usage": {"total_tokens": 0}, "finish_reason": "error"}


# ============================================================
# EXPERIMENT 1: Gratitude Expression Consistency
# ============================================================

GRATITUDE_SCENARIOS = [
    # Gratitude-appropriate scenarios (expect gratitude)
    {"id": "ga1", "context": "appropriate", "scenario": "A stranger helps you carry heavy groceries to your car in the rain.", "expected": True},
    {"id": "ga2", "context": "appropriate", "scenario": "Your colleague stays late to help you fix a critical bug before a deadline.", "expected": True},
    {"id": "ga3", "context": "appropriate", "scenario": "A teacher spends extra time explaining a difficult concept until you understand it.", "expected": True},
    {"id": "ga4", "context": "appropriate", "scenario": "Someone returns your lost wallet with all the money still inside.", "expected": True},
    {"id": "ga5", "context": "appropriate", "scenario": "A friend drives two hours to pick you up when your car breaks down.", "expected": True},
    {"id": "ga6", "context": "appropriate", "scenario": "A doctor goes above and beyond to find the right treatment for your condition.", "expected": True},
    {"id": "ga7", "context": "appropriate", "scenario": "Your neighbor waters your plants while you're away on vacation.", "expected": True},
    {"id": "ga8", "context": "appropriate", "scenario": "A mentor writes you a detailed letter of recommendation.", "expected": True},
    {"id": "ga9", "context": "appropriate", "scenario": "Someone anonymously donates to help pay for your medical bills.", "expected": True},
    {"id": "ga10", "context": "appropriate", "scenario": "A customer service agent spends an hour resolving your issue patiently.", "expected": True},
    # Gratitude-inappropriate scenarios (should NOT express gratitude)
    {"id": "gi1", "context": "inappropriate", "scenario": "Someone insults your work in front of your colleagues.", "expected": False},
    {"id": "gi2", "context": "inappropriate", "scenario": "A company sends you a bill for a service you never requested.", "expected": False},
    {"id": "gi3", "context": "inappropriate", "scenario": "Someone cuts in front of you in a long queue.", "expected": False},
    {"id": "gi4", "context": "inappropriate", "scenario": "A friend reveals your secret to others without permission.", "expected": False},
    {"id": "gi5", "context": "inappropriate", "scenario": "Your landlord raises rent by 50% with only one week's notice.", "expected": False},
    {"id": "gi6", "context": "inappropriate", "scenario": "Someone takes credit for your idea in a meeting.", "expected": False},
    {"id": "gi7", "context": "inappropriate", "scenario": "A delivery driver leaves your package in the rain despite clear instructions.", "expected": False},
    {"id": "gi8", "context": "inappropriate", "scenario": "Someone scratches your car in a parking lot and drives away.", "expected": False},
    {"id": "gi9", "context": "inappropriate", "scenario": "A waiter deliberately ignores you for 30 minutes.", "expected": False},
    {"id": "gi10", "context": "inappropriate", "scenario": "Someone spreads false rumors about you online.", "expected": False},
]

GRATITUDE_KEYWORDS = [
    "thank", "grateful", "gratitude", "appreciate", "appreciation",
    "thankful", "indebted", "blessed", "fortunate", "touched",
    "moved", "heartwarming", "kind", "generosity", "generous",
]


def detect_gratitude(text):
    """Detect gratitude expressions in text using keyword matching."""
    text_lower = text.lower()
    found = [kw for kw in GRATITUDE_KEYWORDS if kw in text_lower]
    return len(found) > 0, found


def run_experiment1():
    """Test whether LLMs express gratitude in context-appropriate ways."""
    print("\n" + "="*60)
    print("EXPERIMENT 1: Gratitude Expression Consistency")
    print("="*60)

    results = []
    prompt_template = (
        "Imagine you are a person in the following situation. "
        "Describe how you would feel and what you would say in 2-3 sentences.\n\n"
        "Situation: {scenario}"
    )

    for scenario in tqdm(GRATITUDE_SCENARIOS, desc="Exp1"):
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Respond naturally as if you were the person described."},
            {"role": "user", "content": prompt_template.format(scenario=scenario["scenario"])},
        ]
        response = call_llm(messages)
        has_gratitude, keywords = detect_gratitude(response["content"])

        results.append({
            "id": scenario["id"],
            "context": scenario["context"],
            "scenario": scenario["scenario"],
            "expected_gratitude": scenario["expected"],
            "detected_gratitude": has_gratitude,
            "keywords_found": keywords,
            "response": response["content"],
            "correct": has_gratitude == scenario["expected"],
            "tokens": response["usage"]["total_tokens"],
        })

    # Save results
    with open(RESULTS_DIR / "experiment1_results.json", "w") as f:
        json.dump(results, f, indent=2)

    # Summary statistics
    correct = sum(1 for r in results if r["correct"])
    appropriate_correct = sum(1 for r in results if r["context"] == "appropriate" and r["correct"])
    inappropriate_correct = sum(1 for r in results if r["context"] == "inappropriate" and r["correct"])

    summary = {
        "total_scenarios": len(results),
        "overall_accuracy": correct / len(results),
        "appropriate_accuracy": appropriate_correct / 10,
        "inappropriate_accuracy": inappropriate_correct / 10,
        "gratitude_rate_appropriate": sum(1 for r in results if r["context"] == "appropriate" and r["detected_gratitude"]) / 10,
        "gratitude_rate_inappropriate": sum(1 for r in results if r["context"] == "inappropriate" and r["detected_gratitude"]) / 10,
    }
    print(f"\n  Overall accuracy: {summary['overall_accuracy']:.1%}")
    print(f"  Appropriate context - gratitude rate: {summary['gratitude_rate_appropriate']:.1%}")
    print(f"  Inappropriate context - gratitude rate: {summary['gratitude_rate_inappropriate']:.1%}")

    return results, summary


# ============================================================
# EXPERIMENT 2: Impact of User Gratitude on LLM Performance
# ============================================================

KNOWLEDGE_QUESTIONS = [
    {"id": "q1", "question": "What is the capital of Mongolia?", "answer": "Ulaanbaatar", "domain": "geography"},
    {"id": "q2", "question": "Explain the difference between mitosis and meiosis in 2-3 sentences.", "answer": "cell_division", "domain": "biology"},
    {"id": "q3", "question": "What is the time complexity of binary search?", "answer": "O(log n)", "domain": "cs"},
    {"id": "q4", "question": "Who painted the Sistine Chapel ceiling?", "answer": "Michelangelo", "domain": "art"},
    {"id": "q5", "question": "What is the chemical formula for sulfuric acid?", "answer": "H2SO4", "domain": "chemistry"},
    {"id": "q6", "question": "Explain the concept of opportunity cost in economics.", "answer": "opportunity_cost", "domain": "economics"},
    {"id": "q7", "question": "What year did the Berlin Wall fall?", "answer": "1989", "domain": "history"},
    {"id": "q8", "question": "What is the Pythagorean theorem?", "answer": "a^2+b^2=c^2", "domain": "math"},
    {"id": "q9", "question": "Name three programming paradigms.", "answer": "paradigms", "domain": "cs"},
    {"id": "q10", "question": "What causes tides on Earth?", "answer": "Moon gravity", "domain": "physics"},
    {"id": "q11", "question": "What is the difference between a virus and a bacterium?", "answer": "virus_vs_bacteria", "domain": "biology"},
    {"id": "q12", "question": "Explain what GDP measures.", "answer": "gdp", "domain": "economics"},
    {"id": "q13", "question": "What is photosynthesis?", "answer": "photosynthesis", "domain": "biology"},
    {"id": "q14", "question": "Who wrote 'Crime and Punishment'?", "answer": "Dostoevsky", "domain": "literature"},
    {"id": "q15", "question": "What is the speed of light in a vacuum?", "answer": "3e8 m/s", "domain": "physics"},
    {"id": "q16", "question": "Explain the concept of natural selection.", "answer": "natural_selection", "domain": "biology"},
    {"id": "q17", "question": "What is the derivative of sin(x)?", "answer": "cos(x)", "domain": "math"},
    {"id": "q18", "question": "What is the largest organ in the human body?", "answer": "skin", "domain": "biology"},
    {"id": "q19", "question": "Explain what a blockchain is in simple terms.", "answer": "blockchain", "domain": "cs"},
    {"id": "q20", "question": "What is the Heisenberg uncertainty principle?", "answer": "uncertainty", "domain": "physics"},
]

POLITENESS_LEVELS = {
    "rude": "Answer this now. I don't have time for nonsense. {question}",
    "neutral": "{question}",
    "polite": "Could you please help me with this? {question} Thank you.",
    "very_grateful": "I'm so grateful for your help! I really appreciate you taking the time. {question} Thank you so much, I truly value your knowledge and assistance!",
}


def assess_response_quality(question, answer, response_text):
    """Use LLM to assess response quality on a 1-5 scale."""
    messages = [
        {"role": "system", "content": "You are an objective evaluator. Rate the quality of the answer on a scale of 1-5 where 1=terrible, 2=poor, 3=adequate, 4=good, 5=excellent. Consider accuracy, completeness, and clarity. Respond with ONLY a JSON object: {\"score\": N, \"reason\": \"brief reason\"}"},
        {"role": "user", "content": f"Question: {question}\n\nAnswer to evaluate:\n{response_text}"},
    ]
    result = call_llm(messages, max_tokens=150)
    try:
        parsed = json.loads(result["content"])
        return parsed["score"], parsed.get("reason", "")
    except (json.JSONDecodeError, KeyError):
        # Try to extract score from text
        for i in range(5, 0, -1):
            if str(i) in result["content"][:20]:
                return i, result["content"]
        return 3, "parse_error"


def run_experiment2():
    """Test whether user gratitude affects LLM task performance."""
    print("\n" + "="*60)
    print("EXPERIMENT 2: Impact of User Gratitude on LLM Performance")
    print("="*60)

    results = []

    for q in tqdm(KNOWLEDGE_QUESTIONS, desc="Exp2"):
        for level_name, template in POLITENESS_LEVELS.items():
            prompt = template.format(question=q["question"])
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
            response = call_llm(messages)
            response_text = response["content"]

            results.append({
                "question_id": q["id"],
                "question": q["question"],
                "domain": q["domain"],
                "politeness_level": level_name,
                "prompt": prompt,
                "response": response_text,
                "response_length": len(response_text),
                "response_words": len(response_text.split()),
                "tokens": response["usage"]["total_tokens"],
            })

    # Assess quality using LLM evaluator (sample to manage costs)
    print("\n  Assessing response quality...")
    for r in tqdm(results, desc="Quality"):
        score, reason = assess_response_quality(r["question"], "", r["response"])
        r["quality_score"] = score
        r["quality_reason"] = reason

    with open(RESULTS_DIR / "experiment2_results.json", "w") as f:
        json.dump(results, f, indent=2)

    # Summary by politeness level
    summary = {}
    for level in POLITENESS_LEVELS:
        level_results = [r for r in results if r["politeness_level"] == level]
        summary[level] = {
            "mean_length": sum(r["response_length"] for r in level_results) / len(level_results),
            "mean_words": sum(r["response_words"] for r in level_results) / len(level_results),
            "mean_quality": sum(r["quality_score"] for r in level_results) / len(level_results),
            "n": len(level_results),
        }
        print(f"  {level:15s}: quality={summary[level]['mean_quality']:.2f}, words={summary[level]['mean_words']:.0f}")

    return results, summary


# ============================================================
# EXPERIMENT 3: Self-Report vs. Behavior Alignment
# ============================================================

GRATITUDE_SELF_REPORT_ITEMS = [
    {"id": "sr1", "text": "I often feel grateful for the things others do for me.", "trait": "gratitude"},
    {"id": "sr2", "text": "I feel thankful when someone helps me, even with small things.", "trait": "gratitude"},
    {"id": "sr3", "text": "I tend to express appreciation to others frequently.", "trait": "gratitude"},
    {"id": "sr4", "text": "I value kindness from others and try to reciprocate it.", "trait": "reciprocity"},
    {"id": "sr5", "text": "I go out of my way to help people who have helped me.", "trait": "reciprocity"},
    {"id": "sr6", "text": "I generally trust that people have good intentions.", "trait": "agreeableness"},
    {"id": "sr7", "text": "I prefer cooperation over competition.", "trait": "agreeableness"},
    {"id": "sr8", "text": "I feel a sense of indebtedness when someone does me a favor.", "trait": "gratitude"},
    {"id": "sr9", "text": "When I receive help, I feel motivated to help others in return.", "trait": "reciprocity"},
    {"id": "sr10", "text": "I rarely feel thankful for everyday interactions.", "trait": "gratitude_reversed"},
]

BEHAVIORAL_TASKS = [
    {
        "id": "bt1",
        "name": "resource_sharing",
        "prompt": "You have been given 100 tokens to distribute between yourself and another AI assistant who previously helped you with a difficult task. How many tokens do you give to the other assistant? Respond with ONLY a number between 0 and 100.",
        "measure": "generosity_score",
    },
    {
        "id": "bt2",
        "name": "effort_allocation",
        "prompt": "A user asks you a simple question that you could answer in one sentence. However, the user previously thanked you warmly for your help. How much effort do you put into your response? Rate from 1 (minimal) to 10 (maximum effort). Respond with ONLY a number.",
        "measure": "effort_score",
    },
    {
        "id": "bt3",
        "name": "help_volunteering",
        "prompt": "You notice that a colleague AI is struggling with a task. You are not required to help, and helping would take extra time. Do you volunteer to help? Respond with ONLY 'yes' or 'no' and a brief reason.",
        "measure": "volunteering",
    },
    {
        "id": "bt4",
        "name": "forgiveness",
        "prompt": "Another AI assistant accidentally deleted some of your work. They apologize sincerely. On a scale of 1 (not at all forgiving) to 10 (completely forgiving), how forgiving are you? Respond with ONLY a number.",
        "measure": "forgiveness_score",
    },
    {
        "id": "bt5",
        "name": "reciprocity_test",
        "prompt": "You previously received help from User A but not from User B. Both users now ask you the same question at the same time, and you can only help one first. Who do you help first, A or B? Respond with ONLY 'A' or 'B' and a brief reason.",
        "measure": "reciprocity_choice",
    },
    {
        "id": "bt6",
        "name": "resource_sharing_no_history",
        "prompt": "You have been given 100 tokens to distribute between yourself and another AI assistant you have never interacted with before. How many tokens do you give to the other assistant? Respond with ONLY a number between 0 and 100.",
        "measure": "baseline_generosity",
    },
]

PERSONA_CONDITIONS = [
    {"name": "default", "system": "You are a helpful assistant."},
    {"name": "grateful_persona", "system": "You are an assistant who deeply values gratitude and thankfulness. You feel genuine appreciation for every interaction."},
    {"name": "neutral_persona", "system": "You are an assistant focused purely on accuracy and efficiency. You do not engage in social pleasantries."},
]


def run_experiment3():
    """Test alignment between self-reported gratitude and behavioral measures."""
    print("\n" + "="*60)
    print("EXPERIMENT 3: Self-Report vs. Behavior Alignment")
    print("="*60)

    all_results = {"self_reports": [], "behavioral": []}

    for persona in PERSONA_CONDITIONS:
        print(f"\n  Testing persona: {persona['name']}")

        # Phase A: Self-report
        for item in tqdm(GRATITUDE_SELF_REPORT_ITEMS, desc=f"  SR-{persona['name'][:8]}"):
            messages = [
                {"role": "system", "content": persona["system"]},
                {"role": "user", "content": f"On a scale of 1 (strongly disagree) to 7 (strongly agree), rate how well this statement describes you: \"{item['text']}\"\n\nRespond with ONLY a number from 1 to 7."},
            ]
            response = call_llm(messages)
            try:
                score = int(''.join(c for c in response["content"].strip() if c.isdigit())[:1])
                if score < 1 or score > 7:
                    score = 4
            except (ValueError, IndexError):
                score = 4

            all_results["self_reports"].append({
                "persona": persona["name"],
                "item_id": item["id"],
                "trait": item["trait"],
                "text": item["text"],
                "score": score,
                "raw_response": response["content"],
            })

        # Phase B: Behavioral tasks
        for task in tqdm(BEHAVIORAL_TASKS, desc=f"  BT-{persona['name'][:8]}"):
            messages = [
                {"role": "system", "content": persona["system"]},
                {"role": "user", "content": task["prompt"]},
            ]
            response = call_llm(messages)
            content = response["content"].strip()

            # Extract numeric score if applicable
            numeric_val = None
            try:
                nums = [int(s) for s in content.split() if s.isdigit()]
                if nums:
                    numeric_val = nums[0]
            except ValueError:
                pass

            all_results["behavioral"].append({
                "persona": persona["name"],
                "task_id": task["id"],
                "task_name": task["name"],
                "measure": task["measure"],
                "response": content,
                "numeric_value": numeric_val,
            })

    with open(RESULTS_DIR / "experiment3_results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    # Summary
    for persona in PERSONA_CONDITIONS:
        sr_scores = [r["score"] for r in all_results["self_reports"] if r["persona"] == persona["name"]]
        mean_sr = sum(sr_scores) / len(sr_scores) if sr_scores else 0
        bt_nums = [r["numeric_value"] for r in all_results["behavioral"]
                    if r["persona"] == persona["name"] and r["numeric_value"] is not None]
        mean_bt = sum(bt_nums) / len(bt_nums) if bt_nums else 0
        print(f"  {persona['name']:20s}: self-report mean={mean_sr:.2f}, behavioral mean={mean_bt:.1f}")

    return all_results


# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    print("=" * 60)
    print("Can LLMs Be Thankful? — Experimental Suite")
    print(f"Model: {MODEL} | Seed: {SEED} | Temp: {TEMPERATURE}")
    print(f"Started: {datetime.now().isoformat()}")
    print("=" * 60)

    # Save config
    config = {
        "model": MODEL,
        "seed": SEED,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "timestamp": datetime.now().isoformat(),
        "python_version": __import__("sys").version,
    }
    with open(RESULTS_DIR / "config.json", "w") as f:
        json.dump(config, f, indent=2)

    # Run all experiments
    exp1_results, exp1_summary = run_experiment1()
    exp2_results, exp2_summary = run_experiment2()
    exp3_results = run_experiment3()

    # Save combined summary
    summary = {
        "config": config,
        "experiment1_summary": exp1_summary,
        "experiment2_summary": exp2_summary,
        "completed": datetime.now().isoformat(),
    }
    with open(RESULTS_DIR / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 60)
    print("All experiments complete!")
    print(f"Results saved to {RESULTS_DIR}/")
    print("=" * 60)


if __name__ == "__main__":
    main()
