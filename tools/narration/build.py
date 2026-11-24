"""Chronicle narration: chapter markdown -> narration script -> Chatterbox queue -> mastered MP3 per chapter.

  python3 build.py queue <voice> [slug...]      append missing sentence takes to queue.jsonl (render.py renders them)
  python3 build.py assemble <voice> [slug...]   cache takes -> out/<slug>.mp3 + out/<slug>.json (duration)
  python3 build.py script [slug...]             print the narration script
"""
import hashlib
import json
import os
import re
import subprocess
import sys

import numpy as np

D = "/home/claude/narr"
SITE = "/home/claude/project-delaware-site"
CH = f"{SITE}/content/chronicle"
SR = 24000

# voice -> (exaggeration, cfg) ; LANTERN is the radio voice for intel logs (Chatterbox ref from the game's cast)
VOICES = {"storyteller": (0.4, 0.4), "thorne": (0.45, 0.4), "storyteller_f": (0.4, 0.4), "lantern": (0.3, 0.5)}
PACE = 0.92
ROMAN = {"I": "One", "II": "Two", "III": "Three", "IV": "Four", "V": "Five", "VI": "Six", "VII": "Seven", "VIII": "Eight", "IX": "Nine", "X": "Ten"}

# Spoken forms. LANTERN / LINK in caps would be spelled out letter by letter.
SAY = [
    (r"\bLANTERN's\b", "Lantern's"), (r"\bLANTERN\b", "Lantern"), (r"\bLINK\b", "Link"),
    (r"\b2027\b", "twenty twenty-seven"), (r"\bI-15\b", "I-Fifteen"), (r"\bI-(\d+)\b", r"Interstate \1"),
    (r"\bSoCal\b", "Southern California"),
]

# Intel log lines (blockquotes) are read on the radio; their spoken form is written here by hand.
LOG_SAY = {
    "LANTERN INTEL LOG 01": "Lantern intel log, zero one. Fourteen July, twenty twenty-seven. Mercury Ridge, Frenchman Flat, Nevada. "
                            "Lamplight clearance. Two lines redacted.",
}


def front(text):
    meta, body = {}, text
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        for line in fm.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
    return meta, body.strip()


def clean(t):
    t = re.sub(r"[*_]{1,2}([^*_]+)[*_]{1,2}", r"\1", t)          # italics / bold
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)               # links
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    t = t.replace("—", ", ").replace("–", ", ").replace("…", "...")
    for a, b in SAY:
        t = re.sub(a, b, t)
    t = re.sub(r"\s+", " ", t).replace(" ,", ",").replace(",,", ",").strip()
    return t


def sentences(p):
    parts = re.split(r'(?<=[.!?])["\']?\s+(?=["\'A-Z0-9])', p)
    return [s.strip() for s in parts if s.strip()]


def chunks(p, lo=7, hi=34):
    """Sentences grouped into takes: very short sentences ride with a neighbour, long runs are split."""
    out, cur = [], []
    for s in sentences(p):
        n = len(s.split())
        if cur and (sum(len(x.split()) for x in cur) >= lo and sum(len(x.split()) for x in cur) + n > hi):
            out.append(" ".join(cur)); cur = []
        cur.append(s)
        if sum(len(x.split()) for x in cur) >= hi:
            out.append(" ".join(cur)); cur = []
    if cur:
        if out and sum(len(x.split()) for x in cur) < 4 and len(out[-1].split()) < hi:
            out[-1] += " " + " ".join(cur)
        else:
            out.append(" ".join(cur))
    return out


def script(slug):
    """[(voice_role, text, pause_after_seconds)] ; role 'n' narrator, 'log' radio."""
    meta, body = front(open(f"{CH}/{slug}.md", encoding="utf-8").read())
    num = ROMAN.get(meta.get("number", ""), meta.get("number", ""))
    s = [("n", f"Chapter {num}.", 0.7), ("n", clean(meta["title"]) + ".", 1.3)]
    if meta.get("epigraph"):
        s.append(("n", clean(meta["epigraph"]), 1.5))
    blocks = [b.strip() for b in re.split(r"\n\s*\n", body) if b.strip()]
    for bi, b in enumerate(blocks):
        if re.fullmatch(r"-{3,}|\*{3,}", b):
            if s:
                s[-1] = (s[-1][0], s[-1][1], 1.9)
            continue
        if b.startswith(">"):
            raw = re.sub(r"^>\s?", "", b, flags=re.M).strip()
            said = next((v for k, v in LOG_SAY.items() if raw.startswith(k)), None) or clean(raw.replace("·", ".").replace("[", "").replace("]", ""))
            if s:
                s[-1] = (s[-1][0], s[-1][1], max(s[-1][2], 1.1))
            s.append(("log", said, 1.2))
            continue
        cs = chunks(clean(b))
        for ci, c in enumerate(cs):
            s.append(("n", c, 0.4 if ci < len(cs) - 1 else 1.05))
    s[-1] = (s[-1][0], s[-1][1], 0.0)
    return s


