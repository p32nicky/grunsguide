"""Plan (and optionally apply) consolidation of cannibalising Gruns articles.

Groups articles by their underlying topic, keeps the single best page per
topic, and lists the rest for removal + 301 redirect to the keeper.

Default is DRY RUN. Pass --apply to actually delete and write the redirect map.
"""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

ART = Path(r"C:\grunssite\content\articles")
REDIRECTS = Path(r"C:\grunssite\content\redirects.json")

TEMPLATE_PREFIXES = [
    (r"^complete-guide-", 4),
    (r"^does-gr-ns-help-with-", 3),
    (r"^why-gr-ns-for-", 3),
    (r"^gr-ns-solution-for-", 3),
    (r"^honest-", 2),
    (r"^my-experience-with-", 2),
    (r"^is-gr-ns-worth-it-", 2),
]


def base_topic(slug):
    s = slug
    for pat, _ in TEMPLATE_PREFIXES:
        s = re.sub(pat, "", s)
    s = re.sub(r"-and-gr-ns$|-gr-ns$|-and-gruns$", "", s)
    s = re.sub(r"^gr-ns-", "", s)
    return s


def template_rank(slug):
    """Lower = more template-y boilerplate. Used to pick the keeper."""
    for pat, penalty in TEMPLATE_PREFIXES:
        if re.match(pat, slug):
            return penalty
    return 0  # no template prefix = cleanest title


def load(slug):
    try:
        return json.loads((ART / f"{slug}.json").read_text(encoding="utf-8"))
    except Exception:
        return {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    slugs = sorted(p.stem for p in ART.glob("*.json"))
    groups = defaultdict(list)
    for s in slugs:
        groups[base_topic(s)].append(s)

    multi = {k: v for k, v in groups.items() if len(v) > 1}
    redirects, to_delete = {}, []

    for topic, members in sorted(multi.items(), key=lambda kv: -len(kv[1])):
        scored = []
        for s in members:
            d = load(s)
            if d.get("error") or not (d.get("body") or "").strip():
                quality = -1                      # broken page, never keep
            else:
                quality = len(d.get("body", ""))
            scored.append((template_rank(s), -quality, s))
        # cleanest prefix wins; tie-break on longest body
        scored.sort()
        keeper = scored[0][2]
        for _, _, s in scored[1:]:
            to_delete.append(s)
            redirects[s] = keeper

    print(f"articles            : {len(slugs)}")
    print(f"topics with dupes   : {len(multi)}")
    print(f"pages to remove     : {len(to_delete)}")
    print(f"articles after      : {len(slugs) - len(to_delete)}\n")

    print("SAMPLE (worst clusters):")
    shown = 0
    for topic, members in sorted(multi.items(), key=lambda kv: -len(kv[1]))[:6]:
        keeper = [k for k, v in redirects.items() if v]  # noqa
        keep = [m for m in members if m not in redirects]
        print(f"\n  topic: {topic[:64]}  ({len(members)} pages)")
        print(f"    KEEP   {keep[0] if keep else '?'}")
        for m in members:
            if m in redirects:
                print(f"    remove {m[:70]}")
        shown += 1

    if not args.apply:
        print("\n[DRY RUN] nothing changed. Re-run with --apply to execute.")
        return

    REDIRECTS.write_text(json.dumps(redirects, indent=2, ensure_ascii=False),
                         encoding="utf-8")
    for s in to_delete:
        (ART / f"{s}.json").unlink(missing_ok=True)
    print(f"\nAPPLIED: removed {len(to_delete)} pages, "
          f"wrote {len(redirects)} redirects to {REDIRECTS}")


if __name__ == "__main__":
    main()
