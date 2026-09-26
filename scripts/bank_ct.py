"""Connecticut-specific questions. Every item cites an official source."""

from qutil import cgs, rcsa, src, item, DCP_EXAM, DCP_CE, DCP_FUND, PSI, CH814, CH831, CH223, CH822, CH926, DOB_DEP

PSI_SRC = src("PSI CT Real Estate Candidate Information Bulletin (updated Nov. 13, 2025)", PSI)
DCP_SRC = src("CT DCP, Real Estate Salesperson — Initial/Exam", DCP_EXAM)
CE_SRC = src("CT DCP, Real Estate Salesperson — Continuing Education", DCP_CE)
FUND_PAGE = src("CT DCP, Real Estate Guaranty Fund", DCP_FUND)


def ct_questions():
    q = []
    A = q.append

    # --- Licensing (ct-license) ---
    A(item("ct-license",
        "Before a person may schedule the Connecticut salesperson examination, who must approve the applicant?",
        "The Department of Consumer Protection",
        ["Any supervising broker, before the course is finished",
         "The town clerk where the applicant lives",
         "The local association of Realtors"],
        "PSI's candidate bulletin says candidates must be preapproved by the Department of Consumer Protection before they schedule. Broker supervision is not required just to sit for the exam.",
        PSI_SRC, event=True))

    A(item("ct-license",
        "A driver wants to sit for the salesperson exam next spring. Which education credential must be shown before admission to that exam?",
        "A commission- or commissioner-approved real estate principles and practices course of at least 60 classroom hours",
        ["A 15-hour brokerage-principles course only",
         "A 12-hour continuing-education cycle",
         "A broker's license from any state, with no Connecticut course"],
        "For a salesperson applicant, the statute requires proof of an approved principles and practices course of at least 60 classroom hours, or equivalent experience or education the commission or commissioner accepts.",
        cgs("20-314")))

    A(item("ct-license",
        "The DCP salesperson exam page states a minimum age for applicants. What is it?",
        "18",
        ["16", "21", "25"],
        "The Department of Consumer Protection lists being at least 18 as a prerequisite for the salesperson initial/exam application, along with the 60-hour course.",
        DCP_SRC))

    A(item("ct-license",
        "Under the licensing statute, what application fee does a salesperson applicant pay to be admitted to the written examination?",
        "$80",
        ["$59", "$120", "$570"],
        "The statute sets an $80 application fee for a salesperson applicant and a $120 application fee for a broker applicant. The testing service's separate examination fee is paid to that service.",
        cgs("20-314")))

    A(item("ct-license",
        "The November 2025 PSI bulletin lists the salesperson examination fee for a first-time registration covering both portions. What is that fee?",
        "$59",
        ["$51", "$65", "$80"],
        "The updated bulletin states the examination fee is $59 for first-time testing of both portions, whether one or both are taken. It lists retakes at $51. Fees in the bulletin are not refundable.",
        PSI_SRC))

    A(item("ct-license",
        "How long does payment of the salesperson application fee entitle the applicant to take the examination?",
        "Within the one-year period from the date of payment",
        ["Within 30 days", "Within two years", "Until the license is activated"],
        "The statute says each payment of the application fee entitles the applicant to take the examination within the one-year period from the date of payment. DCP also says both portions must be passed within one year of eligibility.",
        cgs("20-314")))

    A(item("ct-license",
        "A candidate passes the national portion in June and the state portion the following April, inside the eligibility year. DCP says the license must be activated within what time after the most recently passed portion?",
        "2 years",
        ["90 days", "1 year", "5 years"],
        "DCP's salesperson page says that after both portions are passed within the eligibility year, the applicant has two years from the most recently passed portion to activate the license.",
        DCP_SRC, event=True))

    A(item("ct-license",
        "What does DCP require before a passing salesperson can activate the license?",
        "Supervision by a Connecticut-licensed broker and payment of the license fee",
        ["Supervision is required to take the exam, but not to activate",
         "Only a town-clerk endorsement",
         "A broker license application instead of a salesperson license"],
        "DCP states broker supervision is not required to take the examination, but activation requires supervision by a Connecticut-licensed broker and payment of the license fee.",
        DCP_SRC))

    A(item("ct-license",
        "The licensing statute sets the fee paid to the department for a real estate salesperson's license, and the same amount for each biennial renewal. What is that amount?",
        "$570",
        ["$80", "$285", "$750"],
        "Section 20-314(f) sets the salesperson license fee and the biennial renewal at $570. A separate one-time $20 guaranty-fund fee is also charged on application under section 20-324b.",
        cgs("20-314")))

    A(item("ct-license",
        "On top of other license fees, what one-time amount does each real estate licensee pay to the Real Estate Guaranty Fund when applying for a license?",
        "$20",
        ["$6", "$8", "$25,000"],
        "Section 20-324b requires an additional one-time fee of $20, credited to the Real Estate Guaranty Fund. DCP's $590 activation figure matches the $570 license fee plus this $20.",
        cgs("20-324b")))

    A(item("ct-license",
        "According to DCP, salesperson licenses expire on which date?",
        "May 31 of every even-numbered year",
        ["March 31 of every odd-numbered year",
         "November 30 every year",
         "The anniversary of the exam date"],
        "DCP's salesperson exam page states that all real estate salesperson licenses expire on May 31 of every even-numbered year. The statute provides that licenses expire biennially and that a reinstated salesperson license expires on the next May 31.",
        DCP_SRC))

    A(item("ct-license",
        "A salesperson who wants a two-year renewal must satisfy continuing education. The statute allows that requirement to be met by approved courses of not less than how many hours?",
        "12 hours",
        ["3 hours", "8 hours", "60 hours"],
        "Section 20-319(b) says the requirement may be satisfied by approved continuing-education courses of not less than 12 hours, or by a written examination, or by equivalent experience under the regulations.",
        cgs("20-319")))

    A(item("ct-license",
        "DCP's salesperson continuing-education page for the cycle running March 1, 2026 through February 28, 2028 describes the 12 hours as which split?",
        "One 3-hour mandatory Connecticut license-law course and 9 hours of electives",
        ["12 hours of electives and no mandatory course",
         "60 hours of principles and practices",
         "A 40-hour broker pre-license course"],
        "DCP states 12 credit hours per two-year cycle, including one three-hour mandatory course and nine hours of electives. A 40-question Connecticut CE examination is an alternative way to meet the renewal education requirement.",
        CE_SRC))

    A(item("ct-license",
        "A salesperson finishes the required continuing education two months after the license period expired. Under the statute, what fee is due for that late completion?",
        "$315",
        ["$8", "$25", "$625"],
        "Section 20-319(e) sets $315 when the licensee reports that education was finished not later than two months after the period expired, and $625 when it is finished more than two months but not later than four months after expiration.",
        cgs("20-319")))

    A(item("ct-license",
        "If continuing education is finished more than two months, but not later than four months, after the license period expired, the statute sets the fee at:",
        "$625",
        ["$315", "$285", "$570"],
        "That later window is the $625 tier in section 20-319(e). The $315 tier is only for completion within two months after the period expired.",
        cgs("20-319")))

    A(item("ct-license",
        "Each salesperson or associate broker who transfers affiliation with a broker must register the transfer and pay what fee to the department?",
        "$25",
        ["$8", "$80", "$570"],
        "Section 20-319a sets a $25 registration fee when a licensed salesperson or associate broker transfers affiliation.",
        cgs("20-319a")))

    A(item("ct-license",
        "The November 2025 PSI bulletin says a salesperson must score at least what percent to pass?",
        "70 percent",
        ["60 percent", "75 percent", "80 percent"],
        "The bulletin states that salesperson examinations require a score of at least 70 percent. It sets the broker examinations at 75 percent, so those numbers should not be swapped.",
        PSI_SRC))

    A(item("ct-license",
        "The PSI examination summary in the November 2025 bulletin gives the salesperson national (general) portion as:",
        "80 scored questions and 120 minutes",
        ["35 scored questions and 45 minutes",
         "110 scored questions and 90 minutes",
         "40 scored questions and 60 minutes"],
        "The summary table lists the salesperson general portion as 80 questions (80 points) and 120 minutes. The state portion is listed separately as 35 questions (35 points) and 45 minutes.",
        PSI_SRC))

    A(item("ct-license",
        "The same bulletin lists the salesperson state portion as:",
        "35 scored questions and 45 minutes",
        ["80 scored questions and 120 minutes",
         "30 scored questions and 30 minutes",
         "15 scored questions and 20 minutes"],
        "The state outline's salesperson item counts (7, 11, 9, and 8) add to 35, matching the summary table's 35 questions and 45 minutes.",
        PSI_SRC))

    A(item("ct-license",
        "A candidate who fails one portion may keep retaking it during the eligibility year. Which statement matches DCP's rule?",
        "Both portions must be passed within one year of eligibility, or the person must reapply",
        ["Only three attempts are allowed in a lifetime",
         "A failed portion never has to be retaken if the other portion was passed",
         "Eligibility lasts five years from the course certificate"],
        "DCP says the exam may be taken on an unlimited basis for up to one year from eligibility, and both portions must be passed within that year. Otherwise the person must reapply.",
        DCP_SRC))

    A(item("ct-license",
        "The Real Estate Commission is created in which agency?",
        "The Department of Consumer Protection",
        ["The Office of the Attorney General",
         "The Department of Banking only",
         "The town clerks' association"],
        "Section 20-311a creates the Connecticut Real Estate Commission in the Department of Consumer Protection.",
        cgs("20-311a")))

    A(item("ct-license",
        "The largest amount the Real Estate Guaranty Fund may pay, in the aggregate, for any one transaction or claim is:",
        "$25,000, regardless of how many people or parcels are involved",
        ["$5,000 per person", "$500,000 per claimant", "The full judgment with no cap"],
        "Section 20-324a caps compensation at $25,000 in the aggregate for any one real estate transaction or claim, no matter how many aggrieved persons or parcels are involved. DCP's guaranty-fund page states the same cap.",
        cgs("20-324a")))

    A(item("ct-license",
        "An aggrieved person wants a guaranty-fund payment after a judgment. The application must be brought no later than:",
        "Two years from the final determination of the judgment, or from the end of the time to appeal",
        ["30 days after the closing",
         "Seven years after the listing was signed",
         "Any time while the licensee is alive"],
        "Section 20-324d bars an application that might result in collection from the fund if it is brought later than two years from final determination of the judgment or expiration of the time to appeal.",
        cgs("20-324d")))

    A(item("ct-license",
        "Which loss can support a guaranty-fund claim against a licensed broker or salesperson?",
        "A loss from embezzlement, false pretenses, forgery, fraud, misrepresentation, or deceit",
        ["Any drop in market value after an honest sale",
         "A buyer's remorse with no misconduct",
         "A commission dispute between two licensees only"],
        "Section 20-324a limits the fund to specified misconduct: embezzlement, money or property taken by false pretenses, artifice, or forgery, and fraud, misrepresentation, or deceit by a licensee or the unlicensed employee of a licensee.",
        cgs("20-324a"), event=True))

    A(item("ct-license",
        "After a hearing under the licensing law, the commission or department may fine a licensee up to how much per violation, besides possible suspension or revocation?",
        "$5,000",
        ["$500", "$1,000", "$25,000"],
        "Section 20-320(a) authorizes a fine of not more than $5,000 per violation, in addition to or instead of suspension or revocation. Fines collected under that section go to the guaranty fund.",
        cgs("20-320")))

    A(item("ct-license",
        "Which conduct is listed in the statute as a ground for license discipline?",
        "Commingling other people's money with the licensee's own funds",
        ["Refusing a net listing that the seller requested",
         "Telling a buyer to get a home inspection",
         "Delivering a copy of a signed listing at the signing table"],
        "Failure to keep others' funds in an escrow or trust account, or commingling them with the licensee's own money, is ground (10) in section 20-320(a).",
        cgs("20-320"), event=True))

    A(item("ct-license",
        "An exclusive listing contains a fixed end date and then says it renews itself for another six months unless the owner cancels. Under Connecticut license law, that clause is:",
        "A ground for discipline",
        ["Required in every listing",
         "Allowed if the font is bold",
         "A problem only for buyer-agency agreements"],
        "Section 20-320(a)(6) treats as discipline an exclusive listing or buyer-agency contract that has a fixed termination date and also provides for automatic continuation beyond that date.",
        cgs("20-320")))

    A(item("ct-license",
        "Who is exempt from salesperson licensure when selling a house?",
        "An owner selling property the owner actually owns",
        ["A friend who negotiates the sale for a fee",
         "An unlicensed assistant who writes and presents the offer for pay",
         "A neighbor who holds open houses every weekend for a commission"],
        "Section 20-329(1) exempts an owner or lessor performing the acts in the definitions with reference to property that person owns or leases. Negotiating for someone else for compensation is not that exemption.",
        cgs("20-329")))

    A(item("ct-license",
        "An unlicensed clerk at a brokerage may do clerical work. Which task does the licensure exemption say that person must not do?",
        "Be a signatory on the broker's escrow account",
        ["File copies of signed disclosures",
         "Schedule an inspection the licensee requested",
         "Prepare a mailing the broker approved"],
        "Section 20-329(11) allows clerical employees but says they shall not negotiate agreement terms, open or be a signatory on the escrow or trust account, or sell, buy, or lease real property for another person for compensation.",
        cgs("20-329"), event=True))

    A(item("ct-license",
        "A salesperson passes the national portion in another state and applies in Connecticut within two years with a score the commission accepts. The statute allows the commission or commissioner to:",
        "Waive the uniform portion of the written examination",
        ["Waive the Connecticut state portion automatically",
         "Issue a broker license with no further education",
         "Skip the 60-hour course and the background questions"],
        "Section 20-314(c) allows waiver of the uniform portion when the national testing-service exam was taken in another state within two years and the score is deemed satisfactory. It does not waive the state portion or the Connecticut course rule by itself.",
        cgs("20-314")))

    # --- Conduct (ct-conduct) ---
    A(item("ct-conduct",
        "A buyer hands a salesperson a deposit check on a signed purchase agreement. What should the salesperson do with that check?",
        "Promptly pay it over to the affiliated broker",
        ["Deposit it in the salesperson's personal account until closing",
         "Hold it in a glove box until the buyer finishes inspections",
         "Cash it and deliver the money to the seller the same day"],
        "Regulation 20-328-7a(a) says a licensee who receives a deposit on a transaction for the affiliated broker shall promptly pay that deposit over to the broker.",
        rcsa("20-328-7a"), event=True))

    A(item("ct-conduct",
        "Once all necessary parties have signed the agreement, how soon must the broker deposit earnest money the broker is holding in trust?",
        "Within three banking days",
        ["Within three calendar hours",
         "Within 21 days",
         "Only after the inspection contingency is removed"],
        "Section 20-324k(c) requires the broker to deposit those trust moneys in the escrow or trust account within three banking days of the date the agreement is signed by all necessary parties.",
        cgs("20-324k"), event=True))

    A(item("ct-conduct",
        "Where must a Connecticut broker keep an escrow account for other people's money?",
        "In a separate account, distinct from the broker's own account, at a bank doing business in this state",
        ["In the broker's operating account, clearly labeled",
         "In any out-of-state investment account the broker prefers",
         "With the town clerk until closing"],
        "Section 20-324k(a) requires a separate escrow or trust account, distinct from the broker's own account, in a bank doing business in Connecticut.",
        cgs("20-324k")))

    A(item("ct-conduct",
        "A broker willfully fails to deposit trust money as section 20-324k requires. The statute's criminal penalty for a willful violation is a fine of not more than:",
        "$1,000, or imprisonment of not more than six months, or both",
        ["$25,000 and a mandatory year in jail",
         "$100 with no possible imprisonment",
         "A warning letter only"],
        "Section 20-324k(e) sets that penalty for a willful violation. License discipline under section 20-320 is a separate track.",
        cgs("20-324k")))

    A(item("ct-conduct",
        "A seller offers a listing in which the broker keeps everything above a set net price. Connecticut regulations say the licensee:",
        "Shall not accept that net listing",
        ["Must accept it if the seller insists",
         "May accept it if both parties initial the net price",
         "May accept it only for commercial land"],
        "Regulation 20-328-6a(c) prohibits a listing in which the broker receives as commission all excess over a minimum price agreed with the seller. If the owner wants a net figure, the agreed fee is added and the listing is written in the usual way.",
        rcsa("20-328-6a"), event=True))

    A(item("ct-conduct",
        "Before a licensee negotiates the sale of a Connecticut home for the owner, the regulations require:",
        "A written listing agreement that identifies the property, states the commission, and has a start date and an expiration date",
        ["An oral listing, if a witness hears it",
         "Only a text message that names the asking price",
         "A deed signed by the seller before any showing"],
        "Regulation 20-328-6a(a)(1) requires a written listing before the licensee negotiates a non-commercial sale, exchange, or lease for the owner. It must identify the property, include the terms including commission, the date entered, and the expiration date, and it must be signed by the owner and the broker or the broker's authorized agent.",
        rcsa("20-328-6a")))

    A(item("ct-conduct",
        "Before negotiating a purchase for a buyer in a non-commercial deal, the regulations require the licensee to:",
        "Enter a written agency agreement with the buyer that includes compensation, the start date, and an expiration date",
        ["Wait until after the offer is accepted",
         "Use the seller's listing agreement as the buyer's contract",
         "Get only the lender's permission"],
        "Regulation 20-328-6a(a)(2) requires a written buyer or lessee agency agreement before the licensee negotiates a non-commercial purchase, exchange, or lease for that person.",
        rcsa("20-328-6a")))

    A(item("ct-conduct",
        "Which notice must appear in a written agreement that fixes the broker's compensation, immediately before the compensation clause, in bold or equally conspicuous type?",
        "The amount or rate of broker compensation is not fixed by law. It is set by each broker individually and may be negotiable.",
        ["Connecticut sets every residential commission at 6 percent.",
         "The salesperson may keep any deposit if the buyer cancels.",
         "Compensation is due even if the agreement is oral."],
        "Section 20-325b requires that notice, in not less than ten-point boldface type or another manner that stands out, immediately before the compensation provision.",
        cgs("20-325b"), event=True))

    A(item("ct-conduct",
        "A salesperson is paid a bonus directly by the seller for extra weekend showings, and never turns it over. The compensation regulation says the salesperson must:",
        "Promptly pay over or assign that compensation to the affiliated broker",
        ["Keep it, because a bonus is not a commission",
         "Split it with the buyer",
         "Deposit it in the escrow account as the salesperson's fee"],
        "Regulation 20-328-8a(f) requires a licensee who receives compensation on a transaction handled for the affiliated broker to promptly pay it over or assign it to that broker.",
        rcsa("20-328-8a"), event=True))

    A(item("ct-conduct",
        "A licensee wants to collect a fee from both the buyer and the seller. The compensation regulation requires:",
        "Notifying all parties before the closing",
        ["Notice only to the supervising broker",
         "Nothing, if each fee is under $500",
         "A court order"],
        "Regulation 20-328-8a(d) says a licensee shall not accept compensation from more than one party without notifying all parties prior to the closing.",
        rcsa("20-328-8a")))

    A(item("ct-conduct",
        "May a licensee pay part of a commission to a person who negotiated the sale but was not licensed as a broker or salesperson when the work was done?",
        "No",
        ["Yes, if the person gets less than half",
         "Yes, if the payment is called a referral gift card",
         "Yes, after the closing is recorded"],
        "Regulation 20-328-8a(e) prohibits sharing compensation from a real estate transaction with a person who was engaging in the real estate business and was not licensed as a broker or salesperson when the services were performed.",
        rcsa("20-328-8a")))

    A(item("ct-conduct",
        "In a cooperative sale, whom does the regulation say the broker should pay?",
        "The cooperating broker, not that broker's salesperson, unless the cooperating broker has expressly consented",
        ["The cooperating salesperson's personal account, always",
         "The buyer, as a rebate, without telling anyone",
         "The town clerk, as a recording tip"],
        "Regulation 20-328-8a(g) says the broker compensates the cooperating broker and does not compensate that broker's salespersons or brokers without the cooperating broker's prior express knowledge and consent.",
        rcsa("20-328-8a")))

    A(item("ct-conduct",
        "The buyer wrongfully refuses to close. The broker believes a commission was earned. What does the regulation say about the deposit?",
        "The broker has no right to any of the deposited money just because compensation may have been earned",
        ["The broker may keep the entire deposit as the fee",
         "The salesperson may take the deposit home",
         "The deposit automatically converts to commission on the third banking day"],
        "Regulation 20-328-8a(b) says that when an owner, lessor, buyer, or lessee wrongfully fails or is unable to close, the broker has no right to the deposited money even though compensation may have been earned.",
        rcsa("20-328-8a"), event=True))

    A(item("ct-conduct",
        "A print ad for a salesperson's listing must show the supervising licensee's contact information in type that is:",
        "The same size or larger than the salesperson's contact information",
        ["Half the size, so the salesperson's number stands out",
         "Omitted, if the salesperson's photo is large",
         "Shown only on the broker's office door"],
        "Regulation 20-328-5a(e) requires the salesperson's licensed name and a phone or email, plus the supervising licensee's licensed name and phone or email, with the supervising licensee's contact information in the same or a larger font.",
        rcsa("20-328-5a")))

    A(item("ct-conduct",
        "A broker's ad for someone else's house reads like a private owner selling without help. That ad is:",
        "Prohibited",
        ["Required, to avoid steering",
         "Allowed if the price is accurate",
         "Allowed on social media only"],
        "Regulation 20-328-5a(c) says a broker shall not advertise another's property in a manner indicating a private party not engaged in the real estate business is making the offer. The broker also must not advertise without disclosing the broker's name.",
        rcsa("20-328-5a"), event=True))

    A(item("ct-conduct",
        "A solo salesperson wants the word 'Team' in an advertisement but is not a licensed business entity. The advertising regulation says:",
        "That word is not allowed, because it implies a business entity",
        ["'Team' is fine if friends help on weekends",
         "'Team' is required on every salesperson ad",
         "Only the word 'Realty' is restricted"],
        "Regulation 20-328-5a(k) bars words such as team, realty, agency, company, or partnership, and similar words, unless the licensee is a licensed business entity.",
        rcsa("20-328-5a")))

    A(item("ct-conduct",
        "A seller tells the licensee to hide a known leak that is a material fact. The misrepresentation regulation requires the licensee to:",
        "Not misrepresent or conceal material facts",
        ["Follow the seller's instruction because of obedience",
         "Conceal it unless the buyer asks three times",
         "Mention it only after the deed is recorded"],
        "Regulation 20-328-5a(a) says a licensee shall not misrepresent or conceal any material facts in any transaction. Obedience does not cover an instruction to hide a material fact.",
        rcsa("20-328-5a"), event=True))

    A(item("ct-conduct",
        "Listing and buyer-agency agreements must contain a statement that the agreement is subject to the Connecticut statutes prohibiting discrimination in commercial and residential real estate transactions. That requirement is in:",
        "Regulation 20-328-4a",
        ["The conveyance-tax return only",
         "The security-deposit statute only",
         "A town ordinance that applies only in Hartford"],
        "Regulation 20-328-4a(b) requires that fair-housing statement, citing title 46a, chapter 814c, in all listing and buyer-agency agreements. Subsection (a) also forbids participating in a violation of section 46a-64c.",
        rcsa("20-328-4a")))

    A(item("ct-conduct",
        "How long must a broker keep purchase contracts, listings, agency agreements, and escrow-account bank records?",
        "At least seven years after closing, final escrow disbursement, or expiration of the agreement, whichever is later",
        ["One year", "Three years", "Until the next license renewal only"],
        "Section 20-325m(a) requires retention for not less than seven years after the transaction closes, escrow funds are disbursed, or the listing or representation agreement expires, whichever occurs later.",
        cgs("20-325m")))

    A(item("ct-conduct",
        "A licensee leaves the brokerage. When must that person turn records obtained during the affiliation back to the broker?",
        "Immediately",
        ["Within one year", "After the next closing season", "Only if the broker asks in court"],
        "Regulation 20-328-10a(a) says that upon termination the licensee shall immediately turn over information and records obtained during the affiliation. The broker then has a written-accounting deadline.",
        rcsa("20-328-10a")))

    A(item("ct-conduct",
        "After a licensee turns records over at the end of an affiliation, the broker's written accounting of active deals and intended compensation is due:",
        "Within 10 days after the records are turned over, or within 45 days of termination, whichever is earlier",
        ["Within three banking days",
         "Within seven years",
         "Only if the licensee files a lawsuit"],
        "Regulation 20-328-10a(b) sets that accounting deadline and says it must cover active listings, agency agreements, transactions, commissions, and the compensation the broker intends to pay.",
        rcsa("20-328-10a")))

    A(item("ct-conduct",
        "A licensee offers a cash kickback to a lender for sending buyers. Connecticut license law:",
        "Prohibits a paid referral of a buyer to an attorney, mortgage broker, or lender",
        ["Allows it if it is disclosed on the closing statement",
         "Allows it under $50",
         "Requires it in every financed sale"],
        "Section 20-320a prohibits a real estate licensee from paying or receiving compensation for referring a buyer to an attorney, mortgage broker, or lender.",
        cgs("20-320a"), event=True))

    A(item("ct-conduct",
        "A salesperson pressures an appraiser to hit the contract price. That conduct is:",
        "Prohibited by statute",
        ["A normal part of advocating for the buyer",
         "Required when the loan is conventional",
         "Allowed if the seller consents in writing"],
        "Section 20-320b prohibits a licensee from influencing a residential real estate appraisal.",
        cgs("20-320b")))

    A(item("ct-conduct",
        "A licensee copies another broker's exclusive listing by persuading the owner to cancel it so the licensee can take over. The interference regulation:",
        "Prohibits inducing a breach of an exclusive listing in order to substitute a new one",
        ["Requires the attempt, as competition",
         "Applies only after closing",
         "Allows it if the new commission is lower"],
        "Regulation 20-328-9a(c) prohibits inducing an owner to breach or terminate an exclusive right-to-sell, exclusive agency, or a buyer's exclusive representation agreement in order to substitute a new agreement.",
        rcsa("20-328-9a"), event=True))

    A(item("ct-conduct",
        "If a broker is sued because an affiliated independent-contractor salesperson harmed a third party, the statute makes the broker:",
        "Liable to the same extent as if the salesperson had been an employee",
        ["Immune, because independent contractors are never the broker's responsibility",
         "Liable only for property damage under $100",
         "Required to sue the salesperson before any victim may sue"],
        "Section 20-312a says the broker is liable to the same extent as if that affiliate had been employed as a salesperson.",
        cgs("20-312a")))

    A(item("ct-conduct",
        "An associate broker's affiliation ends and no new supervising licensee is in place. The associate broker must notify the department within:",
        "14 calendar days after termination",
        ["3 banking days", "45 days", "7 years"],
        "Section 20-312c(c) requires notice not later than 14 calendar days after termination or affiliation with another supervising licensee, whichever occurs first.",
        cgs("20-312c")))

    # --- CT agency ---
    A(item("ct-agency",
        "At the first personal meeting with a prospective party, a licensee must disclose in writing:",
        "The types of agency relationships available, and that confidential information should wait until a written representation agreement exists",
        ["The seller's lowest acceptable price",
         "Only the licensee's cell phone number",
         "Nothing until the deed is signed"],
        "Section 20-325d(b) requires that written disclosure not later than the first personal meeting. In a residential transaction the licensee must also provide fair-housing information. The disclosures may be delivered electronically.",
        cgs("20-325d"), event=True))

    A(item("ct-agency",
        "A residential prospect asks who the licensee represents. Besides agency choices, section 20-325d(b) requires the licensee to provide:",
        "Information on fair housing discrimination, protected classes, and where to get more help",
        ["A promise that every offer will be accepted",
         "The brokerage's net-listing policy",
         "The seller's medical history"],
        "For residential transactions, the first-meeting disclosure includes fair-housing information: federal and state law, protected classes, where to obtain more information, and available resources.",
        cgs("20-325d")))

    A(item("ct-agency",
        "An unrepresented party asks, in the middle of a deal, who the licensee's client is. The licensee must:",
        "Disclose the client's identity in writing if asked",
        ["Refuse, because the client's name is always confidential",
         "Answer only after closing",
         "Give the name orally and never in writing"],
        "Section 20-325d(a) says a licensee who represents a seller, lessor, buyer, or lessee shall, upon request, disclose the client's identity in writing to a party who is not represented by another licensee.",
        cgs("20-325d")))

    A(item("ct-agency",
        "When must written dual-agency consent be signed to gain the statute's conclusive presumption of informed consent?",
        "Before the person executes a contract to purchase, sell, or lease",
        ["Any time before the deed is recorded",
         "Only after a dispute arises",
         "It may stay oral if both sides nod"],
        "Section 20-325g creates a conclusive presumption of informed consent when the person executes the statutory written consent before executing any contract or agreement for the purchase, sale, or lease.",
        cgs("20-325g"), event=True))

    A(item("ct-agency",
        "In a Connecticut dual-agency relationship, the brokerage may tell the buyer that the seller will take less than the list price only if:",
        "The seller has instructed the brokerage in writing to do so",
        ["The buyer asks nicely",
         "The salesperson thinks it will help the deal",
         "The listing has been on the market for 30 days"],
        "The statutory dual-agency consent in section 20-325g says the firm may not disclose that the seller will accept less than the asking price unless the seller instructs it in writing. The same idea protects how much the buyer will pay, motivations, and financing flexibility.",
        cgs("20-325g"), event=True))

    A(item("ct-agency",
        "Even in dual agency, which information still has to be disclosed?",
        "Material property defects known to the brokerage, and other information the law requires",
        ["The seller's divorce plans",
         "The buyer's maximum loan approval",
         "Every other offer's financing terms"],
        "Section 20-325g(3) says confidential personal, financial, or other information is not disclosed without express written consent, other than material property defects known to the firm and other information the law requires.",
        cgs("20-325g")))

    A(item("ct-agency",
        "A broker appoints one licensee to represent the seller and a different licensee in the same firm to represent the buyer. Those designated agents are:",
        "Not dual agents, unless the same person is designated for both sides",
        ["Automatically dual agents because they share an office",
         "Forbidden by statute",
         "Customers, not agents"],
        "Section 20-325i says a designated seller agent or designated buyer agent is not deemed a dual agent, except when one individual is designated to represent both sides in the same transaction.",
        cgs("20-325i"), event=True))

    A(item("ct-agency",
        "May a Connecticut broker make a unilateral offer of subagency?",
        "No",
        ["Yes, in every multiple-listing remark",
         "Yes, if the commission is 3 percent or less",
         "Yes, for out-of-state land only"],
        "Section 20-325f says no broker shall make any unilateral offer of subagency or agree to compensate, appoint, employ, cooperate with, or otherwise affiliate with a subagent for the sale or purchase of real property.",
        cgs("20-325f")))

    A(item("ct-agency",
        "After a listing ends, the licensee still must not reveal the client's confidential information, except in narrow cases. One of those cases is:",
        "When legal process requires it",
        ["When a curious neighbor asks",
         "When it would help the licensee's next listing",
         "When the information is merely embarrassing"],
        "Section 20-325h bars revealing or using confidential information of a prospective party or a person the licensee represented, except as required by legal process, to defend the licensee from allegations of wrongful or negligent conduct, or to prevent a crime.",
        cgs("20-325h")))

    A(item("ct-agency",
        "A licensee acts for both sides and never tells one of them. That is:",
        "A statutory ground for discipline",
        ["Standard dual agency",
         "Allowed if the commission is shared evenly",
         "Required in designated agency"],
        "Section 20-320(a)(3) lists acting as an agent for more than one party in a transaction without the knowledge of all parties for whom the licensee acted.",
        cgs("20-320"), event=True))

    A(item("ct-agency",
        "A buyer who is making a bona fide offer writes that it matters whether a death occurred in the house. The owner's agent should:",
        "Report the owner's findings in writing, or, if the owner refuses, tell the buyer in writing that the owner refused",
        ["Stay silent, because a death can never be discussed",
         "Announce the death in the next open-house ad",
         "Cancel the offer without telling anyone"],
        "Section 20-329ee says that if a purchaser or lessee who is making a bona fide offer asks in writing, the owner through the agent shall report findings in writing, consistent with privacy laws. If the owner refuses, the agent shall so advise the buyer or lessee in writing.",
        cgs("20-329ee"), event=True))

    A(item("ct-agency",
        "Is the fact that an occupant has a disease on the public-health commissioner's list of reportable diseases a material fact that must be disclosed?",
        "No. The statute treats it as a nonmaterial fact",
        ["Yes, in every advertisement",
         "Yes, but only the diagnosis code",
         "Yes, if the buyer is a family with children"],
        "Section 20-329cc defines a nonmaterial fact to include infection with a disease on that list, and that the property was suspected to have been the site of a death or felony. Section 20-329dd says a nonmaterial fact need not be disclosed and creates no cause of action for that silence.",
        cgs("20-329cc")))

    A(item("ct-agency",
        "A physical defect in the house is serious. Do the nonmaterial-fact sections excuse hiding it?",
        "No. Those sections do not take away rights related to physical deficiencies",
        ["Yes, if the defect is behind a wall",
         "Yes, after the buyer waives an inspection",
         "Yes, whenever the seller marks the report 'unknown'"],
        "Section 20-329ff says nothing in the nonmaterial-fact sections alters a purchaser's or lessee's legal rights concerning physical deficiencies.",
        cgs("20-329ff")))

    A(item("ct-agency",
        "A buyer uses an interpreter who is not the licensee and not the licensee's employee. The licensee must:",
        "Give the statutory interpreter form to the buyer and the interpreter and get both signatures",
        ["Skip paperwork if the interpreter seems fluent",
         "Have the interpreter sign the deed as a grantee",
         "Refuse to work with any interpreter"],
        "Section 20-327i(a) requires that form, including the statements that the contract obligations were explained in the buyer's or renter's native language.",
        cgs("20-327i")))

    A(item("ct-agency",
        "If the licensee personally acts as the buyer's interpreter, the statute requires a form:",
        "In the buyer's native language, unless that language cannot be reduced to writing",
        ["Only in Latin",
         "That transfers the licensee's commission to the buyer",
         "That waives all property disclosures"],
        "Section 20-327i(b) requires a signed form in the buyer's or renter's native language when the licensee acts as interpreter. If the language cannot be written, subsection (c) says the form is in English.",
        cgs("20-327i")))

    # --- CT-specific laws ---
    A(item("ct-laws",
        "A person offers a one-to-four family Connecticut home for sale. When is the written residential condition report due to the buyer?",
        "Any time before the buyer signs a binder, purchase contract, option, or lease that contains a purchase option",
        ["Within three days after closing",
         "Only if the buyer hires an inspector",
         "After the deed is recorded"],
        "Section 20-327b(a) requires the report at any time prior to the buyer's execution of any binder, contract to purchase, option, or lease containing a purchase option. A copy with the buyer's receipt is attached to the offer, binder, or contract.",
        cgs("20-327b"), event=True))

    A(item("ct-laws",
        "The residential condition report statute applies to residential property of how many dwelling units?",
        "One to four, including cooperatives and condominiums",
        ["Only single-family houses on two or more acres",
         "Any property with five or more units",
         "Commercial warehouses only"],
        "Section 20-327b(c) limits the section to sales, exchanges, or leases with option to buy of residential property of not less than one nor more than four dwelling units, including cooperatives and condominiums, whether or not a licensee is involved.",
        cgs("20-327b")))

    A(item("ct-laws",
        "The statutory instructions on the residential condition report tell the seller:",
        "Your real estate licensee cannot complete this form on your behalf",
        ["Your licensee must fill in every answer",
         "Leave all answers blank until the inspection",
         "The report replaces a warranty deed"],
        "The template text in section 20-327b(d) says the seller must answer all questions to the best of the seller's knowledge and that the real estate licensee cannot complete the form for the seller.",
        cgs("20-327b")))

    A(item("ct-laws",
        "The seller never provides a required residential condition report. The purchase agreement must require the seller to credit the buyer how much at closing?",
        "$500",
        ["$300", "$1,000", "Nothing, if the seller offers an inspection"],
        "Section 20-327c(a) requires a $500 credit at closing if the seller fails to furnish the required report. Giving the credit does not excuse disclosure of a known defect that significantly impairs value, health or safety, or useful life.",
        cgs("20-327c"), event=True))

    A(item("ct-laws",
        "The seller gives the $500 credit and stays quiet about a known foundation problem that significantly impairs the house. The credit:",
        "Does not excuse that nondisclosure",
        ["Ends every duty to disclose",
         "Transfers liability to the town clerk",
         "Creates a new warranty that the house is perfect"],
        "Section 20-327c(b) says the credit does not excuse failure to disclose a defect that must be disclosed, is within the seller's actual knowledge, and significantly impairs value, health or safety, or useful life. The buyer may sue for actual damages.",
        cgs("20-327c")))

    A(item("ct-laws",
        "Does the condition-report law force the seller to hire an inspector?",
        "No. It creates no new warranty and does not require the seller to obtain inspections or tests",
        ["Yes, a licensed inspector is mandatory before every listing",
         "Yes, but only for condominiums",
         "Yes, and the licensee must pay for it"],
        "Section 20-327d says the report sections do not create a new implied or express warranty and do not require the seller to secure inspections, tests, or other methods of determining condition.",
        cgs("20-327d")))

    A(item("ct-laws",
        "The seller's statements on the residential condition report are measured by:",
        "The seller's actual knowledge",
        ["A guarantee of future condition",
         "Whatever the listing photos imply",
         "The buyer's hope for the neighborhood"],
        "Section 20-327e says the seller's representations are construed to extend to the seller's actual knowledge only.",
        cgs("20-327e")))

    A(item("ct-laws",
        "Which transfer is exempt from the ordinary residential condition report?",
        "A transfer by an executor, administrator, trustee, or conservator",
        ["An arm's-length sale of a lived-in three-family house",
         "A sale of a condominium unit by its occupant",
         "A lease with an option to buy a single-family house"],
        "Section 20-327b(b) lists exemptions, including transfers by executors, administrators, trustees, or conservators, certain family gifts, co-owner transfers, some new construction, and specified foreclosure-type transfers. Foreclosure properties in crumbling-foundation municipalities have a separate foundation report under subsections (g) and (h).",
        cgs("20-327b")))

    A(item("ct-laws",
        "The statutory condition-report template asks the seller about pyrrhotite. A separate Residential Foundation Condition Report is required for certain foreclosure and municipal transfers in municipalities that the Capitol Region Council of Governments finds affected by crumbling foundations. That special report covers:",
        "Known pyrrhotite and known foundation damage or deterioration",
        ["Only roof shingles",
         "The buyer's credit score",
         "School-district test scores"],
        "Sections 20-327b(g) and (h) require disclosure of actual knowledge about pyrrhotite in a concrete foundation and about damage or deterioration, including damage caused by pyrrhotite, through the Residential Foundation Condition Report.",
        cgs("20-327b")))

    A(item("ct-laws",
        "The condition-report template required by statute includes questions about:",
        "Lead paint and the number and condition of smoke and carbon monoxide detectors",
        ["The seller's income-tax return",
         "How much the buyer will borrow",
         "The licensee's commission split"],
        "The template in section 20-327b includes an asbestos/lead subsection asking whether lead paint is present, and a question on whether carbon monoxide or smoke detectors are located in a dwelling and whether there have been problems with them.",
        cgs("20-327b")))

    A(item("ct-laws",
        "Under section 46a-64c(a)(1), which reason for refusing to rent after a bona fide offer is a discriminatory housing practice?",
        "The applicant's lawful source of income",
        ["The applicant's offered rent is below the advertised rent",
         "The applicant refused to sign a lease",
         "The unit is already rented to someone else"],
        "Section 46a-64c(a)(1) prohibits refusing to sell or rent, or refusing to negotiate, because of race, creed, color, national origin, ancestry, sex, gender identity or expression, marital status, age, lawful source of income, familial status, veteran status, or status as a victim of domestic violence, sexual assault, or trafficking.",
        cgs("46a-64c", CH814), event=True))

    A(item("ct-laws",
        "Lawful source of income, as defined for Connecticut discrimination law, includes:",
        "Housing assistance, Social Security, child support, alimony, and public or state-administered general assistance",
        ["Only wages from a private employer",
         "Gifts that have not been reported",
         "A roommate's promise with no income"],
        "Section 46a-63(3) defines lawful source of income to include income from Social Security, supplemental security income, housing assistance, child support, alimony, or public or state-administered general assistance.",
        cgs("46a-63", CH814)))

    A(item("ct-laws",
        "A landlord refuses every applicant who uses housing assistance and will not look at any of them individually. That practice runs into the ban on discrimination based on:",
        "Lawful source of income",
        ["The conveyance tax",
         "Adverse possession",
         "Net listings"],
        "Housing assistance is a lawful source of income under section 46a-63, and section 46a-64c(a) forbids refusing to rent because of it. Subsection (b)(5) still allows denial based on insufficient income. That is not a license to reject every assistance recipient as a class.",
        cgs("46a-64c", CH814), event=True))

    A(item("ct-laws",
        "Refusing a reasonable accommodation in rules or services that a person with a disability needs in order to use a dwelling is addressed in Connecticut fair housing law as:",
        "Discrimination on the basis of physical or mental disability",
        ["A permitted owner preference",
         "A conveyance-tax exemption",
         "Something only federal law mentions, not Connecticut law"],
        "Section 46a-64c(a)(6) treats disability-based refusals to sell or rent, and refusals to make reasonable accommodations in rules, policies, practices, or services, as discriminatory.",
        cgs("46a-64c", CH814)))

    A(item("ct-laws",
        "Steering a buyer only toward neighborhoods identified with the buyer's protected class, while another suitable dwelling is available elsewhere, is described in section 46a-64c as:",
        "A discriminatory restriction of housing choice",
        ["Ordinary customer service",
         "Required designated agency",
         "A municipal tax option"],
        "Section 46a-64c(a)(4)(B) makes it a violation to restrict a buyer or renter's choices to an area substantially populated by the same protected class when another dwelling that meets their stated criteria is available in an area that is not.",
        cgs("46a-64c", CH814), event=True))

    A(item("ct-laws",
        "For profit, urging owners to sell because people of a particular protected class are moving into the neighborhood is:",
        "Prohibited inducement under section 46a-64c",
        ["A required listing presentation",
         "Allowed if the statements are rumors",
         "Called blockbusting only when it happens in another state"],
        "Section 46a-64c(a)(5) prohibits, for profit, inducing or attempting to induce a person to sell or rent by representations about the entry of persons of a particular protected class. That is the statute's blockbusting-style ban.",
        cgs("46a-64c", CH814)))

    A(item("ct-laws",
        "The fair-housing exemptions in section 46a-64c(b) include:",
        "Rental of a unit in an owner-occupied dwelling of no more than two families",
        ["Every apartment building with an elevator",
         "Any refusal based on lawful source of income, with no exception for insufficient income",
         "Advertising that states a racial preference"],
        "Subsection (b)(1) exempts rental of rooms in an owner-occupied single-family dwelling and a unit in an owner-occupied dwelling of no more than two families. Other subsections narrow marital status, age, familial status, and insufficient-income situations. Advertising a prohibited preference is still covered by subsection (a)(3).",
        cgs("46a-64c", CH814)))

    A(item("ct-laws",
        "A landlord demands a security deposit from a tenant who is 40 years old. The maximum the statute allows is:",
        "Two months' rent",
        ["One month's rent", "Three months' rent", "There is no statutory cap"],
        "Section 47a-21(b)(1) says a landlord shall not demand a security deposit exceeding two months' rent from a tenant under 62. For a tenant 62 or older, the cap is one month's rent.",
        cgs("47a-21", CH831)))

    A(item("ct-laws",
        "A tenant is 62 or older. The security-deposit cap is:",
        "One month's rent",
        ["Two months' rent", "Half of one month's rent", "Four months' rent"],
        "Section 47a-21(b)(2) limits the demand to one month's rent when the tenant is 62 or older, and it tells the landlord to return the excess on request if the tenant turns 62 after paying a larger deposit.",
        cgs("47a-21", CH831)))

    A(item("ct-laws",
        "Whose property is a residential security deposit while the landlord holds it?",
        "The tenant's property, with the landlord holding a security interest",
        ["The landlord's property as soon as it is paid",
         "The town's property",
         "The broker's commission"],
        "Section 47a-21(c) says the deposit remains the tenant's property and the landlord has a security interest to secure the tenant's obligations. It is not subject to the landlord's creditors.",
        cgs("47a-21", CH831)))

    A(item("ct-laws",
        "After a tenancy ends, the landlord must return the security deposit and interest, or send an itemized damage statement, not later than:",
        "21 days after termination, or 15 days after written notice of a forwarding address, whichever is later",
        ["3 banking days", "The next May 31", "One year"],
        "Section 47a-21(d)(2) sets that timing. A landlord who violates the return rules can be liable for twice the deposit, with a smaller penalty if the only failure is to deliver accrued interest.",
        cgs("47a-21", CH831), event=True))

    A(item("ct-laws",
        "A residential landlord must put the security deposit:",
        "Immediately into an escrow account at a financial institution in Connecticut",
        ["In the landlord's personal checking account",
         "In cash in the unit",
         "With the real estate commission"],
        "Section 47a-21(h) requires the entire deposit to go immediately into one or more escrow accounts in a financial institution for the tenant's benefit. The landlord is the escrow agent and may withdraw only for reasons the statute lists. The Department of Banking's security-deposit page explains the same escrow rule.",
        src("Conn. Gen. Stat. § 47a-21 and CT Department of Banking, Rental Security Deposits", DOB_DEP)))

    A(item("ct-laws",
        "The state real-estate conveyance tax applies when consideration equals or exceeds:",
        "$2,000",
        ["$800", "$800,000", "$2,500,000"],
        "Section 12-494 imposes the tax when consideration equals or exceeds $2,000. Section 12-498(a)(10) exempts deeds when consideration is less than $2,000. The $800,000 and $2,500,000 figures are brackets for the higher state rates on residential estates, not the threshold for whether any tax applies.",
        cgs("12-494", CH223)))

    A(item("ct-laws",
        "On a residential sale, the basic state conveyance-tax rate on consideration up to $800,000 is:",
        "Three-quarters of one percent (0.75%)",
        ["One-quarter of one percent (0.25%)",
         "One and one-quarter percent (1.25%) on the entire price",
         "Two and one-quarter percent (2.25%) on the first dollar"],
        "Section 12-494(a)(1) sets the state rate at three-quarters of one percent, and subsection (b)(2) keeps that rate on the portion of a residential estate up to and including $800,000. The municipal piece under subsection (a)(2) is a separate one-quarter of one percent.",
        cgs("12-494", CH223)))

    A(item("ct-laws",
        "For a residential estate, the state conveyance-tax rate on the portion of consideration above $800,000 and up to $2,500,000 is:",
        "1.25 percent",
        ["0.25 percent", "0.75 percent", "2.25 percent"],
        "Section 12-494(b)(2)(C) sets, on and after July 1, 2020, a state rate of one and one-quarter percent on that middle band, and two and one-quarter percent only on the portion above $2,500,000.",
        cgs("12-494", CH223)))

    A(item("ct-laws",
        "The municipal conveyance tax at the base rate in section 12-494(a)(2) is:",
        "One-quarter of one percent of the consideration",
        ["Three-quarters of one percent",
         "A flat $500",
         "Paid to the Commissioner of Revenue Services by the buyer"],
        "The municipal component is one-fourth of one percent and becomes part of the municipality's general revenue. A targeted investment community, or a municipality with a qualifying manufacturing plant, may impose an additional local tax of up to another one-fourth of one percent under subsection (c).",
        cgs("12-494", CH223)))

    A(item("ct-laws",
        "Who pays the conveyance tax, and to whom, when the deed is recorded?",
        "The person conveying the property pays the town clerk of the town where the property is situated",
        ["The buyer pays the Real Estate Commission",
         "The listing salesperson pays PSI",
         "The lender withholds it from the mortgage"],
        "Section 12-495 says the tax is payable by the person conveying the property, to the town clerk of the town where the real property or any part of it is situated, upon recording.",
        cgs("12-495", CH223)))

    A(item("ct-laws",
        "A deed between spouses is presented for recording. The conveyance-tax statute:",
        "Exempts deeds between spouses",
        ["Taxes them at 2.25 percent",
         "Exempts them only if the price is over $800,000",
         "Requires the $500 condition-report credit instead of tax"],
        "Section 12-498(a)(14) says the conveyance tax shall not apply to deeds between spouses. Other exemptions include deeds that merely change the form of ownership with no change in beneficial ownership.",
        cgs("12-498", CH223)))

    A(item("ct-laws",
        "A first transfer of the owner's principal residence can be exempt from conveyance tax when a licensed engineer has found the concrete foundation was made with defective concrete because of pyrrhotite. The exemption is not available if:",
        "The transferor received financial assistance to repair or replace that foundation from the Crumbling Foundations Assistance Fund",
        ["The house is in Connecticut",
         "The buyer intends to live there",
         "The deed is recorded with the town clerk"],
        "Section 12-498(a)(21) creates that exemption for the first transfer after the written evaluation, and it withholds the exemption from a transferor who received that fund assistance.",
        cgs("12-498", CH223)))

    A(item("ct-laws",
        "Uninterrupted adverse use for a right-of-way over someone else's land must continue for how long before a prescriptive easement can arise under the statute?",
        "15 years",
        ["5 years", "7 years", "21 years"],
        "Section 47-37 says no person may acquire a right-of-way or other easement by adverse use unless the use has continued uninterrupted for fifteen years.",
        cgs("47-37", CH822)))

    A(item("ct-laws",
        "Connecticut's statute on entry upon land, which sets the period associated with adverse possession, uses a period of:",
        "15 years",
        ["10 years", "20 years", "30 years"],
        "Section 52-575 requires entry upon land to be made within fifteen years. The Office of Legislative Research describes adverse possession as open, visible, and exclusive possession uninterruptedly for that 15-year period.",
        src("Conn. Gen. Stat. § 52-575", f"{CH926}#sec_52-575")))

    A(item("ct-laws",
        "Property used for a purpose other than residential use, except unimproved land, is taxed at what state conveyance-tax rate?",
        "1.25 percent of the consideration",
        ["0.25 percent", "0.75 percent of only the first $800,000", "2.25 percent of the first dollar"],
        "Section 12-494(b)(1) imposes the state tax at one and one-quarter percent on conveyances of real property used for any purpose other than residential use, except unimproved land. Unimproved land includes land designated as farm, forest, or open space.",
        cgs("12-494", CH223)))

    A(item("ct-laws",
        "A willful misrepresentation of a fact required on a license application is punishable as:",
        "A crime under the misrepresentation section of the license law, separate from administrative discipline",
        ["A conveyance-tax exemption",
         "Nothing, if the exam was passed",
         "A reason to waive continuing education forever"],
        "Section 20-324 penalizes willfully misrepresenting any fact required to be disclosed in an application or other paper filed under the chapter. Administrative suspension or revocation can also follow a license obtained by false representation under section 20-320.",
        cgs("20-324")))

    A(item("ct-laws",
        "The November 2025 PSI bulletin tells candidates to arrive at the test center at least how long before the appointment?",
        "15 minutes",
        ["At the start time is fine", "Two hours", "The night before"],
        "The bulletin says to arrive at least 15 minutes early for sign-in and identification. A late arrival may mean the candidate is not admitted and forfeits the fee. It also says one valid, unexpired, photo identification is required.",
        PSI_SRC))

    A(item("ct-laws",
        "The November 2025 PSI security rules list which item among prohibited items in the examination room?",
        "A handheld calculator",
        ["The candidate's photo identification",
         "Eyeglasses used for reading",
         "A religious head covering"],
        "The updated bulletin's prohibited-item list includes handheld calculators, phones, notes, and other personal items. An on-screen testing system is not the same as bringing a handheld calculator. Religious head coverings are distinguished from hats worn for other reasons.",
        PSI_SRC, event=True))

    return q
