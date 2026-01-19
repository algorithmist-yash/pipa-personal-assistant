from analyzer import analyze_dsa_depth
from analyzer import analyze_ai_depth
from analyzer import analyze_upsc_balance
from database import fetch_last_n_days
from database import fetch_last_n_days
from analyzer import analyze_trends
from analyzer import analyze_day
from database import create_table, insert_daily_log
import streamlit as st
from datetime import date

st.set_page_config(
    page_title="PIPA – Personal Intelligence & Progress Analyzer",
    layout="centered"
)

create_table()

st.title("🧠 PIPA – Daily Study Analyzer")

st.markdown("### 📅 Daily Log")

log_date = st.date_input("Date", value=date.today())

st.markdown("### 📝 Planned Tasks")
planned_tasks = st.text_area(
    "What did you plan to do today?",
    height=150,
    placeholder="Example:\n- Maths: Vector spaces PYQs\n- Polity: Fundamental Rights\n- AI: Linear Regression from scratch"
)

st.markdown("### ✅ Actual Work Done")
actual_tasks = st.text_area(
    "What did you actually complete?",
    height=150
)

st.markdown("### 🔋 Self Assessment")
energy = st.slider("Energy Level", 1, 10, 5)
clarity = st.slider("Clarity / Confidence Level", 1, 10, 5)

st.markdown("### 🧠 Reflection")
reflection = st.text_area(
    "What went well? What didn’t? Why?",
    height=120
)

if st.button("📊 Analyze My Day"):
    insert_daily_log(
        log_date,
        planned_tasks,
        actual_tasks,
        energy,
        clarity,
        reflection
    )

    analysis = analyze_day(
        planned_tasks,
        actual_tasks,
        energy,
        clarity
    )

    st.success("✅ Day saved & analyzed")

    st.markdown("## 📈 Analysis Summary")

    st.write(f"**Completion Ratio:** {analysis['completion_ratio']}")
    st.write(f"**Productivity Score:** {analysis['productivity_score']}")
    st.write(f"**Burnout Risk:** {analysis['burnout_flag']}")

    if analysis["gaps"]:
        st.markdown("### ⚠️ Gaps Detected")
        for gap in analysis["gaps"]:
            st.warning(gap)

    if analysis["risk_flags"]:
        st.markdown("### 🚨 Risk Flags")
        for risk in analysis["risk_flags"]:
            st.error(risk)

st.markdown("---")
st.markdown("## 📊 Weekly Intelligence Dashboard")

if st.button("🔍 Analyze Last 7 Days"):
    logs = fetch_last_n_days(7)
    trend = analyze_trends(logs)

    if not trend:
        st.info("No historical data available yet.")
    else:
        st.write(f"**Days Analyzed:** {trend['days_analyzed']}")
        st.write(f"**Average Completion:** {trend['avg_completion']}")
        st.write(f"**Average Energy:** {trend['avg_energy']}")
        st.write(f"**Average Clarity:** {trend['avg_clarity']}")
        st.write(f"**Consistency:** {trend['consistency']}")
        st.write(f"**Burnout Risk:** {trend['burnout_risk']}")

        if trend["burnout_risk"] != "LOW":
            st.warning("⚠️ Burnout trend detected. Consider reducing load or improving recovery.")

        if trend["consistency"] == "POOR":
            st.error("🚨 Low consistency. Long-term targets at risk if pattern continues.")

st.markdown("---")
st.markdown("## 🎯 UPSC Balance Intelligence")

if st.button("📚 Analyze UPSC Focus (Last 7 Days)"):
    logs = fetch_last_n_days(7)
    upsc_analysis = analyze_upsc_balance(logs)

    st.write(f"**Days Analyzed:** {upsc_analysis['days_analyzed']}")
    st.write("### Coverage Summary")
    st.write(upsc_analysis["coverage"])

    if upsc_analysis["risks"]:
        st.markdown("### 🚨 UPSC Risk Alerts")
        for risk in upsc_analysis["risks"]:
            st.error(risk)
    else:
        st.success("✅ UPSC preparation balance looks healthy.")

st.markdown("---")
st.markdown("## 🤖 AI Researcher Progress Tracker")

if st.button("🧠 Analyze AI Research Depth (Last 14 Days)"):
    logs = fetch_last_n_days(14)
    ai_analysis = analyze_ai_depth(logs)

    st.write("### AI Activity by Level")
    st.write(ai_analysis["level_score"])

    st.write(f"**Dominant AI Level:** {ai_analysis['dominant_level']}")

    if ai_analysis["warnings"]:
        st.markdown("### 🚨 AI Progress Warnings")
        for w in ai_analysis["warnings"]:
            st.error(w)
    else:
        st.success("✅ AI progression shows healthy depth.")

st.markdown("---")
st.markdown("🧩 DSA Problem-Solving Tracker")

if st.button("📐 Analyze DSA Progress (Last 14 Days)"):
    logs = fetch_last_n_days(14)
    dsa_analysis = analyze_dsa_depth(logs)

    st.write("### DSA Activity by Level")
    st.write(dsa_analysis["level_score"])

    st.write(f"**Dominant DSA Level:** {dsa_analysis['dominant_level']}")

    if dsa_analysis["warnings"]:
        st.markdown("### 🚨 DSA Warnings")
        for w in dsa_analysis["warnings"]:
            st.error(w)
    else:
        st.success("✅ DSA progression looks healthy.")
