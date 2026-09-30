"""
app.py

PC Learner - a beginner-friendly PC building app.

This is the ONLY file you need to run:
    streamlit run app.py

It uses two helper files sitting in the same folder:
    - component_info.py   (a dictionary of beginner explanations)
    - components.csv      (a spreadsheet of real PC parts and prices)

The "Ask AI" bonus box uses Groq's free API to answer follow-up
questions. See the setup note above the ask_groq() function below.
"""

import streamlit as st
import pandas as pd
from component_info import COMPONENT_INFO

# ---------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------
st.set_page_config(page_title="PC Learner", page_icon="🖥️", layout="wide")
st.title("🖥️ PC Learner")
st.write("Learn how PCs work, and get a build recommendation that fits you.")

# Modern CSS Styling
modern_css = """
<style>
    /* Root color variables */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #ec4899;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --dark-bg: #0f172a;
        --light-bg: #f8fafc;
        --card-bg: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --border-color: #e2e8f0;
        --shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }

    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    }

    /* Header styling */
    h1 {
        background: linear-gradient(135deg, #6366f1 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.5px;
    }

    h2, h3 {
        color: #1e293b;
        font-weight: 600;
    }

    /* Subheader text */
    .stMarkdown > div:first-child {
        color: #64748b;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background-color: #f1f5f9;
        border-radius: 12px;
        padding: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: #64748b;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
        color: #6366f1;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);
    }

    .stTabs [aria-selected="false"]:hover {
        background-color: rgba(99, 102, 241, 0.05);
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #818cf8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Selectbox styling */
    .stSelectbox [data-baseweb="select"] {
        background-color: #ffffff;
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }

    .stSelectbox [data-baseweb="select"]:hover {
        border-color: #6366f1;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.1);
    }

    .stSelectbox [data-baseweb="select"]:focus-within {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }

    /* Slider styling */
    .stSlider [data-testid="stSliderThumb"] {
        background-color: #6366f1 !important;
    }

    .stSlider [data-testid="stSliderTickBar"] {
        background-color: #e2e8f0 !important;
    }

    .stSlider > div > div {
        background-color: #6366f1 !important;
    }

    /* Text input styling */
    .stTextInput input {
        background-color: #ffffff;
        border: 2px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease;
    }

    .stTextInput input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }

    /* Info box styling */
    .stInfo {
        background-color: #dbeafe !important;
        border-left: 4px solid #3b82f6 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }

    .stInfo > div {
        color: #1e40af !important;
        font-weight: 500 !important;
    }

    /* Success box styling */
    .stSuccess {
        background-color: #d1fae5 !important;
        border-left: 4px solid #10b981 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }

    .stSuccess > div {
        color: #065f46 !important;
        font-weight: 500 !important;
    }

    /* Warning box styling */
    .stWarning {
        background-color: #fef3c7 !important;
        border-left: 4px solid #f59e0b !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }

    .stWarning > div {
        color: #78350f !important;
        font-weight: 500 !important;
    }

    /* Expander styling */
    .stExpander {
        background-color: #f8fafc;
        border: 2px solid #e2e8f0 !important;
        border-radius: 10px !important;
        transition: all 0.3s ease;
    }

    .stExpander:hover {
        border-color: #6366f1;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.1);
    }

    .stExpander > div:first-child {
        color: #1e293b;
        font-weight: 600;
        padding: 1rem;
    }

    /* Metric styling */
    .stMetric {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }

    .stMetric [data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 600;
    }

    .stMetric [data-testid="stMetricValue"] {
        color: #6366f1;
        font-size: 2rem !important;
    }

    /* Divider styling */
    .stDivider {
        border-top: 2px solid #e2e8f0 !important;
        margin: 2rem 0 !important;
    }

    /* Write/text styling */
    .stMarkdown {
        color: #1e293b;
        line-height: 1.6;
    }

    /* Subheader styling */
    h4, h5, h6 {
        color: #1e293b;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    /* Spinner styling */
    .stSpinner {
        color: #6366f1 !important;
    }

    /* Overall text color */
    body {
        color: #1e293b;
    }

    /* Sidebar styling */
    .stSidebar {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }

    /* Code block styling */
    code {
        background-color: #f1f5f9;
        border-radius: 6px;
        padding: 0.25rem 0.5rem;
        color: #ec4899;
        font-weight: 500;
    }

    /* Link styling */
    a {
        color: #6366f1;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s ease;
    }

    a:hover {
        color: #ec4899;
    }
</style>
"""

