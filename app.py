"""Project DELAWARE — the game's website, built with Streamlit.

Run locally:   streamlit run app.py
Edit content:  content/*.toml, content/chronicle/*.md, content/devlog/*.md, images in static/shots/
"""
import streamlit as st

from lib import ui

st.set_page_config(
    page_title="Project DELAWARE",
    page_icon="static/brand/Symbol.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)
ui.inject_css()

pages = [
    st.Page("views/home.py", title="Home", default=True),
    st.Page("views/world.py", title="The World", url_path="world"),
    st.Page("views/chronicle.py", title="Chronicle", url_path="chronicle"),
    st.Page("views/media.py", title="Media", url_path="media"),
    st.Page("views/devlog.py", title="Devlog", url_path="devlog"),
    st.Page("views/download.py", title="Download", url_path="download"),
    st.Page("views/support.py", title="Support", url_path="support"),
]
st.logo("static/brand/GameWordmark.png", size="large", icon_image="static/brand/Symbol.png")
st.navigation(pages, position="top").run()
ui.footer()
