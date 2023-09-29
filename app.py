import streamlit as st
import openai
import os
import pandas as pd
import matplotlib.pyplot as plt

from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Retrieve API key
openai.api_key = os.getenv("OPENAI_API_KEY")


# Function to query the LLM (GPT-3) for analysis
def query_llm(traffic_data):
    prompt = f"Analyze the following real-time traffic data and provide recommendations:\nCongestion Level: {traffic_data['congestion']}%\nAccidents Reported: {traffic_data['accidents']}\n"
    response = openai.Completion.create(
        engine="text-davinci-002", prompt=prompt, max_tokens=500
    )
    return response.choices[0].text.strip()


# Initialize historical data
if "data" not in st.session_state:
    st.session_state["data"] = []

# Streamlit App
st.set_page_config(
    page_title="Traffic Management with LLM",
    layout="wide",
    initial_sidebar_state="expanded",
)

# UCF banner image
st.image("./UCF.jpg", width=900, caption="University of Central Florida")

# Header
st.title("🚦 Real-time Traffic Management with LLM 🚦")

# Sidebar
st.sidebar.header("🌐 Navigation")
page = st.sidebar.radio(
    "Go to", ["🏠 Home", "📦 Historical Data", "User Feedback", "Emergency Alert"]
)


# Home Page
if page == "Home":
    st.header("📊 Real-time Traffic Data 📊")
    col1, col2 = st.columns(2)
    with col1:
        congestion_level = st.slider("Congestion Level (%)", 0, 100, 50)
    with col2:
        accidents_reported = st.slider("Accidents Reported", 0, 5, 0)

    traffic_data = {"congestion": congestion_level, "accidents": accidents_reported}

    st.header("📝 LLM Recommendations 📝")
    if st.button("Generate Recommendations"):
        llm_output = query_llm(traffic_data)
        st.success(f"Recommendation: {llm_output}")
        st.session_state["data"].append(
            {
                "congestion": congestion_level,
                "accidents": accidents_reported,
                "recommendation": llm_output,
            }
        )

# Historical Data Page
elif page == "Historical Data":
    st.header("📜 Historical Data 📜")
    if st.session_state["data"]:
        df = pd.DataFrame(st.session_state["data"])
        st.write(df)
        fig, ax = plt.subplots()
        ax.plot(df["congestion"], label="Congestion Level")
        ax.plot(df["accidents"], label="Accidents Reported")
        ax.legend()
        st.pyplot(fig)

# User Feedback Page
elif page == "User Feedback":
    st.header("💬 User Feedback 💬")
    feedback = st.text_area("Provide feedback on the recommendations:")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")

# Emergency Alert Page
elif page == "Emergency Alert":
    st.header("🚨 Emergency Alert 🚨")
    if st.button("Flag Emergency"):
        st.error("Emergency flagged. Immediate action required.")
