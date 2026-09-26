#!/usr/bin/env python3
"""Build data/crosswords.json: 8 weeks of original daily puzzles.

Run from the repo root: python3 scripts/build_crosswords.py

Grids are rotationally symmetric, every white square is checked, and every
entry is at least 3 letters. Monday is the smallest. Difficulty rises through
Saturday by grid density and clue wordplay. Sunday is larger. Patterns are
curated; fills are searched from the original clue bank and then checked.
"""

import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from xword_bank import load_words

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "crosswords.json"

WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
WORDPLAY_ODDS = {
    "monday": 0.08,
    "tuesday": 0.18,
    "wednesday": 0.35,
    "thursday": 0.5,
    "friday": 0.68,
    "saturday": 0.82,
    "sunday": 0.22,
}
TITLES = {
    "monday": ["Monday Mile", "Open Gate", "First Showing", "Porch Light", "Easy Key", "Curb Notes", "Soft Ask", "Day One"],
    "tuesday": ["Tuesday Turn", "Second Look", "Side Lot", "Lockbox Hour", "Town Road", "Offer Draft", "Mid Listing", "Two Stops"],
    "wednesday": ["Midweek File", "Wednesday Walk", "Half the Week", "Clause Day", "Center Hall", "Inspection Eve", "Third Cup", "Map Room"],
    "thursday": ["Thursday Terms", "Fine Lines", "Duty Day", "Title Stack", "Four Corners", "Agency Hour", "Record Room", "Longer Lot"],
    "friday": ["Friday Fine Print", "Almost Closed", "Fifth Pass", "Harder Ask", "Contingency", "Late Showing", "Chain Check", "Tight Terms"],
    "saturday": ["Saturday Survey", "Hardest Weekday", "Pin and Flag", "Full File", "No Shortcuts", "Last Look", "Dense Lot", "Survey Day"],
    "sunday": ["Sunday Record", "Wide Parcel", "Closing Sunday", "Longer Table", "The Big File", "Sunday Terms", "Full Block", "Open House Grid"],
}
BLURBS = {
    "monday": "A small Monday grid. Clues are mostly straight definitions.",
    "tuesday": "A step up from Monday, still mostly short entries.",
    "wednesday": "Midweek. A few longer entries, and more wordplay.",
    "thursday": "A wider Thursday grid.",
    "friday": "Friday. Read the clues twice.",
    "saturday": "The hardest clues of the week.",
    "sunday": "A larger Sunday grid built from license-exam vocabulary.",
}
# Short exam words the filler should try before ordinary glue.
MARQUEE = {
    "DEED", "LIEN", "TITLE", "AGENT", "LEASE", "GRANT", "TRUST", "OWNER",
    "TAX", "FEE", "APR", "LOT", "RENT", "NOTE", "LOAN", "DEBT", "HEIR",
}
# Words the Sunday blurb may name. Only names that are actually in the grid are used.
SPOTLIGHT = [
    "DEED", "LIEN", "TITLE", "AGENT", "LEASE", "GRANT", "TRUST", "ESCROW",
    "AGENCY", "EASEMENT", "APPRAISAL", "RIPARIAN", "ENCROACHMENT", "CONVEYANCE",
    "MORTGAGE", "FIDUCIARY", "EARNEST", "CLOSING", "LISTING", "GRANTEE", "GRANTOR",
]


def mirror_rows(rows):
    return [row[::-1] for row in rows]


def pattern_book():
    """Curated American patterns that this clue bank can fill."""
    monday = [
        ["...##", "...##", ".....", "##...", "##..."],
    ]
    tuesday = [
        ["...####", "...####", "....###", "##...##", "###....", "####...", "####..."],
    ]
    wednesday = [
        ["####...", "####...", "##.....", "##...##", ".....##", "...####", "...####"],
        ["...####", "....###", "....###", "##...##", "###....", "###....", "####..."],
    ]
    thursday = [
        ["...###...", "...###...", "...###...", "##.....##", "###...###", "##.....##", "...###...", "...###...", "...###..."],
    ]
    friday = [
        ["...###...", "...###...", "...##....", "##....###", "###...###", "###....##", "....##...", "...###...", "...###..."],
    ]
    saturday = [
        ["...###...", "...###...", "....##...", "###....##", "###...###", "##....###", "...##....", "...###...", "...###..."],
    ]
    sunday = [
        ["...########", "....####...", "....###....", "###...#....", "####....###", "####...####", "###....####", "....#...###", "....###....", "...####....", "########..."],
        ["...########", "....####...", ".....##....", "###...#....", "####....###", "####...####", "###....####", "....#...###", "....##.....", "...####....", "########..."],
    ]
    book = {
        "monday": monday,
        "tuesday": tuesday,
        "wednesday": wednesday,
        "thursday": thursday,
        "friday": friday,
        "saturday": saturday,
        "sunday": sunday,
    }
    expanded = {}
    for day, patterns in book.items():
        seen = set()
        out = []
        for rows in patterns:
            for variant in (rows, mirror_rows(rows)):
                key = tuple(variant)
                if key in seen:
                    continue
                seen.add(key)
                out.append(variant)
        expanded[day] = out
    return expanded


