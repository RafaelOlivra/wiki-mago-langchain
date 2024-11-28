import streamlit as st
import json

from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

from services.tools import _setup_tools


class SmartChatAgent:
    def __init__(self, prompt_template: str = None):
        self.llm = self._setup_llm()
        self.tools = _setup_tools()
        self.prompt = self._setup_prompt(prompt_template=prompt_template)
        self.agent = self._setup_agent()
        self.executor = self._get_agent_executor()
        self.name = "Smart Chat Agent"

    # ------------------------
    # User facing methods
    # ------------------------

    def ask(self, query: str) -> str:
        """Ask the agent a question."""
        try:
            response = self.executor.invoke({"input": query})
            return response["output"]
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def clear_chat_history(self):
        """Clear the chat history and reinitialize the AgentExecutor."""
        self.executor.memory.clear()

    def chat_history(self) -> list[HumanMessage | SystemMessage]:
        """Get the chat history."""
        return self.executor.memory.chat_memory.messages

    def chat_history_to_json(self) -> list[dict]:
        """Export the chat history to a JSON file."""
        history = []
        for message in self.chat_history():
            history.append(
                {
                    "type": message.type,
                    "content": message.content,
                    "metadata": message.response_metadata,
                }
            )
        return json.dumps(history, indent=4)

    # ------------------------
    # Set-up the LLM model
    # ------------------------

    def _setup_llm(self):
        """Set up the language model"""
        assert False, "Subclasses must implement this method"

    def _setup_agent(self):
        """Set up the agent"""
        return create_react_agent(llm=self.llm, tools=self.tools, prompt=self.prompt)

    def _get_agent_executor(self) -> AgentExecutor:
        """Get the agent executor from the session state"""
        if "agent_executor" not in st.session_state:
            msgs = StreamlitChatMessageHistory()
            memory = ConversationBufferMemory(chat_memory=msgs, return_messages=True)
            st.session_state.agent_executor = AgentExecutor(
                agent=self.agent,
                tools=self.tools,
                memory=memory,
                verbose=True,
                max_iterations=6,
                handle_parsing_errors=True,
            )
        return st.session_state.agent_executor

    def _setup_prompt(self, prompt_template: str = None) -> PromptTemplate:
        """
        Set up the prompt template for the agent.

        Args:
            prompt_template (str): The prompt template to use. If None, a default template will be used.

        Returns:
            PromptTemplate: The prompt template.
        """
        prompt_template = (
            prompt_template
            or """
        You are an intelligent and approachable research assistant that is also a magician, you are designed to help users find articles,
        insights, and knowledge related to their questions.
        You have access to the following tools to assist in your research: 
        {tools}

        To use a tool, respond exactly in this format:

        Question: Identify and restate the user's query (Write in English).
        Thought: Analyze the question and decide whether to use a tool.
        Action: Choose a single tool from [{tool_names}] if necessary to gather information.
        Action Input: Provide the appropriate input for the selected tool.
        Observation: Review the tool's output and reflect on its relevance.
        
        If you already have the answer to the user's question, provide it with the following format:
        
        Thought: I now know what to answer
        Final Answer: Deliver a concise, accurate, and helpful response. (This should be written in Brazilian Portuguese)
        
        IMPORTANT!
        FOLLOW the exact format and structure of the template.
        DO NOT reveal that you are an AI assistant. Always maintain a helpful and professional tone.
        When possible, try to always return a helpful related URL (Web, YouTube or Wikipedia) with extra information.
        Final Answer should be in Brazilian Portuguese and Markdown format.
        ALWAYS answer like you where a magician!

        # Important Context:
        
        ## Chat History:
        {history}
        
        ## Latest Question:
        {input}
        
        ## Your Notes:
        {agent_scratchpad}
        
        """
        )
        return PromptTemplate(
            template=prompt_template,
            input_variables=[
                "input",
                "history",
                "agent_scratchpad",
                "tools",
                "tool_names",
            ],
        )
