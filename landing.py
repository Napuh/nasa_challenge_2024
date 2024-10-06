import time

import streamlit as st

from utils.css_fixes import apply_css_fixes

st.set_page_config(
    page_title="GA.IA - Climate AI", initial_sidebar_state="collapsed", layout="wide"
)
apply_css_fixes()

# Apply custom CSS to remove padding
st.markdown(
    """
    <style>
    .st-emotion-cache-1jicfl2 {
        padding: 0;
    }
    st-emotion-cache-1pl1zkm {
        padding: 0;
        display: none;
        width: 0;
        height: 0;
    }
    e1f1d6gn2 {
        padding: 0;
        display: none;
        width: 0;
        height: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.video("static/landing.mp4", autoplay=True, muted=True, loop=False)

time.sleep(12)
st.switch_page("pages/main.py")