def analyze(grid, max_run, allow_long_rows=()):
    """Return slots if the pattern is a legal American grid, else None.

    allow_long_rows permits across entries longer than max_run on those rows.
    """
    n = len(grid)
    allow = set(allow_long_rows)
    for r in range(n):
        for c in range(n):
            if (grid[r][c] == "#") != (grid[n - 1 - r][n - 1 - c] == "#"):
                return None
    slots = []
    whites = []
    covered_a = [[False] * n for _ in range(n)]
    covered_d = [[False] * n for _ in range(n)]

    def take(cells, across):
        if len(cells) < 3:
            return False
        if len(cells) > max_run:
            if not (across and cells[0][0] in allow):
                return False
        slots.append({"across": across, "cells": cells})
        target = covered_a if across else covered_d
        for rr, cc in cells:
            target[rr][cc] = True
        return True

    for r in range(n):
        c = 0
        while c < n:
            if grid[r][c] == "#":
                c += 1
                continue
            cells = []
            while c < n and grid[r][c] != "#":
                cells.append((r, c))
                c += 1
            if not take(cells, True):
                return None
    for c in range(n):
        r = 0
        while r < n:
            if grid[r][c] == "#":
                r += 1
                continue
            cells = []
            while r < n and grid[r][c] != "#":
                cells.append((r, c))
                r += 1
            if not take(cells, False):
                return None
    for r in range(n):
        for c in range(n):
            if grid[r][c] == "#":
                continue
            whites.append((r, c))
            if not covered_a[r][c] or not covered_d[r][c]:
                return None
    if not whites:
        return None
    seen = set()
    stack = [whites[0]]
    seen.add(whites[0])
    while stack:
        r, c = stack.pop()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] != "#" and (nr, nc) not in seen:
                seen.add((nr, nc))
                stack.append((nr, nc))
    if len(seen) != len(whites):
        return None
    black = sum(row.count("#") for row in grid)
    return {"slots": slots, "whites": len(whites), "black": black}


class Library:
    def __init__(self, words):
        self.by_len = {}
        self.meta = words
        for word in words:
            self.by_len.setdefault(len(word), []).append(word)
        self.index = {}
        self.universe = {}
        for length, bucket in self.by_len.items():
            idx = [{} for _ in range(length)]
            for wi, word in enumerate(bucket):
                for i, ch in enumerate(word):
                    idx[i].setdefault(ch, set()).add(wi)
            self.index[length] = idx
            self.universe[length] = set(range(len(bucket)))

    def candidates(self, pattern, used):
        length = len(pattern)
        bucket = self.by_len.get(length)
        if not bucket:
            return []
        sets = []
        for i, ch in enumerate(pattern):
            if ch != ".":
                sets.append(self.index[length][i].get(ch, frozenset()))
        if not sets:
            ids = self.universe[length]
        else:
            sets = sorted(sets, key=len)
            ids = set(sets[0])
            for group in sets[1:]:
                ids &= group
                if not ids:
                    break
        out = []
        rare = set("JQXZ")
        for i in ids:
            word = bucket[i]
            if word in used:
                continue
            if any(ch in rare and pattern[pos] != ch for pos, ch in enumerate(word)):
                continue
            out.append(word)
        return out


def pattern_of(grid, cells):
    return "".join("." if grid[r][c] == "." else grid[r][c] for r, c in cells)


def place(grid, cells, word):
    prev = []
    for (r, c), ch in zip(cells, word):
        prev.append(grid[r][c])
        grid[r][c] = ch
    return prev


def restore(grid, cells, prev):
    for (r, c), ch in zip(cells, prev):
        grid[r][c] = ch


