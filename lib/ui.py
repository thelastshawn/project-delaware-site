"""Look and building blocks for the Project DELAWARE site: CSS, hero, banners, cards and the footer."""
from __future__ import annotations

import html as _html

import streamlit as st

from lib import content as C

AMBER = "#E39A3B"
TEAL = "#2FE3B4"
EMBER = "#E0502A"

CSS = """
<style>
:root {
  --amber: #E39A3B; --amber-hi: #F0B45A; --teal: #2FE3B4; --ember: #E0502A;
  --bg: #0A0B0C; --panel: #121518; --panel-2: #181C20; --line: #262A2F;
  --text: #E7E1D5; --muted: #A39C90; --dim: #6F6A62;
}
[data-testid="stMainBlockContainer"] { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1280px; }
[data-testid="stHeader"] { background: rgba(10,11,12,0.92); backdrop-filter: blur(6px); border-bottom: 1px solid var(--line); }
/* top navigation: condensed caps, amber underline on the current page */
[data-testid="stTopNavLink"] p {
  font-family: 'Barlow Condensed', sans-serif; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; font-size: .92rem; }
a { text-decoration: none; }
h1, h2, h3 { letter-spacing: .02em; }
.dl-kicker { font-family: 'Barlow Condensed', sans-serif; font-weight: 600; letter-spacing: .32em; text-transform: uppercase;
  color: var(--amber); font-size: .82rem; margin: 0 0 .35rem 0; }
.dl-h { font-family: 'Barlow Condensed', sans-serif; font-weight: 700; font-size: clamp(1.9rem, 3.2vw, 2.7rem); line-height: 1.04;
  letter-spacing: .02em; text-transform: uppercase; margin: 0 0 .6rem 0; color: var(--text); }
.dl-lead { color: var(--muted); font-size: 1.08rem; line-height: 1.6; max-width: 62ch; margin: 0; }
.dl-section { margin: 3.2rem 0 1.2rem 0; }
.dl-rule { height: 1px; background: linear-gradient(90deg, var(--amber) 0, var(--line) 18%, transparent 100%); margin: 2.6rem 0 0 0; border: 0; }

/* hero */
.dl-hero { position: relative; min-height: min(76vh, 760px); border-radius: 6px; overflow: hidden; display: flex; align-items: flex-end;
  border: 1px solid var(--line); background: #0d0f10; }
.dl-hero img.dl-hero-bg { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0; }
.dl-hero::before { content: ""; position: absolute; inset: 0; z-index: 1;
  background: linear-gradient(180deg, rgba(10,11,12,.15) 0%, rgba(10,11,12,.35) 45%, rgba(10,11,12,.96) 100%),
              linear-gradient(90deg, rgba(10,11,12,.75) 0%, rgba(10,11,12,0) 60%); }
.dl-hero-inner { position: relative; z-index: 2; padding: 0 4.5vw 5.5vh 4.5vw; max-width: 760px; }
.dl-hero img.dl-wordmark { width: min(500px, 82vw); display: block; margin: 0 0 1.1rem -6px; filter: drop-shadow(0 4px 18px rgba(0,0,0,.6)); }
.dl-tagline { font-family: 'Cinzel', serif; font-weight: 600; font-size: clamp(1.15rem, 2vw, 1.6rem); letter-spacing: .18em;
  text-transform: uppercase; color: #F3E9D6; margin: 0 0 .9rem 0; text-shadow: 0 2px 12px rgba(0,0,0,.8); }
.dl-hero p.dl-body { color: #D9D2C4; font-size: 1.08rem; line-height: 1.62; margin: 0 0 1.5rem 0; max-width: 58ch; text-shadow: 0 1px 8px rgba(0,0,0,.8); }
.dl-btns { display: flex; flex-wrap: wrap; gap: .7rem; }
.dl-btn { display: inline-block; padding: .78rem 1.35rem; border-radius: 3px; font-family: 'Barlow Condensed', sans-serif; font-weight: 700;
  letter-spacing: .16em; text-transform: uppercase; font-size: .95rem; border: 1px solid var(--amber); color: var(--text) !important;
  background: rgba(10,11,12,.55); transition: background .15s, color .15s; }
.dl-btn:hover { background: rgba(227,154,59,.16); }
.dl-btn.primary { background: var(--amber); color: #120D06 !important; }
.dl-btn.primary:hover { background: var(--amber-hi); }
.dl-btn.disabled { border-color: var(--line); color: var(--dim) !important; pointer-events: none; background: transparent; }

/* page banner */
.dl-banner { position: relative; height: 34vh; min-height: 240px; max-height: 380px; border-radius: 6px; overflow: hidden; background-size: cover;
  background-position: center; background-repeat: no-repeat; border: 1px solid var(--line); display: flex; align-items: flex-end; margin-bottom: 1.4rem; }
.dl-banner::before { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(10,11,12,.1), rgba(10,11,12,.94)); }
.dl-banner > div { position: relative; padding: 0 3vw 3.2vh 3vw; }
.dl-banner .dl-h { font-size: clamp(2.2rem, 4.2vw, 3.4rem); margin: 0; }
.dl-banner .dl-lead { color: #CFC7B8; margin-top: .4rem; }

/* cards */
.dl-grid { display: grid; gap: 14px; grid-template-columns: repeat(auto-fill, minmax(var(--min, 260px), 1fr)); }
.dl-card { background: var(--panel); border: 1px solid var(--line); border-radius: 5px; overflow: hidden; display: flex; flex-direction: column; }
.dl-card .dl-card-img { aspect-ratio: 16 / 9; background-size: cover; background-position: center; background-repeat: no-repeat; border-bottom: 1px solid var(--line); }
.dl-card .dl-card-body { padding: 1rem 1.1rem 1.15rem 1.1rem; }
.dl-card h4 { font-family: 'Barlow Condensed', sans-serif; font-weight: 700; text-transform: uppercase; letter-spacing: .06em;
  font-size: 1.3rem; margin: .1rem 0 .45rem 0; color: var(--text); padding: 0; }
.dl-card p { color: var(--muted); line-height: 1.55; margin: 0; font-size: .98rem; }
.dl-card .dl-tag { font-family: 'Barlow Condensed', sans-serif; letter-spacing: .26em; text-transform: uppercase; font-size: .74rem; color: var(--amber); }
.dl-card.teal .dl-tag { color: var(--teal); }
.dl-card.ember .dl-tag { color: var(--ember); }
.dl-card.locked .dl-card-img { filter: grayscale(1) brightness(.45); }
.dl-card .dl-classified { filter: none !important; display: flex; align-items: center; justify-content: center;
  background: repeating-linear-gradient(135deg, #121417 0 14px, #16191c 14px 28px); }
.dl-card .dl-classified span { font-family: 'Barlow Condensed', sans-serif; font-weight: 700; letter-spacing: .4em; text-transform: uppercase;
  color: #5a554d; border: 2px solid #3a3630; padding: .35rem .9rem .35rem 1.3rem; transform: rotate(-6deg); font-size: 1.05rem; }
.dl-strip { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.dl-strip a { display: block; aspect-ratio: 16 / 9; border-radius: 4px; overflow: hidden; border: 1px solid var(--line); }
.dl-strip img { width: 100%; height: 100%; object-fit: cover; transition: transform .4s; }
.dl-strip a:hover img { transform: scale(1.04); }
@media (max-width: 760px) { .dl-strip { grid-template-columns: repeat(2, 1fr); } }
.dl-num { font-family: 'Cinzel', serif; color: var(--amber); font-size: 1.05rem; letter-spacing: .1em; }

/* cast */
.dl-cast { display: grid; grid-template-columns: 210px 1fr; gap: 1.4rem; background: radial-gradient(120% 90% at 0% 100%, rgba(227,154,59,.10), transparent 60%), var(--panel);
  border: 1px solid var(--line); border-radius: 6px; padding: 1.2rem 1.4rem; align-items: end; }
.dl-cast.ember { background: radial-gradient(120% 90% at 0% 100%, rgba(224,80,42,.16), transparent 60%), var(--panel); }
.dl-cast.violet { background: radial-gradient(120% 90% at 0% 100%, rgba(150,110,230,.15), transparent 60%), var(--panel); }
.dl-cast img { width: 100%; max-height: 360px; object-fit: contain; object-position: bottom; filter: drop-shadow(0 6px 14px rgba(0,0,0,.6)); }
.dl-cast h3 { font-family: 'Barlow Condensed', sans-serif; text-transform: uppercase; letter-spacing: .05em; margin: 0 0 .1rem 0; font-size: 2rem; padding: 0; }
.dl-cast .dl-role { color: var(--amber); font-family: 'Barlow Condensed', sans-serif; letter-spacing: .22em; text-transform: uppercase; font-size: .85rem; margin-bottom: .8rem; }
.dl-cast p { color: #CFC8BB; line-height: 1.62; margin: 0 0 .7rem 0; }
.dl-cast ul { margin: .2rem 0 0 1.1rem; color: var(--muted); }
.dl-mini { text-align: center; background: var(--panel); border: 1px solid var(--line); border-radius: 6px; padding: 1rem .9rem 1.1rem .9rem; }
.dl-mini img { height: 250px; max-width: 100%; object-fit: contain; filter: drop-shadow(0 6px 12px rgba(0,0,0,.55)); }
.dl-mini h4 { font-family: 'Barlow Condensed', sans-serif; text-transform: uppercase; letter-spacing: .05em; font-size: 1.35rem; margin: .5rem 0 0 0; padding: 0; }
.dl-mini .dl-role { color: var(--amber); font-family: 'Barlow Condensed', sans-serif; letter-spacing: .2em; text-transform: uppercase; font-size: .76rem; }
.dl-mini p { color: var(--muted); font-size: .93rem; line-height: 1.5; margin: .55rem 0 0 0; text-align: left; }
.dl-mini .dl-kit { margin-top: .6rem; text-align: left; font-size: .9rem; color: #CFC8BB; border-top: 1px solid var(--line); padding-top: .55rem; }
.dl-mini .dl-kit b { color: var(--amber-hi); font-weight: 600; }

/* glossary */
.dl-gloss { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 10px 22px; }
.dl-gloss div { border-left: 2px solid var(--amber); padding: .15rem 0 .2rem .8rem; }
.dl-gloss b { font-family: 'Barlow Condensed', sans-serif; letter-spacing: .1em; text-transform: uppercase; color: var(--text); }
.dl-gloss span { display: block; color: var(--muted); font-size: .93rem; line-height: 1.45; }

/* tabs and pills in the game's type */
[data-testid="stTab"] p { font-family: 'Barlow Condensed', sans-serif; font-weight: 600; letter-spacing: .14em;
  text-transform: uppercase; font-size: 1rem; }
.dl-chapter-img { width: 100%; aspect-ratio: 2.4 / 1; object-fit: cover; border-radius: 5px; border: 1px solid var(--line); margin: 0 0 1.6rem 0; display: block; }
/* reading column (chronicle, devlog) */
.dl-read { max-width: 720px; margin: 0 auto; }
.dl-read .dl-chapter-no { font-family: 'Cinzel', serif; color: var(--amber); letter-spacing: .3em; font-size: .95rem; text-align: center; margin: 1.6rem 0 .4rem 0; }
.dl-read h2.dl-chapter { font-family: 'Cormorant', serif; font-weight: 700; font-size: clamp(2.3rem, 4vw, 3.1rem); text-align: center; margin: 0 0 .4rem 0; letter-spacing: .01em; text-transform: none; padding: 0; }
.dl-read .dl-epigraph { font-family: 'Cormorant', serif; font-style: italic; color: var(--muted); text-align: center; font-size: 1.25rem; margin: .4rem 0 2rem 0; }
.dl-prose p { font-family: 'Cormorant', serif; font-weight: 500; font-size: 1.32rem; line-height: 1.72; color: #E4DDCF; margin: 0 0 1.15rem 0; }
.dl-prose p em { color: #F3E7CF; }
.dl-prose blockquote { border-left: 2px solid var(--teal); margin: 1.4rem 0; padding: .2rem 0 .2rem 1.1rem; }
.dl-prose blockquote p { font-family: 'Barlow', sans-serif; font-size: 1.02rem; color: #BFEFE0; letter-spacing: .02em; line-height: 1.6; }
.dl-prose > p:first-of-type { display: flow-root; }
.dl-prose > p:first-of-type::first-letter { font-family: 'Cinzel', serif; float: left; font-size: 3.6rem; line-height: .9; padding: .35rem .5rem 0 0; color: var(--amber); }
.dl-prose hr { border: 0; text-align: center; margin: 1.8rem 0; }
.dl-prose hr::after { content: "◆"; color: var(--amber); font-size: .8rem; letter-spacing: 1rem; }
/* chapter narration */
.dl-listen { display: flex; align-items: baseline; justify-content: space-between; gap: 12px; border-top: 1px solid var(--line);
  padding: .7rem 0 .35rem 0; margin: 0; }
.dl-listen .dl-listen-k { font-family: 'Barlow Condensed', sans-serif; font-weight: 600; letter-spacing: .22em; text-transform: uppercase;
  color: var(--amber); font-size: .9rem; }
.dl-listen .dl-listen-k::before { content: "◆"; color: var(--amber-hi); font-size: .55rem; margin-right: .6rem; vertical-align: .15rem; }
.dl-listen .dl-listen-m { font-family: 'Barlow Condensed', sans-serif; letter-spacing: .12em; text-transform: uppercase; color: var(--dim); font-size: .8rem; }
[data-testid="stAudio"] { color-scheme: dark; width: 100%; height: 42px; border-radius: 22px; margin-bottom: 1.5rem; }
.dl-post p, .dl-post li { color: #D3CCBF; line-height: 1.65; font-size: 1.04rem; }
.dl-meta { color: var(--dim); font-size: .88rem; letter-spacing: .08em; text-transform: uppercase; font-family: 'Barlow Condensed', sans-serif; }

.dl-note { border: 1px dashed var(--line); border-radius: 5px; padding: .9rem 1rem; color: var(--muted); background: rgba(227,154,59,.05); }
.dl-kit-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; }
.dl-kit-grid div { aspect-ratio: 16 / 10; background: var(--panel); border: 1px solid var(--line); border-radius: 5px; display: flex; align-items: center; justify-content: center; overflow: hidden; }
.dl-kit-grid img { max-width: 88%; max-height: 82%; object-fit: contain; }
.dl-kit-grid img.cover { max-width: 100%; max-height: 100%; width: 100%; height: 100%; object-fit: cover; }
@media (max-width: 760px) { .dl-kit-grid { grid-template-columns: repeat(2, 1fr); } }
/* video placeholder, status, goals */
.dl-soon { position: relative; aspect-ratio: 16 / 9; border-radius: 6px; overflow: hidden; background-size: cover; background-position: center; background-repeat: no-repeat; border: 1px solid var(--line); display: flex; align-items: center; justify-content: center; }
.dl-soon::before { content: ""; position: absolute; inset: 0; background: rgba(10,11,12,.62); }
.dl-soon div { position: relative; text-align: center; }
.dl-soon .dl-play { width: 68px; height: 68px; border-radius: 50%; border: 2px solid var(--amber); margin: 0 auto .9rem auto; position: relative; }
.dl-soon .dl-play::after { content: ""; position: absolute; left: 27px; top: 21px; border-left: 18px solid var(--amber); border-top: 12px solid transparent; border-bottom: 12px solid transparent; }
.dl-soon b { font-family: 'Barlow Condensed', sans-serif; letter-spacing: .22em; text-transform: uppercase; font-size: 1.15rem; display: block; }
.dl-soon span { color: var(--muted); font-size: .95rem; }
.dl-status { display: inline-flex; align-items: center; gap: .55rem; padding: .35rem .8rem; border: 1px solid var(--line); border-radius: 99px;
  font-family: 'Barlow Condensed', sans-serif; letter-spacing: .18em; text-transform: uppercase; font-size: .8rem; color: var(--muted); }
.dl-status i { width: 8px; height: 8px; border-radius: 50%; background: var(--amber); box-shadow: 0 0 10px var(--amber); display: inline-block; }
.dl-status.live i { background: var(--teal); box-shadow: 0 0 10px var(--teal); }
.dl-goal { background: var(--panel); border: 1px solid var(--line); border-radius: 5px; padding: 1rem 1.1rem; }
.dl-goal h4 { font-family: 'Barlow Condensed', sans-serif; text-transform: uppercase; letter-spacing: .06em; margin: 0 0 .3rem 0; font-size: 1.2rem; padding: 0; }
.dl-goal p { color: var(--muted); margin: 0 0 .7rem 0; font-size: .95rem; line-height: 1.5; }
.dl-bar { height: 6px; background: #22262A; border-radius: 3px; overflow: hidden; }
.dl-bar i { display: block; height: 100%; background: linear-gradient(90deg, var(--amber), var(--amber-hi)); }
.dl-goal small { color: var(--dim); }
.dl-band { margin-top: 3rem; border: 1px solid var(--line); border-radius: 6px; padding: 2.2rem 2.4rem;
  background: radial-gradient(90% 140% at 100% 0%, rgba(227,154,59,.16), transparent 55%), var(--panel); }
.dl-band .dl-h { margin-bottom: .4rem; }
.dl-spec td, .dl-spec th { padding: .5rem .9rem .5rem 0; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
.dl-spec th { font-family: 'Barlow Condensed', sans-serif; letter-spacing: .14em; text-transform: uppercase; color: var(--amber); font-weight: 600; width: 30%; }
.dl-spec { border-collapse: collapse; width: 100%; color: #D3CCBF; }

/* footer */
.dl-footer { margin-top: 4rem; padding: 2rem 0 1rem 0; border-top: 1px solid var(--line); display: flex; flex-wrap: wrap; gap: 1.5rem;
  align-items: center; justify-content: space-between; color: var(--dim); font-size: .9rem; }
.dl-footer img { height: 34px; opacity: .9; }
.dl-footer a { color: var(--muted) !important; margin-left: 1.1rem; font-family: 'Barlow Condensed', sans-serif; letter-spacing: .14em; text-transform: uppercase; font-size: .85rem; }
.dl-footer a:hover { color: var(--amber-hi) !important; }
@media (max-width: 760px) {
  .dl-cast { grid-template-columns: 1fr; }
  .dl-cast img { max-height: 300px; }
  .dl-hero { min-height: 82vh; }
}
</style>
"""


