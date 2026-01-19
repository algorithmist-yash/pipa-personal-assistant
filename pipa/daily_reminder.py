from datetime import date

from database import (
    create_table,
    get_last_log_date,
    calculate_streak
)
from analyzer import discipline_score
from telegram_bot import send_telegram_message

def run_daily_reminder():
    create_table()

    today = date.today().isoformat()
    last_log = get_last_log_date()

    if last_log == today:
        return  # already logged today

    streak_status = calculate_streak(today)
    score = discipline_score(streak_status)

    message = "📅 PIPA Daily Check-in\n\n"

    if streak_status == "BROKEN":
        message += "❌ Streak broken.\n"
    elif streak_status == "CONTINUE":
        message += "🔥 Streak intact.\n"
    else:
        message += "🆕 First log day.\n"

    message += f"\n🎯 Discipline Score: {score}/100\n\n"
    message += "Please log your day in PIPA."

    send_telegram_message(message)

if __name__ == "__main__":
    run_daily_reminder()
