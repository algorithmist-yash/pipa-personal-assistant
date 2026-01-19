import streamlit as st
from datetime import date

st.set_page_config(
    page_title="PIPA – Personal Intelligence & Progress Analyzer",
    layout="centered"
)

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
    st.success("Day logged successfully! Analysis engine will be added next.")
