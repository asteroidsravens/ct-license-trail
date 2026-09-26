#!/usr/bin/env python3
"""Course syllabus for CT License Trail.

data/course.json is the editable syllabus. Replace `units` (in teaching order)
when a real syllabus arrives. `words` maps every crossword answer to a unit id.
`topics` maps each quiz topic id to a fallback unit. Rebuild the crossword
library after unit ids, order, or word tags change.

This module classifies the clue bank and the question bank. The committed
course.json map is what the crossword builder reads.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_PATH = ROOT / "data" / "course.json"

# Teaching order. Array order is the course order.
UNITS = [
    {"id": "land", "name": "Property and land basics"},
    {"id": "ownership", "name": "Ownership and estates"},
    {"id": "encumbrances", "name": "Encumbrances"},
    {"id": "title", "name": "Transfer of title and deeds"},
    {"id": "contracts", "name": "Contracts"},
    {"id": "agency", "name": "Agency"},
    {"id": "ct-agency", "name": "Connecticut agency law"},
    {"id": "fair-housing", "name": "Fair housing"},
    {"id": "financing", "name": "Financing"},
    {"id": "appraisal", "name": "Appraisal"},
    {"id": "math", "name": "Math"},
    {"id": "closing", "name": "Closing"},
    {"id": "land-use", "name": "Land use controls"},
    {"id": "leasing", "name": "Leasing and property management"},
    {"id": "disclosures", "name": "Property disclosures"},
    {"id": "practice", "name": "Brokerage practice"},
    {"id": "ct-license", "name": "Connecticut license law"},
]

# Quiz topic id → unit id, used when a question's wording does not match a more specific unit.
TOPICS = {
    "ownership": "ownership",
    "landuse": "land-use",
    "valuation": "appraisal",
    "financing": "financing",
    "contracts": "contracts",
    "agency": "agency",
    "disclosures": "disclosures",
    "management": "leasing",
    "title": "title",
    "practice": "practice",
    "ct-license": "ct-license",
    "ct-conduct": "ct-license",
    "ct-agency": "ct-agency",
    "ct-laws": "ct-license",
    "math": "math",
}

# Hand-checked answers. These win over keyword rules.
# A word that belongs in two units is tagged on the earlier one, because each
# crossword range includes that unit and everything before it.
PINS = {
    "DEED": "title",
    "LIEN": "encumbrances",
    "EASEMENT": "encumbrances",
    "TITLE": "title",
    "AGENCY": "agency",
    "APPRAISAL": "appraisal",
    "ESCROW": "closing",
    "RIPARIAN": "land",
    "CONVEYANCE": "title",
    "MORTGAGE": "financing",
    "ENCROACHMENT": "encumbrances",
    "FEE": "ownership",
    "FIDUCIARY": "agency",
    "EARNEST": "contracts",
    "LISTING": "agency",
    "NETLISTING": "ct-license",
    "SIXTY": "ct-license",
    "SEVENTY": "ct-license",
    "EIGHTEEN": "ct-license",
    "TWELVE": "ct-license",
    "EIGHTY": "ct-license",
    "SEVEN": "ct-license",
    "THREE": "ct-license",
    "TWENTYFIVE": "ct-license",
    "FIVETHOUSAND": "ct-license",
    "FIFTEEN": "encumbrances",
    "TWENTYONE": "leasing",
    "GRANT": "title",
    "GRANTEE": "title",
    "GRANTOR": "title",
    "TRUST": "practice",
    "AGENT": "agency",
    "LEASE": "leasing",
    "OWNER": "ownership",
    "TAX": "land-use",
    "APR": "financing",
    "LOT": "land",
    "RENT": "leasing",
    "NOTE": "financing",
    "LOAN": "financing",
    "DEBT": "financing",
    "HEIR": "ownership",
    "CLOSING": "closing",
    "FEESIMPLE": "ownership",
    "FREEHOLD": "ownership",
    "FREEHOLDS": "ownership",
    "LIFEESTATE": "ownership",
    "LIFE": "ownership",
    "SEVERALTY": "ownership",
    "CONDO": "ownership",
    "COOP": "ownership",
    "REMAINDER": "ownership",
    "REVERSION": "ownership",
    "UNITY": "ownership",
    "JOINT": "ownership",
    "COMMON": "ownership",
    "PARTITION": "ownership",
    "DEVISE": "ownership",
    "WILL": "ownership",
    "PROBATE": "ownership",
    "INTESTATE": "ownership",
    "TESTAMENT": "ownership",
    "TESTATOR": "ownership",
    "TESTATRIX": "ownership",
    "CODICIL": "ownership",
    "INTEREST": "ownership",
    "HEREDITAMENT": "ownership",
    "HOA": "ownership",
    "BYLAWS": "ownership",
    "CURTESY": "ownership",
    "DOWER": "ownership",
    "LEASEHOLD": "ownership",
    "EMBLEMENTS": "land",
    "TRADE": "land",
    "RELATION": "land",
    "SITUS": "land",
    "PRINCIPAL": "agency",
    "IMPLIED": "encumbrances",
    "REPAYMENT": "financing",
    "CAUSE": "agency",
    "BROKER": "agency",
    "DUAL": "agency",
    "DUALAGENT": "ct-agency",
    "SUBAGENCY": "agency",
    "COMMINGLE": "practice",
    "CONVERSION": "practice",
    "DEFALCATE": "practice",
    "FEMA": "disclosures",
    "VALUE": "appraisal",
    "COVENANT": "title",
    "COVENANTS": "encumbrances",
    "JUNIOR": "encumbrances",
    "SENIOR": "encumbrances",
    "PRIORITY": "encumbrances",
    "VOLUNTARY": "encumbrances",
    "LISPENDENS": "encumbrances",
    "ADVERSE": "title",
    "HOSTILE": "title",
    "NOTORIOUS": "title",
    "TACKING": "title",
    "LENDER": "financing",
    "KICKBACK": "financing",
    "TRID": "financing",
    "POINTS": "financing",
    "POINT": "financing",
    "CAPRATE": "appraisal",
    "RUNWITH": "encumbrances",
    "POWER": "agency",
    "ABLE": "financing",
    "ACCELERATE": "financing",
    "BALLOON": "financing",
    "BORROW": "financing",
    "CEILING": "financing",
    "DTI": "financing",
    "EQUITY": "financing",
    "GUARANTOR": "financing",
    "INDEX": "financing",
    "LEVERAGE": "financing",
    "MARGIN": "financing",
    "RATE": "financing",
    "REDEMPTION": "financing",
    "TEASER": "financing",
    "TERM": "financing",
    "SHORTSALE": "financing",
    "USURY": "financing",
    "ARREARS": "financing",
    "DEFICIENCY": "financing",
    "PREMIUM": "financing",
    "HAZARD": "financing",
    "FLOOD": "disclosures",
    "ASIS": "disclosures",
    "CAVEAT": "disclosures",
    "EMPTOR": "disclosures",
    "LATENT": "disclosures",
    "PATENT": "disclosures",
    "STIGMA": "disclosures",
    "LEAD": "disclosures",
    "MOLD": "disclosures",
    "ODOR": "disclosures",
    "CRACK": "disclosures",
    "LEAK": "disclosures",
    "BLIND": "practice",
    "DIVERSION": "practice",
    "PUFF": "practice",
    "POCKET": "practice",
    "MLS": "practice",
    "ASSESS": "land-use",
    "ASSESSING": "land-use",
    "CONDEMN": "land-use",
    "PERMIT": "land-use",
    "ACCRUED": "closing",
    "HUD": "closing",
    "CREDIT": "closing",
    "DEBIT": "closing",
    "PREPAID": "math",
    "AREA": "math",
    "BASIS": "math",
    "SPLIT": "math",
    "VOLUME": "math",
    "COMPARABLES": "appraisal",
    "DEPRECIATE": "appraisal",
    "CURABLE": "appraisal",
    "INCURABLE": "appraisal",
    "REPLACEMENT": "appraisal",
    "REPRODUCTION": "appraisal",
    "GROSSRENT": "appraisal",
    "YIELD": "appraisal",
    "MARKET": "appraisal",
    "COST": "appraisal",
    "BOARD": "ownership",
    "BUDGET": "ownership",
    "DUES": "ownership",
    "PROXY": "ownership",
    "QUORUM": "ownership",
    "SEVER": "ownership",
    "SHARE": "ownership",
    "VOTE": "ownership",
    "UNEQUAL": "ownership",
    "SURVIVE": "ownership",
    "BOOK": "title",
    "ABSTRACT": "title",
    "CHAIN": "title",
    "CLOUD": "title",
    "CLOUDED": "title",
    "QUITCLAIM": "title",
    "WARRANTY": "title",
    "MARKETABLE": "title",
    "VENDOR": "title",
    "VENDEE": "title",
    "CLEAR": "title",
    "QUIET": "title",
    "PAGE": "title",
    "DATE": "title",
    "STAMP": "title",
    "CLERK": "title",
    "ESTATE": "ownership",
    "BINDER": "contracts",
    "BUYER": "contracts",
    "SELLER": "contracts",
    "WAIVE": "contracts",
    "COMPS": "appraisal",
    "ESTIMATED": "appraisal",
    "VALUATION": "appraisal",
    "WORTH": "appraisal",
    "PRICE": "appraisal",
    "COVERAGE": "land-use",
    "EMINENT": "land-use",
    "POLICE": "land-use",
    "FUNDS": "closing",
    "INQUIRY": "disclosures",
    "SMELL": "disclosures",
    "LEGACY": "ownership",
    "LIQUID": "financing",
    "MONTH": "leasing",
    "PERIODIC": "leasing",
    "READY": "financing",
    "WILLING": "financing",
    "KNOWN": "title",
    "SQUARE": "math",
    "MONUMENTS": "land",
    "THENCE": "land",
    "BID": "financing",
    "FED": "land",
}

# First match wins. More specific units come before broad ones.
RULES = [
    ("ct-license", r"connecticut|dcp\b|psi\b|guaranty fund|continuing education|net listing|salesperson exam|real estate commission|licensee|licensure|license law"),
    ("ct-agency", r"designated agent|dual agency|unrepresented|first personal meeting|agency disclosure|subagency|designated agency"),
    ("fair-housing", r"fair housing|protected class|redlin|steering|blockbust|familial status|reasonable accommodation|equal housing|civil rights act|discriminat"),
    ("disclosures", r"material fact|lead[- ]based|lead paint|radon|asbestos|latent defect|patent defect|stigmat|seller disclosure|property condition|red flag|megans"),
    ("financing", r"mortgage|hypothec|amortiz|discount point|promissory|prepayment|underwrit|regulation z|\btila\b|\brespa\b|\bfha\b|\bpiti\b|loan-to-value|\bltv\b|foreclos|secondary mortgage|primary mortgage|alienation clause|acceleration|defeasance clause|usury|equity of redemption|statutory redemption"),
    ("appraisal", r"apprais|market value|sales comparison|cost approach|income approach|capitalization|cap rate|obsolescen|reproduction cost|replacement cost|\bcma\b|comparative market|gross rent multiplier|\bgrm\b|depreciation"),
    ("math", r"\bprorat|commission split|square foot|cubic|front foot|\bacreage\b|area of|percentage lease math|mill rate math"),
    ("closing", r"\bclosing\b|settlement statement|closing disclosure|walk-?through|escrow|good funds|proration at"),
    ("land-use", r"zoning|variance|nonconforming|setback|eminent domain|condemnation|escheat|ad valorem|special assessment|police power|building code|comprehensive plan|subdivision|plat map|buffer|spot zon|downzon|conditional use|special use|certificate of occupancy|\bc of o\b|property tax|mill rate|assessed value"),
    ("leasing", r"\blease\b|lessor|lessee|\btenant\b|landlord|security deposit|evict|property manager|gross lease|net lease|percentage lease|sublet|assignment of lease|holdover|periodic tenancy|estate for years|tenancy at will|tenancy at sufferance"),
    ("practice", r"antitrust|sherman|price fix|group boycott|tie-in|advertis|puffing|blind ad|referral fee|kickback|commingl|conversion of funds|trust account|escrow account|do not call|telemarket|can-spam|independent contractor|code of ethics|procuring cause"),
    ("contracts", r"\bcontract\b|\boffer\b|acceptance|consideration|statute of frauds|contingenc|addendum|amendment|bilateral|unilateral|\bvoid\b|voidable|executory|executed contract|specific performance|liquidated|earnest|option contract|resciss|novation|counteroffer|meeting of the minds|competent part|legal purpose|\bvalid contract\b|breach"),
    ("agency", r"\bagency\b|\bagent\b|fiduciary|principal|procuring|client and customer|special agent|general agent|universal agent|single agency|transaction broker|listing agreement|buyer representation|obedience|loyalty"),
    ("encumbrances", r"encumbrance|easement|encroach|\blien\b|servient|dominant estate|prescriptive|prescription|restrictive covenant|deed restriction|appurtenant|easement in gross|mechanic|judgment lien|attachment|lis pendens|profit a prendre|party wall|license to use"),
    ("title", r"\bdeed\b|\btitle\b|convey|grantor|grantee|quitclaim|warranty deed|habendum|acknowledgment|recording|constructive notice|actual notice|chain of title|abstract of title|title insurance|cloud on title|quiet title|alienation|adverse possession|devise|intestate|probate|marketable title|seisin|delivery and acceptance|voluntary alienation|involuntary alienation"),
    ("ownership", r"fee simple|life estate|freehold|leasehold estate|remainderman|reversion|joint tenant|tenancy in common|tenancy by the entirety|severalty|community property|condominium|cooperative|time-?share|bundle of rights|dower|curtesy|homestead|pur autre vie|defeasible|estate in severalty|right of survivorship"),
    ("land", r"real property|personal property|fixture|trade fixture|riparian|littoral|accretion|avulsion|erosion|reliction|appurtenance|air rights|subsurface|mineral right|water right|metes|bounds|lot and block|rectangular survey|township|section|monument|chattel|emblement|fructus|immobilit|heterogen|situs|improvement|real estate|legal description|benchmark|datum|encroachment wait"),
]

# Quiz items in mixed topics. Checked before the topic fallback. Math stays math.
QUESTION_OVERRIDES = {
    "ownership": [
        ("land", r"fixture|riparian|littoral|personal property|real property|metes|bounds|appurtenance|emblement|trade fixture|chattel|accretion|avulsion|legal description|air rights"),
        ("encumbrances", r"easement|encumbrance|encroach|\blien\b|restrictive covenant|deed restriction|prescriptive"),
    ],
    "title": [
        ("closing", r"closing statement|settlement statement|\bescrow\b|proration"),
    ],
    "practice": [
        ("fair-housing", r"fair housing|blockbust|steering|redlin|protected class|familial status|discriminat"),
    ],
    "ct-laws": [
        ("fair-housing", r"fair housing|blockbust|steering|redlin|protected class|familial status|discriminat"),
        ("leasing", r"security deposit|landlord|tenant"),
        ("closing", r"conveyance tax"),
        ("disclosures", r"condition report|material fact|disclosure|lead"),
        ("land-use", r"zoning|eminent|property tax|conveyance"),
    ],
    "ct-conduct": [
        ("practice", r"advertis|blind ad"),
    ],
    "financing": [
        ("closing", r"closing disclosure"),
    ],
    "landuse": [
        ("encumbrances", r"deed restriction|restrictive covenant|easement"),
    ],
}


def unit_ids():
    return [unit["id"] for unit in UNITS]


def classify_word(word, straight, wordplay=""):
    """Tag a crossword answer.

    Wordplay is ignored on purpose. Many jokes say the answer is "not" some
    later-unit term, and that would file glue words too early in the course.
    """
    del wordplay
    if word in PINS:
        return PINS[word]
    text = f"{word} {straight}".lower()
    for unit, pattern in RULES:
        if re.search(pattern, text):
            return unit
    return "land"


def classify_question(topic, stem, explanation=""):
    if topic == "math":
        return "math"
    text = f"{stem} {explanation}".lower()
    for unit, pattern in QUESTION_OVERRIDES.get(topic, []):
        if re.search(pattern, text):
            return unit
    mapped = TOPICS.get(topic)
    if not mapped:
        raise SystemExit(f"No course unit for quiz topic {topic}")
    return mapped


def course_document(words):
    mapping = {}
    for word, meta in sorted(words.items()):
        mapping[word] = classify_word(word, meta["straight"], meta.get("wordplay") or "")
    return {
        "version": 1,
        "note": (
            "Editable syllabus for CT License Trail. Units are in teaching order. "
            "Replace this list with a real course outline when you have one; keep each id stable "
            "or retag words and questions to the new ids. The words map sends every crossword answer "
            "to one unit. The topics map is the fallback for quiz questions. "
            "Daily crosswords use a prebuilt library for each unit and every unit before it. "
            "After you change units, order, or word tags, run python3 scripts/build_crosswords.py."
        ),
        "units": UNITS,
        "topics": TOPICS,
        "words": mapping,
    }


def load_course():
    if not COURSE_PATH.exists():
        raise SystemExit(f"Missing {COURSE_PATH}")
    course = json.loads(COURSE_PATH.read_text(encoding="utf-8"))
    ids = [unit["id"] for unit in course["units"]]
    if len(ids) != len(set(ids)):
        raise SystemExit("Duplicate unit id in course.json")
    if not ids:
        raise SystemExit("course.json has no units")
    return course


def apply_word_units(words, course=None):
    course = course or load_course()
    known = {unit["id"] for unit in course["units"]}
    missing = sorted(word for word in words if word not in course["words"])
    if missing:
        raise SystemExit("Crossword words missing a unit in data/course.json: " + ", ".join(missing[:30]))
    bad = sorted(f"{word}->{unit}" for word, unit in course["words"].items() if unit not in known)
    if bad:
        raise SystemExit("Unknown unit ids in course.json words: " + ", ".join(bad[:20]))
    for word, meta in words.items():
        meta["unit"] = course["words"][word]
    return course


def stamp_questions(questions, course=None):
    course = course or load_course()
    topics = course["topics"]
    known = {unit["id"] for unit in course["units"]}
    for question in questions:
        unit = question.get("unit")
        if not unit:
            unit = classify_question(question["topic"], question["stem"], question.get("explanation") or "")
        if unit not in known and unit not in topics.values():
            raise SystemExit(f"Bad unit {unit} on {question.get('id')}")
        if unit not in known:
            raise SystemExit(f"Unit {unit} is not in the syllabus")
        question["unit"] = unit
    return questions


def main():
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from xword_bank import load_words

    words = load_words()
    doc = course_document(words)
    COURSE_PATH.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    ids = unit_ids()
    counts = {unit: 0 for unit in ids}
    threes = {unit: 0 for unit in ids}
    long = {unit: 0 for unit in ids}
    for word, unit in doc["words"].items():
        counts[unit] += 1
        if len(word) == 3:
            threes[unit] += 1
        if len(word) >= 5:
            long[unit] += 1
    print(f"Wrote {COURSE_PATH} ({len(doc['words'])} words)")
    running = running3 = running5 = 0
    for unit in ids:
        running += counts[unit]
        running3 += threes[unit]
        running5 += long[unit]
        print(f"  {unit:16} {counts[unit]:4}  3s {threes[unit]:3}  >=5 {long[unit]:3}  cum {running:4} / {running3} threes / {running5} long")
    land_exam = []
    for word, meta in words.items():
        if doc["words"][word] == "land" and meta["exam"] and len(word) >= 5:
            land_exam.append(f"{word}: {meta['straight']}")
    print(f"land exam words length>=5: {len(land_exam)}")
    for line in sorted(land_exam):
        print("   ", line)

    bank_path = ROOT / "data" / "questions.json"
    if bank_path.exists():
        bank = json.loads(bank_path.read_text(encoding="utf-8"))
        stamp_questions(bank["questions"], doc)
        bank_path.write_text(json.dumps(bank, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Stamped unit on {len(bank['questions'])} questions")


if __name__ == "__main__":
    main()