def esc(s) -> str:
    return _html.escape(str(s), quote=True)


def inject_css() -> None:
    st.html(CSS)


def html(markup: str) -> None:
    st.html(markup)


def hero(image: str, tagline: str, body: str, buttons: list[tuple[str, str, str]], zoom: float = 1.0, origin: str = "50% 50%") -> None:
    """Full-bleed key art with the wordmark. buttons: (label, href, style) with style 'primary' | '' | 'disabled'."""
    btns = "".join(f'<a class="dl-btn {s}" href="{esc(h)}" target="_self">{esc(l)}</a>' for l, h, s in buttons)
    html(f"""
<div class="dl-hero">
  <img class="dl-hero-bg" src="{C.static_url('shots/' + image)}" alt="" style="transform:scale({zoom});transform-origin:{origin}">
  <div class="dl-hero-inner">
    <img class="dl-wordmark" src="{C.static_url('brand/GameWordmark.png')}" alt="Project DELAWARE">
    <p class="dl-tagline">{esc(tagline)}</p>
    <p class="dl-body">{esc(body)}</p>
    <div class="dl-btns">{btns}</div>
  </div>
</div>""")


def banner(image: str, kicker: str, title: str, lead: str = "") -> None:
    lead_html = f'<p class="dl-lead">{esc(lead)}</p>' if lead else ""
    html(f"""
<div class="dl-banner" style="background-image:url('{C.static_url('shots/' + image)}')">
  <div><p class="dl-kicker">{esc(kicker)}</p><h1 class="dl-h">{esc(title)}</h1>{lead_html}</div>
</div>""")


