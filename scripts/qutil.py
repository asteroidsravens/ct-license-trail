"""Helpers for the CT License Trail question bank."""


def src(label, url):
    return {"label": label, "url": url}


CGS = "https://www.cga.ct.gov/current/pub/chap_392.htm"
CH223 = "https://www.cga.ct.gov/current/pub/chap_223.htm"
CH814 = "https://www.cga.ct.gov/current/pub/chap_814c.htm"
CH831 = "https://www.cga.ct.gov/current/pub/chap_831.htm"
CH822 = "https://www.cga.ct.gov/current/pub/chap_822.htm"
CH926 = "https://www.cga.ct.gov/current/pub/chap_926.htm"
DCP_EXAM = "https://portal.ct.gov/dcp/license-services-division/all-license-applications/real-estate-salesperson---initialexam"
DCP_CE = "https://portal.ct.gov/dcp/continuing-education/real-estate-salesperson---continuing-education"
DCP_FUND = "https://portal.ct.gov/dcp/common-elements/consumer-facts-and-contacts/real-estate-guaranty-fund"
PSI = "https://test-takers.psiexams.com/ctre"
REGS = "https://eregulations.ct.gov/eRegsPortal/Browse/getDocument?guid={600C4895-0000-C737-BB27-7C13924592E0}"
DOB_DEP = "https://portal.ct.gov/dob/rental-security-deposits/rental-security-deposits/rental-security-deposits"


def cgs(section, chapter_url=CGS):
    anchor = section.replace(" ", "")
    return src(f"Conn. Gen. Stat. § {section}", f"{chapter_url}#sec_{anchor}")


def rcsa(section):
    return src(f"Regs. Conn. State Agencies § {section}", REGS)


def item(topic, stem, correct, wrongs, explanation, source=None, math=False, steps=None, event=False, pools=None, chapter=None, ct_law=False, flavor=None):
    if len(wrongs) != 3:
        raise ValueError(f"Need 3 wrong answers: {stem[:90]}")
    choices = [correct, *wrongs]
    if len(set(choices)) != 4:
        raise ValueError(f"Duplicate choices: {stem[:90]}")
    if not explanation.strip():
        raise ValueError(f"Missing explanation: {stem[:90]}")
    return {
        "topic": topic,
        "stem": " ".join(stem.split()),
        "correct": correct,
        "wrongs": list(wrongs),
        "explanation": " ".join(explanation.split()),
        "source": source,
        "math": math,
        "steps": steps,
        "event": event,
        "pools": pools or [topic],
        "chapter": chapter,
        "ct_law": ct_law,
        "flavor": flavor,
    }
