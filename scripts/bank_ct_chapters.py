"""Connecticut law questions tagged to course chapters.

Chapter titles are topic tags. These items are original and cite official
Connecticut statutes, regulations, or agency pages. Scene lines are flavor
only; they do not state the rule.
"""

from qutil import cgs, rcsa, item, CH814, CH831, CH223, CH822, CH926

CH821 = "https://www.cga.ct.gov/current/pub/chap_821.htm"
CH124 = "https://www.cga.ct.gov/current/pub/chap_124.htm"
CH440 = "https://www.cga.ct.gov/current/pub/chap_440.htm"
CH134 = "https://www.cga.ct.gov/current/pub/chap_134.htm"
CH923 = "https://www.cga.ct.gov/current/pub/chap_923.htm"


def scene(outdoors, adventure, history):
    return {"outdoors": outdoors, "adventure": adventure, "history": history}


def law(topic, chapter, stem, correct, wrongs, explanation, source, event=False, pools=None, flavor=None):
    return item(
        topic, stem, correct, wrongs, explanation, source,
        event=event, pools=pools or ["ct-laws"], chapter=chapter, ct_law=True, flavor=flavor,
    )


def ct_chapter_questions():
    q = []
    A = q.append

    A(law("ct-license", 1,
        "Section 20-314(c) lets the commission or commissioner waive an examination portion when a person passed the national testing-service exam in another state within two years and the score is accepted. Which portion may be waived?",
        "The uniform portion, not the Connecticut state portion",
        ["The Connecticut state portion, automatically",
         "Both portions, if the person once held any out-of-state license",
         "Neither portion; the statute has no waiver"],
        "The statute allows a waiver of the uniform portion only. A satisfactory out-of-state national score does not, by itself, waive the Connecticut state portion.",
        cgs("20-314"), event=True,
        pools=["ct-license"],
        flavor=scene(
            "At a picnic table beside a boat launch, a friend asks about an out-of-state exam score.",
            "Between two road stops, a rider asks about an out-of-state exam score.",
            "On the steps of an old town hall, a newcomer asks about an out-of-state exam score.",
        )))

    A(law("ct-license", 1,
        "DCP's salesperson page separates sitting for the exam from activating the license. Which statement matches that page?",
        "Broker supervision is not required to take the exam, and it is required to activate the license",
        ["Broker supervision is required before the exam may be scheduled",
         "Activation does not require a Connecticut broker",
         "The exam itself issues the license the same day"],
        "DCP states that broker supervision is not required to take the examination. Activation requires supervision by a Connecticut-licensed broker and payment of the license fee.",
        cgs("20-314"),
        pools=["ct-license"],
        flavor=scene(
            "Under a trail shelter, someone asks when a supervising broker has to be in place.",
            "At a roadside pull-off, someone asks when a supervising broker has to be in place.",
            "In a mill-town library, someone asks when a supervising broker has to be in place.",
        )))

    A(law("ownership", 3,
        "A path across a neighbor's lot has been used as a right-of-way. Under section 47-37, that use does not ripen into an easement unless it has continued uninterrupted for:",
        "15 years",
        ["5 years", "7 years", "21 years"],
        "Section 47-37 says no person may acquire a right-of-way or other easement by adverse use unless the use has continued uninterrupted for fifteen years.",
        cgs("47-37", CH822), event=True,
        flavor=scene(
            "On a woods path between two lots, a hiker asks how long a crossing must last.",
            "On a dirt track between two camps, a rider asks how long a crossing must last.",
            "Beside a stone wall that divides two old farms, a neighbor asks how long a crossing must last.",
        )))

    A(law("ownership", 3,
        "Section 52-575 is the statute tied to how long someone has to enter upon land. That period is:",
        "15 years",
        ["10 years", "20 years", "30 years"],
        "Section 52-575 requires entry upon land to be made within fifteen years. That is the period associated with an adverse-possession claim in Connecticut.",
        cgs("52-575", CH926),
        flavor=scene(
            "At a field edge, a landowner asks about the time limit for entering on land.",
            "At a trail junction, a landowner asks about the time limit for entering on land.",
            "By an old boundary oak, a landowner asks about the time limit for entering on land.",
        )))

    A(law("ownership", 4,
        "A deed runs to two people and adds the words \"as joint tenants\" after their names. Under section 47-14a, that form creates:",
        "A joint tenancy in fee simple with right of survivorship",
        ["A tenancy in common with no survivorship, because Connecticut never allows survivorship",
         "A tenancy at will",
         "A lease for years"],
        "Section 47-14a says a conveyance that runs to the grantees as joint tenants, or with the words \"as joint tenants\" after their names, creates a joint tenancy in fee simple with right of survivorship. The same section allows equal or unequal shares.",
        cgs("47-14a", CH821), event=True,
        flavor=scene(
            "At a lakeside cottage, two buyers ask what those deed words do.",
            "At a trailhead parking lot, two buyers ask what those deed words do.",
            "In a colonial deed office, two buyers ask what those deed words do.",
        )))

    A(law("ownership", 4,
        "Two joint tenants want to convey the estate they hold together. Section 47-14b says they may do that:",
        "By an instrument executed by all of them, subject to section 47-14e",
        ["By a text message from either one of them",
         "Only by dying and letting survivorship work",
         "Only if a court first converts them to tenants by the entirety"],
        "Subject to section 47-14e, section 47-14b lets joint tenants convey or encumber the estate they hold, or a portion of it, by an instrument executed by all of them, in the same manner as if they held as tenants in common.",
        cgs("47-14b", CH821),
        flavor=scene(
            "On a porch overlooking a marsh, co-owners ask how they can deed the place.",
            "At a camp clearing, co-owners ask how they can deed the place.",
            "In a historic probate office, co-owners ask how they can deed the place.",
        )))

    A(law("title", 5,
        "An affidavit of facts that may affect title is recorded under section 47-12a. The affidavit must include:",
        "A description of the land and the name of the record owner at the time of recording",
        ["Only the affiant's phone number",
         "The buyer's loan estimate",
         "A waiver of all future taxes"],
        "Section 47-12a(c) requires every such affidavit to describe the land whose title may be affected and to name the person who appears of record as the owner when the affidavit is recorded. The town clerk indexes it in that owner's name.",
        cgs("47-12a", CH821), event=True,
        flavor=scene(
            "At a survey stake in the woods, someone asks what a title affidavit has to identify.",
            "On a ridge trail, someone asks what a title affidavit has to identify.",
            "At a town vault of old maps, someone asks what a title affidavit has to identify.",
        )))

    A(law("title", 5,
        "Section 47-12a(b) lists matters a recorded title affidavit may cover. One of them is:",
        "Conflicts and ambiguities in the description of land in recorded instruments",
        ["The salesperson's commission split",
         "A lender's internal underwriting notes",
         "A neighbor's opinion of the paint color"],
        "Subsection (b) allows affidavits about conflicts and ambiguities in description, along with facts such as heirship, marital status, possession, and adverse use. The affidavit still has to describe the land.",
        cgs("47-12a", CH821),
        flavor=scene(
            "Looking at two overlapping lot sketches outdoors, a reader asks what an affidavit can clear up.",
            "Comparing two trail maps, a reader asks what an affidavit can clear up.",
            "Comparing two handwritten deeds, a reader asks what an affidavit can clear up.",
        )))

    A(law("title", 6,
        "Section 47-5(a) says a conveyance of land in Connecticut must be attested by:",
        "Two witnesses, with their own hands",
        ["No witnesses, if a notary signs",
         "One witness",
         "The town clerk only, with no other formality"],
        "Section 47-5(a) requires a conveyance of land to be in writing, subscribed by the grantor or a proper agent, acknowledged, and attested by two witnesses with their own hands.",
        cgs("47-5", CH821), event=True,
        flavor=scene(
            "At an outdoor closing table, the grantor asks how many people must witness the deed.",
            "At a trail lodge used as a signing spot, the grantor asks how many people must witness the deed.",
            "In a nineteenth-century clerk's room, the grantor asks how many people must witness the deed.",
        )))

    A(law("title", 6,
        "An acknowledgment of a Connecticut deed is taken inside this state. Section 47-5a allows it to be taken before:",
        "A notary public, or a town clerk or assistant town clerk, among other listed officers",
        ["Only a judge of the Connecticut Supreme Court",
         "Any neighbor who watches the signing",
         "The listing salesperson, because of the license"],
        "Section 47-5a lists who may take an in-state acknowledgment, including a notary public and a town clerk or assistant town clerk. The officer acts only inside the territory of that office.",
        cgs("47-5a", CH821),
        flavor=scene(
            "Under a park pavilion, a signer asks who in town can take the acknowledgment.",
            "At a ranger station, a signer asks who in town can take the acknowledgment.",
            "At a historic town clerk's counter, a signer asks who can take the acknowledgment.",
        )))

    A(law("title", 7,
        "A deed is signed and delivered but never recorded. Against whom does section 47-10(a) say that unrecorded conveyance still holds the land?",
        "The grantor and the grantor's heirs, but not other people",
        ["Every later buyer in the state, automatically",
         "Only the town tax collector",
         "No one, including the grantor"],
        "Section 47-10(a) says no conveyance is effectual to hold land against any person other than the grantor and the grantor's heirs unless it is recorded on the records of the town where the land lies.",
        cgs("47-10", CH821), event=True,
        flavor=scene(
            "On a bluff above the lot, a buyer asks what happens if the deed stays in a drawer.",
            "On a long dirt road, a buyer asks what happens if the deed stays in a drawer.",
            "In a courthouse hallway, a buyer asks what happens if the deed stays in a drawer.",
        )))

    A(law("title", 7,
        "A deed is signed by an agent under a power of attorney. Section 47-10(a) says the power of attorney:",
        "Must be recorded with the deed, unless it is already on the town land records and the deed refers to it",
        ["Never has to be recorded",
         "Is recorded only with the Secretary of the State, never in the town",
         "Replaces the need for any deed"],
        "When a conveyance is executed by a power of attorney, section 47-10(a) requires the power to be recorded with the deed unless it was already recorded in that town and the deed refers to it.",
        cgs("47-10", CH821),
        flavor=scene(
            "At a campsite signing, an agent asks where the power of attorney has to be filed.",
            "At a ferry landing, an agent asks where the power of attorney has to be filed.",
            "In an old land-records vault, an agent asks where the power of attorney has to be filed.",
        )))

    A(law("ct-conduct", 8,
        "A broker's advertisement offers someone else's house and never shows that a broker is involved. Regulation 20-328-5a(c) treats that ad as:",
        "Prohibited, because it looks like a private party who is not in the real estate business is offering the property",
        ["Required, so the seller's name can stay private",
         "Allowed if the price is accurate",
         "Allowed when the ad is only on paper, not online"],
        "The regulation says a broker shall not advertise in a manner that indicates a private party not engaged in the real estate business is making the offer. The broker also must not advertise without disclosing the broker's name.",
        rcsa("20-328-5a"), event=True,
        pools=["ct-conduct"],
        flavor=scene(
            "At a trailhead bulletin board, a posted house ad has no brokerage name.",
            "On a roadhouse wall, a posted house ad has no brokerage name.",
            "On a historic green, a posted house ad has no brokerage name.",
        )))

    A(law("ct-conduct", 8,
        "A licensee receives a deposit on a deal the licensee is handling for the affiliated broker. Regulation 20-328-7a(a) says the licensee shall:",
        "Promptly pay that deposit over to the broker",
        ["Keep it in a personal account until the inspection is done",
         "Cash it and pay the seller the same hour",
         "Mail it to the Real Estate Commission"],
        "The regulation requires a licensee who receives a deposit on a transaction for the affiliated broker to promptly pay that deposit over to the broker.",
        rcsa("20-328-7a"),
        pools=["ct-conduct"],
        flavor=scene(
            "At a lakeside showing, a buyer hands over a deposit check.",
            "At a mountain pull-off, a buyer hands over a deposit check.",
            "On a town-green bench, a buyer hands over a deposit check.",
        )))

    A(law("ct-agency", 9,
        "The listing has ended. The former client does not want the reason for selling repeated. Section 20-325h generally tells the licensee:",
        "Not to reveal or use that confidential information, with narrow exceptions such as legal process, a defense to a claim of wrongful conduct, or preventing a crime",
        ["To post the reason in the next advertisement",
         "To tell every new buyer, because the listing is over",
         "To keep the secret only until the next open house"],
        "Section 20-325h bars revealing or using confidential information of a person the licensee represented, except when legal process requires it, when the licensee is defending against allegations of wrongful or negligent conduct, or when the disclosure would prevent a crime.",
        cgs("20-325h"), event=True,
        pools=["ct-agency"],
        flavor=scene(
            "On a quiet stretch of trail, a former client asks that a private reason stay private.",
            "After a long ride, a former client asks that a private reason stay private.",
            "Outside an old meetinghouse, a former client asks that a private reason stay private.",
        )))

    A(law("ct-agency", 9,
        "Section 20-325f addresses subagency in a Connecticut sale or purchase. The statute says a broker:",
        "Shall not make a unilateral offer of subagency or agree to compensate or affiliate with a subagent",
        ["Must offer subagency in every listing",
         "May offer subagency if the commission is under 3 percent",
         "May offer subagency only for land over ten acres"],
        "Section 20-325f says no broker shall make any unilateral offer of subagency or agree to compensate, appoint, employ, cooperate with, or otherwise affiliate with a subagent for the sale or purchase of real property.",
        cgs("20-325f"),
        pools=["ct-agency"],
        flavor=scene(
            "At a campfire, two licensees argue about offering subagency.",
            "At a trail junction, two licensees argue about offering subagency.",
            "In a historic brokerage office, two licensees argue about offering subagency.",
        )))

    A(law("ct-conduct", 10,
        "Before a licensee negotiates a non-commercial sale for an owner, regulation 20-328-6a(a)(1) requires:",
        "A written listing that identifies the property, states the commission, and has a start date and an expiration date",
        ["An oral listing, if a friend heard it",
         "Only a text that names the asking price",
         "A recorded deed before any showing"],
        "The regulation requires that written listing before the licensee negotiates a non-commercial sale, exchange, or lease for the owner. The owner and the broker, or the broker's authorized agent, sign it.",
        rcsa("20-328-6a"), event=True,
        pools=["ct-conduct"],
        flavor=scene(
            "On a cabin porch, an owner asks whether a handshake listing is enough.",
            "At a trail register, an owner asks whether a handshake listing is enough.",
            "In a colonial parlor, an owner asks whether a handshake listing is enough.",
        )))

    A(law("ct-conduct", 10,
        "A written agreement sets the broker's pay. Section 20-325b requires a notice, in bold or equally conspicuous type, immediately before the compensation clause. The notice says:",
        "The amount or rate of broker compensation is not fixed by law and may be negotiable",
        ["Connecticut sets every residential commission at 6 percent",
         "The deposit becomes the fee on the third banking day",
         "Oral agreements are enough if the rate is fair"],
        "Section 20-325b requires that notice in not less than ten-point boldface type, or another way that stands out, immediately before the compensation provision.",
        cgs("20-325b"),
        pools=["ct-conduct"],
        flavor=scene(
            "At a picnic-table signing, a client points at the pay paragraph.",
            "At a roadside inn, a client points at the pay paragraph.",
            "At a clerk's high desk, a client points at the pay paragraph.",
        )))

    A(law("contracts", 11,
        "A civil action is brought on an agreement for the sale of real property. Section 52-550(a)(4) says the action may be maintained only if:",
        "The agreement, or a memorandum of it, is in writing and signed by the party to be charged, or that party's agent",
        ["The parties shook hands in front of two neighbors",
         "The price was fair, even with nothing in writing",
         "A licensee remembers the terms"],
        "Connecticut's statute of frauds lists an agreement for the sale of real property, or any interest in or concerning real property, among the agreements that need a signed writing or memorandum.",
        cgs("52-550", CH923), event=True,
        flavor=scene(
            "Beside a stone wall, a seller asks whether a spoken land deal can be sued on.",
            "At a river crossing, a seller asks whether a spoken land deal can be sued on.",
            "In a historic courtroom hallway, a seller asks whether a spoken land deal can be sued on.",
        )))

    A(law("contracts", 11,
        "Regulation 20-328-6a(c) covers a listing in which the broker keeps everything above a price the owner sets. The regulation says the licensee:",
        "Shall not accept that net listing",
        ["Must accept it if the owner insists",
         "May accept it for any commercial parcel",
         "May accept it if the excess is under $1,000"],
        "The regulation prohibits a listing in which the broker's commission is all of the excess over a minimum price agreed with the seller. If the owner wants a net figure, the agreed fee is added and the listing is written in the usual way.",
        rcsa("20-328-6a"),
        flavor=scene(
            "At a campsite, an owner offers a deal that leaves the broker everything above a set price.",
            "On a cliff road, an owner offers a deal that leaves the broker everything above a set price.",
            "In a Victorian parlor, an owner offers a deal that leaves the broker everything above a set price.",
        )))

    A(law("financing", 12,
        "Someone wants to sue on an agreement for a loan of more than $50,000. Section 52-550(a)(6) requires:",
        "A written agreement or memorandum signed by the party to be charged, or that party's agent",
        ["Only a verbal promise, because loans are outside the statute of frauds",
         "A deed instead of any loan writing",
         "Approval from the town clerk before the promise is made"],
        "Section 52-550(a)(6) includes an agreement for a loan that exceeds fifty thousand dollars among the cases that need a signed writing before a civil action may be maintained.",
        cgs("52-550", CH923), event=True,
        flavor=scene(
            "At a fishing dock, a borrower asks whether a large loan promise has to be written.",
            "At a canyon overlook, a borrower asks whether a large loan promise has to be written.",
            "In a brick bank lobby from another century, a borrower asks whether a large loan promise has to be written.",
        )))

    A(law("financing", 12,
        "Section 20-320a limits referral payments by a real estate licensee. The statute prohibits paying or receiving compensation for referring a buyer to:",
        "An attorney, a mortgage broker, or a lender",
        ["The town clerk who records the deed",
         "A home inspector the buyer already chose",
         "The affiliated broker, as an ordinary commission split"],
        "Section 20-320a prohibits a real estate licensee from paying or receiving compensation for referring a buyer to an attorney, mortgage broker, or lender.",
        cgs("20-320a"),
        flavor=scene(
            "On a footbridge, a licensee is offered money to send a buyer to a lender.",
            "At a mountain hut, a licensee is offered money to send a buyer to a lender.",
            "On a historic main street, a licensee is offered money to send a buyer to a lender.",
        )))

    A(law("financing", 13,
        "Section 8-244 creates the Connecticut Housing Finance Authority and describes what kind of body it is. The authority is:",
        "A public instrumentality and political subdivision of the state, and not a department, institution, or agency of the state",
        ["A private bank with no public role",
         "A department of the state, the same as DCP",
         "A town zoning board"],
        "Section 8-244 constitutes the authority as a public instrumentality and political subdivision. It says the authority shall not be construed to be a department, institution, or agency of the state, and that its powers are an essential public and governmental function.",
        cgs("8-244", CH134), event=True,
        flavor=scene(
            "At a state-park pavilion, a buyer asks what the housing finance authority is.",
            "On a long highway pull-off, a buyer asks what the housing finance authority is.",
            "In a capitol hallway, a buyer asks what the housing finance authority is.",
        )))

    A(law("financing", 13,
        "Section 8-250 states the purpose of the Connecticut Housing Finance Authority. That purpose is:",
        "To alleviate the shortage of housing for low and moderate income families and persons, and, when appropriate, to promote or maintain economic development through employer-assisted housing",
        ["To set every private mortgage rate in Connecticut",
         "To replace town clerks",
         "To license real estate salespersons"],
        "Section 8-250 says the authority's purpose is to alleviate the shortage of housing for low and moderate income families and persons and, when appropriate, to promote or maintain the economic development of the state through employer-assisted housing efforts.",
        cgs("8-250", CH134),
        flavor=scene(
            "At a community garden, a neighbor asks why the housing finance authority exists.",
            "At a trail town, a neighbor asks why the housing finance authority exists.",
            "In a mill neighborhood, a neighbor asks why the housing finance authority exists.",
        )))

    A(law("ct-laws", 14,
        "Section 12-495 says the real-estate conveyance tax is paid when the deed is recorded. Who pays it, and to whom?",
        "The person conveying the property pays the town clerk of the town where the property lies",
        ["The buyer pays the Real Estate Commission",
         "The salesperson pays PSI",
         "The lender keeps it as a mortgage fee"],
        "Section 12-495 makes the tax payable by the person conveying the property, to the town clerk of the town where the real property or any part of it is situated, upon recording.",
        cgs("12-495", CH223), event=True,
        flavor=scene(
            "Outside a small-town clerk's door after a hike, a seller asks who takes the conveyance tax.",
            "After a river crossing, a seller asks who takes the conveyance tax.",
            "On the steps of a nineteenth-century town hall, a seller asks who takes the conveyance tax.",
        )))

    A(law("ct-laws", 14,
        "A deed between spouses is offered for recording. Section 12-498(a)(14) says the conveyance tax:",
        "Does not apply to deeds between spouses",
        ["Applies at 2.25 percent",
         "Applies only if the spouses live in different towns",
         "Is replaced by the $500 condition-report credit"],
        "Section 12-498(a)(14) exempts deeds between spouses from the conveyance tax.",
        cgs("12-498", CH223),
        flavor=scene(
            "At a garden wedding reception, a couple asks about tax on a deed between them.",
            "At a trail wedding, a couple asks about tax on a deed between them.",
            "In a historic church hall, a couple asks about tax on a deed between them.",
        )))

    A(law("ct-laws", 15,
        "A deed shows consideration of $1,500. Section 12-498(a)(10) and the threshold in section 12-494 mean the conveyance tax:",
        "Does not apply, because consideration is under $2,000",
        ["Applies at 1.25 percent of $1,500",
         "Applies only to the buyer",
         "Is a flat $500"],
        "Section 12-494 imposes the tax when consideration equals or exceeds $2,000. Section 12-498(a)(10) exempts deeds when consideration is less than $2,000.",
        cgs("12-498", CH223), event=True,
        flavor=scene(
            "At a farm stand, a seller asks about tax on a very small deed price.",
            "At a back-road crossing, a seller asks about tax on a very small deed price.",
            "At an old grange hall, a seller asks about tax on a very small deed price.",
        )))

    A(law("ct-laws", 15,
        "The municipal piece of the conveyance tax in section 12-494(a)(2), before any extra local tax a qualifying town may add, is:",
        "One-quarter of one percent of the consideration",
        ["Three-quarters of one percent, with no separate municipal piece",
         "A flat $20 paid to the guaranty fund",
         "Paid to the Commissioner of Revenue Services by the buyer"],
        "Section 12-494(a)(2) sets the municipal component at one-fourth of one percent. A targeted investment community, or a municipality with a qualifying manufacturing plant, may add up to another one-fourth of one percent under subsection (c).",
        cgs("12-494", CH223),
        flavor=scene(
            "On a town green, a resident asks what share of the conveyance tax stays with the town.",
            "At a trail-town general store, a resident asks what share of the conveyance tax stays with the town.",
            "In a historic assessor's office, a resident asks what share of the conveyance tax stays with the town.",
        )))

    A(law("valuation", 16,
        "A licensee tells a residential appraiser to raise the value so the loan will match the contract price. Section 20-320b says that conduct is:",
        "Prohibited",
        ["A required part of advocating for the client",
         "Allowed if the seller agrees in writing",
         "Allowed for conventional loans only"],
        "Section 20-320b prohibits a real estate licensee from influencing a residential real estate appraisal.",
        cgs("20-320b"), event=True,
        flavor=scene(
            "At a hilltop lot, a licensee is tempted to push an appraiser's number.",
            "At a canyon rim, a licensee is tempted to push an appraiser's number.",
            "In an old bank conference room, a licensee is tempted to push an appraiser's number.",
        )))

    A(law("valuation", 16,
        "Section 20-320b is aimed at influence by a real estate licensee. The appraisal it covers is:",
        "A residential real estate appraisal",
        ["Only a commercial rent roll",
         "Only a town tax assessment",
         "A broker price opinion that the licensee writes alone"],
        "The statute prohibits influencing a residential real estate appraisal. It is a license-law limit on the licensee, separate from the appraiser's own standards.",
        cgs("20-320b"),
        flavor=scene(
            "On a wooded house lot, a student asks which appraisals the influence ban covers.",
            "On a ridge road, a student asks which appraisals the influence ban covers.",
            "In a historic house tour, a student asks which appraisals the influence ban covers.",
        )))

    A(law("management", 17,
        "A residential landlord receives a security deposit. Section 47a-21(h) requires the landlord to:",
        "Put the entire deposit immediately into an escrow account at a financial institution in Connecticut",
        ["Mix it into the landlord's personal checking account",
         "Keep it as cash in the unit",
         "Send it to the Real Estate Commission"],
        "Section 47a-21(h) requires the entire security deposit to go immediately into one or more escrow accounts in a financial institution for the benefit of the tenant. The landlord is the escrow agent.",
        cgs("47a-21", CH831), event=True,
        flavor=scene(
            "At a lakeside cottage rental, a tenant hands over a security deposit.",
            "At a trail cabin rental, a tenant hands over a security deposit.",
            "At a brick rooming house from another era, a tenant hands over a security deposit.",
        )))

    A(law("management", 17,
        "A tenant who is 62 or older asks for the statutory cap on a residential security deposit. Section 47a-21(b)(2) sets that cap at:",
        "One month's rent",
        ["Two months' rent", "Three months' rent", "There is no cap after age 62"],
        "Section 47a-21(b)(1) caps a demand at two months' rent when the tenant is under 62. Subsection (b)(2) caps it at one month's rent when the tenant is 62 or older.",
        cgs("47a-21", CH831),
        flavor=scene(
            "On a garden walk, an older tenant asks about the deposit cap.",
            "On a gentle trail, an older tenant asks about the deposit cap.",
            "On a historic porch, an older tenant asks about the deposit cap.",
        )))

    A(law("practice", 18,
        "An advertisement for a Connecticut dwelling states a preference based on race. Section 46a-64c treats that kind of notice as:",
        "A discriminatory housing practice",
        ["Protected opinion, because it is only an ad",
         "Required, so buyers know the neighborhood",
         "A conveyance-tax exemption"],
        "Section 46a-64c(a)(3) makes it unlawful to make, print, or publish a notice, statement, or advertisement that indicates a preference, limitation, or discrimination based on a protected class, or an intention to make such a preference.",
        cgs("46a-64c", CH814), event=True,
        flavor=scene(
            "On a park kiosk, a housing ad states a racial preference.",
            "On a trail-town board, a housing ad states a racial preference.",
            "On a historic storefront, a housing ad states a racial preference.",
        )))

    A(law("practice", 18,
        "A person with a disability needs a reasonable change in building rules in order to use a dwelling. Section 46a-64c(a)(6) treats a refusal to make that accommodation as:",
        "Discrimination because of physical or mental disability",
        ["A decision only federal law mentions",
         "Allowed whenever the landlord prefers the old rule",
         "A matter for the conveyance tax, not fair housing"],
        "Section 46a-64c(a)(6) includes, as disability discrimination, a refusal to make reasonable accommodations in rules, policies, practices, or services when the accommodations may be necessary for a person with a disability to use and enjoy a dwelling.",
        cgs("46a-64c", CH814),
        flavor=scene(
            "At an accessible trailhead, a renter asks about a needed rule change.",
            "At a mountain lodge, a renter asks about a needed rule change.",
            "At an old rooming house, a renter asks about a needed rule change.",
        )))

    A(law("landuse", 20,
        "Section 8-2 authorizes a municipal zoning commission to regulate, inside that municipality:",
        "Building height and size, the share of the lot that may be covered, yards and open space, density, and the use of land",
        ["The salesperson's commission rate",
         "Who may sit for the real estate exam",
         "The state conveyance-tax brackets"],
        "Section 8-2(a) lets the zoning commission regulate height, number of stories, and size of buildings; the percentage of the lot that may be occupied; yards and other open spaces; density; and the location and use of buildings and land, among other listed items.",
        cgs("8-2", CH124), event=True,
        flavor=scene(
            "Looking over a valley of houses, a resident asks what a zoning commission may regulate.",
            "From a ridge road, a resident asks what a zoning commission may regulate.",
            "From a historic overlook, a resident asks what a zoning commission may regulate.",
        )))

    A(law("landuse", 20,
        "A lot has conditions that do not affect the zoning district generally, and a literal reading of the rules would cause exceptional difficulty or unusual hardship. Section 8-6 gives the power to vary those rules to:",
        "The zoning board of appeals",
        ["Any salesperson with a listing",
         "The Real Estate Commission",
         "The buyer, by signing the offer"],
        "Section 8-6(a)(3) authorizes the zoning board of appeals to vary the regulations for a parcel where conditions especially affecting that parcel, but not the district generally, would cause exceptional difficulty or unusual hardship. The board need not rehear the same variance for six months after a decision.",
        cgs("8-6", CH124),
        flavor=scene(
            "On a steep wooded lot, an owner asks who can vary the zoning rule.",
            "On a switchback road, an owner asks who can vary the zoning rule.",
            "Beside an old mill pond, an owner asks who can vary the zoning rule.",
        )))

    A(law("disclosures", 21,
        "Section 22a-42 states Connecticut's public policy on inland wetlands and watercourses. That policy is:",
        "To require municipal regulation of activities that affect wetlands and watercourses inside the municipality",
        ["To leave every wetland decision to the listing broker",
         "To ban all municipal wetland rules",
         "To replace the residential condition report"],
        "Section 22a-42(a) declares it the public policy of the state to require municipal regulation of activities affecting the wetlands and watercourses within the territorial limits of the municipalities or districts.",
        cgs("22a-42", CH440), event=True,
        flavor=scene(
            "At the edge of a marsh, a builder asks who regulates work in the wetland.",
            "At a river put-in, a builder asks who regulates work in the wetland.",
            "Beside an old mill race, a builder asks who regulates work in the wetland.",
        )))

    A(law("disclosures", 21,
        "The residential condition-report template in section 20-327b includes an asbestos and lead subsection. That subsection asks the seller about:",
        "Whether lead paint is present, to the seller's actual knowledge",
        ["The buyer's credit score",
         "The broker's commission",
         "The town's zoning map colors"],
        "The statutory template includes questions on asbestos and lead, including whether lead paint is present. Section 20-327e measures the seller's statements by actual knowledge. The report is not a new warranty under section 20-327d.",
        cgs("20-327b"),
        flavor=scene(
            "In a house beside a state forest, a seller looks at the lead question on the condition report.",
            "In a cabin on a long trail, a seller looks at the lead question on the condition report.",
            "In a nineteenth-century house, a seller looks at the lead question on the condition report.",
        )))

    return q
