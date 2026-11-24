import streamlit as st

from lib import content as C
from lib import ui

S = C.site()
M = C.media()
W = C.world()
meta = S["site"]
dl = S["download"]

available = dl.get("status") == "available" and C.has(dl.get("url", ""))
ui.hero(
    "road_gantry.jpg",
    meta["tagline"],
    meta["pitch"],
    [
        ("Download the demo" if available else "Demo coming soon", "download", "primary"),
        ("Read the Chronicle", "chronicle", ""),
        ("Watch & see", "media", ""),
    ],
    zoom=1.45,
    origin="0% 38%",
)

# ---- the trailer ----
ui.section("First look", "The long road", "A survival shooter that plays like a soulslike: every fight can kill you, every boss was a person, and the night belongs to them.")
trailers = M.get("trailers", [])
first = next((t for t in trailers if C.has(t.get("url", ""))), None)
if first:
    st.video(first["url"])
    st.caption(first["title"])
else:
    t = trailers[0] if trailers else {"title": "Trailer", "note": "In production.", "still": "cine_convoy.jpg"}
    ui.video_placeholder(t.get("still", "cine_convoy.jpg"), t["title"], t.get("note", "Coming soon."))

# ---- what it is ----
ui.section("The game", "What waits on the road")
ui.cards([
    {"tag": "Combat", "title": "Every fight can kill you", "image": "firefight.jpg",
     "body": "Third-person gunfights that punish mistakes. Use cover, read the flank, and know there are few Waylights between you and the next safe fire."},
    {"tag": "Apexes", "title": "Every boss was a person", "image": "cine_heretic.jpg", "tone": "teal",
     "body": "Each region is held by an apex that remembers who it was. Learn its life on the way in. End it anyway."},
    {"tag": "Night", "title": "The dark belongs to them", "image": "night_infected.jpg", "tone": "teal",
     "body": "Nights are truly dark and the hives grow bolder. Your lantern lights a few metres of road. Choose when to walk."},
    {"tag": "Operatives", "title": "Two operatives, one road", "image": "strain_rend.jpg", "tone": "ember",
     "body": "Play Marcus, the infected man who kept his mind, or Sarah, half rebuilt by LANTERN. The other talks you through it on the LINK."},
    {"tag": "The team", "title": "A team worth keeping", "image": "convoy_smoke.jpg",
     "body": "Four companions, each with a signature weapon and a special. Take one with you, or walk alone."},
    {"tag": "Story", "title": "Told like a soulslike", "image": "pass_aerial.jpg",
     "body": "Few cutscenes, each one essential. The rest is in the world: notes, tallies on the walls, and the bodies where they fell."},
], min_width=300)

# ---- the demo ----
ui.section("The demo", "Three regions, free", "The demo covers the first leg of the road, north from the Cajon Pass into Nevada.")
regions = []
for r in W.get("regions", []):
    regions.append({"tag": f"Region {r['no']}", "title": r["title"], "body": r["body"],
                    "image": r.get("image", ""), "locked": r.get("locked", False)})
ui.cards(regions, min_width=300)

# ---- screens ----
ui.section("Screens", "From the road")
shots = ["pass_aerial.jpg", "horde.jpg", "cine_baptized.jpg", "veil_day.jpg"]
ui.html('<div class="dl-strip">' + "".join(f'<a href="media" target="_self"><img src="{C.static_url("shots/" + f)}" alt=""></a>' for f in shots) + "</div>")
st.page_link("views/media.py", label="All screenshots and videos", icon=":material/arrow_forward:")

# ---- band ----
ui.html(f"""
<div class="dl-band">
  <p class="dl-kicker">Made by one developer</p>
  <h2 class="dl-h">{ui.esc(meta['motto'])}</h2>
  <p class="dl-lead">Project DELAWARE is built by a single developer at {ui.esc(meta['studio'])}, with free tools and no budget.
  If you want to help it reach the end of the road, there are a few ways to do it.</p>
  <div class="dl-btns" style="margin-top:1.2rem">
    <a class="dl-btn primary" href="support" target="_self">Support the project</a>
    <a class="dl-btn" href="devlog" target="_self">Read the devlog</a>
  </div>
</div>""")