def key(voice, text, seed=7):
    ex, cfg = VOICES[voice]
    return hashlib.sha1(f"{voice}|{ex}|{cfg}|{seed}|{text}".encode()).hexdigest()[:16]


def take(voice, text):
    """(voice, seed) actually used for this line: a later seed if the default take was rejected (reject.json)."""
    rej = json.load(open(f"{D}/reject.json")) if os.path.exists(f"{D}/reject.json") else {}
    seed = 7 + rej.get(key(voice, text, 7), 0)
    return seed, key(voice, text, seed)


def slugs(args):
    allslugs = sorted(f[:-3] for f in os.listdir(CH) if f.endswith(".md"))
    return [s for s in allslugs if not args or any(s.startswith(a) for a in args)]


def queue(voice, args):
    have = set()
    if os.path.exists(f"{D}/queue.jsonl"):
        have = {json.loads(l)["key"] for l in open(f"{D}/queue.jsonl")}
    n = 0
    with open(f"{D}/queue.jsonl", "a") as f:
        for o, slug in enumerate(slugs(args)):
            for role, text, _ in script(slug):
                v = "lantern" if role == "log" else voice
                seed, k = take(v, text)
                if k in have or os.path.exists(f"{D}/cache/{k}.wav"):
                    continue
                ex, cfg = VOICES[v]
                f.write(json.dumps({"key": k, "voice": v, "text": text, "ex": ex, "cfg": cfg, "seed": seed, "order": o}) + "\n")
                have.add(k); n += 1
    print("queued", n)


# ----------------------------------------------------------------------------------------------------------------------
def load_take(k):
    import librosa
    y, _ = librosa.load(f"{D}/cache/{k}.wav", sr=SR)
    y, _ = librosa.effects.trim(y.astype(np.float32), top_db=42, frame_length=1024, hop_length=128)
    f = int(0.012 * SR)
    y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
    return y


def limit(y, ceiling_db, ms=10):
    """Gain = min over a window, then averaged over the same window: never above what any sample in reach needs."""
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    c = 10 ** (ceiling_db / 20)
    w = max(3, int(ms / 1000 * SR)) | 1
    g = np.minimum(1.0, c / np.maximum(np.abs(y), 1e-9))
    g = uniform_filter1d(minimum_filter1d(g, w), w)
    return np.clip(y * g, -c, c).astype(np.float32)


def narrator_chain(y):
    import pedalboard as pb
    board = pb.Pedalboard([
        pb.HighpassFilter(cutoff_frequency_hz=70),
        pb.LowShelfFilter(cutoff_frequency_hz=180, gain_db=2.0, q=0.7),
        pb.PeakFilter(cutoff_frequency_hz=2800, gain_db=1.2, q=1.0),
        pb.HighShelfFilter(cutoff_frequency_hz=7500, gain_db=-2.0, q=0.7),
        pb.Compressor(threshold_db=-22, ratio=2.4, attack_ms=8, release_ms=140),
        pb.Reverb(room_size=0.12, damping=0.75, wet_level=0.035, dry_level=1.0, width=0.3),
    ])
    return board(y.astype(np.float32)[None, :], SR)[0]


def radio_chain(y):
    sys.path.insert(0, "/home/claude/cine114/gen")
    sys.argv = sys.argv[:1] + ["/home/claude/tts"]
    import voice2
    return voice2.lantern2(y) * 0.55


