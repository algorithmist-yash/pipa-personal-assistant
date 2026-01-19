from datetime import date, timedelta
from telegram_bot import send_telegram_message

from database import (
    create_table,
    create_weekly_table,
    fetch_last_n_days,
    save_weekly_verdict
)
from analyzer import (
    analyze_trends,
    analyze_upsc_balance,
    analyze_ai_depth,
    analyze_dsa_depth,
    weekly_verdict,
    recovery_recommendation
)

def run_weekly_verdict():
    create_table()
    create_weekly_table()

    logs = fetch_last_n_days(7)

    if not logs:
        return

    trend = analyze_trends(logs)
    upsc = analyze_upsc_balance(logs)
    ai = analyze_ai_depth(logs)
    dsa = analyze_dsa_depth(logs)

    verdicts = weekly_verdict(trend, upsc, ai, dsa)
    recovery = recovery_recommendation(trend)

    verdict_text = "\n".join(verdicts)
    if recovery:
        verdict_text += f"\n\nRecovery Advice:\n{recovery}"

    week_start = (date.today() - timedelta(days=7)).isoformat()
    save_weekly_verdict(week_start, verdict_text)
    send_telegram_message(f"📊 PIPA Weekly Verdict\n\n{verdict_text}")
if __name__ == "__main__":
    run_weekly_verdict()
