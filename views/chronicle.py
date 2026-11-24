import markdown as _md
import streamlit as st

from lib import content as C
from lib import ui

chapters = C.posts("chronicle")

ui.banner("road_north.jpg", "The Chronicle", "The story so far", "How the world ended, as the people still walking it tell it. Read it in order, or start anywhere.")

if not chapters:
    st.info("No chapters yet.")
    st.stop()

labels = [f"{c['meta'].get('number', i + 1)}. {c['meta']['title']}" for i, c in enumerate(chapters)]
if "chapter" not in st.session_state:
    st.session_state.chapter = 0
qp = st.query_params.get("ch")
if qp and qp.isdigit() and 0 < int(qp) <= len(chapters):
    st.session_state.chapter = int(qp) - 1

picked = st.pills("Chapters", labels, selection_mode="single", default=labels[st.session_state.chapter], label_visibility="collapsed")
if picked and labels.index(picked) != st.session_state.chapter:
    st.session_state.chapter = labels.index(picked)
    st.query_params["ch"] = str(st.session_state.chapter + 1)
    st.rerun()

i = st.session_state.chapter
ch = chapters[i]
meta = ch["meta"]
body_html = _md.markdown(ch["body"], extensions=["smarty"])

ui.html(f"""
<div class="dl-read">
  <div class="dl-chapter-no">CHAPTER {ui.esc(meta.get('number', i + 1))}</div>
  <h2 class="dl-chapter">{ui.esc(meta['title'])}</h2>
  <div class="dl-epigraph">{ui.esc(meta.get('epigraph', ''))}</div>
</div>""")

left, mid, right = st.columns([1, 6, 1])
with mid:
    narration = C.toml("narration.toml") if (C.CONTENT / "narration.toml").exists() else {}
    audio = C.static_path(f"audio/chronicle/{ch['slug']}.mp3")
    if audio.exists():
        secs = float(narration.get("chapters", {}).get(ch["slug"], 0))
        length = f"{int(secs // 60)}:{int(secs % 60):02d}" if secs else ""
        credit = narration.get("credit", "")
        ui.html(f"""<div class="dl-listen"><span class="dl-listen-k">Listen to this chapter</span>
<span class="dl-listen-m">{ui.esc(" · ".join(x for x in (length, credit) if x))}</span></div>""")
        st.audio(str(audio), format="audio/mpeg")
    img =f'<img class="dl-chapter-img" src="{C.static_url("shots/" + meta["image"])}" alt="">' if meta.get("image") else ""
    ui.html(f'{img}<div class="dl-read dl-prose">{body_html}</div>')

    prev_col, _, next_col = st.columns([1, 1, 1])
    if i > 0 and prev_col.button(f"← {chapters[i - 1]['meta']['title']}", width="stretch"):
        st.session_state.chapter = i - 1
        st.query_params["ch"] = str(i)
        st.rerun()
    if i < len(chapters) - 1 and next_col.button(f"{chapters[i + 1]['meta']['title']} →", width="stretch", type="primary"):
        st.session_state.chapter = i + 1
        st.query_params["ch"] = str(i + 2)
        st.rerun()
