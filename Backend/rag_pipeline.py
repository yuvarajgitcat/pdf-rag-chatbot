from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma  
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
chat_model = ChatOpenAI(model_name="gpt-4", temperature=0)
vectorstore = None
PERSIST_DIRECTORY = os.getenv("CHROMA_DB_DIR")

def ingest_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    chunks = splitter.split_documents(docs)
    global vectorstore
    vectorstore = Chroma.from_documents(chunks, embedding_model, persist_directory=PERSIST_DIRECTORY)

def answer_question(question):
    global vectorstore
    if not vectorstore:
        vectorstore = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embedding_model)
    retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 2})
    docs = retriever.get_relevant_documents(question)
    context = "\n".join([doc.page_content for doc in docs])
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an assistant answering questions based on uploaded documents."),
        ("human", "Question: {question}\nContext: {context}")
    ])
    chain = prompt | chat_model | StrOutputParser()
    return chain.invoke({"question": question, "context": context})
