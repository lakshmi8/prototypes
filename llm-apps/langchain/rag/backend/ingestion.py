from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter


def ingest_docs(file_path):
    print("Ingesting documents....")

    # Load the pdf document
    pdf_loader = PyPDFLoader(file_path)
    document = pdf_loader.load()

    # Split the document into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50, separator='\n')
    text_chunks = text_splitter.split_documents(document)
    print(f"We have split the document into {len(text_chunks)} chunks")

    # Initialize embeddings & vector store
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma(collection_name="pdf_documents", embedding_function=embeddings)

    # Load chunks into the vector store
    for chunk in text_chunks:
        vector_store.add_texts(chunk.page_content, [chunk.metadata])
