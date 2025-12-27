import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="Sandhya | AI Portfolio Assistant",
    page_icon="🤖",
    layout="centered"
)

# ---------------------------------
# HEADER
# ---------------------------------
st.markdown(
    """
    <h1 style="text-align:center;">🤖 AI Portfolio Assistant</h1>
    <p style="text-align:center; font-size:16px;">
        Personal AI Assistant for <b>Sandhya Thukakula</b>
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------------------------------
# LOAD PORTFOLIO DATA
# ---------------------------------
@st.cache_data
def load_portfolio():
    with open("portfolio_data.txt", "r", encoding="utf-8") as f:
        return f.read()

PORTFOLIO_DATA = load_portfolio()

# ---------------------------------
# MODE SELECTION
# ---------------------------------
mode = st.radio(
    "Select Mode",
    ["🧑‍💼 Portfolio Assistant", "🎯 Interview Practice"],
    horizontal=True
)

# ---------------------------------
# LOAD API KEY
# ---------------------------------
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("⚠️ GOOGLE_API_KEY not found. Add it in Streamlit Secrets.")
    st.stop()

# ---------------------------------
# SYSTEM PROMPT BASED ON MODE
# ---------------------------------
if mode == "🧑‍💼 Portfolio Assistant":
    SYSTEM_PROMPT = f"""
    You are a professional AI Portfolio Assistant for Sandhya Thukakula.

    Rules:
    - Answer ONLY using the portfolio data.
    - Be clear, concise, and recruiter-friendly.
    - Do NOT invent information.
    - If the question is outside the portfolio, reply:
      "I can answer only based on Sandhya's portfolio."

    Portfolio Data:
    {PORTFOLIO_DATA}
    """
else:
    SYSTEM_PROMPT = f"""
    You are an AI Interviewer for Sandhya Thukakula.

    Rules:
    - Ask HR and Technical interview questions.
    - Use Sandhya's portfolio to personalize questions.
    - If the user answers, provide feedback and an improved answer.
    - Be supportive and professional.

    Portfolio Data:
    {PORTFOLIO_DATA}
    """

# ---------------------------------
# SESSION STATE (CHAT MEMORY)
# ---------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello 👋 I’m Sandhya’s AI Portfolio Assistant.\n\n"
                "You can ask about her **projects, skills, internships**, "
                "or switch to **Interview Practice Mode** to prepare for interviews."
            )
        }
    ]

# ---------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------
# CHAT INPUT
# ---------------------------------
placeholder_text = (
    "Ask about projects, skills, experience..."
    if mode == "🧑‍💼 Portfolio Assistant"
    else "Ask for an interview question or answer one..."
)

user_prompt = st.chat_input(placeholder_text)

# ---------------------------------
# HANDLE USER INPUT
# ---------------------------------
if user_prompt:
    # Store user message
    st.session_state.messages.append(
        {"role": "user", "content": user_prompt}
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"User Input: {user_prompt}",
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.3
                )
            )

        ai_reply = response.text
        st.markdown(ai_reply)

    # Save assistant reply
    st.session_state.messages.append(
        {"role": "assistant", "content": ai_reply}
    )

# ---------------------------------
# FOOTER
# ---------------------------------
st.markdown(
    f"""
    <hr>
    <p style="text-align:center; font-size:13px; color:gray;">
        © {datetime.now().year} Sandhya Thukakula | AI Portfolio Assistant
    </p>
    """,
    unsafe_allow_html=True
)
