#!/usr/bin/env python3
"""Course chapters for CT License Trail.

data/course.json is the editable chapter list. Names are topic tags only.
Do not add a school name or a book title. Do not copy or closely paraphrase
textbook wording, questions, glossary definitions, or figures. Questions,
clues, and definitions stay original and follow the PSI outline, Connecticut
statutes, and DCP sources. Words map each crossword answer to a chapter
number. Chapter 0 is not a course chapter: it marks everyday filler the grid
may use no matter which chapters are checked. Questions use chapters 1 through 21.

Rebuild the crossword library after chapter titles or word tags change:
python3 scripts/build_crosswords.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_PATH = ROOT / "data" / "course.json"

CHAPTERS = [
    {"n": 1, "name": "Introduction to the Real Estate Business"},
    {"n": 2, "name": "Real Property and the Law"},
    {"n": 3, "name": "Interests in Real Estate"},
    {"n": 4, "name": "Forms of Real Estate Ownership"},
    {"n": 5, "name": "Land Description"},
    {"n": 6, "name": "Transfer of Title"},
    {"n": 7, "name": "Title Records"},
    {"n": 8, "name": "Real Estate Brokerage"},
    {"n": 9, "name": "Real Estate Agency"},
    {"n": 10, "name": "Client Representation Agreement"},
    {"n": 11, "name": "Real Estate Contracts"},
    {"n": 12, "name": "Real Estate Financing"},
    {"n": 13, "name": "Government Involvement in Real Estate Financing"},
    {"n": 14, "name": "Closing the Real Estate Transaction"},
    {"n": 15, "name": "Real Estate Taxes and Other Liens"},
    {"n": 16, "name": "Real Estate Appraisal"},
    {"n": 17, "name": "Leases"},
    {"n": 18, "name": "Fair Housing"},
    {"n": 19, "name": "Property Management"},
    {"n": 20, "name": "Land Use Controls and Property Development"},
    {"n": 21, "name": "Environmental Issues in Real Estate"},
]

DEFAULT_COMPLETED = [2, 3, 6, 7, 14, 15, 16, 17, 20]

# Quiz topic id → chapter, used only when the wording does not match a rule.
TOPICS = {
    "ownership": 3,
    "landuse": 20,
    "valuation": 16,
    "financing": 12,
    "contracts": 11,
    "agency": 9,
    "disclosures": 21,
    "management": 19,
    "title": 6,
    "practice": 8,
    "ct-license": 1,
    "ct-conduct": 8,
    "ct-agency": 9,
    "ct-laws": 21,
    "math": 14,
}

# Hand-checked crossword answers. These win over the keyword rules.
PINS = {
    "DEED": 6,
    "TITLE": 6,
    "CONVEYANCE": 6,
    "GRANT": 6,
    "GRANTEE": 6,
    "GRANTOR": 6,
    "QUITCLAIM": 6,
    "WARRANTY": 6,
    "ABSTRACT": 7,
    "CHAIN": 7,
    "CLOUD": 7,
    "CLOUDED": 7,
    "MARKETABLE": 7,
    "LIEN": 15,
    "TAX": 15,
    "EASEMENT": 3,
    "ENCROACHMENT": 3,
    "FIFTEEN": 3,
    "FEE": 3,
    "FREEHOLD": 3,
    "FREEHOLDS": 3,
    "FEESIMPLE": 3,
    "LIFEESTATE": 3,
    "LIFE": 3,
    "ESTATE": 3,
    "OWNER": 4,
    "HEIR": 6,
    "LEASE": 17,
    "LEASEHOLD": 17,
    "RENT": 17,
    "TWENTYONE": 17,
    "AGENCY": 9,
    "AGENT": 9,
    "FIDUCIARY": 9,
    "BROKER": 8,
    "LISTING": 10,
    "NETLISTING": 10,
    "EARNEST": 11,
    "MORTGAGE": 12,
    "NOTE": 12,
    "LOAN": 12,
    "DEBT": 12,
    "APR": 12,
    "POINTS": 12,
    "POINT": 12,
    "APPRAISAL": 16,
    "VALUE": 16,
    "ESCROW": 14,
    "CLOSING": 14,
    "RIPARIAN": 2,
    "LOT": 5,
    "SIXTY": 1,
    "SEVENTY": 1,
    "EIGHTEEN": 1,
    "TWELVE": 1,
    "EIGHTY": 1,
    "TWENTYFIVE": 1,
    "TWENTY": 1,
    "SEVEN": 8,
    "THREE": 8,
    "FIVETHOUSAND": 8,
    "TRUST": 8,
    "COMMINGLE": 8,
    "CONVERSION": 8,
    "DUALAGENT": 9,
    "DUAL": 9,
    "SUBAGENCY": 9,
    "PRINCIPAL": 9,
    "FHA": 13,
    "VA": 13,
    "PITI": 12,
    "LTV": 12,
    "PMI": 12,
    "TILA": 12,
    "RESPA": 12,
    "TRID": 14,
    "CMA": 16,
    "GRM": 16,
    "NOI": 16,
    "CAPRATE": 16,
    "ADA": 18,
    "ECOA": 18,
    "HUD": 13,
    "MLS": 8,
    "HOA": 4,
    "CONDO": 4,
    "COOP": 4,
    "JOINT": 4,
    "COMMON": 4,
    "SEVERALTY": 4,
    "EMINENT": 20,
    "ESCHEAT": 20,
    "ZONING": 20,
    "VARIANCE": 20,
    "PLAT": 20,
    "DEVISE": 6,
    "WILL": 6,
    "PROBATE": 6,
    "INTESTATE": 6,
    "ADVERSE": 6,
    "HOSTILE": 6,
    "TACKING": 6,
    "NOTORIOUS": 6,
    "FIXTURE": 2,
    "CHATTEL": 2,
    "EMBLEMENTS": 2,
    "ACCRETION": 2,
    "METES": 5,
    "TOWNSHIP": 5,
    "SECTION": 5,
    "MONUMENTS": 5,
    "BENCHMARK": 5,
    "SURVEY": 5,
    "BINDER": 11,
    "OFFER": 11,
    "WAIVE": 11,
    "BUYER": 11,
    "SELLER": 11,
    "JUNIOR": 15,
    "SENIOR": 15,
    "PRIORITY": 15,
    "LISPENDENS": 15,
    "VOLUNTARY": 15,
    "COVENANT": 20,
    "COVENANTS": 20,
    "RUNWITH": 20,
    "IMPLIED": 3,
    "KICKBACK": 8,
    "PUFFING": 8,
    "PUFF": 8,
    "BLIND": 8,
    "DEFALCATE": 8,
    "DIVERSION": 8,
    "LENDER": 12,
    "FORECLOSE": 12,
    "AMORTIZE": 12,
    "BALLOON": 12,
    "USURY": 12,
    "REDEMPTION": 12,
    "EQUITY": 12,
    "LEVERAGE": 12,
    "STEERING": 18,
    "REDLINING": 18,
    "BLOCKBUSTING": 18,
    "EVICTION": 17,
    "LESSOR": 17,
    "LESSEE": 17,
    "TENANT": 17,
    "HOLDOVER": 17,
    "RADON": 21,
    "ASBESTOS": 21,
    "MOLD": 21,
    "LEAD": 21,
    "LATENT": 21,
    "PATENT": 21,
    "STIGMA": 21,
    "FLOOD": 21,
    "FEMA": 21,
    "ASIS": 21,
    "CAVEAT": 21,
    "APPURTENANT": 3,
    "PRESCRIPTIVE": 3,
    "DOMINANT": 3,
    "SERVIENT": 3,
    "MECHANICS": 15,
    "CURTESY": 3,
    "DOWER": 3,
    "REMAINDER": 3,
    "REVERSION": 3,
    "PUR": 3,
    "VIE": 3,
    "UNITY": 4,
    "PARTITION": 4,
    "SURVIVE": 4,
    "CAUSE": 8,
    "POWER": 9,
    "CLIENT": 9,
    "CUSTOMER": 9,
    "OBEDIENCE": 9,
    "READY": 12,
    "WILLING": 12,
    "ABLE": 12,
    "AREA": 5,
    "ACRE": 5,
    "PRORATE": 14,
    "PRORATION": 14,
    "ACCRUED": 14,
    "CREDIT": 14,
    "DEBIT": 14,
    "PREPAID": 14,
    "SPLIT": 8,
    "BASIS": 15,
    "SQUARE": 5,
    "VOLUME": 5,
    "COMPARABLES": 16,
    "COMPS": 16,
    "DEPRECIATE": 16,
    "CURABLE": 16,
    "INCURABLE": 16,
    "REPLACEMENT": 16,
    "REPRODUCTION": 16,
    "GROSSRENT": 16,
    "YIELD": 16,
    "MARKET": 16,
    "COST": 16,
    "PRICE": 16,
    "ESTIMATED": 16,
    "VALUATION": 16,
    "WORTH": 16,
    "CAP": 16,
    "ASSESS": 15,
    "ASSESSING": 15,
    "CONDEMN": 20,
    "PERMIT": 20,
    "COVERAGE": 20,
    "POLICE": 20,
    "FUNDS": 14,
    "INQUIRY": 21,
    "SMELL": 21,
    "ODOR": 21,
    "CRACK": 21,
    "LEAK": 21,
    "MONTH": 17,
    "PERIODIC": 17,
    "YEAR": 17,
    "NET": 17,
    "GROSS": 17,
    "LET": 17,
    "WASTE": 17,
    "KNOWN": 7,
    "BOOK": 7,
    "PAGE": 7,
    "DATE": 7,
    "STAMP": 7,
    "CLERK": 7,
    "CLEAR": 7,
    "QUIET": 7,
    "VENDOR": 6,
    "VENDEE": 6,
    "SEISIN": 6,
    "HABENDUM": 6,
    "ALIENATION": 6,
    "TESTAMENT": 6,
    "TESTATOR": 6,
    "TESTATRIX": 6,
    "CODICIL": 6,
    "LEGACY": 6,
    "FINE": 8,
    "POCKET": 10,
    "REF": 8,
    "INDEX": 12,
    "MARGIN": 12,
    "RATE": 12,
    "TEASER": 12,
    "TERM": 12,
    "SHORTSALE": 12,
    "ARREARS": 12,
    "DEFICIENCY": 12,
    "PREMIUM": 12,
    "HAZARD": 12,
    "DTI": 12,
    "GUARANTOR": 12,
    "CEILING": 12,
    "BORROW": 12,
    "ACCELERATE": 12,
    "REPAYMENT": 12,
    "ARM": 12,
    "BID": 12,
    "LIQUID": 12,
    "BOARD": 4,
    "BUDGET": 19,
    "BYLAWS": 4,
    "DUES": 4,
    "PROXY": 4,
    "QUORUM": 4,
    "VOTE": 4,
    "SHARE": 4,
    "UNEQUAL": 4,
    "SEVER": 4,
    "INTEREST": 4,
    "HEREDITAMENT": 3,
    "SITUS": 2,
    "TRADE": 2,
    "RELATION": 2,
    "AIRRIGHTS": 2,
    "ANNEXATION": 2,
    "SEVERANCE": 2,
    "PERSONALTY": 2,
    "REALTY": 2,
    "FRONTAGE": 5,
    "FRONTFOOT": 5,
    "AZIMUTH": 5,
    "BEARING": 5,
    "THENCE": 5,
    "FURLONG": 5,
    "ROD": 5,
    "RODS": 5,
    "HECTARE": 5,
    "LINK": 5,
    "RANGE": 5,
    "BUFFER": 20,
    "EARNESTMONEY": 11,
    "EMPTOR": 21,
    "ESCHEATED": 20,
    "FRUCTUS": 2,
    "NAVIGABLE": 2,
    "RELICTION": 2,
    "SEPTIC": 21,
    "SURVEYING": 5,
    "TRUSTEE": 4,
    "TRUSTOR": 12,
    "DEPTH": 5,
    "WIDTH": 5,
    "LENGTH": 5,
}

# First match wins.
RULES = [
    (21, r"lead[- ]based|lead paint|\bradon\b|asbestos|\bmold\b|environmental|underground storage|contaminat|wetland|hazardous waste|condition report|latent defect|patent defect|material defect|\bstigma\b"),
    (18, r"fair housing|blockbust|steering|redlin|protected class|familial status|discriminat|reasonable accommodation|disabilities act|\becoa\b"),
    (13, r"\bfha\b|va loan|ginnie mae|fannie mae|freddie mac|federal reserve|\bhud\b"),
    (11, r"\boffer\b|\bcounteroffer\b|statute of frauds"),
    (8, r"trust account|escrow account|commingl|antitrust|sherman act|blind ad|procuring cause|independent contractor|kickback|record retention|guaranty fund is not"),
    (10, r"listing agreement|buyer representation|exclusive right to sell|net listing|open listing|pocket listing"),
    (15, r"\blien\b|property tax|ad valorem|mill rate|special assessment|mechanic's lien|conveyance tax|judgment lien|tax lien"),
    (14, r"\bclosing\b|settlement statement|closing disclosure|\bprorat|good funds|debit to|credit to"),
    (12, r"mortgage|amortiz|promissory note|loan-to-value|\bltv\b|\bpiti\b|discount point|foreclos|regulation z|\btila\b|\brespa\b|\bapr\b|prepayment"),
    (16, r"apprais|\bcma\b|sales comparison|cost approach|income approach|cap rate|obsolescen|\bgrm\b|market value|depreciat|comparative market"),
    (17, r"\blease\b|lessor|lessee|\btenant\b|landlord|security deposit|evict|gross lease|net lease|percentage lease|holdover|tenancy at"),
    (19, r"property manager|management agreement|operating budget"),
    (20, r"zoning|variance|eminent domain|\bescheat\b|nonconforming|setback|police power|subdivision|building code|comprehensive plan|deed restriction|restrictive covenant|certificate of occupancy"),
    (9, r"\bagency\b|fiduciary|dual agency|designated agent|subagent|client and customer"),
    (1, r"salesperson exam|continuing[- ]education|classroom hours|passing score|minimum age|application fee|guaranty fund|principles and practice"),
    (11, r"\bcontract\b|statute of frauds|contingenc|\bearnest\b|option contract|\baddendum\b|specific performance|\boffer\b|\bcounteroffer\b"),
    (7, r"title insurance|chain of title|constructive notice|\brecording\b|abstract of title|cloud on title|marketable title|quiet title|title search"),
    (6, r"\bdeed\b|conveyance|grantor|grantee|quitclaim|adverse possession|warranty deed|intestate|\bprobate\b|transfer of title"),
    (5, r"metes and bounds|lot and block|rectangular survey|\btownship\b|legal description|\bmonument\b|\bbenchmark\b|square feet|\bacre\b|front foot"),
    (4, r"joint tenant|tenancy in common|tenancy by the entirety|severalty|condominium|cooperative|community property|right of survivorship|time-?share"),
    (3, r"easement|life estate|fee simple|freehold|encroach|prescriptive|remainderman|reversion|dower|curtesy|encumbrance"),
    (2, r"real property|personal property|\bfixture\b|riparian|littoral|accretion|avulsion|trade fixture|chattel|appurtenance|air rights|bundle of rights|emblement|subsurface"),
]


def chapter_numbers():
    return [row["n"] for row in CHAPTERS]


def classify_text(text):
    low = text.lower()
    for number, pattern in RULES:
        if re.search(pattern, low):
            return number
    return 0


def classify_word(word, straight, wordplay=""):
    del wordplay
    if word in PINS:
        return PINS[word]
    found = classify_text(f"{word} {straight}")
    return found


def classify_question(topic, stem, explanation=""):
    del explanation
    found = classify_text(stem)
    if found:
        return found
    mapped = TOPICS.get(topic)
    if not mapped:
        raise SystemExit(f"No course chapter for quiz topic {topic}")
    return mapped


def course_document(words):
    mapping = {}
    for word, meta in sorted(words.items()):
        mapping[word] = classify_word(word, meta["straight"], meta.get("wordplay") or "")
    return {
        "version": 2,
        "note": (
            "Course chapters for CT License Trail. Chapter titles are topic tags only. "
            "Do not add a school name or a book title. Do not copy or closely paraphrase textbook wording, questions, glossary definitions, or figures. "
            "Questions, clues, and definitions stay original and follow the PSI outline, Connecticut statutes, and DCP sources. "
            "The words map sends every crossword answer to a chapter number. "
            "Chapter 0 is everyday filler the crossword may use in any puzzle; it is not a course chapter. "
            "defaultCompleted is the checklist the app starts with. "
            "After you change chapters or word tags, run python3 scripts/build_crosswords.py."
        ),
        "chapters": CHAPTERS,
        "defaultCompleted": DEFAULT_COMPLETED,
        "topics": TOPICS,
        "words": mapping,
    }


def load_course():
    if not COURSE_PATH.exists():
        raise SystemExit(f"Missing {COURSE_PATH}")
    course = json.loads(COURSE_PATH.read_text(encoding="utf-8"))
    numbers = [row["n"] for row in course["chapters"]]
    if numbers != list(range(1, len(numbers) + 1)):
        raise SystemExit("course.json chapters must be numbered 1..N in order")
    known = set(numbers)
    bad_default = [n for n in course.get("defaultCompleted", []) if n not in known]
    if bad_default:
        raise SystemExit(f"defaultCompleted has unknown chapters: {bad_default}")
    return course


def apply_word_chapters(words, course=None):
    course = course or load_course()
    known = {row["n"] for row in course["chapters"]} | {0}
    missing = sorted(word for word in words if word not in course["words"])
    if missing:
        raise SystemExit("Crossword words missing a chapter in data/course.json: " + ", ".join(missing[:30]))
    bad = sorted(f"{word}->{chapter}" for word, chapter in course["words"].items() if chapter not in known)
    if bad:
        raise SystemExit("Unknown chapter numbers in course.json words: " + ", ".join(bad[:20]))
    for word, meta in words.items():
        meta["chapter"] = course["words"][word]
    return course


def stamp_questions(questions, course=None):
    course = course or load_course()
    known = {row["n"] for row in course["chapters"]}
    for question in questions:
        chapter = classify_question(question["topic"], question["stem"], question.get("explanation") or "")
        if chapter not in known:
            raise SystemExit(f"Bad chapter {chapter} on {question.get('id')}")
        question["chapter"] = chapter
        question.pop("unit", None)
    return questions


def main():
    import sys
    from collections import Counter

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from xword_bank import load_words

    words = load_words()
    doc = course_document(words)
    COURSE_PATH.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    counts = Counter(doc["words"].values())
    print(f"Wrote {COURSE_PATH} ({len(doc['words'])} words)")
    print(f"  filler chapter 0: {counts[0]}")
    for row in CHAPTERS:
        print(f"  ch {row['n']:2} {counts[row['n']]:4}  {row['name']}")

    bank_path = ROOT / "data" / "questions.json"
    if bank_path.exists():
        bank = json.loads(bank_path.read_text(encoding="utf-8"))
        stamp_questions(bank["questions"], doc)
        bank_path.write_text(json.dumps(bank, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        qcounts = Counter(q["chapter"] for q in bank["questions"])
        print(f"Stamped chapter on {len(bank['questions'])} questions")
        for row in CHAPTERS:
            print(f"  q ch {row['n']:2} {qcounts[row['n']]:4}")


if __name__ == "__main__":
    main()