st.markdown(modern_css, unsafe_allow_html=True)

# Load the spreadsheet of parts once, so every tab can use it
parts = pd.read_csv("components.csv")

# Streamlit tabs = an easy way to have "sections" without extra files/pages
tab_learn, tab_recommend = st.tabs(["📚 Learn", "🎯 Get a Recommendation"])


# ---------------------------------------------------------
# BONUS: ASK AI (uses Groq's free API)
# ---------------------------------------------------------
# Setup (one-time):
#   1. Get a free key at https://console.groq.com/keys (no credit card)
#   2. Create a file called .streamlit/secrets.toml next to this app with:
#          GROQ_API_KEY = "your-key-here"
#   3. Run: pip install groq
#
# This function asks Groq's AI a question and returns the answer as text.
# If anything goes wrong (no key, no internet, etc.) it returns a friendly
# error message instead of crashing the app.
def ask_groq(question, topic_hint):
    try:
        api_key = st.secrets.get("GROQ_API_KEY", None)
    except Exception:
        # This happens if secrets.toml doesn't exist at all yet
        api_key = None

    if not api_key:
        return None, "AI isn't set up yet (no GROQ_API_KEY found in secrets.toml)."

    try:
        from groq import Groq
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly teacher explaining PC hardware to a "
                        "complete beginner. Keep answers short (3-4 sentences), "
                        "avoid jargon, and use simple everyday analogies. "
                        f"The user is currently learning about: {topic_hint}."
                    ),
                },
                {"role": "user", "content": question},
            ],
        )
        return response.choices[0].message.content, None

    except Exception as e:
        return None, f"AI request failed: {e}"


# ---------------------------------------------------------
# TAB 1: LEARNING SECTION
# ---------------------------------------------------------
with tab_learn:
    st.header("📚 Learn About PC Parts")

    # A dropdown built straight from the dictionary's keys
    component_names = list(COMPONENT_INFO.keys())
    choice = st.selectbox("Pick a part to learn about:", component_names)

    info = COMPONENT_INFO[choice]

    st.subheader(f"{info['emoji']} {choice}")
    st.write(info["summary"])
    st.info(f"💡 Tip: {info['tip']}")

    # --- Bonus AI box ---
    with st.expander("🤖 Bonus: Ask AI a question about this part"):
        question = st.text_input(
            "Type your question:",
            placeholder=f"e.g. Do I really need a good {choice} for gaming?",
            key=f"ai_question_{choice}",
        )
        if question:
            with st.spinner("Thinking..."):
                answer, error = ask_groq(question, topic_hint=choice)
            if answer:
                st.success(answer)
            else:
                st.warning(error)


# ---------------------------------------------------------
# TAB 2: RECOMMENDATION SECTION
# ---------------------------------------------------------
with tab_recommend:
    st.header("🎯 Get a Build Recommendation")

    use_case = st.selectbox(
        "What will you mainly use this PC for?",
        ["Gaming", "Video/photo editing", "Office and school work", "General everyday use"],
    )

    budget = st.slider("What's your budget (USD)?", 300, 3000, 800, step=50)

    if st.button("Build My PC!", type="primary"):
        st.divider()
        st.subheader("Your Recommended Build")

        total_price = 0
        # For each part TYPE (CPU, GPU, RAM, ...), pick one matching row
        part_types = parts["type"].unique()

        for part_type in part_types:
            # Only look at rows of this part type
            options = parts[parts["type"] == part_type]

            # Try to find one matching the chosen use case
            matches = options[options["use_case"] == use_case]

            # If none match the use case, just use any option of this type
            if matches.empty:
                matches = options

            # Pick the cheapest matching option that's under our leftover budget
            # (a simple, beginner-friendly way to "fit" a budget)
            choice_row = matches.sort_values("price").iloc[0]

            st.write(f"**{part_type}:** {choice_row['name']} — ${choice_row['price']:.2f}")
            total_price += choice_row["price"]

        st.metric("Estimated Total", f"${total_price:.2f}")

        if total_price <= budget:
            st.success("✅ This build fits your budget!")
        else:
            st.warning("⚠️ This build goes over your budget a bit.")
