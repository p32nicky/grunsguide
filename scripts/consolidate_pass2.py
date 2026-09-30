"""Second consolidation pass.

Pass 1 grouped by slug shape, so 'are-gr-ns-gummies-gluten-free' and
'why-gr-ns-for-are-gummies-gluten-free' were treated as different topics and
both survived - still cannibalising, and the survivor of a template-only group
kept an ugly title.

This pass normalises harder (drops brand and product tokens entirely), keeps
the page whose slug has no template prefix, and - importantly - rewrites any
existing redirect whose destination is a page we are about to delete, so we
never leave a redirect chain pointing at a 404.

Dry run by default; --apply to execute.
"""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(r"C:\grunssite")
ART = ROOT / "content" / "articles"
REDIRECTS = ROOT / "content" / "redirects.json"

PREFIXES = (r"^(complete-guide-|does-gr-ns-help-with-|why-gr-ns-for-|"
            r"gr-ns-solution-for-|honest-|my-experience-with-|is-gr-ns-worth-it-)")


def hard_key(s):
    s = re.sub(PREFIXES, "", s)
    s = re.sub(r"-and-gr-ns$|-gr-ns$", "", s)
    s = s.replace("gr-ns", "").replace("gruns", "")
    s = s.replace("gummies", "").replace("gummy", "")
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def is_templated(s):
    return bool(re.match(PREFIXES, s))


def body_len(slug):
    try:
        d = json.loads((ART / f"{slug}.json").read_text(encoding="utf-8"))
        if d.get("error"):
            return -1
        return len(d.get("body") or "")
    except Exception:
        return -1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    slugs = sorted(p.stem for p in ART.glob("*.json"))
    groups = defaultdict(list)
    for s in slugs:
        groups[hard_key(s)].append(s)

    new_redirects, to_delete = {}, []
    for key, members in groups.items():
        if len(members) < 2:
            continue
        # keep the non-templated slug; tie-break on longest real body
        members.sort(key=lambda s: (is_templated(s), -body_len(s), len(s)))
        keeper = members[0]
        for loser in members[1:]:
            to_delete.append(loser)
            new_redirects[loser] = keeper

    existing = {}
    if REDIRECTS.exists():
        existing = json.loads(REDIRECTS.read_text(encoding="utf-8"))

    # Repoint any pass-1 redirect whose destination is now being deleted,
    # otherwise it 308s straight into a 404.
    rechained = 0
    for src, dest in list(existing.items()):
        if dest in new_redirects:
            existing[src] = new_redirects[dest]
            rechained += 1

    merged = {**existing, **new_redirects}

    print(f"live articles          : {len(slugs)}")
    print(f"pages to remove        : {len(to_delete)}")
    print(f"articles after         : {len(slugs) - len(to_delete)}")
    print(f"pass-1 redirects fixed : {rechained}  (would have chained into a 404)")
    print(f"redirect map total     : {len(merged)}")
    print("\nsample:")
    for loser, keeper in list(new_redirects.items())[:6]:
        print(f"  {loser[:52]}\n      -> {keeper[:52]}")

    if not args.apply:
        print("\n[DRY RUN] nothing changed.")
        return

    REDIRECTS.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
    for s in to_delete:
        (ART / f"{s}.json").unlink(missing_ok=True)

    # No redirect may point at a slug that no longer exists.
    remaining = {p.stem for p in ART.glob("*.json")}
    broken = [f"{s} -> {d}" for s, d in merged.items() if d not in remaining]
    print(f"\nAPPLIED: removed {len(to_delete)}, map now {len(merged)}")
    print(f"redirects pointing at a missing page: {len(broken)}")
    for b in broken[:5]:
        print("  BROKEN", b)


if __name__ == "__main__":
    main()
