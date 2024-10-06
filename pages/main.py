import base64
import time

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient

from prompts.intro_messages_main_page import intro_text
from utils.css_fixes import apply_css_fixes


def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true" style="display:none;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

st.set_page_config(page_title="GA.IA", initial_sidebar_state="collapsed", page_icon="🌎")

apply_css_fixes()
load_dotenv()

def char_streamer(text, delay=0.05):
    for char in text:
        if char == "&":
            time.sleep(delay*10)
        else:
            yield char
            time.sleep(delay)

###### CONFIGURE SESSION_STATE
if "embeddings_client" not in st.session_state:
    st.session_state["embeddings_client"] = OpenAIEmbeddings(model="text-embedding-3-large")
if "qdrant_client" not in st.session_state:
    st.session_state["qdrant_client"] = QdrantClient(host="localhost", port=6333)
if "collection_to_ask" not in st.session_state:
    st.session_state["collection_to_ask"] = None
if "intro_shown" not in st.session_state:
    autoplay_audio("static/audio_intro_main_page.mp3")
    st.session_state["intro_shown"] = False

if not st.session_state["intro_shown"]:
    st.write_stream(char_streamer("# **GA.IA**", delay=0.1))  # Slower delay for GAIA title
    st.write_stream(char_streamer(intro_text))
    st.session_state["intro_shown"] = True
else:
    st.write("# **GA.IA**")
    st.write(intro_text.replace("&", ""))

st.link_button(label="Access CO₂ Concentrations Data", url="https://earth.gov/ghgcenter/data-catalog/noaa-gggrn-co2-concentrations")

if not st.session_state["intro_shown"]:
    time.sleep(2)



if not st.session_state["intro_shown"]:
    st.write_stream(char_streamer("## What do you want to learn about?", delay=0.015))
else:
    st.write("## What do you want to learn about?")

container_temperature = st.container(border=True)

with container_temperature:
    col1, col2 = st.columns([3, 6])
    col1.image("static/rising_temperatures.jpg", width=200)
    col2.markdown("## Increase in Global Temperature")
    col2.markdown("Explore the impacts of rising global temperatures.")
    if st.button("Go to chat", use_container_width=True, key="temperature"):
        st.switch_page(page="pages/increase_in_global_temperature.py")


container_drought = st.container(border=True)

with container_drought:
    col1, col2 = st.columns([3, 6])
    col1.image("static/drought.jpeg", width=200)
    col2.markdown("## Drought")
    col2.markdown("Learn about the causes and effects of droughts.")
    if st.button("Go to chat", use_container_width=True, key="drought"):
        st.switch_page(page="pages/drought.py")


container_wildfires = st.container(border=True)

with container_wildfires:
    col1, col2 = st.columns([3, 6])
    col1.image("static/wildfire.jpg", width=200)
    col2.markdown("## Wildfires")
    col2.markdown("Understand the impact of wildfires on the environment.")
    if st.button("Go to chat", use_container_width=True, key="wildfires"):
        st.switch_page(page="pages/wildfires.py")


container_rainstorms = st.container(border=True)

with container_rainstorms:
    col1, col2 = st.columns([3, 6])
    col1.image("static/rainstorm.jpg", width=200)
    col2.markdown("## Tropical Rainstorms")
    col2.markdown("Discover the effects of tropical rainstorms.")
    if st.button("Go to chat", use_container_width=True, key="rainstorms"):
        st.switch_page(page="pages/tropical_rainstorms.py")


container_sea_level = st.container(border=True)

with container_sea_level:
    col1, col2 = st.columns([3, 6])
    col1.image("static/sea_level.jpg", width=200)
    col2.markdown("## Rising Sea Level")
    col2.markdown("Examine the consequences of rising sea levels.")
    if st.button("Go to chat", use_container_width=True, key="sea_level"):
        st.switch_page(page="pages/rising_sea_level.py")
