#!/usr/bin/env python3
import argparse, base64
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(parents=True, exist_ok=True)
PLAN_B64 = """IyBBZ2VudGljIERqYW5nbyBQbGFuIChKdWxlcy1TdHlsZSkKCj4gQWx3YXlzIHJ1bjoKPgo+IGBgYGJhc2gKPiBiYXNoIHNjcmlwdHMvanVsZXNfcHJlYW1ibGUuc2gKPiBgYGAK"""
AGENTS_B64 = """IyBBR0VOVFMubWQKClNlZSBwbGFuOyBzY2FmZm9sZCBhZ2VudHMgYXMgc3BlY2lmaWVkLgo="""

def write_plan():
    (DOCS / "Agentic-Django-Plan.md").write_bytes(base64.b64decode(PLAN_B64))

def write_agents():
    (DOCS / "AGENTS.md").write_bytes(base64.b64decode(AGENTS_B64))

def main():
    write_plan(); write_agents(); print("[restore_docs] ok")
if __name__ == "__main__":
    main()
