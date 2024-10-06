import streamlit as st


def apply_css_fixes():
    st.markdown(
        """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
        .st-emotion-cache-w3nhqi {
            display: none
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # hide anchors
    st.markdown(
        """
        <style>
        /* Hide the link button */
        .stApp a:not([class]) {
            display: initial;
        }
        .css-15zrgzn, .st-emotion-cache-eczf16, .css-jn99sy {
            display: none;
        }
        .elnzilvr3 {
            display: none;
        }
        [data-testid="stHeaderActionElements"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
