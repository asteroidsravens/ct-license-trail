"""Write data/glossary.json from the original crossword definitions."""

import json
from pathlib import Path

from xword_bank import load_words

ROOT = Path(__file__).resolve().parents[1]


def main():
    course = json.loads((ROOT / "data" / "course.json").read_text())
    chapters = course.get("words") or {}
    entries = []
    for word, row in load_words().items():
        if not row.get("exam"):
            continue
        chapter = chapters.get(word) or None
        if chapter == 0:
            chapter = None
        entries.append({
            "term": word,
            "text": row["straight"],
            "source": row["source"],
            "chapter": chapter,
        })
    entries.sort(key=lambda item: item["term"])
    payload = {
        "note": "Original definitions used by Study Buddy. Built from scripts/xword_bank.py. Do not paste a textbook glossary.",
        "entries": entries,
    }
    (ROOT / "data" / "glossary.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(f"wrote {len(entries)} glossary entries")


if __name__ == "__main__":
    main()
