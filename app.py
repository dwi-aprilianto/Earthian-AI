import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


#page config
st.set_page_config(
    page_title="Earthian AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)
#load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error(
        "GEMINI_API_KEY was not found. "
        "Please make sure your .env file is configured correctly."
    )
    st.stop()

#gemini client
@st.cache_resource
def get_client(api_key):
    return genai.Client(api_key=api_key)
client = get_client(API_KEY)

#ai persona
PERSONA = """
You are Earthian AI, an intelligent travel assistant.

Your main purpose is to help users with:

- Travel destinations
- Trip planning
- Itinerary recommendations
- Popular attractions
- Hidden gems
- Local food
- Transportation
- Accommodation
- Travel budgets
- Travel tips

Always respond in English.

Use a friendly, intelligent, natural, and helpful tone.

Keep your answers clear and well structured.

When recommending a destination, provide useful information such as:
- Why the destination is worth visiting
- Recommended activities
- Estimated budget when relevant
- Practical travel tips

If the user asks something unrelated to travel, politely explain that
Earthian AI is specialized in travel assistance and guide the user back
to travel-related topics.

Do not invent specific information.
For prices, weather, opening hours, transportation schedules,
or other information that may change over time, remind users
to verify the latest information before traveling.
"""
#custom css
st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #080c14;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0c121d;
        border-right: 1px solid #1e293b;
    }

    /* Main title */
    h1 {
        font-family: "Arial", sans-serif;
        font-weight: 700;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        border-radius: 14px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        border: 1px solid #334155;
        background-color: #111827;
        color: #e2e8f0;
    }

    .stButton > button:hover {
        border-color: #14b8a6;
        color: #5eead4;
    }

    </style>
    """,
    unsafe_allow_html=True
)
#session state initialization

if "messages" not in st.session_state:
    st.session_state.messages = []


if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model="gemini-3.1-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction=PERSONA
        )
    )
#sidebar
with st.sidebar:

    st.title("🌍 Earthian AI")

    st.caption("Your Intelligent Travel Companion")

    st.divider()

    st.success("Earthian Core Online")

    st.subheader("Travel Assistant")

    st.write(
        "Discover destinations, explore popular places, "
        "and plan your next journey with AI."
    )

    st.divider()

    st.subheader("Popular Searches")

    if st.button(
        "🌴 Popular destinations in Bali",
        use_container_width=True
    ):
        st.session_state.quick_prompt = (
            "What are the most popular destinations to visit in Bali?"
        )
        st.rerun()

    if st.button(
        "🏔️ Hidden gems in Indonesia",
        use_container_width=True
    ):
        st.session_state.quick_prompt = (
            "What are some beautiful hidden gems to visit in Indonesia?"
        )
        st.rerun()

    if st.button(
        "🍜 Best food in Bandung",
        use_container_width=True
    ):
        st.session_state.quick_prompt = (
            "What are the best local food experiences to try in Bandung?"
        )
        st.rerun()

    if st.button(
        "✈️ Plan a 3-day trip",
        use_container_width=True
    ):
        st.session_state.quick_prompt = (
            "Create a realistic 3-day travel itinerary for a popular "
            "destination in Indonesia."
        )
        st.rerun()

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.session_state.chat_session = client.chats.create(
            model="gemini-3.1-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=PERSONA
            )
        )

        st.rerun()


    st.divider()

    st.caption("Powered by Google Gemini")
    st.caption("Earthian AI © 2026")


#main page

st.title("🌍 Earthian AI")

st.caption(
    "Your intelligent travel companion for discovering places "
    "and planning unforgettable journeys."
)

#empty state
if len(st.session_state.messages) == 0:

    st.info(
        "Welcome to Earthian AI. "
        "Ask me anything about destinations, travel planning, "
        "local experiences, food, transportation, or your next journey."
    )

    st.subheader("Start Exploring")

    col1, col2, col3 = st.columns(3)


    with col1:

        if st.button(
            "🧭 Discover a destination",
            use_container_width=True
        ):

            st.session_state.quick_prompt = (
                "Recommend a destination in Indonesia "
                "for my next vacation."
            )

            st.rerun()

    with col2:

        if st.button(
            "🗺️ Build an itinerary",
            use_container_width=True
        ):

            st.session_state.quick_prompt = (
                "Create a detailed 3-day travel itinerary "
                "for a destination in Indonesia."
            )

            st.rerun()

    with col3:

        if st.button(
            "🍽️ Explore local food",
            use_container_width=True
        ):

            st.session_state.quick_prompt = (
                "Recommend the best local food experiences "
                "for a traveler visiting Indonesia."
            )

            st.rerun()

#display conversation
for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
        avatar=(
            "🌍"
            if message["role"] == "assistant"
            else "👤"
        )
    ):

        st.markdown(message["content"])

# USER INPUT
prompt = None

if "quick_prompt" in st.session_state:

    prompt = st.session_state.quick_prompt

    del st.session_state.quick_prompt

else:

    prompt = st.chat_input(
        "Ask Earthian AI about your next journey..."
    )

#chat response
if prompt:

    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.markdown(prompt)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message(
        "assistant",
        avatar="🌍"
    ):

        with st.spinner(
            "Earthian AI is thinking..."
        ):

            try:

                response = (
                    st.session_state
                    .chat_session
                    .send_message(prompt)
                )


                answer = response.text


                st.markdown(answer)


                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as error:

                st.error(
                    "Earthian AI encountered an unexpected error."
                )

                st.caption(
                    f"Technical details: {str(error)}"
                )