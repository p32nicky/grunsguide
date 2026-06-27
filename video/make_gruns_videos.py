"""Turn Grüns articles into 1 video each (OpenMontage / Remotion Explainer).

Usage:
  python make_gruns_videos.py --limit 1        # test on first pending article
  python make_gruns_videos.py --only <slug>    # render one specific article
  python make_gruns_videos.py                  # render ALL pending articles

Output: C:/Users/nickd/Downloads/grunsvideos/<slug>.mp4
Skips articles whose mp4 already exists, so it is resumable.
"""
from __future__ import annotations
import argparse, json, re, subprocess, sys, html, wave
from pathlib import Path

import os as _os
ARTICLES_DIR = Path(_os.environ.get("GRUNS_ARTICLES_DIR", r"C:/grunssite/content/articles"))
COMPOSER_DIR = Path(_os.environ.get("GRUNS_COMPOSER_DIR", str(Path(__file__).resolve().parent / "remotion-composer")))
PROPS_DIR    = COMPOSER_DIR / "public" / "demo-props"
AUDIO_DIR    = COMPOSER_DIR / "public" / "gruns-audio"
OUT_DIR      = Path(_os.environ.get("GRUNS_OUT_DIR", r"C:/Users/nickd/Downloads/grunsvideos"))
AFFILIATE    = "https://www.gruns.co/pages/vip?snowball=NICK67621"
PIPER_VOICE  = Path(_os.environ.get("GRUNS_PIPER_VOICE", str(Path(__file__).resolve().parent / "piper-voices" / "en_US-lessac-medium.onnx")))
PAD_SECONDS  = 0.7   # silence after each scene's narration before the next

# Gruns scene backgrounds (relative to remotion public/)
BGS = [
    "gruns-images/gruns-hero-product.jpg",
    "gruns-images/gruns-pouch.jpg",
    "gruns-images/gruns-product-showcase.jpg",
    "gruns-images/gruns-hero-lede.webp",
]

def fix_text(s: str) -> str:
    if not s:
        return ""
    s = s.replace("�", "ü")          # Gr�ns -> Grüns
    s = html.unescape(s)
    s = re.sub(r"<[^>]+>", "", s)          # strip any stray tags
    return re.sub(r"\s+", " ", s).strip()

def first_sentence(text: str, maxlen: int = 140) -> str:
    text = fix_text(text)
    m = re.split(r"(?<=[.!?])\s", text)
    out = m[0] if m else text
    if len(out) > maxlen:
        out = out[:maxlen].rsplit(" ", 1)[0] + "…"
    return out

def _paras_text(html_seg: str) -> str:
    """All paragraph text in a chunk of HTML, joined."""
    out = []
    for p in re.findall(r"<p[^>]*>(.*?)</p>", html_seg, re.S):
        t = fix_text(p)
        if len(t) > 20:
            out.append(t)
    # also capture list items as sentences
    for li in re.findall(r"<li[^>]*>(.*?)</li>", html_seg, re.S):
        t = fix_text(li)
        if len(t) > 10:
            out.append(t)
    return " ".join(out)

def chunk_sentences(text: str, max_sentences: int = 2, max_chars: int = 230):
    """Split text into on-screen-sized chunks of ~1-2 sentences."""
    text = fix_text(text)
    if not text:
        return []
    sents = re.split(r"(?<=[.!?])\s+", text)
    chunks, cur = [], ""
    n = 0
    for s in sents:
        s = s.strip()
        if not s:
            continue
        cand = (cur + " " + s).strip()
        if cur and (n >= max_sentences or len(cand) > max_chars):
            chunks.append(cur); cur = s; n = 1
        else:
            cur = cand; n += 1
    if cur:
        chunks.append(cur)
    return chunks

