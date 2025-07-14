from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq  # Groq-hosted LLMs
from dotenv import load_dotenv
import os

# Load environment variables (for GROQ_API_KEY and others)
load_dotenv()

# ---- Configuration ----
PERSIST_DIRECTORY = os.getenv("CHROMA_DB_DIR", "./chroma_store")
embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
groq_api_key = os.getenv("GROQ_API_KEY")

# ---- Initialize Embeddings (Free from Hugging Face) ----
embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name)

# ---- Initialize Free LLM (Groq-hosted Mistral 7B) ----
chat_model = ChatGroq(
    groq_api_key=groq_api_key,
        model_name="llama3-70b-8192"
  # or mistral-7b, llama3-8b
)

vectorstore = None  # Global store (used for persistence)


# ---- Function to Ingest PDF and Build Vector Store ----
def ingest_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20
    )
    chunks = splitter.split_documents(docs)

    global vectorstore
    vectorstore = Chroma.from_documents(
        chunks,
        embedding_model,
        persist_directory=PERSIST_DIRECTORY
    )


# ---- Function to Answer Questions using RAG ----
def answer_question(question):
    global vectorstore

    try:
        if not vectorstore:
            vectorstore = Chroma(
                persist_directory=PERSIST_DIRECTORY,
                embedding_function=embedding_model
            )

        retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 2}
        )

        docs = retriever.invoke(question)  # ✅ New way

        context = "\n".join([doc.page_content for doc in docs])

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an assistant answering questions based only on uploaded documents."),
            ("human", "Question: {question}\nContext: {context}")
        ])

        chain = prompt | chat_model | StrOutputParser()
        return chain.invoke({"question": question, "context": context})
    
    except Exception as e:
        print("❌ Error in answer_question:", e)
        raise  # This will help Flask return the error with 500
