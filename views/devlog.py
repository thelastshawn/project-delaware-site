import markdown as _md
import streamlit as st

from lib import content as C
from lib import ui

posts = list(reversed(C.posts("devlog")))   # newest first (file names start with the date)

ui.banner("firefight.jpg", "Devlog", "From the workbench", "Notes from building a game alone: what changed, what broke, what's next.")

if not posts:
    st.info("No posts yet.")
    st.stop()

for n, p in enumerate(posts):
    meta = p["meta"]
    body = _md.markdown(p["body"], extensions=["smarty"])
    if n == 0:
        left, mid, right = st.columns([1, 6, 1])
        with mid:
            ui.html(f'<p class="dl-meta">{ui.esc(meta.get("date", ""))} · latest</p><h2 class="dl-h">{ui.esc(meta["title"])}</h2>')
            if meta.get("image"):
                st.image(str(C.static_path("shots/" + meta["image"])), width="stretch")
            ui.html(f'<div class="dl-post">{body}</div>')
    else:
        with st.expander(f"{meta.get('date', '')} · {meta['title']}"):
            if meta.get("summary"):
                st.caption(meta["summary"])
            ui.html(f'<div class="dl-post">{body}</div>')
