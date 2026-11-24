"""Loads the site's editable content: content/*.toml and the markdown files in content/chronicle and content/devlog."""
from __future__ import annotations

import pathlib
import tomllib

import streamlit as st

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
STATIC = ROOT / "static"


@st.cache_data(show_spinner=False)
def _toml(name: str, mtime: float) -> dict:
    with open(CONTENT / name, "rb") as f:
        return tomllib.load(f)


def toml(name: str) -> dict:
    """A content/*.toml file (re-read when the file changes)."""
    p = CONTENT / name
    return _toml(name, p.stat().st_mtime)


def site() -> dict:
    return toml("site.toml")


def media() -> dict:
    return toml("media.toml")


def world() -> dict:
    return toml("world.toml")


def _front_matter(text: str) -> tuple[dict, str]:
    """Splits '---\\nkey: value\\n---\\nbody' into (meta, body). Values are plain strings."""
    meta: dict[str, str] = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"')
            text = text[end + 4:].lstrip("\n")
    return meta, text


@st.cache_data(show_spinner=False)
def _posts(folder: str, stamp: tuple) -> list[dict]:
    out = []
    for p in sorted((CONTENT / folder).glob("*.md")):
        meta, body = _front_matter(p.read_text(encoding="utf-8"))
        meta.setdefault("title", p.stem)
        out.append({"slug": p.stem, "meta": meta, "body": body})
    return out


def posts(folder: str) -> list[dict]:
    """Markdown files in content/<folder>, sorted by file name (prefix them 01-, 02- or with a date)."""
    files = sorted((CONTENT / folder).glob("*.md"))
    stamp = tuple((p.name, p.stat().st_mtime) for p in files)
    return _posts(folder, stamp)


def static_url(rel: str) -> str:
    """URL of a file in ./static, for <img> tags and CSS (served by Streamlit's static file serving)."""
    return "app/static/" + rel.lstrip("/")


def static_path(rel: str) -> pathlib.Path:
    return STATIC / rel


def has(value) -> bool:
    """True for a filled-in setting (non-empty string, non-zero number, non-empty list)."""
    if isinstance(value, str):
        return bool(value.strip())
    return bool(value)