def parse_article(a: dict) -> dict:
    body = a.get("body", "") or ""
    title = fix_text(a.get("title", ""))
    body_no_h1 = re.sub(r"<h1[^>]*>.*?</h1>", "", body, count=1, flags=re.S)
    # intro = everything before first <h2>
    first_h2 = re.search(r"<h2", body_no_h1)
    intro = _paras_text(body_no_h1[:first_h2.start()] if first_h2 else body_no_h1)
    if not intro:
        intro = fix_text(a.get("metaDescription", ""))
    # sections: each h2 + ALL paragraphs under it (full text)
    sections = []
    for m in re.finditer(r"<h2[^>]*>(.*?)</h2>(.*?)(?=<h2|\Z)", body_no_h1, re.S):
        head = fix_text(m.group(1))
        body_txt = _paras_text(m.group(2))
        if head:
            sections.append((head, body_txt))
    return {"title": title, "intro": intro, "sections": sections}

def _say(text: str) -> str:
    """Narration-friendly text: spell brand for the TTS, drop emoji/odd chars."""
    # Phonetic respelling so Piper pronounces the brand "groons", not "gruh-ns"
    text = fix_text(text)
    text = re.sub(r"Gr[üu]ns", "Groons", text)
    text = re.sub(r"gr[üu]ns", "Groons", text)
    return text

def synth_scene_wav(text: str, dst: Path) -> float:
    """Synthesize one line with Piper; return audio duration in seconds."""
    p = subprocess.run([sys.executable, "-m", "piper", "-m", str(PIPER_VOICE),
                        "-f", str(dst)], input=_say(text), text=True,
                       capture_output=True)
    if p.returncode != 0 or not dst.exists():
        raise RuntimeError(f"piper failed: {p.stderr[-300:]}")
    with wave.open(str(dst), "rb") as w:
        return w.getnframes() / float(w.getframerate())

def build_narration(slug: str, scenes: list[tuple[str, str]]):
    """scenes = [(scene_id, narration_text)]. Synth each, concat into one WAV
    with PAD_SECONDS of silence after each. Returns (rel_audio_path, [durations])."""
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    tmp = AUDIO_DIR / f"_tmp_{slug}"
    tmp.mkdir(exist_ok=True)
    durations, frames_all, params = [], [], None
    for i, (_sid, text) in enumerate(scenes):
        wav = tmp / f"{i}.wav"
        dur = synth_scene_wav(text, wav)
        with wave.open(str(wav), "rb") as w:
            if params is None:
                params = w.getparams()
            frames_all.append(w.readframes(w.getnframes()))
        # silence pad
        sil = int(params.framerate * PAD_SECONDS) * params.sampwidth * params.nchannels
        frames_all.append(b"\x00" * sil)
        durations.append(round(dur + PAD_SECONDS, 3))
        wav.unlink(missing_ok=True)
    master = AUDIO_DIR / f"{slug}.wav"
    with wave.open(str(master), "wb") as w:
        w.setparams(params)
        w.writeframes(b"".join(frames_all))
    try: tmp.rmdir()
    except OSError: pass
    return f"gruns-audio/{slug}.wav", durations

