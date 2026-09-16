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
st.set_page_config(page_title="PC Learner", page_icon="🖥️")
st.title("🖥️ PC Learner")
st.write("Learn how PCs work, and get a build recommendation that fits you.")

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
