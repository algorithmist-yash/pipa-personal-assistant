def analyze_day(planned_tasks, actual_tasks, energy, clarity):
    """
    Core deterministic analyzer for daily performance.
    """

    # Basic completion heuristic
    planned_count = max(len(planned_tasks.split("\n")), 1)
    actual_count = len(actual_tasks.split("\n"))

    completion_ratio = min(actual_count / planned_count, 1.0)

    # Productivity score (weighted)
    productivity_score = round(
        (0.6 * completion_ratio + 0.2 * (energy / 10) + 0.2 * (clarity / 10)),
        2
    )

    # Burnout signal
    burnout_flag = "LOW"
    if energy <= 3 and completion_ratio < 0.5:
        burnout_flag = "HIGH"
    elif energy <= 5 and completion_ratio < 0.6:
        burnout_flag = "MODERATE"

    # Gap detection (simple keyword heuristic)
    gaps = []
    planned_lower = planned_tasks.lower()
    actual_lower = actual_tasks.lower()

    if "math" in planned_lower and "math" not in actual_lower:
        gaps.append("Maths optional not executed as planned")

    if "polity" in planned_lower and "polity" not in actual_lower:
        gaps.append("UPSC GS (Polity) missed")

    if any(x in planned_lower for x in ["ai", "ml", "nlp"]) and \
       not any(x in actual_lower for x in ["ai", "ml", "nlp"]):
        gaps.append("AI / ML block skipped")

    # Risk flags
    risk_flags = []
    if completion_ratio < 0.5:
        risk_flags.append("Low task completion")

    if burnout_flag == "HIGH":
        risk_flags.append("Burnout risk detected")

    if clarity <= 4:
        risk_flags.append("Low conceptual clarity")

    return {
        "completion_ratio": round(completion_ratio, 2),
        "productivity_score": productivity_score,
        "burnout_flag": burnout_flag,
        "gaps": gaps,
        "risk_flags": risk_flags
    }

def analyze_trends(logs):
    """
    Analyze weekly/monthly trends from historical logs.
    """

    if not logs:
        return {}

    total_days = len(logs)
    completion_scores = []
    energy_levels = []
    clarity_levels = []

    for log in logs:
        _, planned, actual, energy, clarity = log

        planned_count = max(len(planned.split("\n")), 1)
        actual_count = len(actual.split("\n"))
        completion = min(actual_count / planned_count, 1.0)

        completion_scores.append(completion)
        energy_levels.append(energy)
        clarity_levels.append(clarity)

    avg_completion = round(sum(completion_scores) / total_days, 2)
    avg_energy = round(sum(energy_levels) / total_days, 2)
    avg_clarity = round(sum(clarity_levels) / total_days, 2)

    burnout_risk = "LOW"
    if avg_energy <= 4:
        burnout_risk = "HIGH"
    elif avg_energy <= 6:
        burnout_risk = "MODERATE"

    consistency = "GOOD" if avg_completion >= 0.7 else "POOR"

    return {
        "days_analyzed": total_days,
        "avg_completion": avg_completion,
        "avg_energy": avg_energy,
        "avg_clarity": avg_clarity,
        "burnout_risk": burnout_risk,
        "consistency": consistency
    }

def classify_tasks(text):
    text = text.lower()

    gs_keywords = ["polity", "geography", "economy", "history", "ethics", "gs"]
    maths_keywords = ["math", "algebra", "calculus", "probability", "statistics", "vector"]
    ai_keywords = ["ai", "ml", "nlp", "deep learning", "transformer", "llm"]

    gs = any(k in text for k in gs_keywords)
    maths = any(k in text for k in maths_keywords)
    ai = any(k in text for k in ai_keywords)

    return {
        "GS": int(gs),
        "MATHS": int(maths),
        "AI": int(ai)
    }


