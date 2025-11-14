import os
import streamlit as st
from typing import List

from os import environ
if not environ.get("OPENAI_API_KEY"):
    environ["OPENAI_API_KEY"] = os.environ.get("API_KEY", "")
if not environ.get("OPENAI_BASE_URL"):
    environ["OPENAI_BASE_URL"] = "https://api.ai.it.cornell.edu"

# LangChain model
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

# set up the Streamlit UI
st.set_page_config(page_title="📄 RAG Chat", page_icon="💬")
st.title("💬 Retrieval Augmented Generation Chat Agent with Documents")

PERSIST_DIR = "./chroma_db"
COLLECTION = "docs"



def render_hero():
    
    chunks = 0
    collection_name = "docs"
    persist_dir = "./chroma_db"

    
    try:
        if "vs" in st.session_state and st.session_state["vs"] is not None:
            chunks = st.session_state["vs"]._collection.count()
        if "COLLECTION" in globals():
            collection_name = COLLECTION
        if "PERSIST_DIR" in globals():
            persist_dir = PERSIST_DIR
    except Exception:
        pass

    
    st.markdown(
        f"""
        <div style="
            background:linear-gradient(180deg,#f8fafc,#ffffff);
            border-radius:16px;
            padding:20px 28px;
            margin-top:8px;
            margin-bottom:20px;
            border:1px solid #e5e7eb;
        ">
            <h3 style="color:#1f2937; margin:0 0 6px;">🔎 RAG Chat — Docs Assistant</h3>
            <p style="color:#374151; font-size:15.5px; line-height:1.65; margin:6px 0 10px;">
                Upload <b>.txt</b> or <b>.pdf</b> files and ask questions about them.
                We chunk, embed, and retrieve with <b>LangChain</b> + <b>ChromaDB</b>,
                and generate answers using the <b>Cornell AI Gateway</b>.
            </p>
            <ul style="color:#334155; font-size:15px; line-height:1.6; margin:0 0 8px 18px;">
                <li>📤 Multiple file uploads (.txt & .pdf)</li>
                <li>🧩 Chunking 1000 / overlap 200 • semantic search (k=4)</li>
                <li>📝 Source citations (filename:page)</li>
            </ul>
            <div style="margin-top:6px; font-size:13px; color:#6b7280;">
                Collection: <code>{collection_name}</code> • Persist dir: <code>{persist_dir}</code> • Indexed chunks: <b>{chunks}</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
render_hero()

def get_vectorstore() -> Chroma:
    if "vs" not in st.session_state:
        embeddings = OpenAIEmbeddings(
            model="openai.text-embedding-3-large",
            openai_api_key=environ["OPENAI_API_KEY"],
            openai_api_base=environ["OPENAI_BASE_URL"],
        )
        st.session_state["vs"] = Chroma(
            collection_name=COLLECTION,
            embedding_function=embeddings,
            persist_directory=PERSIST_DIR,
        )
    return st.session_state["vs"]

# read txt file
def read_txt(f) -> Document:
    text = f.read().decode("utf-8", errors="ignore")
    return Document(page_content=text, metadata={"source": f.name})

# read pdf file
def read_pdf(f) -> List[Document]:
    try:
        from pypdf import PdfReader
    except Exception:
        from PyPDF2 import PdfReader
    reader = PdfReader(f)
    out: List[Document] = []
    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        out.append(Document(page_content=text, metadata={"source": f.name, "page": i+1}))
    return out

def split_docs(docs: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(docs)

# upload multiple files including txt and pdf
uploaded_files = st.file_uploader(
    "Upload documents (.txt / .pdf)",
    type=["txt", "pdf"],
    accept_multiple_files=True,
)

if uploaded_files:
    raw_docs: List[Document] = []
    for f in uploaded_files:
        name = f.name.lower()
        if name.endswith(".txt"):
            raw_docs.append(read_txt(f))
        else:
            raw_docs.extend(read_pdf(f))

    chunks = split_docs(raw_docs)
    vs = get_vectorstore()
    if chunks:
        vs.add_documents(chunks)
        st.success(f"Indexed {len(uploaded_files)} files, {len(chunks)} chunks created.")

# remember the chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Upload .txt/.pdf and ask a question!"}
    ]

for m in st.session_state["messages"]:
    st.chat_message(m["role"]).write(m["content"])

# LLM initialization
llm = ChatOpenAI(
    model="openai.gpt-4o",
    temperature=0.2,
    openai_api_key=environ["OPENAI_API_KEY"],
    openai_api_base=environ["OPENAI_BASE_URL"],
)

# build context
def build_context(docs: List[Document]) -> str:
    return "\n\n".join(d.page_content for d in docs)

def lc_history_from_streamlit(history: List[dict]) -> List:
    out = []
    for m in history:
        role = m.get("role")
        content = m.get("content", "")
        if role == "user":
            out.append(HumanMessage(content=content))
        elif role == "assistant":
            out.append(AIMessage(content=content))
    return out

# user input 
# =========================
user_q = st.chat_input("Ask your question…")
if user_q:
    
    st.session_state["messages"].append({"role": "user", "content": user_q})
    st.chat_message("user").write(user_q)

    
    with st.chat_message("assistant"):
        try:
            
            vs = get_vectorstore()

            
            history_msgs = lc_history_from_streamlit(st.session_state["messages"])

            
            def condense_question(llm, history_msgs: list, user_q: str) -> str:
                prompt = [
                    SystemMessage(content=(
                        "You rewrite the latest user question to a standalone, fully-specified query "
                        "using the prior dialogue for context. Output only the rewritten question."
                    )),
                    *history_msgs[-6:],  
                    HumanMessage(content=f"Rewrite the user's latest question to a standalone query:\n\n{user_q}")
                ]
                return llm.invoke(prompt).content.strip()

            condensed_q = condense_question(llm, history_msgs, user_q)

            
            retrieved = vs.as_retriever(search_kwargs={"k": 4}).invoke(condensed_q)
            if not retrieved:
                msg = "I don't know based on the provided documents."
                st.write(msg)
                st.session_state["messages"].append({"role": "assistant", "content": msg})
                st.stop()

            
            context = build_context(retrieved)

            
            sys = SystemMessage(
                content=(
                    "You are a helpful assistant for RAG. "
                    "Answer ONLY using the provided document context. "
                    "If the answer is not in the context, say you don't know."
                )
            )
            usr = HumanMessage(content=f"Question: {user_q}\n\nContext:\n{context}")
            messages = [sys] + history_msgs[-6:] + [usr]

            result = llm.invoke(messages)
            answer = result.content

            
            cites = []
            for d in retrieved:
                src = d.metadata.get("source", "")
                page = d.metadata.get("page")
                cites.append(f"{src}" + (f":p{page}" if page else ""))
            cites = "; ".join(dict.fromkeys(cites))
            answer += f"\n\nSources: {cites}"

            
            st.write(answer)
            st.session_state["messages"].append({"role": "assistant", "content": answer})

        except Exception as e:
            st.error(f"Error: {e}")
