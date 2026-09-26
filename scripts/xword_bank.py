"""Original clue bank for CT License Trail crosswords.

Clues are written for this project. A clue that states a Connecticut fact
carries a source key. Nothing here is taken from a published crossword.
"""

SOURCES = {
    "psi": {
        "label": "PSI CT Real Estate Candidate Information Bulletin (updated Nov. 13, 2025)",
        "url": "https://test-takers.psiexams.com/ctre",
    },
    "dcp-exam": {
        "label": "CT DCP, Real Estate Salesperson — Initial/Exam",
        "url": "https://portal.ct.gov/dcp/license-services-division/all-license-applications/real-estate-salesperson---initialexam",
    },
    "dcp-ce": {
        "label": "CT DCP, Real Estate Salesperson — Continuing Education",
        "url": "https://portal.ct.gov/dcp/continuing-education/real-estate-salesperson---continuing-education",
    },
    "20-314": {
        "label": "Conn. Gen. Stat. § 20-314",
        "url": "https://www.cga.ct.gov/current/pub/chap_392.htm#sec_20-314",
    },
    "20-319": {
        "label": "Conn. Gen. Stat. § 20-319",
        "url": "https://www.cga.ct.gov/current/pub/chap_392.htm#sec_20-319",
    },
    "20-319a": {
        "label": "Conn. Gen. Stat. § 20-319a",
        "url": "https://www.cga.ct.gov/current/pub/chap_392.htm#sec_20-319a",
    },
    "20-320": {
        "label": "Conn. Gen. Stat. § 20-320",
        "url": "https://www.cga.ct.gov/current/pub/chap_392.htm#sec_20-320",
    },
    "20-324a": {
        "label": "Conn. Gen. Stat. § 20-324a",
        "url": "https://www.cga.ct.gov/current/pub/chap_392.htm#sec_20-324a",
    },
    "20-324b": {
        "label": "Conn. Gen. Stat. § 20-324b",
        "url": "https://www.cga.ct.gov/current/pub/chap_392.htm#sec_20-324b",
    },
    "20-324k": {
        "label": "Conn. Gen. Stat. § 20-324k",
        "url": "https://www.cga.ct.gov/current/pub/chap_392.htm#sec_20-324k",
    },
    "20-325m": {
        "label": "Conn. Gen. Stat. § 20-325m",
        "url": "https://www.cga.ct.gov/current/pub/chap_392.htm#sec_20-325m",
    },
    "20-325f": {
        "label": "Conn. Gen. Stat. § 20-325f",
        "url": "https://www.cga.ct.gov/current/pub/chap_392.htm#sec_20-325f",
    },
    "47-37": {
        "label": "Conn. Gen. Stat. § 47-37",
        "url": "https://www.cga.ct.gov/current/pub/chap_822.htm#sec_47-37",
    },
    "12-494": {
        "label": "Conn. Gen. Stat. § 12-494",
        "url": "https://www.cga.ct.gov/current/pub/chap_223.htm#sec_12-494",
    },
}

