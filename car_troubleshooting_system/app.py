import streamlit as st
from inference_engine import load_rules, find_causes_with_chain, normalize

# Page configuration
st.set_page_config(
    page_title="Car Troubleshooting System",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("🚗 Car Troubleshooting System")
st.markdown("Enter your car's symptoms below, separated by commas, and get possible causes and fixes!")

# Load rules once
rules = load_rules()

# User input
symptoms_input = st.text_area(
    "Enter symptoms (comma-separated):",
    placeholder="e.g., engine does not start, headlights dim"
)

# Button to analyze
if st.button("Analyze Symptoms"):
    if symptoms_input.strip() == "":
        st.warning("Please enter at least one symptom!")
    else:
        symptoms = [normalize(s) for s in symptoms_input.split(",")]
        st.subheader("🔍 Analysis Results")

        for symptom in symptoms:
            causes = find_causes_with_chain(symptom, rules)
            st.markdown(f"**Symptom:** {symptom}")
            if causes:
                st.markdown("**Possible causes and fixes:**")
                for cause in causes:
                    st.markdown(f"- {cause}")
                st.success("✅ After all this, your problem should resolve.")
            else:
                st.error("⚠️ Cannot classify this symptom. Please check a service.")
