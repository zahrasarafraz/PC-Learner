import streamlit as st
 
st.set_page_config(page_title="PC Learner")
 
st.title("🖥️ PC Learner")
 
st.write("Learn about PC components and build your first PC.")

name = st.text_input("What is your name?")
 
if name:
    st.write(f"Welcome, {name}! Let's learn about PCs.")

component = st.selectbox(
    "Which PC part do you want to learn about?",
    ["CPU", "GPU", "RAM", "Storage"]
)
 
st.write(f"You selected: {component}")
   