# word, straight clue, optional wordplay, optional source key, exam flag
RAW = """
ESCROW|Money a neutral party holds until the deal closes|Cash that sits between offer and keys||1
EASEMENT|A right to use part of someone else's land|Permission to cross, stuck to the dirt||1
LIEN|A claim that attaches to title as security for a debt|What a creditor hangs on the deed||1
DEED|The document that transfers title to real estate|Paper that walks ownership across the street||1
AGENCY|The relationship in which one person acts for another|Who works for whom||1
TITLE|The right to own real estate, and the evidence of it|What the closer is really handing over||1
APPRAISAL|A supported opinion of value|A number with a reason attached||1
RIPARIAN|Rights that come with land beside flowing water|The riverbank's legal handshake||1
CONVEYANCE|The transfer of real estate from one owner to another|How title changes hands||1
FIDUCIARY|A duty of loyalty and care owed to a client|The highest hat an agent wears||1
EARNEST|Deposit that shows a buyer is serious|Money that means "I mean it"||1
LISTING|A broker's agreement to market a property|The sign before the sale||1
MORTGAGE|A pledge of real estate as security for a loan|The house, offered as collateral||1
AMORTIZE|To pay a loan down by regular installments|The slow goodbye to principal||1
CLOSING|The meeting where the deal is funded and title passes|The last appointment on the contract||1
PRORATE|To divide an expense by time between the parties|Splitting the bill by the calendar||1
EQUITY|The owner's interest above the liens|Value minus what is owed||1
POINTS|Prepaid interest charged as a percent of the loan|Discount dots on the lender's price||1
LEASE|A contract that transfers possession, not ownership|Rent, in writing||1
LESSEE|The tenant under a lease|The one who gets the keys and the rent bill||1
LESSOR|The landlord under a lease|The owner who lends possession||1
TENANT|A person who occupies under a lease|Someone living on another person's title||1
ZONING|Public rules that divide land by use|The map that says what may be built||1
SETBACK|The required distance between a building and the lot line|How far the porch must stay from the neighbor||1
GRANTOR|The person who transfers title by deed|The name that signs the deed away||1
GRANTEE|The person who receives title by deed|The name the deed is made out to||1
ADVERSE|Possession that is hostile to the owner's title|Holding land like you own it, without permission||1
FIXTURE|Personal property that has become part of the real estate|The chandelier that grew roots||1
CHATTEL|An item of personal property|Moveable property, not the land||1
REALTY|A short word for real property|Land, spelled the formal way||1
COVENANT|A promise in a deed or other real estate contract|A clause that swears to something||1
ABSTRACT|A summary of the documents in the chain of title|Title's greatest hits, in order||1
QUITCLAIM|A deed that transfers whatever interest the grantor has, with no warranties|The deed that shrugs||1
WARRANTY|A deed promise that the title is good|The grantor's "I'll stand behind this"||1
INTESTATE|Dying without a valid will|No will, so the statute writes one||1
TESTAMENT|A will|The document that speaks after death||1
PROBATE|The court process that settles a decedent's estate|Where a will goes to be believed||1
DEVISE|A gift of real property by will|Land left in a will||1
CODICIL|An amendment to a will|A will's postscript||1
ESCHEAT|The state's taking of property when no heir can be found|Title that comes home to the state||1
ESCHEATED|Taken by the state because no heir could be found|Title that reverted to the public||1
ESTIMATED|Given an approximate value|Priced before the appraisal is final||1
FREEHOLDS|Ownership estates, as opposed to leaseholds|Titles that are not rentals||1
REPAYMENT|Paying back the principal of a loan|The long job of the note||1
FRONTFOOT|A lot's street frontage, as one word|The measure along the curb||1
EMINENT|The power behind a taking for public use|Half of the phrase for condemnation power||1
CONDEMN|To take private land for public use with just compensation|The formal way the road gets wider||1
VARIANCE|Permission to break a zoning rule in a specific case|A zoning exception with a hardship story||1
PLAT|A map of a subdivision|The drawing that cuts one tract into lots||1
METES|The distances and directions in a survey description|The "how far, which way" half of a legal description||1
SURVEY|A measurement of land and its improvements|The tape measure, professionally||1
ACRE|A land measure of 43,560 square feet|The lot size that is not quite a football field||1
SECTION|A square mile in the rectangular survey, about 640 acres|One slice of a township||1
TOWNSHIP|A six-mile square in the government survey|Thirty-six sections, on paper||1
ASSESS|To set a value for taxation|What the town does before it sends the bill||1
MORTGAGEE|The lender who holds a mortgage|The bank's name on the security instrument||1
MORTGAGOR|The borrower who gives a mortgage|The owner who pledges the house||1
GUARANTOR|A person who promises to pay if the borrower does not|The backup signature on the debt||1
SEVERALTY|Ownership by one person alone|Title with no co-owner||1
REMAINDER|A future estate that follows a life estate|Who takes the land when the life tenant's estate ends||1
REVERSION|A future estate that returns to the grantor|Title that comes back home||1
PRORATION|The time-based split of an expense at closing|Taxes and rent, cut to the day||1
AMORTIZED|Paid off by a schedule of principal and interest|A loan with a finish line||1
PRINCIPAL|The unpaid amount of a loan, or a person who hires an agent|The sum that is not the interest||1
COMMINGLE|To mix client funds with a licensee's own money|Trust money in the wrong pocket||1
CONVERSION|Using trust funds as if they were your own|Escrow money that gets spent||1
DEFALCATE|To embezzle money entrusted to you|A fiduciary's worst verb||1
DIVERSION|Turning trust funds aside for a personal use|Client money sent the wrong way||1
ACCRETION|Gradual addition of land by water depositing soil|The slow gift of a river||1
RELICTION|Land uncovered when water recedes permanently|The shore that shows up and stays||1
NAVIGABLE|Waters the public may use for travel|A river the law treats as a highway||1
BENCHMARK|A survey mark of known elevation|The brass disk the surveyor trusts||1
MONUMENTS|Physical markers used in a legal description|Iron pins, stones, and old oaks in a deed||1
SURVEYING|Measuring land boundaries and features|The fieldwork behind the map||1
VALUATION|The process of estimating what property is worth|Appraisal's longer name||1
ASSESSING|Setting values for the tax roll|The assessor's day job||1
REDLINING|Refusing housing services in an area because of who lives there|A map used as a weapon||1
EXEMPTION|A statutory exception to a rule|The fine print that says "this law sits this one out"||1
DISPARATE|A kind of impact that can be discriminatory even if a rule looks neutral|Uneven results, even without a confession||1
OBEDIENCE|An agent's duty to follow lawful instructions|Doing what the client asked, if the law allows||1
SUBAGENCY|An agency relationship under another agent|An agent working under someone else's agent||1
DUALAGENT|One licensee assisting both parties in the same deal|Both sides of the table, one license||1
COVENANTS|Promises that run with a deed or a subdivision|The rules written into the land records||1
FEESIMPLE|The broadest private ownership of land|Ownership with no built-in end date||1
LIFEESTATE|Ownership limited to someone's lifetime|Title that ends when a named life does||1
DOMINANT|The estate that benefits from an appurtenant easement|The lot that gets to use the driveway||1
SERVIENT|The estate burdened by an easement|The lot that has to put up with the path||1
ENCUMBER|To place a lien, easement, or other burden on title|Adding weight to the deed||1
CHAIN|The sequence of past owners in a title search|Everyone who held the deed, in order||1
CLOUD|A claim or defect that makes title doubtful|The smudge on an otherwise clean deed||1
QUIET|A lawsuit brought to remove a cloud on title|Asking a court to hush a bad claim||1
BINDER|Money or a short agreement that holds a deal together early|The receipt that says the offer is real||1
OPTION|A contract right to buy during a set time, without a duty to buy|The right to say yes later||1
NOVATION|Replacing a contract or party with a new obligation|A fresh deal that retires the old one||1
ASSIGN|To transfer contract rights to someone else|Handing your side of the contract over||1
BREACH|A failure to perform a contract duty|The promise that did not happen||1
REMEDY|The cure a court or contract gives for a breach|What the injured party can ask for||1
PAROL|Oral evidence, as opposed to the written contract|Words that never made it onto the page||1
WAIVE|To give up a known right|Letting a contingency go on purpose||1
STEERING|Guiding buyers toward or away from an area because of a protected class|The tour that is really a sorting||1
PUFFING|Sales talk that a reasonable person would not take as fact|The adjective that got away||1
LATENT|A defect that is hidden and not easily discovered|The crack behind the paint||1
PATENT|A defect that is visible on an ordinary inspection|The hole you can see from the sidewalk||1
STIGMA|A nonphysical history that some buyers mind and the law may not require disclosing|The story the house cannot shake||1
KICKBACK|An illegal payment for a settlement referral|A thank-you check the law will not allow||1
BOYCOTT|A group refusal to deal, forbidden by antitrust law|Competitors agreeing to freeze someone out||1
LISTOR|A made-up nonword to ignore|
ESCROWED|Placed into a trust account|Parked with the neutral party||1
EARNESTMONEY|The buyer's good-faith deposit, in two words|Serious money, unspaced||1
NETLISTING|A listing in which the broker keeps everything above a set price|The listing Connecticut regulations do not allow|20-328-6a|1
BLOCKBUSTING|Pushing owners to sell by stirring fear about who is moving in|Panic, used as a sales pitch||1
PRESCRIPTIVE|An easement claimed through long adverse use|The path that became a right by time||1
APPURTENANT|An easement that benefits a neighboring parcel|The driveway right that belongs to the next lot||1
MARKETABLE|Title a reasonable buyer would accept|Title clear enough to sell||1
HABENDUM|The deed clause that begins "to have and to hold"|The deed's "what you get" paragraph||1
SEISIN|The covenant that the grantor actually owns the estate|A deed promise of true ownership||1
ALIENATION|The transfer of title, or a clause that limits it|Giving the property away, in one long word||1
ACCELERATE|To call an entire loan due after a default|The due date that jumps forward||1
DEFICIENCY|The debt left after a foreclosure sale does not cover the loan|What is still owed when the auction falls short||1
SHORTSALE|A sale for less than the mortgage balance, with the lender's approval|Closing under water, with permission||1
FORECLOSE|To enforce a lien by forcing a sale|The lender's last chapter||1
REDEMPTION|The right to reclaim property by paying what is owed|Buying the house back from the debt||1
LISPENDENS|Recorded notice that a property is in litigation|A lawsuit, posted on the land records||1
MECHANICS|A lien for unpaid work or materials on real estate|The contractor's claim on the building||1
VOLUNTARY|A lien the owner agreed to, such as a mortgage|The debt the owner signed up for||1
JUNIOR|A lien that gets paid after an earlier one|Second in line at the foreclosure||1
SENIOR|A lien with higher priority than later ones|First in line to be paid||1
PRIORITY|The order in which liens get paid|Who eats first when the property is sold||1
CONSTRUCTIVE|Notice the law pretends you have because a document was recorded|Notice you have even if you never looked||1
INQUIRY|Notice that would come from asking an obvious question|The duty to follow up on a red flag||1
PARTITION|A court split of co-owned property|When co-owners cannot share and a judge divides||1
TACKING|Adding a prior owner's adverse time to your own|Stacking years of hostile possession||1
HOSTILE|Possession without the owner's permission|The mindset adverse possession requires||1
NOTORIOUS|Possession open enough that the owner could notice|Hiding is not how you claim their land||1
IMPLIED|An easement or agency the law infers from conduct|The right nobody wrote down||1
NECESSITY|An easement required because a parcel would otherwise be landlocked|The legal way off a trapped lot||1
EMBLEMENTS|Crops that a tenant may return to harvest|Annual plants the farmer still owns||1
PERSONALTY|Personal property|The stuff that is not the land||1
ANNEXATION|Attaching personal property so it becomes a fixture|Bolting the shelves into the building||1
SEVERANCE|Removing a fixture so it is personal property again|Unbolting what had become real||1
COMPARABLES|Recent similar sales used to estimate value|The neighbors' closings, used as evidence||1
DEPRECIATE|To lose value from age or wear|The building's slow step down||1
FUNCTIONAL|Obsolescence from a poor design, not from age alone|A house that works badly even when it is new||1
EXTERNAL|Obsolescence caused by something outside the property|Value lost because of the street, not the kitchen||1
CURABLE|A defect whose repair makes economic sense|Worth fixing||1
INCURABLE|A defect that costs more to fix than it returns|Not worth the hammer||1
REPLACEMENT|The cost to build a similar utility with modern materials|Today's version of the building||1
REPRODUCTION|The cost to build an exact replica|Same house, same details, new invoice||1
GROSSRENT|Income before vacancy and expenses, in two squeezed words|The top line of a rental||1
CAPRATE|Net operating income divided by value|The percent that turns income into price||1
YIELD|The investor's return|What the money earns||1
USURY|Illegally high interest|A rate the law will not bless||1
BALLOON|A loan with a large final payment|The payment that saves the surprise for last||1
TEASER|A low introductory rate that will not last|The interest rate with a short friendship||1
CEILING|The highest a variable rate may go|The cap on the climb||1
MARGIN|The lender's add-on above an index|The spread stacked on the index||1
INDEX|The outside rate an adjustable loan follows|The number the ARM watches||1
PREPAID|An item paid ahead, credited at closing|Money already sent to the future||1
ARREARS|An item paid after it is earned, such as mortgage interest|The bill that looks backward||1
ACCRUED|An expense built up but not yet paid|What has been earned and is still unpaid||1
HAZARD|Insurance against fire and similar damage|The policy that covers the structure||1
PREMIUM|The price of an insurance policy|What you pay to keep the coverage||1
OPINION|What title insurance relies on a search to support|The examiner's view of the record||1
CLOUDED|Title with a defect or competing claim|Ownership with a question mark||1
MARKET|The place where buyers and sellers meet, or a value based on it|Where the price gets discovered||1
SITUS|The location of the land for tax and legal purposes|Where the parcel actually sits||1
FRONTAGE|The length of a lot along a street or water|The edge the address lives on||1
DEPTH|How far a lot runs back from the front|The dimension behind the curb||1
BUFFER|Land left open to separate different uses|The green gap zoning likes||1
DENSITY|How many units a zoning rule allows on the land|The crowd the ordinance will permit||1
HEIGHT|A zoning limit on how tall a building may be|The vertical line you may not cross||1
COVERAGE|The portion of a lot a building may cover|Footprint, as a zoning ratio||1
PERMIT|Official permission to build or occupy|The paper the inspector wants to see||1
ORDINANCE|A local law, such as a zoning code|The town's own statute||1
POLICE|The government power to regulate for health and safety|Half of the power that supports zoning||1
POWER|Authority to act|What an agent must be given||1
DOMAIN|The public-use side of eminent domain|The "public" half of a taking||1
COMPS|Sales used as evidence of value|Appraisal shorthand for comparables||1
BASIS|An owner's cost for tax purposes|The number gain or loss starts from||1
LEVERAGE|Using borrowed money to buy more property|Other people's money, on purpose||1
LIQUID|Assets that can be turned into cash quickly|Money that does not have to wait for a buyer||1
CAVEAT|A warning, as in caveat emptor|Latin for "watch out"||1
EMPTOR|The buyer in the phrase caveat emptor|The "buyer" half of an old warning||1
READY|One of the three words in a buyer who can complete the purchase|Willing and able's partner||1
WILLING|A buyer who actually wants to go through with the deal|Ready and able, plus desire||1
ABLE|Financially capable of completing the purchase|The buyer who can actually pay||1
CAUSE|The broker's effort that leads to the sale|Procuring ___, the reason the fee is earned||1
SPLIT|How two brokers divide one commission|The cut between the firms||1
POCKET|A listing kept out of the broader market|The card that never hits the service||1
BLIND|An ad that hides the broker's licensed identity|A sign with no name to call||1
PUFF|Exaggerated praise that is not a factual promise|Talk that sounds bigger than the facts||1
CLIENT|The person an agent represents|Not the customer||1
CUSTOMER|A person an agent assists without representing|The party on the other side of the duty||1
BROKER|The licensee who may operate independently and supervise others|The license above salesperson||1
SELLER|The owner offering property for sale|The grantor-to-be||1
BUYER|The person seeking to purchase|The offer's author||1
OWNER|The person who holds title|Whose name is on the deed||1
LENDER|The one who advances the loan|Money's source at the closing table||1
BORROW|To take a loan|What the mortgagor does||1
CREDIT|Money shown in someone's favor on a closing statement|The column that reduces what you bring||1
DEBIT|A charge on a closing statement|The column that increases what you owe||1
OFFER|A proposal that can become a contract if accepted|The first move toward a deal||1
ACCEPT|To agree to an offer and form a contract|The yes that binds||1
REJECT|To turn an offer down|The no that ends that proposal||1
COUNTER|A reply that changes the offer|The yes that is really a new offer||1
REVOKE|To take an offer back before it is accepted|Pulling the proposal off the table||1
VOID|A contract with no legal effect|The agreement that never was||1
VALID|A contract that the law will enforce|The agreement that holds||1
ORAL|Spoken, not written|A deal that may run into the statute of frauds||1
SEAL|An old formality on an instrument|The mark that once made a deed solemn||1
HEIR|A person who inherits under a statute|Family the intestacy rules pick||1
DEVISE|A gift of real estate by will|Land named in a will||1
LEGACY|A gift of personal property by will|What the will leaves that is not the land||1
TESTATOR|A person who dies leaving a valid will|The will's author||1
TESTATRIX|A woman who dies leaving a valid will|The will's author, in the older feminine form||1
DOWER|A surviving spouse's historical interest in land|An old marital estate||1
CURTESY|A surviving husband's historical estate|Dower's old counterpart||1
FREEHOLD|An ownership estate of uncertain duration|Title, as opposed to a leasehold||1
LEASEHOLD|The tenant's estate in the property|Possession measured by the lease||1
PERIODIC|A tenancy that renews from period to period|Month to month, until someone gives notice||1
SUFFER|A tenancy at ___ , when a holdover stays without permission|The estate of staying too long||1
HOLDOVER|A tenant who remains after the lease ends|The renter who did not leave||1
EVICTION|The legal removal of a tenant|How a landlord retakes possession through process||1
QUIET|The covenant of ___ enjoyment|The promise that possession will not be disturbed||1
WASTE|Damage by a tenant that hurts the property's value|Letting the house fall apart on purpose or by neglect||1
RENT|The price of possession|What the lease is priced in||1
GROSS|A lease in which the landlord pays the operating expenses|The rent that includes the extras||1
NET|A lease in which the tenant pays some ownership expenses|Rent, plus the bills the owner used to pay||1
PERCENT|A lease rent based on sales|The retail tenant's extra check||1
GROUND|A long lease of land, often for the tenant to build|Rent for the dirt, not the tower||1
ESTATE|An interest in real property|What you hold, from fee simple on down||1
FEE|An inheritable freehold estate|The ownership that can last forever||1
LIFE|The measuring stick of a life estate|Whose years limit the title||1
PUR|The Latin bit in pur autre vie|Someone else's life, in a phrase||1
VIE|Life, in the phrase pur autre vie|The French half of "another's life"||1
JOINT|A tenancy with survivorship|The co-ownership that skips the will||1
COMMON|A tenancy that allows unequal shares and no survivorship|Co-owners who can leave their share by will||1
UNITY|One of the four requirements of a joint tenancy|Time, title, interest, or possession||1
TIME|One of the four unities|The "we took title together" requirement||1
INTEREST|A unity, and also the cost of borrowing|The share that must match, or the lender's price||1
WHOLE|The right of survivorship, in a phrase: the survivor takes the ___ |What joint tenancy hands to the last owner||1
SURVIVE|To take a co-owner's share at death under joint tenancy|Outlast the other name on the deed||1
SEVER|To end a joint tenancy as to someone's share|Breaking the survivorship||1
PARTITION|Dividing co-owned land|The lawsuit that unsticks co-owners||1
CONDO|A unit owned separately, with a share of the common elements|An apartment you can deed||1
COOP|A building owned by a corporation, occupied by shareholders|Shares, a proprietary lease, and a board||1
BYLAWS|The internal rules of an association|How the condo governs itself||1
HOA|The owners' association, for short|Three letters that send the assessment||1
LIEN|A money claim on property||1
NOTE|The borrower's promise to pay|The IOU beside the mortgage||1
LOAN|Money advanced to be repaid|What the note describes||1
RATE|The price of the loan, as a percent|Interest, in a single syllable's neighbor||1
TERM|The length of a loan|How long the payments run||1
ARM|A loan whose rate can change|Three letters for an adjustable mortgage||1
FHA|A federal mortgage-insurance program|The initials on many low-down-payment loans||1
PMI|Private mortgage insurance|The policy that protects the lender above a high loan-to-value||1
APR|The loan's yearly cost, including certain fees|Interest plus the extras, as one percent||1
LTV|Loan amount compared with value|The fraction lenders watch||1
DTI|Debt payments compared with income|The ratio that asks if the borrower can carry it||1
PITI|Principal, interest, taxes, and insurance|The four-part house payment||1
NOI|Income left after operating expenses|The number a cap rate multiplies toward value||1
GRM|Price divided by gross rent|A quick rental multiplier||1
CMA|A broker's comparison of recent sales|Not an appraisal, and the letters say so||1
MLS|A shared listing database|Where cooperating brokers post the houses||1
HUD|The federal housing department, by its initials|Three letters on a lot of housing programs||1
ADA|The federal disability-access law, by its initials|The statute behind a reasonable accommodation||1
ECOA|The federal law against credit discrimination|Equal credit, in four letters||1
RESPA|The federal law against settlement kickbacks|The statute that watches closing charges||1
TILA|The federal truth-in-lending law|The statute behind a lot of loan disclosures||1
TRID|The integrated loan-disclosure rule, by its nickname|Loan estimate and closing disclosure, shortened||1
HMDA|The federal mortgage-data law|The statute that makes lenders report loan patterns||1
USPAP|Appraisal standards, by their initials|The rulebook an appraiser is judged by||1
ALTA|A title-insurance policy form, by its initials|Four letters on many owner's policies||1
FEMA|The agency behind flood maps|The mapmaker lenders ask about water||1
LEAD|The paint hazard in much older housing|The metal in a pre-1978 disclosure||1
RADON|A gas that can enter from the soil|The invisible basement test||1
MOLD|A moisture problem buyers and inspectors look for|What a wet wall can grow||1
SEPTIC|An on-site wastewater system|The tank instead of a sewer||1
WELL|A private water source|The hole that stands in for city water||1
FLOOD|The zone that can change insurance and loan rules|Water, as a mapped risk||1
EASE|To relieve, or the start of easement|Make it lighter||
LOT|A single parcel in a subdivision|The piece with its own boundaries||1
TAX|A government charge on property|The bill that follows assessment||1
FEE|A charge for a service|What the broker's agreement prices||1
CAP|A limit on a rate, or the start of capitalization|The lid, or the rate in reverse||1
NET|What remains after deductions|The lease or the listing that is not gross||1
ARM|An adjustable-rate mortgage, briefly|The loan that can wake up and change||1
AGE|How old an improvement is|A number in the cost approach||1
USE|What the zoning ordinance cares about first|Residential, commercial, or neither||1
MAP|A plat, less formally|How you see the lots||1
PIN|A parcel identification number, briefly|The assessor's label for the lot||1
ODD|Not even, or a strange exception|The leftover lot||1
OWN|To hold title|The verb before owner||1
PAY|To satisfy a debt|What retires the note||1
BID|An offer at an auction|The number shouted at a foreclosure sale||1
ASK|The seller's current price|What the listing hopes for||1
LOW|Under the asking price|Where many first offers sit||1
APP|Short for application|The form before the loan||1
REF|A referral, briefly|Sending a client and hoping that is legal||1
COD|Collect on delivery|Pay when it arrives||1
ETA|When you expect to arrive|The closing time, estimated||1
FAQ|Questions everyone asks|The sheet of usual answers||1
PDF|A document file buyers actually open|The contract, attached||1
SQL|Not a real estate term, skip|
SEVENTY|The Connecticut salesperson exam passing score, spelled out|Seven tens|psi|1
SIXTY|The minimum classroom hours of principles and practice before the Connecticut salesperson exam|A dozen times five|20-314|1
EIGHTEEN|The minimum age DCP lists for a salesperson applicant, spelled out|A dozen plus a half dozen|dcp-exam|1
TWELVE|The minimum continuing-education hours in a Connecticut two-year cycle, spelled out|A dozen|20-319|1
TWENTY|The one-time Real Estate Guaranty Fund fee, in dollars, spelled out|A score|20-324b|1
EIGHTY|The Connecticut salesperson application fee to be admitted to the exam, in dollars, spelled out|Four times twenty|20-314|1
FIFTEEN|The years of uninterrupted adverse use required for a Connecticut prescriptive easement|Three times five|47-37|1
SEVEN|The minimum years of Connecticut record retention after closing, disbursement, or expiration, spelled out|A week of days|20-325m|1
THREE|The banking days a Connecticut broker has to deposit trust money after all parties sign|A trio|20-324k|1
TWENTYFIVE|The affiliation-transfer fee for a Connecticut salesperson, in dollars, as one word|A quarter of a hundred|20-319a|1
FIVETHOUSAND|The maximum Connecticut license fine per violation, in dollars, as one word|Fifty hundreds|20-320|1
TWENTYONE|Days after termination in one prong of Connecticut's security-deposit return rule|Three weeks|47a-21|1
BLOCKBUST|Forcing a sale by fear, cut short unfairly|
AGENT|A person authorized to act for another|The license in the middle||1
OFFEROR|The person who makes an offer|The first pen on the proposal||1
OFFEREE|The person who receives an offer|The one who can accept||1
VENDEE|The buyer, in older deed language|The purchaser's formal name||1
VENDOR|The seller, in older deed language|The seller's formal name||1
TRUSTEE|A person who holds title for someone else|The name on a deed of trust's middle seat||1
TRUSTOR|The borrower under a deed of trust|The owner who conveys to the trustee||1
BENEFIT|What an appurtenant easement gives the dominant estate|The use the neighbor gets||1
BURDEN|What an easement puts on the servient estate|The duty to allow the use||1
RUNWITH|A covenant that stays with the land, squeezed together|It follows the dirt, not the person||1
AIRRIGHTS|The right to use the space above the land|Ownership that leaves the ground||1
SUBSURFACE|Rights to minerals and other materials below the surface|What is under the lawn||1
FRUCTUS|Crops, in the Latin property phrases|Fruit of the soil, as a legal word||1
NATURAL|Emblements are not the ___ crops that grow without annual labor|What perennial plants are, compared with a planted field||1
TRADE|A ___ fixture, removable by a commercial tenant|The tenant's shelves, in one word of a phrase||1
ADAPT|How well an item fits the building, in fixture tests|One of the questions: was it adapted?||1
INTEND|What the parties meant, in a fixture dispute|The annexation test that is in someone's head||1
METHOD|How an item was attached, in a fixture test|Bolts or gravity||1
RELATION|The parties' connection, which can decide a fixture|Landlord and tenant, or seller and buyer||1
HEREDITAMENT|Any property that can be inherited|A very long word for what heirs can take||1
BEARING|A survey direction|The compass piece of metes||1
AZIMUTH|A direction measured in degrees from north|A surveyor's angle||1
CHAIN|A survey unit of 66 feet, and also a title history|Four rods, or the owners in a row||1
ROD|A survey unit of 16.5 feet|A quarter of a chain||1
LINK|A hundredth of a survey chain|7.92 inches, in old fieldwork||1
FURLONG|A distance of 40 rods|An old land measure, also a horse-racing word||1
HECTARE|A metric land measure of 10,000 square meters|The acre's metric cousin||1
SQUARE|A shape, or the word before footage|The area word||1
WIDTH|The side-to-side measure|Frontage's indoor cousin||1
LENGTH|The long measure|How far the boundary runs||1
AREA|Length times width, for a rectangle|The size inside the lines||1
VOLUME|The space inside a three-dimensional shape|What a warehouse cube is measured in||1
RANGE|A column of townships east or west of a meridian|The government survey's sideways count||1
TIER|A row of townships north or south of a baseline|The government survey's vertical count||1
BASE|The line townships are counted from, briefly|Where the tiers begin||1
NORTH|A cardinal direction on a survey|The top of most maps||1
SOUTH|The opposite of north on a survey|Toward the bottom of the map||1
EAST|A cardinal direction|Where the sun comes up, on a deed||1
WEST|A cardinal direction|Sunset, as a bearing||1
ANGLE|The turn between two survey lines|Where metes change direction||1
POINT|A place where a boundary begins, or a loan charge|Of beginning, or a percent of the loan||1
BEGIN|The starting place in a metes-and-bounds description|Where the description says "commencing"||1
THENCE|The survey word that means "from there"|The deed's way of saying "next"||1
ALONG|Following a boundary|The word before "the stone wall"||1
ABOUT|Approximately, in an old description|The deed's shrug about a distance||1
MORE|Extra, as in "more or less"|The phrase that softens a distance||1
LESS|The other half of "more or less"|Not exact||1
SAID|Already mentioned, in deed language|The lot previously named||1
BEING|A deed word that introduces a description|The clause that starts "the same premises"||1
KNOWN|Identified, as a lot on a recorded map|The parcel people can find||1
LOTNO|A lot number, squeezed together|What the plat uses instead of a novel||1
BLOCK|A group of lots|The plat's bigger box||1
PHASE|A section of a larger development|The part they build first||1
UNIT|One condo or one dwelling|The thing the deed actually describes in a condo||1
SHARE|A co-owner's fraction|Your piece of the common elements||1
VOTE|What an association member casts|How bylaws get amended||1
BOARD|The group that runs an association|Who hires the manager||1
PROXY|Authority to vote for someone else|A ballot sent with a neighbor||1
QUORUM|The number who must be present to vote|Enough owners to hold the meeting||1
MINUTES|The written record of a meeting|What the board secretary keeps||1
BUDGET|The association's spending plan|Where the assessment comes from||1
DUES|Regular association charges|The HOA bill||1
FINE|A penalty an association or a license law may impose|The costly kind of mistake||1
RULE|A bylaw or a license restriction|What you do not get to invent||1
SIGN|The board in the yard|How the street learns it is for sale||1
LOCK|A keybox, briefly|How the showing gets in||1
SHOW|To tour a property with a buyer|The appointment after the inquiry||1
OPEN|A house event the public may attend|Sunday afternoon, with the sign out||1
TOUR|A broker's caravan of listings|Looking, with colleagues||1
PRICE|What the seller hopes, until the market answers|The number on the listing||1
VALUE|What it is worth, which may not be the price|Appraisal's target||1
COST|What you spend to build or buy|Not the same as value||1
WORTH|Value, in plainer speech|What a buyer will pay is a clue to it||1
CASH|Money that is not a promise|The earnest form lenders understand||1
WIRE|How closing funds often move|The transfer you verify twice||1
CHECK|A written order to pay, risky as earnest money|Paper payment||1
FUNDS|Money available to close|What "good" modifies at the closing||1
CLEAR|Title with no unacceptable defects|Marketable, in one word||1
CLEAN|Free of problems|The inspection you hope for||1
DIRT|Land, in slang|What this whole exam is about||1
KEYS|What changes hands with possession|The metal end of the closing||1
DOOR|The way in|Where the lockbox hangs||1
YARD|The land around a house|Setback's outdoor room||1
FENCE|A possible encroachment|The board that may have crossed the line||1
SHED|An outbuilding|Personal taste, and sometimes a permit question||1
POOL|A water feature that can matter to value and insurance|The backyard that needs a fence||1
DECK|An exterior improvement|Wood that may or may not be a fixture fight||1
ROOF|The inspection item everyone asks about|What keeps the NOI from leaking||1
HVAC|Heating and cooling, as four letters|The system the inspector starts up||1
SEWER|A public wastewater line|The alternative to a septic tank||1
WATER|A utility, or the source of riparian rights|What the well or the town supplies||1
POWER|Electric service, or legal authority|What the meter measures, or the agency grant||1
CABLE|A utility line|The wire that is not the deed||1
SOLAR|Energy equipment that raises fixture questions|Panels, and whose property they are||1
GREEN|Building practices that can affect value|Efficiency, as a selling word||1
URBAN|A location type|Not the farm||1
RURAL|A location outside the city|Where the septic system is more likely||1
SUBURB|A residential area near a city|The lawn between downtown and the farm||1
AVENUE|A street type in a legal description|The word after the name on many addresses||1
STREET|A public way|Frontage's neighbor||1
ALLEY|A narrow way behind lots|The access easement you might have missed||1
CURB|The edge of the street|Where the sign gets planted||1
WALK|A sidewalk|The path in a municipal easement||1
PARK|To leave the car, or a public green|The noun beside "ing" at a showing||1
RIDE|A trip between appointments|Why this game is built in threes||1
ROAD|The way from town to town|This app's metaphor, and a frontage word||1
TOWN|A municipality|Where the deed gets recorded||1
CITY|A larger municipality|Hartford, for example, without making it a clue fact||1
CLERK|The town official who records deeds|Who stamps the conveyance||1
STAMP|What the recording office puts on a deed|Proof it landed in the records||1
BOOK|A volume of land records|Where the page number lives||1
PAGE|The place in the land records|The second half of book and ___||1
DATE|When a document was signed or recorded|The line above the signature||1
YEAR|Twelve months, or a lease term|What "annual" divides into||1
MONTH|A rent period|The usual periodic tenancy||1
WEEK|Seven days|A short rental, and a crossword's Monday||1
HOUR|Sixty minutes|How prelicense class time is counted||1
DAYS|Calendar units longer than hours|The proration pieces||
TIME|A unity of joint tenancy, or the clock|When the owners took title together||1
SOON|Coming ___, a listing phrase that is still advertising|Not yet on the market, but already talking||1
LATER|After now|When the contingency is due||1
NEVER|Not at any time|On no calendar||
ALWAYS|At all times|How often client funds should stay out of a personal account||1
PRIOR|Earlier|The lien that was recorded first||1
AFTER|Later than|The junior lien's position||1
UNDER|Below|Where minerals sit||1
ABOVE|Higher than|Where air rights are||1
EQUAL|The same|What joint tenants' interests traditionally are||1
UNEQUAL|Not the same size|What tenants in common are allowed to own||1
SHARE|A fraction of ownership|Your piece||1
HALF|Fifty percent|A common co-owner's fraction||1
THIRD|One of three|A sibling's intestacy piece, sometimes||1
WHOLE|One hundred percent|Severalty's amount||1
NONE|Zero|The warranties in a quitclaim deed||1
SOME|A partial interest|What a life tenant has, not the fee||1
BOTH|The two parties|Who must consent before dual agency is real||1
EACH|Every one|Apiece||
PER|For each|The word before "violation" in the fine statute||1
ALL|Everyone|The whole group||
ANY|Whichever|A buyer ready, willing, and able||1
ONE|A single|Severalty's headcount||1
TWO|A pair|How many parties make an agency relationship||1
FOUR|The number of unities in a joint tenancy|Time, title, interest, possession||1
FIVE|A handful|Fingers, not a license fine||1
SIX|A half dozen|One less than the record-retention years||1
NINE|A digit|Three squared||1
TEN|A decade of units|The word before "ancy" in a leasehold estate's cousin||1
ACE|A playing card of the highest rank in many games|A top mark||
ACT|A statute, or to do something|What the legislature passes||
ADD|To put on|Annex, in arithmetic||
AGE|Years since construction|Actual, not effective||
AID|Help|Assistance||
AIM|A goal|What the listing price should have||
AIR|The space above land|Rights, vertically||
ALE|A drink|Not escrow||
ANT|A small insect|Picnic guest||
APE|A primate|Copy, as a verb in old slang, but here the animal||
APT|Fitting|A suitable description||
ARC|A curve|Part of a circle on a fancy plat||
ARE|A metric land measure of 100 square meters|Exist, or a small area unit||
ARK|A boat in an old story|What a flood map hopes you do not need||
ART|Creative work|Not a fixture unless it is bolted and intended to stay||
ASH|A tree, or what a fire leaves|Monument material, sometimes||
ATE|Consumed|Past tense of eat||
AWE|Wonder|The feeling a cleared title can give||
AXE|A tool|How you might sever timber, carefully||
BAD|Not good|A defect||
BAG|A sack|What you do not put the earnest money in||
BAN|A prohibition|What antitrust law puts on price fixing||
BAR|To prevent|What a cloud can do to a sale||
BAT|A flying mammal, or a club|The animal in a belfry inspection joke||
BAY|A part of a building, or a body of water|Window ___||
BED|A piece of furniture, usually personal property|Where you sleep, and usually not a fixture||
BEE|An insect|Spelling contest||
BET|A wager|Not a financing plan||
BID|An offer|Auction word||
BIG|Large|The lot you wanted||
BIN|A container|Storage||
BIT|A small piece|A little of the commission||
BOA|A snake, or a scarf|Not a deed||
BOW|A knot, or the front of a ship|Ribbon||
BOX|A container|Lock___||
BOY|A child|Not a party to the contract||
BUD|A flower not yet open|Spring, on the inspection calendar||
BUG|An insect|Inspection surprise||
BUN|A bread roll|Snack between showings||
BUS|A large vehicle|Transit, which can affect value||
BUT|Except|The conjunction in "all but"||
BUY|To purchase|The client's verb||
CAB|A taxi|A ride, not a closing||
CAN|Is able|Able, in smaller letters||
CAP|A limit|Rate ceiling||
CAR|An automobile|Not real property||
CAT|A pet|Personal property with opinions||
COW|A farm animal|Chattel, unless you have a very odd deed||
CUP|A drinking vessel|Personal property||
CUT|To divide|What a plat does to acreage||
DAM|A barrier on water|Something that can change riparian facts||
DAY|Twenty-four hours|The proration unit||
DEN|A room|The office on the listing sheet||
DEW|Morning moisture|Not a cloud on title||
DID|Performed|Past tense of do||
DIG|To excavate|What you need a permit for, often||
DIP|A decline|A small drop in the market||
DOC|A document, informally|The deed, to a friend||
DOG|A pet|Personal property that is not an emblement||
DOT|A small mark|On the survey||
DRY|Not wet|The basement you advertise carefully||
DUB|To nickname|Call||
DUE|Owed|The balloon, when it is ___||
DUG|Excavated|Past tense of dig||
DYE|A colorant|Not "die"||
EAR|The organ of hearing|Lend an ___||
EAT|To consume|What taxes do to equity, slowly||
EEL|A fish|Slippery, like a bad legal description||
EGG|An oval breakfast|Not a fixture||
ELF|A folklore figure|Tiny||
ELK|A large deer|Wildlife, not a chattel in the listing||
ELM|A tree|Possible monument||
EMU|A large bird|Australian, not a deed form||
END|The last part|Of the listing period||
ERA|A period of time|Age||
EVE|The day before|Closing ___||
EWE|A female sheep|Sounds like "you"||
EYE|The organ of sight|What a patent defect is obvious to||
FAN|An admirer, or a ventilator|Ceiling ___, often a fixture fight||
FAR|Distant|Not the subject property||
FAT|Thick|A file||
FAX|A telecopied document|Old-fashioned delivery of an offer||
FED|A federal agency, informally|The level above the town||
FEE|An estate or a charge|Simple, or the broker's||
FEW|Not many|Comps, in a thin market||
FIG|A fruit|Not an emblement unless someone planted it as a crop||
FIN|A fish part|End||
FIR|An evergreen|Possible natural monument||
FIT|Suitable|Habitability's cousin||
FIX|To repair|Cure a defect||
FOG|Thick mist|Not a cloud on title, though the metaphor is tempting||
FOR|In favor of|The word before "sale"||
FOX|A wild canine|Sly||
FRY|To cook in oil|Small fish||
FUN|Enjoyment|Not a contract element||
FUR|An animal coat|Personal property||
GAP|An opening|A break in the chain of title||
GAS|A utility|The line the seller should not "forget"||
GEM|A jewel|A house the buyer loves||
GET|To obtain|Receive title||
GIG|A job|The showing||
GIN|A card game, or a machine|Rummy||
GOT|Obtained|Past tense of get||
GUM|A chewy candy, or a tree|Stick||
GUN|A weapon|Not a closing gift||
GUT|To strip a building's interior|Renovate down to the studs||
GUY|A person, informally|Fellow||
GYM|An exercise room|A condo amenity||
HAD|Possessed|Past tense of have||
HAM|A cured meat|Not an emblement after it is packaged||
HAS|Possesses|Holds||
HAT|Headwear|What you do not wear as a second undisclosed agency||
HAY|Dried grass|An emblement, if it is this year's crop||
HEN|A female chicken|Livestock||
HER|That woman|Pronoun||
HEW|To chop|Cut timber||
HID|Concealed|What you may not do with a material defect||
HIM|That man|Pronoun||
HIP|The roof's external angle|Architecture, and a style||
HIT|To strike|Reach a price||
HOG|A pig|Livestock||
HOP|A small jump|Skip||
HOT|High in demand|A market, or a water heater||
HOW|In what way|The method of annexation||
HUB|A center|A survey stake, sometimes||
HUE|A color|Shade||
HUG|An embrace|Not a contract||
HUM|A low sound|The transformer, maybe||
HUT|A small shelter|Not usually a dwelling on the exam||
ICE|Frozen water|A sidewalk liability, not a title defect||
ICY|Covered in ice|Slippery||
ILL|Sick|Not habitable, maybe||
IMP|A mischievous creature|Small troublemaker||
INK|What a deed used to require|The signature's medium||
INN|A small hotel|Commercial use||
ION|A charged atom|Science class||
IRE|Anger|What commingling deserves||
IRK|To annoy|Bother||
ITS|Belonging to it|Possessive||
IVY|A climbing plant|On the wall, and sometimes in the siding||
JAM|A fruit spread, or a tight spot|Traffic, or jelly||
JAR|A container|Shock||
JAW|The mouth's hinge|Talk||
JET|A stream, or an aircraft|Black stone, or a plane||
JOB|Work|The listing||
JOG|A short run, or a bend in a boundary|A little turn in the property line||
JOY|Happiness|Closing day, if the numbers work||
JUG|A pitcher|Container||
KEY|What opens the door|Consideration, metaphorically, or the metal one||
KID|A child, or a young goat|Youngster||
KIN|Relatives|Heirs, informally||
KIT|A set of parts|Small collection||
LAB|A laboratory, or a dog|Room for tests||
LAD|A boy|Youth||
LAG|A delay|The time between offer and acceptance||
LAP|The top of the legs when seated|One circuit||
LAW|A binding rule|What this exam is full of||
LAY|To place|Set down||
LEA|A meadow|Open land||
LED|Guided|Past tense of lead||
LEG|A part of a journey or a survey course|One metes segment||
LET|To lease, in older usage|Allow, or rent out||
LID|A cover|Cap||
LIE|A false statement|The kind of misrepresentation that is not puffing||
LIP|The edge|Rim||
LIT|Illuminated, or sued|Past tense of light||
LOG|A record, or a piece of timber|The book of showings||
LOT|A parcel|Plot||
LOW|Not high|Below market||
LUG|To carry|Haul||
MAD|Angry|Upset||
MAN|An adult male|Person||
MAP|A drawing of land|Plat||
MAT|A floor covering|Rug||
MAW|A mouth|Jaws||
MAY|Is permitted|The month, or the verb of discretion||
MEN|Adult males|People||
MET|Encountered|Past tense of meet||
MIX|To combine|What you must not do with escrow funds||
MOB|A crowd|Throng||
MOD|A modification, briefly|Change order||
MOP|A cleaning tool|Swab||
MUD|Wet soil|The inspection after rain||
MUG|A cup|Face, informally||
NAB|To catch|Grab||
NAG|To pester|A horse, or a reminder||
NAP|A short sleep|Rest between rides||
NET|After expenses|The lease type||
NEW|Not old|Recent construction||
NIL|Nothing|Zero||
NOD|A small bow|Agree silently||
NOR|And not|Neither's partner||
NOT|Negation|The word in "___ a fixture"||
NOW|At this time|The possession date you hope for||
NUN|A woman in a religious order|Sister||
NUT|A seed, or a cost to carry|Slang for the monthly number||
OAK|A hardwood tree|A classic monument||
OAR|A boat paddle|Row||
OAT|A grain|A crop||
ODD|Strange, or not even|Leftover||
ODE|A poem|Lyric||
OIL|A mineral|Subsurface, often||
OLD|Not new|Pre-1978, sometimes, for paint||
ONE|A single unit|Number before two||
OPT|To choose|Elect||
ORB|A sphere|Globe||
ORE|Raw mineral|What a mine estate is about||
OUR|Belonging to us|Possessive||
OUT|Not in|The sign direction||
OVA|Eggs|Plural of ovum||
OWE|To be indebted|What the note says you ___||
OWL|A night bird|Wise stereotype||
OWN|To have title|Hold||
PAD|A cushion, or a building site|Launch ___||
PAL|A friend|Buddy||
PAN|A cooking vessel, or to criticize|Skillet||
PAP|Soft food|Father, informally||
PAR|Equal to face|Standard||
PAT|A light tap|Dab||
PAW|An animal's foot|Foot||
PAY|To give money owed|Satisfy||
PEA|A small vegetable|A crop||
PEG|A pin|Stake||
PEN|A writing tool|What signs the deed||
PEP|Energy|Vigor||
PER|For each|Apiece||
PET|An animal companion|Personal property||
PEW|A bench in a church|Seat||
PIE|A baked dish|Chart||
PIG|A hog|Livestock||
PIN|A fastener, or a parcel number|Parcel ID, briefly||
PIT|A hole|The low spot on the lot||
PLY|A layer|Fold||
POD|A small group, or a seed case|Cluster||
POP|A sudden sound, or a parent|Soda, in some towns||
POT|A cooking vessel|Kettle||
POW|A comic-book hit|Impact||
PRY|To snoop, or a lever|Nose into||
PUB|A tavern|Public house||
PUN|A word joke|What a few of these clues are||
PUP|A young dog|Small canine||
PUT|To place|Set||
RAG|A scrap of cloth|Tatter||
RAM|A male sheep|Push||
RAN|Moved quickly in the past|Past tense of run||
RAP|A knock|Tap||
RAT|A rodent|Inspection problem||
RAW|Uncooked, or unimproved|Land with no building||
RAY|A beam of light|Sunbeam||
RED|A color|The ink you hope not to need||
RIB|A bone, or to tease|Tease||
RID|To free from|Clear away||
RIG|Equipment|Gear||
RIM|An edge|Lip||
RIP|To tear|A current||
ROB|To steal|Take wrongfully||
ROD|A survey measure of 16.5 feet|Perch||
ROE|Fish eggs|Deer partner in a phrase||
ROT|Decay|What a wet sill does||
ROW|A line|Of townships, or of seats||
RUB|To scrape|Friction||
RUG|A floor covering that is usually personal property|The textile that is not the floor||
RUM|A liquor|Odd||
RUN|To operate, or a survey course|Go||
RUT|A groove|Habit||
RYE|A grain|A bread, or a crop||
SAD|Unhappy|Down||
SAG|To droop|A roof problem||
SAP|Tree fluid|Energy||
SAT|Rested on a seat|Past tense of sit||
SAW|A cutting tool, or viewed|Past tense of see||
SAY|To speak|State||
SEA|A large body of water|Not usually riparian, which wants a current||
SET|A collection, or to place|Group||
SEW|To stitch|Join with thread||
SHE|That woman|Pronoun||
SHY|Bashful|Short, as a loan amount can be||
SIN|A wrong|Fault||
SIP|A small drink|Taste||
SIR|A polite title|Mister||
SIT|To be located|Where the house does||
SIX|The number before seven|Half a dozen||
SKI|To slide on snow|Winter sport||
SKY|The air above|Air rights' backdrop||
SLY|Cunning|Crafty||
SOB|To cry|Weep||
SOD|Turf|Grass with roots, which can be a crop or part of the land||
SON|A male child|Heir, sometimes||
SOP|A conciliatory gift|Bribe, which you still may not take||
SOT|A habitual drunkard|Toper||
SOW|To plant, or a female pig|Plant seed||
SOY|A bean|A crop||
SPA|A hot tub|Personal property until it is built in||
SPY|To watch secretly|Snoop||
STY|A pigpen|Mess||
SUE|To file a lawsuit|Take to court||
SUM|A total|The bottom of the closing statement||
SUN|The star, or a Sunday puzzle|Daylight||
TAB|A small bill, or a flap|Account||
TAD|A little bit|Bit||
TAG|A label|Price ___||
TAN|A brown color|Hide||
TAP|To draw liquid, or a light hit|Faucet||
TAR|A black road substance|Pitch||
TAT|To make lace|Tap's partner||
TAX|A levy|The town's bill||
TEA|A drink|Brew||
TEN|A number|Double five||
THE|The definite article|Grammar's most common word||
THY|Your, in old deed language|Archaic possessive||
TIC|A habit|Jerk||
TIE|An equal score, or a beam|Draw||
TIN|A metal|Roof material||
TIP|A helpful hint, not a kickback|Gratuity, which is not a referral fee||
TOE|A part of the foot|Digit||
TON|A heavy weight|A lot||
TOO|Also|Excessively||
TOP|The highest part|Summit||
TOW|To pull a vehicle|Drag||
TOY|A plaything|Chattel||
TUB|A bathtub, often a fixture|Bath||
TUG|To pull|Yank||
TWO|A pair|Number after one||
URN|A vase|Vessel||
USE|To employ|Zoning's favorite noun||
VAN|A vehicle|Mover's ___||
VAT|A large tub|Tank||
VET|To examine carefully|Check out, as a buyer should the title||
VEX|To annoy|Irk||
VIA|By way of|Through||
VIE|To compete|Contend, or "life" in pur autre vie||
VOW|A solemn promise|Oath||
WAD|A lump|Bundle of bills, which still is not an escrow account||
WAG|To swing|Shake||
WAR|A conflict|Fight||
WAS|Past tense of is|Used to be||
WAX|To grow, or a substance|Polish||
WAY|A path or method|Road, or manner||
WEB|A network, or a spider's work|Net||
WED|To marry|Join||
WEE|Very small|Tiny||
WET|Covered with water|The basement you disclose||
WHO|Which person|The agency question||
WHY|For what reason|The client's motive, which is confidential||
WIG|A hairpiece|Hair||
WIN|To succeed|Get the offer accepted||
WIT|Humor|Intelligence||
WOE|Sorrow|Trouble||
WOK|A cooking pan|Pan||
WON|Past tense of win|Did win||
WOO|To court|Seek||
WOW|Amazement|A strong offer||
YAK|A long-haired ox, or to chatter|Talk||
YAM|A sweet potato|A crop||
YAP|To bark|Chatter||
YAW|To swerve|Turn off course||
YEA|Yes, in a vote|Aye||
YES|Affirmative|The acceptance you want||
YET|Still|So far||
YEW|An evergreen tree|A possible monument||
YOU|The person addressed|Second person||
ZAP|To strike suddenly|Hit||
ZED|The letter Z, in some dialects|British Z||
ZEN|Calm focus|A good state for a closing||
ZIP|A postal code, briefly|Energy, or the code||
ZIT|A pimple|Blemish||
ZOO|A place with animals|Menagerie||
AREA|The size of a surface|Length times width||1
DEED|The instrument that passes title|The paper at the center of the recording||1
LIEN|A charge against property for a debt|The claim that follows the land||1
LOAN|Borrowed money|The reason for the note||1
NOTE|The promise to repay|IOU, formally||1
RATE|Interest as a percentage|The price of borrowing||1
RENT|Payment for possession|The lease's price||1
WILL|A testament|The document probate reads||1
HEIR|One who takes under intestacy law|Statute-picked successor||1
SITE|The land where a building sits|Location||1
PLOT|A lot, or to chart a course|Parcel||1
PLAT|A subdivision map|Recorded lots||1
ACRE|43,560 square feet|The classic land unit||1
FOOT|Twelve inches|The unit frontage is often measured in||1
YARD|Three feet, or the land around a house|A small distance, or a lawn||1
MILE|5,280 feet|Eight furlongs||1
RODS|Survey units of 16.5 feet|Old measuring sticks||1
LINK|7.92 inches in a survey chain|A small survey piece||1
EAST|A bearing|Toward sunrise||1
WEST|A bearing|Toward sunset||1
NORTH|A bearing|Up on most plats||1
SOUTH|A bearing|Down on most plats||1
DATE|When something happens|The closing ___||1
YEAR|Annual measure|365 days, usually||1
TERM|Duration|Of the loan or the listing||1
CAVE|A hollow, or the start of caveat|Warning's first half||1
EMIT|To give off|Radon can||1
ODOR|A smell that can be a material clue|What a careful buyer notices||1
MOLD|A fungus associated with moisture|The spot an inspector swabs||1
RUST|Oxidation|What a wet lintel does||1
LEAK|An escape of water|Roof trouble||1
CRACK|A split in a wall or foundation|Something the condition report asks about||1
BEAM|A structural support|What holds the floor up||1
STUD|A wall framing member|Vertical lumber||1
JOIST|A floor or ceiling beam|The parallel supports||1
RAFTER|A sloping roof beam|Roof framing||1
SOFFIT|The underside of an eave|The boxed-in overhang||1
FASCIA|The board along a roof edge|Where the gutter hangs||1
GUTTER|A channel for roof water|The trough||1
DRAIN|A way water leaves|Sump or sewer||1
SUMP|A pit for collecting water|Pump's home||1
PUMP|A machine that moves water|Well equipment||1
METER|A utility measuring device|What the reading comes from||1
PANEL|An electrical box|Breakers' home||1
WIRE|An electrical conductor|How power moves||1
PIPE|A tube for water or gas|Plumbing||1
VENT|An air opening|Plumbing or radon||1
FLUE|A chimney passage|Where smoke should go||1
HEARTH|A fireplace floor|Masonry||1
STAIR|A stepway|Egress, sometimes||1
PORCH|A covered entrance|Front sitting||1
PATIO|An outdoor paved area|The stone living room||1
FENCE|A barrier that can encroach|The neighbor dispute, in lumber||1
HEDGE|A living fence|Shrubs in a line||1
GRASS|A lawn|Not usually an emblement||1
TREE|A possible natural monument|The oak in the deed||1
STUMP|What is left after a tree is cut|A remnant||1
ROCK|Stone|A monument you can find||1
SOIL|Earth|What a perc test cares about||1
SAND|Fine mineral|Drainage material||1
CLAY|A soil that drains slowly|Heavy ground||1
LOAM|Rich soil|Good growing dirt||1
BOG|Wet ground|Marsh||1
POND|A small body of water|Still water||1
LAKE|A larger inland water|Littoral, maybe||1
BROOK|A small stream|Riparian neighbor||1
CREEK|A stream|Water with a current||1
RIVER|Flowing water that can create riparian rights|The classic riparian setting||1
SHORE|The land along water|Where littoral rights start||1
TIDAL|Affected by tides|Often littoral rather than riparian||1
DOCK|A structure for boats|Pier||1
PIER|A platform over water|Dock||1
SLIP|A boat's parking spot|Marina space||1
VIEW|A scene, which is not itself a property right unless granted|What the listing photo sells||1
LIGHT|Illumination, or an old easement of light|Windows||1
NOISE|Sound|A stigma or a nuisance, depending||1
SMELL|Odor|A fact a buyer can notice||1
TRAFFIC|Cars, which can affect value|The road's busy-ness||1
SCHOOL|A district buyers ask about|Education, as a location factor||1
STORE|A shop|Commercial use||1
SHOP|A store|Retail||1
MALL|A shopping center|Commercial property||1
CAFE|A small restaurant|Business use||1
BARN|A farm building|Agricultural improvement||1
SILO|A farm storage tower|Grain's tower||1
CROP|A planting that may be an emblement|This year's harvest||1
CORN|A crop|An emblement candidate||1
HAYBALE|A tied bundle of hay|Stored crop||1
WHEAT|A grain crop|Emblement material||1
FARM|Agricultural land|Where emblements and fences meet||1
RANCH|A livestock property, or a house style|One-story house, or acreage||1
CABIN|A small dwelling|Cottage||1
VILLA|A house style|Larger home||1
MANOR|A large house|Estate house||1
TOWER|A tall structure|High-rise piece||1
LOBBY|A building entrance hall|Where the condo directory is||1
ATTIC|The space under the roof|Storage, and insulation questions||1
CELLAR|A basement|Below grade||1
BASEMENT|The level below the first floor|Where water and radon get discussed||1
GARAGE|A car shelter|Attached or not, and maybe a fixture issue||1
CARPORT|A roofed parking space without full walls|The open garage||1
DRIVE|A private roadway on a lot|Where the easement often is||1
APRON|The paved approach to a garage or street|Concrete pad||1
CURB|The edge of the pavement|Street boundary clue||1
SEWER|Municipal wastewater|Pipes, not a septic tank||1
SEPTIC|An on-site waste system|Tank and field||1
LEACH|What a septic field does with water|Filter into the soil||1
PERC|A soil test for septic suitability|The hole that tells you if the lot can drain||1
GRADE|The slope of land|How the water runs||1
SLOPE|Incline|Grade||1
LEVEL|Flat|Even grade||1
FILL|Soil added to a site|Dirt brought in||1
CUT|Soil removed from a site|Excavation||1
BERM|A raised bank of earth|A landscaped mound||1
SWALE|A shallow drainage channel|Where stormwater is sent||1
EASE|Comfort, or the start of a right-of-way word|Relief||
MENT|A suffix you do not enter alone|
AGENT|One who represents a principal|The fiduciary||1
BUYER|The purchaser|Offeree, often||1
OWNER|Holder of title|The name before "of record"||1
PRICE|The amount asked or paid|Consideration's number||1
VALUE|Worth|What appraisal estimates||1
COST|Expenditure|Replacement's input||1
LOAN|Debt principal advanced|Mortgage's partner||1
LIEN|Security interest in title|Attachment to the land||1
DEED|Title-transfer document|Record this||1
WILL|Testament|Probate's script||1
HEIR|Intestate successor|The statute's chosen relative||1
SITE|Parcel location|Situs, plainly||1
LAND|Real property's foundation|The dirt||1
SOIL|Ground|Earth||1
HOME|A dwelling|The emotional word for a house||1
ROOM|An interior space|Bedroom, on the listing||1
BATH|A bathroom, in listing shorthand|Where the plumbing fixture cluster is||1
HALF|A partial bath, often|Two fixtures, not three||1
FULL|Complete|A bath with the usual three fixtures||1
DOOR|An entry|Egress||1
LOCK|A security device|Keyhole's partner||1
KEY|Opens a lock|Showing tool||1
SIGN|Advertising on the lawn|Listing's roadside announcement||1
AD|A short advertisement|A tiny promotion||
MLS|Multiple listing service|Shared inventory||1
CMA|Comparative market analysis|Broker price opinion's cousin, not an appraisal||1
APR|Annual percentage rate|The loan's big-picture cost||1
ARM|Adjustable rate mortgage|Variable loan||1
FHA|Federal Housing Administration|Insured loans||1
LTV|Loan to value|Debt divided by worth||1
DTI|Debt to income|Carry capacity||1
PITI|The four-part monthly house payment|Principal, interest, taxes, insurance||1
NOI|Net operating income|Cap rate's numerator||1
GRM|Gross rent multiplier|A fast rental rule of thumb||1
PMI|Private mortgage insurance|High-LTV protection for the lender||1
HUD|Housing and Urban Development|Federal housing department||1
ADA|Americans with Disabilities Act|Access law||1
ECOA|Equal Credit Opportunity Act|Fair lending initials||1
RESPA|Real Estate Settlement Procedures Act|Anti-kickback statute||1
TILA|Truth in Lending Act|Loan-cost disclosure law||1
TRID|TILA-RESPA integrated disclosures|The LE and CD rule||1
HMDA|Home Mortgage Disclosure Act|Loan-data statute||1
USPAP|Uniform Standards of Professional Appraisal Practice|Appraiser standards||1
LEAD|Paint that triggers a federal disclosure in older housing|Pre-1978 concern||1
ASIS|Sold without promises of repair, in four characters|The clause that is not a cloak for fraud||1
DUAL|Acting for both parties|Two masters||1
NET|A lease or a forbidden listing style|After expenses||1
FEE|Compensation or an estate|Simple's partner||1
TAX|Ad valorem charge|Town revenue from land||1
MAP|Plat|Drawing of lots||1
PIN|Parcel identifier|Tax map number||1
ROW|A line, or right of way briefly|Easement corridor, informally||1
DOT|A point|On the plan||1
COD|Cash on delivery|Pay at the door||1
ETA|Estimated time of arrival|When the closer thinks you will be there||1
FAQ|Frequently asked questions|Common answers||1
PDF|A file format|How the contract travels||1
"""

