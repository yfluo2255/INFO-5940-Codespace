
---

## ref-log.md

```markdown
# 🧾 Reference Log (ref-log.md)

This document records external tools, libraries, and GenAI usage for the **RAG Chat Agent**.

---

## 1) GenAI Usage

| Tool / Model | When / Where | Purpose | Rationale |
| --- | --- | --- | --- |
| **ChatGPT (GPT-5)** | During development | Code review, debugging tips, UI copy, README/ref-log drafting | Speed up non-core tasks; final logic implemented and verified by author |
| **OpenAI GPT-4o (Cornell Gateway)** | At runtime (app) | Conversational answer generation | High-quality responses grounded in retrieved context |
| **text-embedding-3-large** | At runtime (app) | Create document embeddings for Chroma | Better semantic retrieval quality |

> Notes: GenAI assistance did not generate assignment content; it helped with refactoring and documentation. All source code was validated and integrated by the author.

---

## 2) External Libraries & Tools

- **Streamlit** — UI and chat components  
- **LangChain** (`langchain`, `langchain-openai`, `langchain-chroma`, `langchain-text-splitters`)  
- **ChromaDB** — vector store  
- **pypdf / PyPDF2** — PDF parsing fallback  
- **tiktoken** — tokenizer support  
- **Python stdlib** — `os`, `typing`, etc.  
- **Cornell AI Gateway** — OpenAI-compatible endpoint

---

## 3) Documentation / References

- LangChain Python Docs — https://python.langchain.com/  
- ChromaDB Docs — https://docs.trychroma.com/  
- Streamlit Docs — https://docs.streamlit.io/  
- INFO 5940 course repo (assignment1 template and examples)  

---

## 4) Implementation Notes

- **Question Condensation**: rewrite follow-up queries with chat history to improve retrieval recall.  
- **History Injection**: last 6 turns are included in generation to support multi-turn conversation.  
- **Citations**: filenames + (optional) page numbers deduplicated before display.  
- **Hero Card**: dynamic UI showing collection, persist dir, and indexed chunk count.  
- **Compatibility**: dependencies pinned to **LangChain 0.3** to avoid conflicts with `langgraph-prebuilt`.

---

📅 Last updated: 2025-11  
👤 Author: Yifei Luo
