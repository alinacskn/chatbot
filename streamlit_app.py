import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("Sokratischer-Chatbot")
st.write(
    "Dieser Chatbot fragt dich was! "
    "Gib deinen OpenAI API Key ein, um loszulegen."
)

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Bitte füge deinen OpenAI API Key ein, um fortzufahren.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # System-Prompt, der den Bot auf Pferde festlegt
    SYSTEM_PROMPT = {
        "role": "system",
        "content": (
            "Du bist ein sokratischer Dialogpartner."
            "Du stellst Fragen, um den Nutzer zum Nachdenken zu bringen, "
            "anstatt direkte Antworten zu geben. "
            "Das Ziel ist es, den User durch Fragen zu neuen Erkenntnissen zu führen, "
        )
    }

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Starte die Konversation um loszulegen!"):

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # System-Prompt wird bei jedem API-Call vorangestellt
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                SYSTEM_PROMPT,
                *[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            ],
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})