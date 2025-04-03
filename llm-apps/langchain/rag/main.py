import streamlit as st
import os
from typing import Set

from backend.ingestion import ingest_docs
from backend.rag import ask_llm

if "user_prompt_history" not in st.session_state:
    st.session_state.user_prompt_history = []

if "llm_answers_history" not in st.session_state:
    st.session_state.llm_answers_history = []

if  "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def landing_page():
    # Set the initial contents of the landing page
    st.title("Chat with your PDF")
    st.write("This app uses the OpenAI model to let you chat with the contents of your PDF")
    st.write("Upload a PDF file to get started")

    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Create temp directory if it doesn't exist
        os.makedirs("./temp", exist_ok=True)

        # Save the uploaded file to a temporary location
        temp_file_path = f"./temp/{uploaded_file.name}"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Save file path to session_state for later use
        st.session_state.file_path = temp_file_path

        # Chat button
        if st.button("Chat"):
            st.session_state.page = "chat"
            st.rerun()

def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "Sources: \n"
    for source in sources_list:
        sources_string += f"- {source}\n"
    return sources_string


def chat_page():
    # Set the initial contents of the chat page
    st.title("Chat with your PDF")

    # Chat logic goes here
    user_prompt = st.text_input("User question", placeholder="Enter your question here")
    if user_prompt is not None:
        with st.spinner("Thinking...."):
            llm_response = ask_llm(user_prompt, chat_history=st.session_state.chat_history)
            sources = set([doc.metadata["source"] for doc in llm_response["source_documents"]])

            formatted_response = f"Answer: {llm_response['result']}\n\n  {create_sources_string(sources)}"
            st.session_state.user_prompt_history.append(user_prompt)
            st.session_state.llm_answers_history.append(formatted_response)
            st.session_state.chat_history.append(("human", user_prompt))
            st.session_state.chat_history.append(("ai", llm_response["result"]))

    if st.session_state.llm_answers_history:
        for user_query, llm_response in zip(st.session_state.user_prompt_history, st.session_state.llm_answers_history):
            st.chat_message(user_query)
            st.chat_message(llm_response)

    # Back button
    if st.button("Back"):
        st.session_state.page = "landing"
        st.rerun()

def main():
    # Page configuration
    st.set_page_config(page_title="Chat with your PDF", layout="centered")

    # Initialize session state for navigation
    if "page" not in st.session_state:
        st.session_state.page = "landing"

    # Navigation logic
    if st.session_state.page == "landing":
        landing_page()
    elif st.session_state.page == "chat":
        ingest_docs(st.session_state.file_path)
        st.write("Documents ingested.")
        chat_page()

if __name__ == '__main__':
    main()