# Fix: I accidentally included some junk entries. Filter them in load().

JUNK = {"LISTOR", "SQL", "MENT", "BLOCKBUST", "HAYBALE"}

# 20-328-6a and 47a-21 were referenced; add if used.
SOURCES["20-328-6a"] = {
    "label": "Regs. Conn. State Agencies § 20-328-6a",
    "url": "https://eregulations.ct.gov/eRegsPortal/Browse/getDocument?guid={600C4895-0000-C737-BB27-7C13924592E0}",
}
SOURCES["47a-21"] = {
    "label": "Conn. Gen. Stat. § 47a-21",
    "url": "https://www.cga.ct.gov/current/pub/chap_831.htm#sec_47a-21",
}


def load_words():
    words = {}
    for line in RAW.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("|")
        if len(parts) < 2:
            continue
        while len(parts) < 5:
            parts.append("")
        word, straight, wordplay, source, exam = parts[:5]
        word = word.strip().upper()
        if not word.isalpha() or len(word) < 3 or word in JUNK:
            continue
        if word in words:
            continue
        straight = " ".join(straight.split())
        wordplay = " ".join(wordplay.split()) or None
        source = source.strip() or None
        if source and source not in SOURCES:
            raise SystemExit(f"Unknown source {source} for {word}")
        if not straight:
            continue
        words[word] = {
            "word": word,
            "straight": straight,
            "wordplay": wordplay,
            "source": SOURCES[source] if source else None,
            "exam": exam.strip() == "1" or bool(source),
        }
    return words


