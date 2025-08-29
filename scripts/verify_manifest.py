#!/usr/bin/env python3
import sys, hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def load_manifest() -> dict:
    p = ROOT / "docs" / "manifest.yaml"
    if not p.exists():
        return {"required":[
            {"path":"docs/Agentic-Django-Plan.md"},
            {"path":"docs/AGENTS.md"},
            {"path":"scripts/jules_preamble.sh"},
            {"path":"scripts/restore_docs.py"},
            {"path":"scripts/verify_manifest.py"},
            {"path":".github/workflows/verify-docs.yml"},
            {"path":"README.md"},
        ]}
    try:
        # manifest.yaml is actually JSON for stdlib-only parsing
        return json.loads(p.read_text())
    except Exception as e:
        print("Failed to parse manifest:", e)
        sys.exit(1)

def check(manifest: dict) -> int:
    missing, mismatch = [], []
    for item in manifest.get("required", []):
        path = item["path"]; p = ROOT / path
        if not p.exists(): missing.append(path); continue
        expect = item.get("sha256")
        if expect:
            got = sha256(p)
            if got != expect: mismatch.append((path, expect, got))
    if missing or mismatch:
        if missing:
            print("Missing files:"); [print(" -", m) for m in missing]
        if mismatch:
            print("Checksum mismatches:")
            for path, exp, got in mismatch:
                print(f" - {path}\n   expected: {exp}\n   got:      {got}")
        return 1
    print("Manifest OK"); return 0

def update(manifest: dict) -> int:
    changed = False
    for item in manifest.get("required", []):
        p = ROOT / item["path"]
        if not p.exists(): continue
        s = sha256(p)
        if item.get("sha256") != s:
            item["sha256"] = s; changed = True
    if changed:
        out = ROOT / "docs" / "manifest.yaml"
        out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print("Updated manifest with new checksums."); return 0
    print("No updates needed."); return 0

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--update", action="store_true")
    args = ap.parse_args()
    manifest = load_manifest()
    if args.update: sys.exit(update(manifest))
    sys.exit(check(manifest))
