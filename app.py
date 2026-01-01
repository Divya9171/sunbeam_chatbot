from langchain.chat_models import init_chat_model
import streamlit as st
from langchain.agents import create_agent
from Rag_agent import prompt
from rag_tools.retriever_tool import retrieve_context
from rag_tools.answer_tool import answer_question_tool

st.set_page_config(page_title="Website Chatbot")
st.title("Sunbeam Chatbot", text_alignment="center")


llm = init_chat_model(
    model="openai/gpt-oss-20b",
    model_provider="openai",
    api_key="dummy",
    base_url="http://127.0.0.1:1234/v1"
)

prompt.llm = llm

agent = create_agent(
    model=llm,
    tools=[retrieve_context, answer_question_tool],
    system_prompt="""
        You are a helpful AI assistant.
        Use retrieve_context to answer questions from the documents.
        Never say no, just try to generate answer form given context.
        """
)


if "messages" not in st.session_state:
    st.session_state.messages = []

user_query = st.chat_input("Ask about the website")

if user_query:
    with st.chat_message("user"):
        st.write(user_query)
 
    result = agent.invoke({
        "messages" : [
            {"role": "user", "content": user_query}
        ]
    })
    
    # response = agent.run(user_query)

    with st.chat_message("assistant"):
        st.write(result["messages"][-1].content)

for q, a in st.session_state.messages:
    st.chat_message("user").write(q)
    st.chat_message("assistant").write(a)

