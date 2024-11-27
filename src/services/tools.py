from langchain.agents import Tool
from langchain_community.utilities import (
    WikipediaAPIWrapper,
    GoogleSerperAPIWrapper,
)
import os


def _setup_tools() -> list[Tool]:
    """Set up the tools for the chat agent."""

    search = GoogleSerperAPIWrapper(
        serper_api_key=os.getenv("SERPER_API_KEY"), gl="br", hl="pt-br", k=5
    )

    wikipedia = WikipediaAPIWrapper()

    return [
        Tool(
            name="Search",
            func=search.run,
            description="Useful for when you need to search the web for general data and up to date information.",
        ),
        Tool(
            name="Wikipedia",
            func=wikipedia.run,
            description="Useful for when you need to answer general questions about people, places, companies, facts, historical events, or other subjects. Input should be a search query.",
        ),
    ]
