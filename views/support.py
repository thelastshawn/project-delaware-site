import streamlit as st

from lib import content as C
from lib import ui

S = C.site()
meta = S["site"]
donate = S.get("donate", {})
links = S.get("links", {})

ui.banner("veil_night.jpg", "Support", "Keep the light on", "One developer, no budget, a very long road. Here's how to help it reach Dover.")

left, right = st.columns([3, 2], gap="large")
with left:
    ui.section("Why it matters", "Built by one person", top=False)
    st.markdown(
        f"Project DELAWARE is made by a single developer at **{meta['studio']}**: the code, the levels, the characters, the cutscenes "
        "and this site. Everything so far is built with free tools and free assets.\n\n"
        "Support doesn't buy you anything in the game, and the demo will stay free. It pays for the things one person can't do alone."
    )
    goals = S.get("goals", [])
    if goals:
        ui.section("Where support goes", "What it pays for")
        for g in goals:
            bar = ""
            if g.get("target", 0) > 0:
                pct = max(0, min(100, round(100 * g.get("raised", 0) / g["target"])))
                bar = (f'<div class="dl-bar"><i style="width:{pct}%"></i></div>'
                       f'<small>${g.get("raised", 0):,} of ${g["target"]:,} · {pct}%</small>')
            ui.html(f'<div class="dl-goal" style="margin-bottom:10px"><h4>{ui.esc(g["name"])}</h4><p>{ui.esc(g["detail"])}</p>{bar}</div>')

with right:
    ui.section("Donate", "Chip in", top=False)
    options = [("kofi", "Ko-fi", ":material/local_cafe:"), ("patreon", "Patreon", ":material/volunteer_activism:"),
               ("paypal", "PayPal", ":material/payments:"), ("github_sponsors", "GitHub Sponsors", ":material/favorite:"),
               ("buymeacoffee", "Buy Me a Coffee", ":material/coffee:")]
    shown = [(n, donate[k], i) for k, n, i in options if C.has(donate.get(k, ""))]
    if shown:
        for n, url, icon in shown:
            st.link_button(n, url, icon=icon, width="stretch", type="primary" if n == shown[0][0] else "secondary")
    else:
        ui.html('<div class="dl-note">Donations open soon. Until then, the free ways below help just as much.</div>')

    ui.section("Free ways to help", "Spread the light")
    st.markdown(
        "- **Share** the trailer or a screenshot with someone who'd like it.\n"
        "- **Play the demo** and say what broke, what bored you and what you loved.\n"
        "- **Follow** for news, so you see it when it lands."
    )
    follow = [(n, links[k]) for k, n in (("discord", "Discord"), ("youtube", "YouTube"), ("x", "X"), ("instagram", "Instagram"), ("tiktok", "TikTok"), ("itch", "itch.io")) if C.has(links.get(k, ""))]
    if follow:
        cols = st.columns(min(3, len(follow)))
        for n, (label, url) in enumerate(follow):
            cols[n % len(cols)].link_button(label, url, width="stretch")
