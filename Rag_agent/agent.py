# from langgraph.prebuilt import create_react_agent
from rag_tools.retriever_tool import retrieve_context
from langchain.agents import create_agent

class RAGAgent:
    def __init__(self, llm):
        self.agent = create_agent(
            model=llm,
            tools=[retrieve_context],
            system_prompt="""
                You are a helpful AI assistant.
                Use retrieve_context to answer questions from the documents.
                If answer not found, say "I don't know".
                """
        )

    # def run(self, query: str) -> str:
    #     response = self.agent.invoke(
    #         {"input": query}
    #     )
    #     return response["messages"][-1].content
