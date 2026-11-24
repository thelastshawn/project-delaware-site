import streamlit as st

from lib import content as C
from lib import ui

S = C.site()
dl = S["download"]
links = S.get("links", {})
available = dl.get("status") == "available" and C.has(dl.get("url", ""))

ui.banner("convoy_smoke.jpg", "Download", "The free demo", "Regions I to III of the long road. Free, for Windows.")

left, right = st.columns([3, 2], gap="large")
with left:
    ui.html(ui.status_pill("Available now" if available else "In development", live=available))
    ui.html(f'<h2 class="dl-h" style="margin-top:.8rem">{ui.esc(dl.get("version", "Demo"))}</h2>')
    if available:
        size = f" · {dl['size']}" if C.has(dl.get("size", "")) else ""
        st.link_button(f"{dl.get('url_label', 'Download')}{size}", dl["url"], type="primary", icon=":material/download:")
        if C.has(dl.get("mirror_url", "")):
            st.link_button(dl.get("mirror_label", "Mirror"), dl["mirror_url"], icon=":material/cloud_download:")
        if C.has(dl.get("sha256", "")):
            st.caption(f"SHA-256: `{dl['sha256']}`")
    else:
        st.markdown(f"The demo isn't out yet. Release: **{dl.get('release_window', 'to be announced')}**.")
        follow = [(n, links[k]) for k, n in (("discord", "Join the Discord"), ("youtube", "Follow on YouTube"), ("itch", "Follow on itch.io"), ("x", "Follow on X")) if C.has(links.get(k, ""))]
        if follow:
            st.markdown("Get told the day it lands:")
            cols = st.columns(len(follow))
            for c, (label, url) in zip(cols, follow):
                c.link_button(label, url, width="stretch")
        st.button("Download (coming soon)", disabled=True, icon=":material/download:")

    st.subheader("What's in it")
    st.markdown((C.CONTENT / "patch_notes.md").read_text(encoding="utf-8"))

with right:
    st.subheader("System requirements")
    ui.html(f"""
<table class="dl-spec">
  <tr><th>OS</th><td>{ui.esc(dl.get('platform', 'Windows 10 / 11 (64-bit)'))}</td></tr>
  <tr><th>Graphics</th><td>NVIDIA RTX 3050 Ti or better<br><span style="color:var(--dim)">Target: 60 fps on High</span></td></tr>
  <tr><th>Memory</th><td>To be confirmed</td></tr>
  <tr><th>Storage</th><td>{ui.esc(dl['size']) if C.has(dl.get('size', '')) else 'To be confirmed'}</td></tr>
  <tr><th>Input</th><td>Keyboard &amp; mouse or gamepad</td></tr>
</table>""")
    st.subheader("How to install")
    st.markdown(
        "1. Download the zip and extract it anywhere, for example `C:\\Games\\Project DELAWARE`.\n"
        "2. Run **Project DELAWARE.exe**.\n"
        "3. If Windows SmartScreen warns about an unknown publisher, click **More info → Run anyway**. Indie builds aren't code-signed yet.\n"
        "4. Saves are kept between versions."
    )
    with st.expander("Questions"):
        st.markdown(
            "**Is it free?** The demo is free.\n\n"
            "**Mac or Linux?** Windows only for now.\n\n"
            "**Steam?** Not yet. The site will say when.\n\n"
            "**Found a bug?** Tell me on the Discord or by email. Every report helps."
        )
