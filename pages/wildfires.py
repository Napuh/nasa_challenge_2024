from typing import List

import streamlit as st
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from prompts.system_message import SYSTEM_MESSAGE
from utils.css_fixes import apply_css_fixes
from utils.images import img_to_html
from utils.llm import simpleLLM

st.set_page_config(page_title="Wildfire Chatbot", initial_sidebar_state="collapsed")
apply_css_fixes()
load_dotenv()

###### CONFIGURE SESSION_STATE
if "embeddings_client" not in st.session_state:
    st.session_state["embeddings_client"] = OpenAIEmbeddings(
        model="text-embedding-3-large"
    )
if "qdrant_client" not in st.session_state:
    st.session_state["qdrant_client"] = QdrantClient(host="localhost", port=6333)
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
st.session_state["collection_to_ask"] = "wildfires"

vector_store = QdrantVectorStore(
    client=st.session_state["qdrant_client"],
    collection_name=st.session_state["collection_to_ask"],
    embedding=st.session_state["embeddings_client"],
)

llm = simpleLLM()

st.title("Wildfire Chatbot")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(
        message["role"],
        avatar="static/user50x50.png"
        if message["role"] == "user"
        else "static/NASA50x50.png",
    ):
        if "image" in message["role"]:
            st.image(message["content"])
        else:
            message_to_show = message["content"]
            # modify here message_to_show to render the images with img_to_html
            if "[[[" in message_to_show and "]]]" in message_to_show:
                start_idx = message_to_show.find("[[[") + 3
                end_idx = message_to_show.find("]]]")
                filename = message_to_show[start_idx:end_idx].strip()
                image_html = f"\n{img_to_html(f'static/{filename}')}\n"
                message_to_show = message_to_show.replace(
                    f"[[[{filename}]]]", image_html
                )

            st.markdown(message_to_show, unsafe_allow_html=True)

# React to user input
if prompt := st.chat_input("Escribe tu mensaje"):
    # Display user message in chat message container with user avatar
    st.chat_message("user", avatar="static/user50x50.png").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Cargando datos..."):
        results: List[Document] = vector_store.similarity_search(prompt, k=12)

        context = ""
        for result in results:
            context += f"{result.metadata['source']}, page {result.metadata['page']}: {result.page_content}\n"

        user_message_with_context = (
            f"USER QUESTION: {prompt}\nRELATED CONTEXT: {context}"
        )

    # Generate response using simpleLLM
    assistant_message = st.chat_message("assistant", avatar="static/NASA50x50.png")
    with assistant_message:
        message_placeholder = st.empty()

        full_response = ""
        for response in llm.generate_completion(
            system_message=SYSTEM_MESSAGE,
            messages=[{"role": "user", "content": user_message_with_context}],
            streaming=True,
        ):
            full_response += response or ""

            message_placeholder.markdown(
                full_response + "🌎",
            )

        message_to_show = full_response
        # modify here message_to_show to render the images with img_to_html
        start_idx = message_to_show.find("[[[")
        end_idx = message_to_show.find("]]]")

        while start_idx != -1 and end_idx != -1:
            filename = message_to_show[start_idx + 3 : end_idx].strip()
            image_html = f"<br>{img_to_html(f'static/{filename}')}<br>"
            message_to_show = message_to_show.replace(f"[[[{filename}]]]", image_html)

            start_idx = message_to_show.find("[[[", end_idx)
            end_idx = message_to_show.find("]]]", start_idx)

        message_placeholder.markdown(message_to_show, unsafe_allow_html=True)

    # Display assistant response in chat message container
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