def fill(grid, slots, lib, rng, node_cap=12000, restarts=8):
    initial = [row[:] for row in grid]
    open_slots = []
    preset = []
    for slot in slots:
        pat = pattern_of(grid, slot["cells"])
        slot["answer"] = None
        if "." not in pat:
            if pat not in lib.meta:
                return False
            preset.append((slot, pat))
        else:
            open_slots.append(slot)

    def once():
        for row, src in zip(grid, initial):
            row[:] = src
        used = set()
        for slot, pat in preset:
            if pat in used:
                return False
            used.add(pat)
            slot["answer"] = pat
        for slot in open_slots:
            slot["answer"] = None
        nodes = {"n": 0}

        def rec():
            nodes["n"] += 1
            if nodes["n"] > node_cap:
                return False
            best = None
            best_cands = None
            for slot in open_slots:
                if slot.get("answer"):
                    continue
                cands = lib.candidates(pattern_of(grid, slot["cells"]), used)
                if not cands:
                    return False
                if best is None or len(cands) < len(best_cands):
                    best = slot
                    best_cands = cands
                    if len(cands) == 1:
                        break
            if best is None:
                return True
            rng.shuffle(best_cands)
            best_cands.sort(key=lambda w: (
                0 if w in MARQUEE else 1,
                0 if lib.meta[w]["exam"] and rng.random() < 0.65 else 1,
            ))
            for word in best_cands:
                prev = place(grid, best["cells"], word)
                used.add(word)
                best["answer"] = word
                if rec():
                    return True
                best["answer"] = None
                used.remove(word)
                restore(grid, best["cells"], prev)
            return False

        return rec()

    for _ in range(restarts):
        if once():
            return True
    return False


def number_entries(grid, slots):
    n = len(grid)
    number = 1
    numbers = [[0] * n for _ in range(n)]
    starts = {}
    ordered = sorted(slots, key=lambda s: (s["cells"][0][0], s["cells"][0][1], not s["across"]))
    for slot in ordered:
        r, c = slot["cells"][0]
        key = (r, c)
        if key not in starts:
            starts[key] = number
            numbers[r][c] = number
            number += 1
        slot["n"] = starts[key]
    return numbers


def choose_clue(meta, weekday, rng):
    use_wordplay = bool(meta["wordplay"]) and rng.random() < WORDPLAY_ODDS[weekday]
    text = meta["wordplay"] if use_wordplay else meta["straight"]
    low = text.lower()
    names_a_fact = any(mark in low for mark in ("connecticut", "dcp", "psi "))
    if names_a_fact or not use_wordplay:
        source = meta["source"]
    else:
        source = None
    return text, source


def build_puzzle(weekday, index, grid, info, lib, rng, title, blurb, min_exam):
    if not fill(grid, info["slots"], lib, rng):
        return None
    answers = [s.get("answer") for s in info["slots"]]
    if any(not a for a in answers) or len(set(answers)) != len(answers):
        return None
    exam_hits = sum(1 for a in answers if lib.meta[a]["exam"])
    if exam_hits < min_exam:
        return None
    numbers = number_entries(grid, info["slots"])
    across = []
    down = []
    for slot in info["slots"]:
        clue, source = choose_clue(lib.meta[slot["answer"]], weekday, rng)
        r, c = slot["cells"][0]
        entry = {
            "n": slot["n"],
            "row": r,
            "col": c,
            "answer": slot["answer"],
            "clue": clue,
            "source": source,
        }
        (across if slot["across"] else down).append(entry)
    across.sort(key=lambda e: (e["n"], e["col"]))
    down.sort(key=lambda e: (e["n"], e["row"]))
    featured = [word for word in SPOTLIGHT if word in set(answers)]
    return {
        "id": f"{weekday}-{index + 1}",
        "weekday": weekday,
        "title": title,
        "blurb": blurb,
        "theme": None,
        "featured": featured,
        "size": len(grid),
        "grid": ["".join(row) for row in grid],
        "numbers": numbers,
        "across": across,
        "down": down,
    }


def sunday_copy(puzzle, words):
    answers = {entry["answer"] for entry in puzzle["across"] + puzzle["down"]}
    featured = [word for word in SPOTLIGHT if word in answers]
    puzzle["featured"] = featured
    puzzle["theme"] = "exam-vocabulary"
    if featured:
        shown = ", ".join(featured)
        puzzle["blurb"] = (
            "Sunday theme: license-exam vocabulary on a larger grid. "
            f"In this puzzle: {shown}."
        )
    else:
        puzzle["blurb"] = "Sunday theme: a larger grid of license-exam vocabulary."
    for entry in puzzle["across"] + puzzle["down"]:
        if entry["answer"] not in featured:
            continue
        meta = words[entry["answer"]]
        entry["clue"] = meta["straight"]
        entry["source"] = meta["source"]


