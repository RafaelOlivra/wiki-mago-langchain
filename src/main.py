import streamlit as st

from dotenv import load_dotenv

from services.gemini_agent import GeminiAgent
from services.openai_agent import OpenAIAgent

from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

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
    col1, col2, col3 = st.columns([5, 2, 2])

    col1.write("## Wiki Mago 🧙‍♂️")

    # Clear the streaming leftover after we get the complete response
    CLEAR_STREAMING_THOUGHTS = True

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
            "wiki-mago-chat-history.json",
            "application/json",
            key="export-chat",
            use_container_width=True,
        )

    # Agent intro
    with st.expander("Abracadabra! ✨", expanded=True):
        st.info(
            """ 
            Sou um chatbot mágico que utiliza dados da 📘 Wikipedia, 📽️ YouTube e da 🌐 Web para responder perguntas sobre qualquer assunto.  \
            
            Precisa de ajuda com uma pesquisa? Tem curiosidade sobre algo específico? Ou só quer assistir vídeos de gatinhos brincando?  \
                
            **O Wiki Mago sabe de tudo!** (Ou quase tudo... 🪄)
            """
        )

    # Display chat messages from history on app rerun
    st.write("#### Chat")

    chat_history = agent.chat_history()
    if not chat_history:
        st.warning(
            """
            Faça uma pergunta para começar!  \
                
            - "Quem é o 7º presidente do Brasil?"
            - "Quem foi o primeiro astronauta a pisar na Lua?"
            - "Principais notícias para São Paulo"
            - "Vídeos sobre como fazer um bolo de chocolate!"
            """
        )

    st.write(" ")
    for message in chat_history:
        with st.chat_message(message.type):
            st.markdown(message.content)

    # Accept user input
    if prompt := st.chat_input("Em que posso ajudar?"):
        with st.chat_message("human"):
            st.markdown(prompt)

        # Get response from agent
        with st.spinner("Pensando✨..."):
            try:
                streaming_callback = StreamlitCallbackHandler(st.container())
                st.markdown(agent.ask(prompt, callbacks=[streaming_callback]))
            except Exception as e:
                st.error(e)

        # Clear the streaming output and show the final response
        if CLEAR_STREAMING_THOUGHTS:
            st.rerun()


if __name__ == "__main__":
    Main()