def section(kicker: str, title: str, lead: str = "", top: bool = True) -> None:
    lead_html = f'<p class="dl-lead">{esc(lead)}</p>' if lead else ""
    html(f'<div class="dl-section" style="{"" if top else "margin-top:.5rem"}"><p class="dl-kicker">{esc(kicker)}</p>'
         f'<h2 class="dl-h">{esc(title)}</h2>{lead_html}</div>')


def cards(items: list[dict], min_width: int = 260) -> None:
    """items: {title, body, tag?, image? (static/shots name), tone? ('teal'|'ember'), locked?}"""
    out = []
    for it in items:
        if it.get("image"):
            img = f'<div class="dl-card-img" style="background-image:url(\'{C.static_url("shots/" + it["image"])}\')"></div>'
        elif it.get("locked"):
            img = '<div class="dl-card-img dl-classified"><span>Classified</span></div>'
        else:
            img = ""
        tag = f'<span class="dl-tag">{esc(it["tag"])}</span>' if it.get("tag") else ""
        cls = " ".join(x for x in (it.get("tone", ""), "locked" if it.get("locked") else "") if x)
        out.append(f'<div class="dl-card {cls}">{img}<div class="dl-card-body">{tag}<h4>{esc(it["title"])}</h4>'
                   f'<p>{esc(it["body"])}</p></div></div>')
    html(f'<div class="dl-grid" style="--min:{min_width}px">{"".join(out)}</div>')


