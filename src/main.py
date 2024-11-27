import streamlit as st

from dotenv import load_dotenv

from services.gemini_agent import GeminiAgent
from services.openai_agent import OpenAIAgent

# ------------------------
# Page layout and setup
# ------------------------

# Load environment variables
load_dotenv()

# Set page title
st.set_page_config(
    page_title="Wiki Mago",
    page_icon="🧙‍♂️",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ------------------------
# Main app
# ------------------------
def Main():
    col1, col2, col3 = st.columns([6, 2, 2])

    col1.write("## Wiki Mago 🧙‍♂️")

    # Select LLM model
    model = st.selectbox(
        "Selecione o LLM", ["Gemini (gemini-1.5-flash)", "OpenAi (gpt-4o-mini)"]
    )
    if model == "Gemini (gemini-1.5-flash)":
        agent = GeminiAgent()
    else:
        agent = OpenAIAgent()

    # Clear chat history
    with col2:
        st.write(" ")
        if st.button("Limpar 🗑", use_container_width=True):
            agent.clear_chat_history()
            st.rerun()

    # Export chat history to JSON
    with col3:
        st.write(" ")
        json = agent.chat_history_to_json()
        st.download_button(
            "Exportar ⬇️",
            json,
            "chat_history.json",
            "application/json",
            key="export-chat",
            use_container_width=True,
        )

    # Agent intro
    with st.expander("Abracadabra! ✨", expanded=True):
        st.info(
            """
                Sou um chatbot que utiliza dados da Wikipedia 📘 e da Web 🌐 para trazer respostas mágicas sobre qualquer assunto.  \
                    
                - "Quem é o 7º presidente do Brasil?"
                - "Quem foi o primeiro astronauta a pisar na Lua?"  \

                    
                O Wiki Mago sabe de tudo! (Ou quase tudo...)
        """
        )

    # Display chat messages from history on app rerun
    st.write("#### Chat")
    st.write(" ")
    for message in agent.chat_history():
        with st.chat_message(message.type):
            st.markdown(message.content)

    # Accept user input
    if prompt := st.chat_input("Em que posso ajudar?"):
        # Display user message in chat message container
        with st.chat_message("human"):
            st.markdown(prompt)

        # Get response from agent
        with st.spinner("Pensando✨..."):
            try:
                response = agent.ask(prompt)
            except Exception as e:
                response = str(e)

        # Display agent response in chat message container
        st.rerun()


if __name__ == "__main__":
    Main()
