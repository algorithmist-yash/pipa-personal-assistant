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