def analyze_dsa_depth(logs):
    """
    Analyze DSA problem-solving depth.
    """

    level_score = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0
    }

    dsa_keywords = {
        0: ["dsa video", "lecture", "tutorial"],
        1: ["easy", "leetcode easy", "basic"],
        2: ["medium", "leetcode medium"],
        3: ["hard", "pattern", "sliding window", "dp", "graph", "tree"],
        4: ["explain", "optimize", "time complexity", "revision", "editorial"]
    }

    for log in logs:
        _, _, actual, _, _ = log
        text = actual.lower()

        if "dsa" not in text and "leetcode" not in text:
            continue

        for level, keywords in dsa_keywords.items():
            if any(k in text for k in keywords):
                level_score[level] += 1

    dominant_level = max(level_score, key=level_score.get)

    warnings = []
    if level_score[1] > level_score[2] + level_score[3]:
        warnings.append("⚠️ DSA stuck at easy level")

    if level_score[2] > 0 and level_score[3] == 0:
        warnings.append("⚠️ Medium problems without pattern progression")

    if level_score[4] == 0 and sum(level_score.values()) > 5:
        warnings.append("⚠️ Solving without revision or explanation")

    return {
        "level_score": level_score,
        "dominant_level": dominant_level,
        "warnings": warnings
    }

def analyze_upsc_balance(logs):
    """
    Analyze GS vs Maths vs AI balance over time.
    """

    summary = {"GS": 0, "MATHS": 0, "AI": 0}

    for log in logs:
        _, planned, actual, _, _ = log
        classification = classify_tasks(actual)

        for key in summary:
            summary[key] += classification[key]

    total_days = len(logs)

    risks = []

    if summary["GS"] < total_days * 0.5:
        risks.append("⚠️ GS coverage insufficient — high UPSC risk")

    if summary["MATHS"] > total_days * 0.8:
        risks.append("⚠️ Maths optional dominating — GS may be neglected")

    if summary["AI"] > total_days * 0.7:
        risks.append("⚠️ AI workload high — risk of UPSC focus dilution")

    return {
        "days_analyzed": total_days,
        "coverage": summary,
        "risks": risks
    }

def analyze_ai_depth(logs):
    """
    Analyze AI learning depth and research maturity.
    """

    level_score = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0
    }

    depth_keywords = {
        0: ["video", "watch", "lecture", "blog"],
        1: ["implement", "code", "from scratch", "train"],
        2: ["explain", "intuition", "derive", "why"],
        3: ["modify", "experiment", "change", "custom"],
        4: ["evaluate", "benchmark", "ablation", "metric"],
        5: ["paper", "research", "rag", "agent", "deployment"]
    }

    for log in logs:
        _, _, actual, _, _ = log
        text = actual.lower()

        for level, keywords in depth_keywords.items():
            if any(k in text for k in keywords):
                level_score[level] += 1

    dominant_level = max(level_score, key=level_score.get)

    warnings = []
    if level_score[0] > level_score[1] + level_score[2]:
        warnings.append("⚠️ AI learning stuck at consumption level")

    if level_score[1] > 0 and level_score[2] == 0:
        warnings.append("⚠️ Implementation without understanding detected")

    if level_score[3] == 0 and level_score[4] == 0 and level_score[5] == 0:
        warnings.append("⚠️ No research-grade activity yet")

    return {
        "level_score": level_score,
        "dominant_level": dominant_level,
        "warnings": warnings
    }

def weekly_verdict(trend, upsc, ai, dsa):
    verdicts = []

    if trend["consistency"] == "POOR":
        verdicts.append("❌ Inconsistent week — discipline breakdown")

    if trend["burnout_risk"] != "LOW":
        verdicts.append("⚠️ Burnout accumulating — sustainability at risk")

    if upsc["risks"]:
        verdicts.append("🚨 UPSC imbalance detected — exam risk rising")

    if ai["dominant_level"] <= 1:
        verdicts.append("⚠️ AI learning shallow — consumption over creation")

    if dsa["dominant_level"] <= 1:
        verdicts.append("⚠️ DSA stuck at easy level")

    if not verdicts:
        verdicts.append("✅ Strong week — trajectory healthy")

    return verdicts

def recovery_recommendation(trend):
    if trend["avg_energy"] <= 4:
        return "Recovery Mode: Reduce workload by 30%, focus on sleep & revision."
    if trend["avg_completion"] <= 0.5:
        return "Recovery Mode: Simplify goals, rebuild momentum with easy wins."
    return None