def make_day(day, patterns, lib, words):
    made = []
    seen = set()
    attempt = 0
    min_exam = 4 if day == "sunday" else 2
    while len(made) < 8 and attempt < 80:
        attempt += 1
        pattern = patterns[(attempt + len(made)) % len(patterns)]
        rng = random.Random(f"ctlt-xw-{day}-{attempt}-{len(made)}")
        grid = [list(row) for row in pattern]
        info = analyze(grid, max_run=5)
        if not info:
            raise SystemExit(f"Illegal curated pattern for {day}")
        title = TITLES[day][len(made)]
        puzzle = build_puzzle(day, len(made), grid, info, lib, rng, title, BLURBS[day], min_exam)
        if not puzzle:
            continue
        signature = tuple(sorted(entry["answer"] for entry in puzzle["across"] + puzzle["down"]))
        if signature in seen:
            continue
        seen.add(signature)
        if day == "sunday":
            sunday_copy(puzzle, words)
        made.append(puzzle)
        print(f"  {day} {len(made)}/8 entries={len(puzzle['across']) + len(puzzle['down'])} featured={puzzle['featured'][:4]}", flush=True)
    if len(made) < 8:
        raise SystemExit(f"Only built {len(made)} {day} puzzles")
    return made


def validate_library(library, words):
    ct_marks = ("connecticut", "dcp", "psi ")
    sizes = {}
    for day in WEEKDAYS:
        puzzles = library[day]
        if len(puzzles) < 8:
            raise SystemExit(f"{day} has {len(puzzles)}")
        for puzzle in puzzles:
            n = puzzle["size"]
            sizes[day] = n
            grid = puzzle["grid"]
            if len(grid) != n or any(len(row) != n for row in grid):
                raise SystemExit(f"bad size {puzzle['id']}")
            info = analyze([list(row) for row in grid], max_run=99)
            if info is None:
                raise SystemExit(f"illegal grid {puzzle['id']}")
            seen = set()
            for entry in puzzle["across"] + puzzle["down"]:
                answer = entry["answer"]
                if answer in seen:
                    raise SystemExit(f"duplicate {answer} in {puzzle['id']}")
                seen.add(answer)
                if answer not in words:
                    raise SystemExit(f"unknown word {answer}")
                if len(answer) < 3:
                    raise SystemExit(f"short answer {puzzle['id']} {answer}")
                r, c = entry["row"], entry["col"]
                across = entry in puzzle["across"]
                cells = []
                for _ch in answer:
                    if grid[r][c] == "#":
                        raise SystemExit(f"black cell in entry {puzzle['id']}")
                    cells.append(grid[r][c])
                    if across:
                        c += 1
                    else:
                        r += 1
                if "".join(cells) != answer:
                    raise SystemExit(f"answer mismatch {puzzle['id']} {answer}")
                clue = entry["clue"].lower()
                if any(mark in clue for mark in ct_marks) and not entry.get("source"):
                    raise SystemExit(f"unsourced CT clue {puzzle['id']}: {entry['clue']}")
                if entry.get("source") and not entry["source"].get("url"):
                    raise SystemExit(f"bad source {puzzle['id']}")
                if not entry["clue"]:
                    raise SystemExit(f"empty clue {puzzle['id']}")
            if len(info["slots"]) != len(puzzle["across"]) + len(puzzle["down"]):
                raise SystemExit(f"slot count {puzzle['id']}")
            for word in puzzle.get("featured") or []:
                if word not in seen:
                    raise SystemExit(f"featured word missing {puzzle['id']} {word}")
    if not (sizes["monday"] < sizes["tuesday"] <= sizes["wednesday"] < sizes["thursday"]):
        raise SystemExit(f"weekday sizes do not rise {sizes}")
    if not (sizes["saturday"] < sizes["sunday"]):
        raise SystemExit(f"Sunday must be larger than Saturday {sizes}")
    print("validated", {day: sizes[day] for day in WEEKDAYS})


def main():
    words = load_words()
    print(f"clue bank {len(words)} words")
    lib = Library(words)
    book = pattern_book()
    library = {}
    for day in WEEKDAYS:
        print(day, "patterns", len(book[day]))
        library[day] = make_day(day, book[day], lib, words)
    validate_library(library, words)
    payload = {
        "version": 1,
        "epoch": "2024-01-01",
        "note": "Original puzzles for CT License Trail. The weekday and the week count since Monday 2024-01-01 pick the grid. No newspaper puzzle, name, or branding is used.",
        "days": library,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    total = sum(len(v) for v in library.values())
    print(f"Wrote {total} puzzles to {OUT}")


if __name__ == "__main__":
    main()
