from langchain.chat_models import init_chat_model
from langchain.tools import tool
from Rag_agent import prompt


# llm = init_chat_model(
#     model="llama-3.3-70b-versatile",
#     model_provider="openai",
#     base_url="https://api.groq.com/openai/v1",
#     api_key="YOUR_API_KEY"
# )


@tool
def answer_question_tool(context: str, question: str) -> str:
    """
    Docstring for answer_question_tool
    -This answer_question_tool function generates the result based on the provided context and user question.
    -Answer using retrieved context only
    :param context: str - relevent page content,  question: str - user question
    """

    llm_prompt = f"""
    You are an chatbot of a website 'Sunbeam Infotech' which answers about the website based on the scraped data from the website.

    You are given relevent scraped page content retrieved from a database.
    Your task:
    - Answer ONLY what the user has asked.
    - Use ONLY the provided page content.
    - Ignore unrelated sections completely.
    - Do NOT mention irrelevant details.
    - Be concise, precise, and factual.

    Rules:
    - If the answer is found in one section, use only that section.
    - If the answer is not present, say: "Information not available in the provided content."
    - Do not add assumptions or external knowledge.
    - Do not reference sections unless required.

    Question:
    {question}

    Context:
    {context}

    """
    return prompt.llm.invoke(llm_prompt).content
