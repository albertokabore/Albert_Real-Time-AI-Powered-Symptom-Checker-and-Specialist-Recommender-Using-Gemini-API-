import streamlit as st
from gemini_api import analyze_symptoms

st.set_page_config(page_title="AI-Powered Symptom Checker", page_icon=":hospital:")

st.title("AI-Powered Symptom Checker and Specialist Recommender")

st.markdown("""
Enter your symptoms as you would explain to a doctor.
The system will analyze your input, summarize the main points, suggest likely medical conditions, and recommend the type of specialist you should consult.
""")

user_input = st.text_area("Describe your symptoms here:", height=160)

if st.button("Analyze"):
    if user_input.strip():
        with st.spinner("Consulting the AI model..."):
            result = analyze_symptoms(user_input)
            if "error" in result:
                st.error(result["error"])
            else:
                st.success("AI analysis complete.")
                st.subheader("1. Symptom Summary")
                st.write(result.get("summary", "N/A"))
                st.subheader("2. Possible Medical Conditions")
                st.write(result.get("conditions", "N/A"))
                st.subheader("3. Recommended Specialist")
                st.write(result.get("specialist", "N/A"))
    else:
        st.warning("Please enter your symptoms before clicking Analyze.")
