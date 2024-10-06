import base64
import time
from typing import List

import streamlit as st
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from prompts.intro_messages_rising_temperatures import intro_messages
from prompts.system_message import SYSTEM_MESSAGE
from utils.css_fixes import apply_css_fixes
from utils.images import img_to_html
from utils.llm import simpleLLM


def autoplay_audio(file_path: str):
    print(f"autoplay_audio function called at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
    if not st.session_state["intro_shown"]:
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio autoplay="true" loop="false" style="display:none;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(
                md,
                unsafe_allow_html=True,
            )

def nuke_autoplay():
    md = """
        <audio autoplay="false" style="display:none;">
        </audio>
        """
    st.markdown(
        md,
        unsafe_allow_html=True,
    )
    print("Autoplay has been nuked.")


def char_streamer(text, delay=0.048):
    for char in text:
        if char == "&":
            time.sleep(delay * 20)
        else:
            yield char
            time.sleep(delay)


st.set_page_config(
    page_title="Increase in Global Temperature", initial_sidebar_state="collapsed",
)
apply_css_fixes()
load_dotenv()


introductory_messages = [
    {"role": "assistant", "content": message} for message in intro_messages
]

###### CONFIGURE SESSION_STATE
if "embeddings_client" not in st.session_state:
    st.session_state["embeddings_client"] = OpenAIEmbeddings(
        model="text-embedding-3-large",
    )
if "qdrant_client" not in st.session_state:
    st.session_state["qdrant_client"] = QdrantClient(host="localhost", port=6333)
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.extend(introductory_messages)
    st.session_state["intro_shown"] = False
st.session_state["collection_to_ask"] = "aumento_temperatura"

if not st.session_state["intro_shown"]:
    autoplay_audio("static/audio_intro_rising_temperatures.mp3")

vector_store = QdrantVectorStore(
    client=st.session_state["qdrant_client"],
    collection_name=st.session_state["collection_to_ask"],
    embedding=st.session_state["embeddings_client"],
)

llm = simpleLLM()

st.title("Increase in Global Temperature")

# Display chat messages from history on app rerun
for idx, message in enumerate(st.session_state.messages):
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
                    f"[[[{filename}]]]", image_html,
                )

            if idx < len(introductory_messages) and not st.session_state["intro_shown"]:
                st.write_stream(char_streamer(message_to_show))
                time.sleep(1)
                if idx == len(introductory_messages) - 1:
                    st.session_state["intro_shown"] = True
                    nuke_autoplay()
            else:
                st.markdown(message_to_show, unsafe_allow_html=True)

# React to user input
if prompt := st.chat_input("Escribe tu mensaje"):
    # Display user message in chat message container with user avatar
    st.chat_message("user", avatar="static/user50x50.png").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Loading data..."):
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

            message_placeholder.markdown(full_response + "🌎")

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
