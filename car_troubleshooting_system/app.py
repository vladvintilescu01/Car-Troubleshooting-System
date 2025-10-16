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
st.title("🚗 Car Troubleshooting Helper")
st.markdown(
    """
    🛠️ Describe your car's symptoms below, separated by commas. 
    You'll get **easy-to-understand suggestions** for possible issues and what you can do to fix them.
    """
)

# --- Load rules ---
rules = load_rules()

# --- User input ---
symptoms_input = st.text_area(
    "Describe your car's symptoms:",
    placeholder="e.g., engine won't start, dim headlights, strange noise"
)

# --- Analyze button ---
if st.button("🔎 Analyze"):
    if symptoms_input.strip() == "":
        st.warning("⚠️ Please describe at least one symptom!")
    else:
        symptoms = [normalize(s) for s in symptoms_input.split(",")]
        st.subheader("🧭 Analysis Results")

        for symptom in symptoms:
            causes = find_causes_with_chain(symptom, rules)
            st.markdown(f"### 🔹 Symptom: {symptom.capitalize()}")

            if causes:
                st.markdown("💡 **Possible issues and suggestions:**")

                for idx, cause in enumerate(causes, 1):
                    steps = [step.strip() for step in cause.split("->")]
                    # Use expander for each cause chain
                    with st.expander(f"Option {idx}: {steps[0].replace('_', ' ').capitalize()}"):
                        for i, step in enumerate(steps):
                            icon = "🔹" if i == 0 else "&nbsp;&nbsp;&nbsp;&nbsp;🔧"
                            friendly_step = step.replace("_", " ").capitalize()
                            st.markdown(f"{icon} {friendly_step}")
                st.success("✅ Following these steps should help fix your car!")
            else:
                st.error("⚠️ We couldn't classify this symptom. Consider visiting a mechanic.")
