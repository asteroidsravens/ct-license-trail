#!/usr/bin/env python3
"""Build data/crosswords.json: 8 weeks of original daily puzzles per course range.

Run from the repo root: python3 scripts/build_crosswords.py

Packs are prebuilt for each course chapter, for the default completed set,
and for every chapter together. A pack may use that chapter's terms plus
chapter 0 filler. Grids are rotationally symmetric, every white square is
checked, and every entry is at least 3 letters. Short chapter packs use
mini grids.
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
                0 if lib.meta[w].get("chapter") and rng.random() < 0.8 else 1,
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


def build_puzzle(weekday, index, grid, info, lib, rng, title, blurb, min_exam, prefix, node_cap, restarts, min_content=1):
    if not fill(grid, info["slots"], lib, rng, node_cap=node_cap, restarts=restarts):
        return None
    answers = [s.get("answer") for s in info["slots"]]
    if any(not a for a in answers) or len(set(answers)) != len(answers):
        return None
    exam_hits = sum(1 for a in answers if lib.meta[a]["exam"])
    content_hits = sum(1 for a in answers if lib.meta[a].get("chapter"))
    if exam_hits < min_exam or content_hits < min_content:
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
            "chapter": lib.meta[slot["answer"]]["chapter"],
        }
        (across if slot["across"] else down).append(entry)
    across.sort(key=lambda e: (e["n"], e["col"]))
    down.sort(key=lambda e: (e["n"], e["row"]))
    featured = [word for word in SPOTLIGHT if word in set(answers)]
    return {
        "id": f"{prefix}-{weekday}-{index + 1}",
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


def effort_for(size):
    if size <= 5:
        return 2500, 4
    if size <= 7:
        return 5000, 6
    if size <= 9:
        return 9000, 6
    return 12000, 8


def make_day(day, patterns, lib, words, prefix, min_exam, node_cap, restarts, theme_sunday=False, min_content=1, goal=8, minimum=8):
    made = []
    seen = set()
    attempt = 0
    while len(made) < goal and attempt < 64:
        attempt += 1
        pattern = patterns[(attempt + len(made)) % len(patterns)]
        rng = random.Random(f"ctlt-xw-{prefix}-{day}-{attempt}-{len(made)}")
        grid = [list(row) for row in pattern]
        info = analyze(grid, max_run=5)
        if not info:
            raise SystemExit(f"Illegal curated pattern for {prefix} {day}")
        title = TITLES[day][len(made)]
        puzzle = build_puzzle(
            day, len(made), grid, info, lib, rng, title, BLURBS[day],
            min_exam, prefix, node_cap, restarts, min_content,
        )
        if not puzzle:
            continue
        signature = tuple(sorted(entry["answer"] for entry in puzzle["across"] + puzzle["down"]))
        if signature in seen:
            continue
        seen.add(signature)
        if theme_sunday:
            sunday_copy(puzzle, words)
        made.append(puzzle)
        print(
            f"  {prefix} {day} {len(made)}/8 size={puzzle['size']} featured={puzzle['featured'][:3]}",
            flush=True,
        )
    if len(made) < minimum:
        return None
    return made


def choose_tier(n_long):
    """Grid ladder from how many real-length terms are in the cumulative range.

    Three-letter glue can fill a large grid before the course has enough
    vocabulary, so the count that matters is words of five letters or more.
    """
    if n_long >= 320:
        return "full"
    if n_long >= 180:
        return "mid"
    return "mini"


def day_patterns(book, tier, day):
    if tier == "full":
        return book[day]
    if tier == "mid":
        if day == "monday":
            return book["monday"]
        if day == "sunday":
            return book["thursday"]
        return book["tuesday"]
    if day == "sunday":
        return book["tuesday"]
    return book["monday"]


def attempt_day(prefix, day, patterns, lib, words, min_exam, theme_sunday=False, min_content=1, minimum=8):
    size = len(patterns[0])
    node_cap, restarts = effort_for(size)
    floors = []
    for floor in (min_exam, 1, 0):
        if floor not in floors and floor <= min_exam:
            floors.append(floor)
    for floor in floors:
        made = make_day(
            day, patterns, lib, words, prefix, floor, node_cap, restarts,
            theme_sunday=theme_sunday, min_content=min_content, minimum=minimum,
        )
        if made:
            return made
        print(f"  {prefix} {day} retry with min_exam {floor} failed", flush=True)
    return None


def build_range(pack_id, tier, words, chapters, min_content, minimum=8):
    lib = Library(words)
    book = pattern_book()
    days = {}
    for day in WEEKDAYS:
        patterns = day_patterns(book, tier, day)
        min_exam = 1 if tier == "mini" else (4 if tier == "full" and day == "sunday" else 2)
        made = attempt_day(
            pack_id, day, patterns, lib, words, min_exam,
            theme_sunday=(day == "sunday"), min_content=min_content, minimum=minimum,
        )
        if not made and day == "sunday":
            fallback = book["monday"] if tier == "mini" else book["tuesday"]
            print(f"  {pack_id} sunday using a smaller grid", flush=True)
            made = attempt_day(pack_id, day, fallback, lib, words, 1, theme_sunday=True, min_content=1, minimum=minimum)
        if not made:
            print(f"skip {pack_id} {day} ({tier})", flush=True)
            return None
        if day == "sunday":
            larger = made[0]["size"] > days["saturday"][0]["size"]
            if not larger:
                for puzzle in made:
                    puzzle["blurb"] = "Sunday theme: vocabulary from the chapters in this puzzle."
                    puzzle["theme"] = "exam-vocabulary"
        days[day] = made
        print(f"{pack_id} {tier} {day} size {made[0]['size']}", flush=True)
    return {"chapters": chapters, "tier": tier, "days": days}


def validate_range(pack_id, pack, words):
    ct_marks = ("connecticut", "dcp", "psi ")
    tier = pack["tier"]
    allowed = set(pack["chapters"]) | {0}
    sizes = {}
    days = pack["days"]
    for day in WEEKDAYS:
        puzzles = days[day]
        need = 8 if pack_id in ("default", "all") else 4
        if len(puzzles) < need:
            raise SystemExit(f"{pack_id} {day} has {len(puzzles)}")
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
                if entry.get("chapter") != words[answer]["chapter"]:
                    raise SystemExit(f"chapter mismatch {puzzle['id']} {answer}")
                if entry["chapter"] not in allowed:
                    raise SystemExit(f"{puzzle['id']} uses chapter {entry['chapter']} for {answer}")
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
    if sizes["sunday"] < sizes["saturday"]:
        raise SystemExit(f"{pack_id} Sunday smaller than Saturday {sizes}")
    if tier == "full":
        if not (sizes["monday"] < sizes["tuesday"] <= sizes["wednesday"] < sizes["thursday"]):
            raise SystemExit(f"{pack_id} weekday sizes do not rise {sizes}")
        if not (sizes["saturday"] < sizes["sunday"]):
            raise SystemExit(f"{pack_id} Sunday must be larger than Saturday {sizes}")
    elif tier == "mini":
        if sizes["monday"] > 5 or sizes["saturday"] > 5:
            raise SystemExit(f"{pack_id} mini grid too big {sizes}")
    else:
        if not (sizes["monday"] < sizes["tuesday"] == sizes["saturday"]):
            raise SystemExit(f"{pack_id} mid sizes unexpected {sizes}")
    print("validated", pack_id, tier, {day: sizes[day] for day in WEEKDAYS})


def subset_for(words, chapters):
    allowed = set(chapters) | {0}
    return {word: meta for word, meta in words.items() if meta["chapter"] in allowed}


def main():
    from concurrent.futures import ProcessPoolExecutor, as_completed
    import os

    from course_units import apply_word_chapters, load_course

    course = load_course()
    words = load_words()
    apply_word_chapters(words, course)
    numbers = [row["n"] for row in course["chapters"]]
    print(f"clue bank {len(words)} words, {len(numbers)} chapters")
    jobs = []

    def queue(pack_id, chapters, min_content):
        subset = subset_for(words, chapters)
        n_long = sum(1 for word, meta in subset.items() if meta["chapter"] and len(word) >= 5)
        tier = "mini" if len(chapters) == 1 else ("full" if n_long >= 320 else "mid")
        print(f"queue {pack_id} tier={tier} words={len(subset)} long={n_long}")
        jobs.append((pack_id, tier, subset, chapters, min_content))

    for number in numbers:
        queue(str(number), [number], 1)
    queue("default", list(course["defaultCompleted"]), 2)
    queue("all", numbers, 2)

    packs = {}
    workers = min(4, os.cpu_count() or 2)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        future_map = {
            pool.submit(build_range, pack_id, tier, subset, chapters, min_content): pack_id
            for pack_id, tier, subset, chapters, min_content in jobs
        }
        for future in as_completed(future_map):
            pack_id = future_map[future]
            built = future.result()
            if built:
                packs[pack_id] = built
                print(f"finished {pack_id}", flush=True)
            else:
                print(f"no pack {pack_id}", flush=True)

    for pack_id, pack in packs.items():
        validate_range(pack_id, pack, words)
    if "default" not in packs or "all" not in packs:
        raise SystemExit("The default checklist pack and the all-chapters pack are required")

    payload = {
        "version": 3,
        "epoch": "2024-01-01",
        "defaultCompleted": course["defaultCompleted"],
        "note": (
            "Original puzzles for CT License Trail. Each pack uses course-chapter terms "
            "plus everyday filler. The default pack matches the starting checklist. "
            "The all pack uses every chapter. Single-chapter packs cover any other mix. "
            "The weekday and the week since Monday 2024-01-01 pick the grid. "
            "No newspaper puzzle, name, or branding is used."
        ),
        "packs": packs,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    total = sum(len(day_puzzles) for pack in packs.values() for day_puzzles in pack["days"].values())
    print(f"Wrote {total} puzzles in {len(packs)} packs to {OUT}")


if __name__ == "__main__":
    main()