def build_props(parsed: dict, slug: str) -> dict:
    # Each entry: (scene_id, scene_spec, narration_text). Timing follows narration.
    title, intro = parsed["title"], parsed["intro"]
    scene_specs = []
    bg_i = 0
    def next_bg():
        nonlocal bg_i
        b = BGS[bg_i % len(BGS)]; bg_i += 1
        return b

    # Hero
    scene_specs.append(("hero",
        {"type": "hero_title", "text": title, "heroSubtitle": "Grüns Greens Gummies",
         "backgroundImage": BGS[0], "backgroundOverlay": 0.58},
        f"{title}."))
    bg_i = 1
    # Intro chunks (full intro)
    for j, ch in enumerate(chunk_sentences(intro)):
        scene_specs.append((f"intro{j}",
            {"type": "text_card", "text": ch, "fontSize": 46, "color": "#F8FAFC",
             "backgroundImage": next_bg(), "backgroundOverlay": 0.62}, ch))
    # Each section: heading scene, then every chunk of its full body
    for i, (head, body_txt) in enumerate(parsed["sections"]):
        scene_specs.append((f"sec{i}h",
            {"type": "text_card", "text": head, "fontSize": 60, "color": "#FACC15",
             "backgroundImage": next_bg(), "backgroundOverlay": 0.55}, head + "."))
        for j, ch in enumerate(chunk_sentences(body_txt)):
            scene_specs.append((f"sec{i}_{j}",
                {"type": "text_card", "text": ch, "fontSize": 44, "color": "#F8FAFC",
                 "backgroundImage": next_bg(), "backgroundOverlay": 0.64}, ch))
    # CTA
    scene_specs.append(("cta",
        {"type": "text_card", "text": "Try Grüns VIP today.", "subtitle": "Link in description",
         "color": "#F8FAFC", "backgroundImage": BGS[2], "backgroundOverlay": 0.5},
        "Want in? Try Gruns VIP today. The link is in the description."))

    audio_src, durations = build_narration(slug, [(s[0], s[2]) for s in scene_specs])
    cuts, t = [], 0.0
    for (sid, spec, _txt), dur in zip(scene_specs, durations):
        dur = max(dur, 2.5)
        cut = {"id": sid, "source": "", "in_seconds": round(t, 2),
               "out_seconds": round(t + dur, 2)}
        cut.update(spec)
        cuts.append(cut); t += dur
    return {"theme": "flat-motion-graphics", "cuts": cuts, "overlays": [],
            "captions": [], "audio": {"narration": {"src": audio_src, "volume": 1.0}}}

def render(slug: str, props: dict) -> bool:
    PROPS_DIR.mkdir(parents=True, exist_ok=True)
    props_path = PROPS_DIR / f"_gruns_{slug}.json"
    props_path.write_text(json.dumps(props), encoding="utf-8")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{slug}.mp4"
    npx = "npx.cmd" if sys.platform == "win32" else "npx"
    rel_props = props_path.relative_to(COMPOSER_DIR).as_posix()
    cmd = [npx, "remotion", "render", "src/index.tsx", "Explainer", str(out),
           "--props", rel_props, "--codec", "h264", "--concurrency", "3"]
    r = subprocess.run(cmd, cwd=COMPOSER_DIR)
    props_path.unlink(missing_ok=True)
    (AUDIO_DIR / f"{slug}.wav").unlink(missing_ok=True)   # cleanup narration after render
    return r.returncode == 0 and out.exists()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="max videos this run (0 = all)")
    ap.add_argument("--only", type=str, help="render one slug")
    args = ap.parse_args()

    files = sorted(ARTICLES_DIR.glob("*.json"))
    if args.only:
        files = [f for f in files if f.stem == args.only]
    done = ok = fail = 0
    links = []
    for f in files:
        slug = f.stem
        if (OUT_DIR / f"{slug}.mp4").exists():
            continue
        try:
            a = json.loads(f.read_text(encoding="utf-8", errors="replace"))
        except Exception as e:
            print(f"SKIP {slug}: bad json {e}"); continue
        if a.get("error") or not (a.get("body") or "").strip():
            continue
        parsed = parse_article(a)
        if not parsed["title"]:
            continue
        print(f"\n=== [{done+1}] {parsed['title']} ===")
        if render(slug, build_props(parsed, slug)):
            ok += 1; links.append(f"{slug}.mp4\t{AFFILIATE}")
            print(f"  OK -> {OUT_DIR / (slug + '.mp4')}")
        else:
            fail += 1; print(f"  FAIL {slug}")
        done += 1
        if args.limit and done >= args.limit:
            break
    # append affiliate links manifest
    if links:
        man = OUT_DIR / "affiliate-links.txt"
        with man.open("a", encoding="utf-8") as h:
            h.write("\n".join(links) + "\n")
    print(f"\nDONE. ok={ok} fail={fail} (output: {OUT_DIR})")

if __name__ == "__main__":
    sys.exit(main())
