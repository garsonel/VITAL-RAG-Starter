
"""Working baseline chatbot with RAG toggle and retrieved context."""

import streamlit as st
from llm import ask_llm
from rag import retrieve, build_context

st.title("Project VITAL — LLM + RAG Lab")

# TODO 4: Add an Enable RAG toggle
enable_rag = st.toggle("Enable RAG", value=False)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Ask a question")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    try:
        if enable_rag:
            # Retrieve relevant documents
            results = retrieve(question, k=2)

            # Build context from retrieved documents
            context = build_context(results)

            # Pass context to LLM
            answer = ask_llm(question, context=context)
        else:
            # Regular LLM without RAG
            answer = ask_llm(question)

    except Exception as exc:
        answer = f"Ollama unavailable: {exc}"

    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