def video_placeholder(image: str, title: str, note: str) -> None:
    html(f"""
<div class="dl-soon" style="background-image:url('{C.static_url('shots/' + image)}')">
  <div><div class="dl-play"></div><b>{esc(title)}</b><span>{esc(note)}</span></div>
</div>""")


def status_pill(text: str, live: bool = False) -> str:
    return f'<span class="dl-status {"live" if live else ""}"><i></i>{esc(text)}</span>'


def footer() -> None:
    s = C.site()
    links = s.get("links", {})
    names = [("youtube", "YouTube"), ("discord", "Discord"), ("x", "X"), ("instagram", "Instagram"), ("tiktok", "TikTok"),
             ("itch", "itch.io"), ("steam", "Steam")]
    social = "".join(f'<a href="{esc(links[k])}" target="_blank" rel="noopener">{n}</a>' for k, n in names if C.has(links.get(k, "")))
    if C.has(links.get("email", "")):
        social += f'<a href="mailto:{esc(links["email"])}">Contact</a>'
    meta = s["site"]
    html(f"""
<div class="dl-footer">
  <div style="display:flex;align-items:center;gap:1rem">
    <img src="{C.static_url('brand/StudioLogo.png')}" alt="{esc(meta['studio'])}">
    <span>© {esc(meta['year'])} {esc(meta['studio'])} · {esc(meta['title'])} is in development. Everything shown is work in progress.</span>
  </div>
  <div>{social}</div>
</div>""")
