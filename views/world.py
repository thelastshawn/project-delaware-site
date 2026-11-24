import streamlit as st

from lib import content as C
from lib import ui

W = C.world()

ui.banner("pass_aerial.jpg", "The world", "Five years after", "The American West in November 2032: a sky that never clears, roads nobody drives, and the lights LANTERN keeps burning.")

tab_world, tab_ops, tab_team, tab_others, tab_road = st.tabs(["The world", "The operatives", "The team", "On the road", "The regions"])

with tab_world:
    ui.section("What happened", "The fall", top=False)
    ui.cards([{"tag": s["tag"], "title": s["title"], "body": s["body"], "image": s.get("image"), "tone": s.get("tone", "")}
              for s in W.get("setting", [])], min_width=330)
    ui.section("LANTERN's language", "Words you'll hear on the LINK")
    gloss = "".join(f'<div><b>{ui.esc(g["term"])}</b><span>{ui.esc(g["text"])}</span></div>' for g in W.get("glossary", []))
    ui.html(f'<div class="dl-gloss">{gloss}</div>')

with tab_ops:
    ui.section("Choose who walks", "The operatives", "LANTERN sends one operative east. Whoever you don't choose stays on the LINK, a relay behind, talking you through it.", top=False)
    for o in W.get("operatives", []):
        bio = "".join(f"<p>{ui.esc(p)}</p>" for p in o.get("bio", []))
        kit = "".join(f"<li>{ui.esc(k)}</li>" for k in o.get("kit", []))
        ui.html(f"""
<div class="dl-cast {o.get('tone', '')}" style="margin-bottom:14px">
  <img src="{C.static_url('cast/' + o['key'] + '.png')}" alt="{ui.esc(o['name'])}">
  <div><h3>{ui.esc(o['name'])}</h3><div class="dl-role">{ui.esc(o['role'])}</div>{bio}<ul>{kit}</ul></div>
</div>""")

with tab_team:
    ui.section("One travels with you", "The team", "Four companions. Each carries a signature weapon with a special they use when the moment comes. Take one with you at a Waylight, or go alone.", top=False)
    minis = []
    for t in W.get("team", []):
        minis.append(f"""
<div class="dl-mini">
  <img src="{C.static_url('cast/' + t['key'] + '.png')}" alt="{ui.esc(t['name'])}">
  <h4>{ui.esc(t['name'])}</h4><div class="dl-role">{ui.esc(t['role'])}</div>
  <p>{ui.esc(t['bio'])}</p>
  <div class="dl-kit"><b>{ui.esc(t['weapon'])}</b><br>{ui.esc(t['special'])}</div>
</div>""")
    ui.html(f'<div class="dl-grid" style="--min:250px">{"".join(minis)}</div>')

with tab_others:
    ui.section("Station Four", "The people who stay", "LANTERN's station in the Cajon Pass, and the traders who live under its protection.", top=False)
    minis = []
    for t in W.get("station", []):
        minis.append(f"""
<div class="dl-mini">
  <img src="{C.static_url('cast/' + t['key'] + '.png')}" alt="{ui.esc(t['name'])}">
  <h4>{ui.esc(t['name'])}</h4><div class="dl-role">{ui.esc(t['role'])}</div>
  <p>{ui.esc(t['bio'])}</p>
</div>""")
    ui.html(f'<div class="dl-grid" style="--min:230px">{"".join(minis)}</div>')
    ui.section("Not everyone on the road is dead", "Hostiles")
    ui.cards([{"tag": f["tag"], "title": f["title"], "body": f["body"], "image": f.get("image"), "tone": f.get("tone", "")}
              for f in W.get("factions", [])], min_width=300)

with tab_road:
    ui.section("Ten regions to Dover", "The road east", "The demo covers the first three. Each region is a short story that ends with an apex, and a loss.", top=False)
    ui.cards([{"tag": f"Region {r['no']}", "title": r["title"], "body": r["body"], "image": r.get("image", ""),
               "locked": r.get("locked", False)} for r in W.get("regions", [])], min_width=300)
    st.caption("Seven more regions lie beyond Ground Zero. They are not on any map LANTERN has shared.")
