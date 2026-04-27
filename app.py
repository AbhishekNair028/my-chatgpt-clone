import streamlit as st
from groq import Groq

# 1. UI Styling
st.set_page_config(page_title="Abhishek AI", page_icon="⚡")
st.markdown("""<style> .stApp { background-color: #0b0d11; color: white; } </style>""", unsafe_allow_html=True)
st.title("⚡ My Private GPT")

# 2. Setup Groq (Using Secrets for Security)
# We will add the key in the dashboard later
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle Input
if prompt := st.chat_input("What is the hack?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
