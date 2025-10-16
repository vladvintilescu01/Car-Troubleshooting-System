import streamlit as st
from inference_engine import load_rules, find_causes_with_chain, normalize

# --- Page configuration ---
st.set_page_config(
    page_title="Car Troubleshooting System",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Header ---
st.title("🚗 Car Troubleshooting System")
st.markdown(
    "Enter your car's **symptoms** below (comma-separated), and get step-by-step **possible causes and fixes**."
)

# --- Load rules ---
rules = load_rules()

# --- User input ---
symptoms_input = st.text_area(
    "🩺 Enter symptoms (comma-separated):",
    placeholder="e.g., engine does not start, strange noise under hood"
)

# --- Analyze button ---
if st.button("🔍 Analyze Symptoms"):
    if symptoms_input.strip() == "":
        st.warning("⚠️ Please enter at least one symptom!")
    else:
        # Normalize all symptoms
        symptoms = [normalize(s) for s in symptoms_input.split(",")]
        st.subheader("🧭 Analysis Results")

        for symptom in symptoms:
            # Get all possible cause chains for this symptom
            causes_list = find_causes_with_chain(symptom, rules)

            st.markdown(f"### 🧩 Symptom: {symptom.replace('_',' ').title()}")

            if causes_list:
                for idx, chain in enumerate(causes_list, 1):
                    with st.expander(f"⚙️ Option {idx}: Possible Cause and Fix Chain"):
                        for step_idx, step in enumerate(chain):
                            indent = "&nbsp;&nbsp;&nbsp;&nbsp;" * step_idx
                            icon = "🔹" if step_idx == 0 else "🔧"
                            st.markdown(f"{indent}{icon} **{step.replace('_',' ').title()}**")
                st.success("✅ After checking these steps, your problem should be resolved.")
            else:
                st.error("🚫 Cannot classify this symptom. Please check a service.")