THEMES = [
    {
        "id": "paths",
        "title": "Paths to title",
        "blurb": "Three ways an interest in land shows up in the records.",
        "words": ["TESTAMENT", "INTESTATE", "ESCHEATED"],
    },
    {
        "id": "crowded",
        "title": "Crowded table",
        "blurb": "When more than one duty is in the room.",
        "words": ["FIDUCIARY", "DUALAGENT", "SUBAGENCY"],
    },
    {
        "id": "numbers",
        "title": "Putting a number on it",
        "blurb": "Three words for deciding what property is worth.",
        "words": ["APPRAISAL", "ASSESSING", "ESTIMATED"],
    },
    {
        "id": "note",
        "title": "Names on the note",
        "blurb": "The people around a mortgage debt.",
        "words": ["MORTGAGEE", "MORTGAGOR", "GUARANTOR"],
    },
    {
        "id": "estates",
        "title": "Estates that follow",
        "blurb": "Who holds the land, now or later.",
        "words": ["SEVERALTY", "REMAINDER", "FREEHOLDS"],
    },
    {
        "id": "table",
        "title": "Numbers at the table",
        "blurb": "Math that shows up when the file reaches closing.",
        "words": ["PRORATION", "REPAYMENT", "PRINCIPAL"],
    },
    {
        "id": "trust",
        "title": "Trust-account trouble",
        "blurb": "Three words you do not want near client money.",
        "words": ["COMMINGLE", "DIVERSION", "DEFALCATE"],
    },
    {
        "id": "survey",
        "title": "On the survey",
        "blurb": "How the land gets measured and marked.",
        "words": ["MONUMENTS", "SURVEYING", "FRONTFOOT"],
    },
]
