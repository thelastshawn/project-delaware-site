# Project DELAWARE: the website

The game's official site, built with Streamlit (Python). Pages: **Home, The World, Chronicle, Media, Devlog, Download, Support.**

## Run it on your PC
```
cd Website
pip install -r requirements.txt
streamlit run app.py
```
It opens at http://localhost:8501.

## Change what it says (no code needed)
| To change | Edit |
|---|---|
| Download link, version, release date | `content/site.toml` → `[download]`. Set `status = "available"` and paste `url` to switch the buttons on. |
| Donation buttons (Ko-fi, Patreon, PayPal…) | `content/site.toml` → `[donate]`. Empty ones stay hidden. |
| Social links (YouTube, Discord, X…) | `content/site.toml` → `[links]` |
| Funding goals and progress bars | `content/site.toml` → `[[goals]]` (`target = 0` hides the bar) |
| Trailers and gameplay videos | `content/media.toml`: paste a YouTube link into `url` |
| Screenshots | Put the image in `static/shots/` and add a `[[screenshots]]` entry in `content/media.toml` |
| Lore, characters, regions, glossary | `content/world.toml` |
| The Chronicle (story chapters) | `content/chronicle/NN-name.md`. The number sets the order. |
| Devlog posts | Add `content/devlog/YYYY-MM-DD-title.md`, copying the first post's header lines. Newest shows first. |
| What's in the demo | `content/patch_notes.md` |

Spoiler rule used in all text: only what a player learns in the first hour. Vance is never named as the Heretic, the President's fate stays "died in Nevada", and Sarah's mission stays untold.

## Put it online (free)
1. Make a **public GitHub repo** and upload this folder's contents (app.py at the top level).
2. Go to **share.streamlit.io**, sign in with GitHub, choose **Create app**, pick the repo, the branch and `app.py`, and pick a subdomain (e.g. `project-delaware.streamlit.app`).
3. Every push to the repo updates the site.

Note: on Streamlit Community Cloud, an app with no visitors for 12 hours goes to sleep, and the next visitor sees a "wake up" button first.

## Hosting the game download
Streamlit can't host a multi-GB build. Put the zip on **itch.io** (free; it gives you a download page and analytics) or a **GitHub Release**, then paste the link into `content/site.toml` → `[download] url`.

## Files
- `app.py`: navigation and shared layout
- `views/`: one file per page
- `lib/ui.py`: the look (CSS, hero, cards, footer); `lib/content.py` loads `content/`
- `static/`: images, logos, and the game's fonts (Barlow, Cinzel, Cormorant; OFL licences included)
- `.streamlit/config.toml`: theme colours and fonts
- `tools/smoke_test.py`: runs every page headless and reports errors (`python tools/smoke_test.py`)