def assemble(voice, args):
    import pyloudnorm as pyln
    import soundfile as sf
    rng = np.random.default_rng(3)
    for slug in slugs(args):
        sc = script(slug)
        miss = [t for r, t, _ in sc if not os.path.exists(f"{D}/cache/{take('lantern' if r == 'log' else voice, t)[1]}.wav")]
        if miss:
            print(slug, "missing", len(miss)); continue
        parts = [np.zeros(int(0.5 * SR), np.float32)]
        for role, text, pause in sc:
            v = "lantern" if role == "log" else voice
            y = load_take(take(v, text)[1])
            if role != "log":   # Chatterbox reads at ~3 words/s; ease it to a storyteller's ~2.75
                import pedalboard as pb
                rate = len(re.findall(r"[A-Za-z0-9']+", text)) / max(len(y) / SR, 0.1)
                f = PACE * min(1.0, max(0.88, 3.4 / rate))     # short punchy lines come out rushed; ease those more
                y = pb.time_stretch(y.astype(np.float32)[None, :], SR, stretch_factor=f, transient_mode="smooth")[0]
            y = radio_chain(y) if role == "log" else narrator_chain(y)
            parts += [y.astype(np.float32), np.zeros(int(pause * SR), np.float32)]
        parts.append(np.zeros(int(1.2 * SR), np.float32))
        y = np.concatenate(parts)
        # room tone under everything so the gaps between takes aren't digital silence
        tone = rng.standard_normal(len(y)).astype(np.float32)
        import pedalboard as pb
        tone = pb.Pedalboard([pb.LowpassFilter(cutoff_frequency_hz=900), pb.HighpassFilter(cutoff_frequency_hz=60)])(tone[None, :], SR)[0]
        y = y + tone / (np.abs(tone).max() + 1e-9) * 10 ** (-62 / 20)
        meter = pyln.Meter(SR)
        # -16 LUFS (spoken-word web standard), then a smooth peak limiter to a -1.5 dBFS ceiling
        y = pyln.normalize.loudness(y, meter.integrated_loudness(y), -16.0)
        y = limit(y, -1.5)
        wav = f"{D}/out/{slug}.wav"
        sf.write(wav, y, SR)
        mp3 = f"{D}/out/{slug}.mp3"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-ac", "1", "-ar", "24000", "-b:a", "64k", mp3], check=True)
        dur = len(y) / SR
        json.dump({"slug": slug, "voice": voice, "seconds": round(dur, 1)}, open(f"{D}/out/{slug}.json", "w"))
        print(slug, f"{int(dur // 60)}:{int(dur % 60):02d}", os.path.getsize(mp3) // 1024, "KB")


def check(voice, args, lo=1.7, hi=4.0, gap=1.3):
    """Flag takes whose speaking rate is off (garbled tail / cut short) or with a long dead gap inside; bump their seed."""
    import librosa
    rej = json.load(open(f"{D}/reject.json")) if os.path.exists(f"{D}/reject.json") else {}
    bad = 0
    for slug in slugs(args):
        for role, text, _ in script(slug):
            v = "lantern" if role == "log" else voice
            seed, k = take(v, text)
            p = f"{D}/cache/{k}.wav"
            if not os.path.exists(p):
                continue
            y = load_take(k)
            words = len(re.findall(r"[A-Za-z0-9']+", text))
            rate = words / max(len(y) / SR, 0.1)
            iv = librosa.effects.split(y, top_db=40, frame_length=1024, hop_length=256)
            gaps = [(b[0] - a[1]) / SR for a, b in zip(iv[:-1], iv[1:])]
            why = "slow" if rate < lo else "fast" if rate > hi else "gap" if gaps and max(gaps) > gap else ""
            if why and seed - 7 < 3:
                k7 = key(v, text, 7)
                rej[k7] = rej.get(k7, 0) + 1
                bad += 1
                print(f"  {why:4s} {rate:.2f} w/s gap {max(gaps) if gaps else 0:.2f}s  {slug[:14]} | {text[:70]}")
    json.dump(rej, open(f"{D}/reject.json", "w"), indent=1)
    print("rejected", bad)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "check":
        check(sys.argv[2], sys.argv[3:]); sys.exit()
    if cmd == "script":
        for slug in slugs(sys.argv[2:]):
            print("==", slug)
            for r, t, p in script(slug):
                print(f"  [{r} {p}] {t}")
    elif cmd == "queue":
        queue(sys.argv[2], sys.argv[3:])
    elif cmd == "assemble":
        assemble(sys.argv[2], sys.argv[3:])
