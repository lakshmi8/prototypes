from typing import List, Dict, Any

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain import hub


def ask_llm(user_prompt, chat_history: List[Dict[str,  Any]] = []):
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o")
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma(collection_name="pdf_documents", embedding_function=embeddings)

    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    combine_docs_chain = create_stuff_documents_chain(llm=llm, prompt=retrieval_qa_chat_prompt)
    history_aware_retriever = create_history_aware_retriever(llm=llm, retriever=vector_store.as_retriever(), prompt=rephrase_prompt)

    retrieval_chain = create_retrieval_chain(retriever=history_aware_retriever, combine_docs_chain=combine_docs_chain)
    result = retrieval_chain.invoke(input={"input": user_prompt, "chat_history": chat_history})
    structured_result = {
        "query": result["input"],
        "result": result["answer"],
        "source_documents": result["context"]
    }
    return structured_result