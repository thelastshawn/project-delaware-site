import streamlit as st

from lib import content as C
from lib import ui

M = C.media()

ui.banner("cine_baptized.jpg", "Media", "Trailers, gameplay & screens", "Everything here is captured in the engine from a game in development.")

tab_tr, tab_gp, tab_sc, tab_kit = st.tabs(["Trailers", "Gameplay", "Screenshots", "Press kit"])


def video_grid(items: list[dict]) -> None:
    if not items:
        st.info("Nothing here yet.")
        return
    cols = st.columns(2)
    for n, v in enumerate(items):
        with cols[n % 2]:
            if C.has(v.get("url", "")):
                st.video(v["url"])
            else:
                ui.video_placeholder(v.get("still", "cine_convoy.jpg"), v["title"], v.get("note", "Coming soon."))
            ui.html(f'<p class="dl-kicker" style="margin-top:.6rem">{ui.esc(v["title"])}</p>'
                    f'<p style="color:var(--muted);margin:0 0 1.4rem 0">{ui.esc(v.get("note", ""))}</p>')


with tab_tr:
    video_grid(M.get("trailers", []))

with tab_gp:
    video_grid(M.get("gameplay", []))

with tab_sc:
    shots = M.get("screenshots", [])
    cats = ["All"] + sorted({s.get("category", "Other") for s in shots})
    pick = st.segmented_control("Filter", cats, default="All", label_visibility="collapsed")
    shown = [s for s in shots if pick in (None, "All") or s.get("category") == pick]
    cols = st.columns(3)
    for n, s in enumerate(shown):
        with cols[n % 3]:
            p = C.static_path("shots/" + s["file"])
            if p.exists():
                st.image(str(p), caption=s.get("caption", ""), width="stretch")
    st.caption("Hover over a screenshot and use the expand button to see it full size.")

with tab_kit:
    ui.section("For press and creators", "Press kit", "Logos and key art you're free to use when writing or making videos about the game.", top=False)
    kit = [("Wordmark (PNG, transparent)", "brand/GameWordmark.png"),
           ("Lockup (PNG, transparent)", "brand/GameLockup.png"),
           ("Symbol (PNG, transparent)", "brand/Symbol.png"),
           ("Key art: the Cajon Pass", "shots/road_gantry.jpg"),
           ("Key art: the Heretic", "shots/cine_heretic.jpg")]
    tiles = "".join(f'<div><img class="{"cover" if rel.startswith("shots/") else ""}" src="{C.static_url(rel)}" alt=""></div>' for _, rel in kit)
    ui.html(f'<div class="dl-kit-grid">{tiles}</div>')
    cols = st.columns(len(kit))
    for c, (label, rel) in zip(cols, kit):
        p = C.static_path(rel)
        c.download_button(label, data=p.read_bytes(), file_name=p.name, width="stretch", key="kit_" + p.name)
    meta = C.site()["site"]
    st.markdown(f"**{meta['title']}** · developer and publisher: {meta['studio']} · platform: Windows · price: free demo")
