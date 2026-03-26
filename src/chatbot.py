import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import gradio as gr

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
google_model = os.getenv("GOOGLE_MODEL", "gemini-2.5-flash")

print ("loading vector db...")
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectordb = Chroma(
    embedding_function=embedding,
    persist_directory="vectorstore"
)


llm = ChatGoogleGenerativeAI(
    model=google_model,
    google_api_key=google_api_key,
    temperature=0.3
)

template = """Answer the question based only on the following context:

{context}

Question: {question}

Answer:"""
prompt = PromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": vectordb.as_retriever(search_kwargs={"k": 3}) | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

def chat(question, history):
    # Get relevant documents
    docs = vectordb.as_retriever(search_kwargs={"k": 3}).invoke(question)
    sources = set([doc.metadata.get("source", "unknown") for doc in docs])

    # Get answer
    try:
        answer = rag_chain.invoke(question)
    except Exception as exc:
        return (
            "I could not reach the Gemini API. "
            "Check GOOGLE_API_KEY and GOOGLE_MODEL in your .env file.\n\n"
            f"Details: {exc}"
        )
    
    answer += f"\n\n📚 Sources: {', '.join(sources)}"
    return answer

interface = gr.ChatInterface(
    fn=chat,
    title="Petroleum Engineering AI Assistant",
    description="Ask me anything about upstream petroleum engineering.",
    examples=[
        "What is enhanced oil recovery?",
        "Explain waterflooding",
        "What are the main challenges in petroleum engineering?"
    ]
)
interface.launch()