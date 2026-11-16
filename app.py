
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="FIRESPACE SI",
    page_icon="🔥",
    layout="wide"
)

st.title("🔥 FIRESPACE SI")
st.subheader("Intelligent Fire Risk Analysis System")

st.write(
    "Interactive fire risk simulator for human space exploration."
)

st.warning(
    "Educational prototype. Scores are illustrative and "
    "not validated for real-world safety decisions."
)

if "history" not in st.session_state:
    st.session_state.history = []

st.sidebar.header("Scenario Configuration")

scenario = st.sidebar.selectbox(
    "Scenario Type",
    ["Habitat Cabin", "Material Storage",
     "Work Area", "Experimental Module"]
)

material = st.sidebar.selectbox(
    "Material Type",
    ["Paper", "Plastic", "Textile",
     "Metal", "Wood", "Composite Material"]
)

temperature = st.sidebar.slider(
    "Temperature (°C)", 0, 100, 25
)

fahrenheit = temperature * 9 / 5 + 32

st.sidebar.metric(
    "Temperature (°F)", f"{fahrenheit:.1f} °F"
)

oxygen = st.sidebar.slider(
    "Oxygen Concentration (%)", 0, 100, 21
)

ventilation = st.sidebar.slider(
    "Relative Ventilation (%)", 0, 100, 50
)

material_scores = {
    "Paper": 80,
    "Plastic": 85,
    "Textile": 75,
    "Metal": 10,
    "Wood": 80,
    "Composite Material": 65
}

st.divider()
st.header("Scenario Analysis")

if st.button("🔍 ANALYZE SCENARIO", type="primary"):

    score = (
        temperature * 0.30
        + oxygen * 0.25
        + (100 - ventilation) * 0.15
        + material_scores[material] * 0.30
    )

    score = round(max(0, min(100, score)), 1)

    if score <= 35:
        classification = "LOW RISK"
        interpretation = "The illustrative score is low."

    elif score <= 65:
        classification = "MODERATE RISK"
        interpretation = "The illustrative score is moderate."

    else:
        classification = "HIGH RISK"
        interpretation = "The illustrative score is high."

    result = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Scenario": scenario,
        "Material": material,
        "Temperature_C": temperature,
        "Temperature_F": round(fahrenheit, 1),
        "Oxygen_%": oxygen,
        "Ventilation_%": ventilation,
        "Score": score,
        "Classification": classification
    }

    st.session_state.history.append(result)

    st.subheader("Analysis Results")

    col1, col2 = st.columns(2)

    col1.metric("Risk Score", f"{score}/100")
    col2.metric("Classification", classification)

    st.progress(int(score))
    st.info(interpretation)

    st.write("### Scenario Details")
    st.write(f"Scenario: {scenario}")
    st.write(f"Material: {material}")
    st.write(f"Temperature: {temperature} °C / {fahrenheit:.1f} °F")
    st.write(f"Oxygen: {oxygen}%")
    st.write(f"Ventilation: {ventilation}%")

st.divider()
st.header("Analysis History")

if st.session_state.history:

    history_df = pd.DataFrame(st.session_state.history)

    st.dataframe(history_df, use_container_width=True)

    st.download_button(
        "📥 EXPORT HISTORY TO CSV",
        data=history_df.to_csv(index=False).encode("utf-8"),
        file_name="firespace_history.csv",
        mime="text/csv"
    )

else:
    st.write("No scenarios analyzed yet.")
