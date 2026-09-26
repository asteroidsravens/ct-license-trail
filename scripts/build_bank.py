#!/usr/bin/env python3
"""Build data/questions.json for CT License Trail.

Run from the repo root: python3 scripts/build_bank.py
"""

import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qutil import item, src, cgs, CH223
from course_units import classify_question
from bank_ct import ct_questions
from bank_national import national_questions
from bank_national_b import more_national

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "questions.json"

CONV = src("Conn. Gen. Stat. § 12-494", f"{CH223}#sec_12-494")
CONV_PAY = src("Conn. Gen. Stat. §§ 12-494 and 12-495", f"{CH223}#sec_12-494")


def money(n):
    n = round(float(n) + 1e-9, 2)
    if abs(n - round(n)) < 0.001:
        return f"${n:,.0f}"
    return f"${n:,.2f}"


def pct(n):
    n = round(float(n) + 1e-9, 4)
    text = f"{n:.2f}".rstrip("0").rstrip(".")
    return text + "%"


def math_item(stem, correct, wrongs, explanation, steps, pools, event=False):
    return item(
        "math",
        stem,
        correct,
        wrongs,
        explanation,
        source=CONV_PAY if "conveyance" in stem.lower() or "12-494" in explanation else None,
        math=True,
        steps=steps,
        event=event,
        pools=pools,
    )


def ct_state_tax(price):
    """State conveyance tax on a residential dwelling. Municipal tax is separate."""
    if price < 2000:
        return 0.0
    if price <= 800000:
        return price * 0.0075
    tax = 800000 * 0.0075
    mid = min(price, 2500000) - 800000
    tax += mid * 0.0125
    if price > 2500000:
        tax += (price - 2500000) * 0.0225
    return tax


def muni_tax(price, extra=0.0):
    if price < 2000:
        return 0.0
    return price * (0.0025 + extra)


def unique_wrongs(correct, candidates):
    wrongs = []
    for value in candidates:
        if value != correct and value not in wrongs:
            wrongs.append(value)
        if len(wrongs) == 3:
            return wrongs
    number = None
    if isinstance(correct, str) and correct.startswith("$"):
        number = float(correct.replace("$", "").replace(",", ""))
    bump = 1
    while len(wrongs) < 3:
        if number is not None:
            extra = money(number + (250 * bump))
        elif isinstance(correct, str) and correct.endswith("%"):
            extra = pct(float(correct[:-1]) + bump)
        else:
            extra = f"{correct} (check {bump})"
        if extra != correct and extra not in wrongs:
            wrongs.append(extra)
        bump += 1
        if bump > 12:
            raise RuntimeError(f"Could not build distractors for {correct}")
    return wrongs


def math_questions():
    q = []

    # Straight commission
    deals = [
        (325000, 0.05),
        (410000, 0.06),
        (275000, 0.055),
        (640000, 0.05),
        (189500, 0.06),
        (520000, 0.045),
        (307000, 0.07),
        (450000, 0.03),
    ]
    for price, rate in deals:
        commission = price * rate
        wrongs = unique_wrongs(money(commission), [
            money(price * (rate / 10)),
            money(price * rate + 1000),
            money(price * (rate + 0.01)),
            money(commission / 2),
            money(price * rate * 2),
        ])
        q.append(math_item(
            f"A house sells for {money(price)}. The listing agreement sets the brokerage fee at {pct(rate * 100)}. What is the total commission?",
            money(commission),
            wrongs,
            f"Multiply the sale price by the commission rate. {money(price)} × {rate} = {money(commission)}.",
            [
                f"Write the rate as a decimal: {pct(rate * 100)} = {rate}.",
                f"Multiply: {money(price)} × {rate} = {money(commission)}.",
                "The rate applies to the sale price, not to the loan amount, unless the problem says otherwise.",
            ],
            ["math"],
        ))

    # Splits
    splits = [
        (400000, 0.06, 0.50, 0.60, "listing", "selling"),
        (360000, 0.05, 0.50, 0.70, "selling", "listing"),
        (250000, 0.06, 0.60, 0.50, "listing", "selling"),
        (510000, 0.05, 0.50, 0.55, "selling", "listing"),
        (287000, 0.06, 0.50, 0.65, "selling", "listing"),
        (445000, 0.055, 0.40, 0.60, "listing", "selling"),
    ]
    for price, rate, side_share, agent_share, side, other in splits:
        total = price * rate
        side_amt = total * side_share
        agent = side_amt * agent_share
        q.append(math_item(
            f"A sale closes at {money(price)} with a {pct(rate * 100)} commission. The {side} brokerage keeps {pct(side_share * 100)} of the total commission, and the salesperson on that side keeps {pct(agent_share * 100)} of the brokerage's share. How much does that salesperson earn?",
            money(agent),
            unique_wrongs(money(agent), [
                money(total),
                money(side_amt),
                money(total * agent_share),
                money(price * agent_share),
                money(agent / 2),
            ]),
            f"Total commission is {money(total)}. The {side} side's share is {money(side_amt)}. The salesperson's {pct(agent_share * 100)} of that share is {money(agent)}.",
            [
                f"Total commission: {money(price)} × {rate} = {money(total)}.",
                f"{side.capitalize()} brokerage share: {money(total)} × {side_share} = {money(side_amt)}.",
                f"Salesperson share: {money(side_amt)} × {agent_share} = {money(agent)}.",
            ],
            ["math"],
            event=True,
        ))

    # Seller net: price = (net + costs) / (1 - rate)
    nets = [
        (190000, 0, 0.05),
        (188000, 0, 0.06),
        (185000, 5000, 0.05),
        (176000, 12000, 0.06),
        (223000, 5000, 0.05),
    ]
    for net, costs, rate in nets:
        price = (net + costs) / (1 - rate)
        if abs(price - round(price)) > 0.02:
            raise RuntimeError(f"Seller-net price not whole: {net} {costs} {rate} -> {price}")
        price = round(price)
        check = price - price * rate - costs
        q.append(math_item(
            f"A seller wants {money(net)} after a {pct(rate * 100)} commission and {money(costs)} of other selling costs. What sale price is required? Round to the nearest dollar if needed.",
            money(round(price)),
            unique_wrongs(money(round(price)), [
                money(round(net + costs)),
                money(round((net + costs) * (1 + rate))),
                money(round(net / (1 - rate))),
                money(round((net + costs) / (1 + rate))),
            ]),
            f"The seller keeps 100% minus the commission. Add the costs to the desired net, then divide by {1 - rate:.2f}. The price is {money(round(price))}.",
            [
                f"Dollars that must come out of the price before commission: {money(net)} + {money(costs)} = {money(net + costs)}.",
                f"The seller receives {pct((1 - rate) * 100)} of the price after commission, so divide by {1 - rate}.",
                f"Sale price: {money(net + costs)} ÷ {1 - rate} = {money(round(price))}.",
                f"Check: commission {money(round(price) * rate)} plus costs {money(costs)} leaves about {money(check)}.",
            ],
            ["math"],
        ))

    # Seller proceeds given a price
    proceeds = [
        (375000, 0.05, 210000, 4800),
        (290000, 0.06, 140000, 3200),
        (610000, 0.05, 255000, 9000),
        (228000, 0.06, 0, 1500),
    ]
    for price, rate, mortgage, costs in proceeds:
        commission = price * rate
        net = price - commission - mortgage - costs
        q.append(math_item(
            f"A sale price is {money(price)}. Commission is {pct(rate * 100)}. The seller's mortgage payoff is {money(mortgage)} and other seller costs are {money(costs)}. What are the seller's proceeds?",
            money(net),
            unique_wrongs(money(net), [
                money(price - commission),
                money(price - mortgage),
                money(price - commission - mortgage),
                money(net + costs),
            ]),
            f"Subtract commission, the mortgage payoff, and other costs from the price. Proceeds are {money(net)}.",
            [
                f"Commission: {money(price)} × {rate} = {money(commission)}.",
                f"Subtract commission: {money(price)} − {money(commission)} = {money(price - commission)}.",
                f"Subtract payoff and costs: {money(price - commission)} − {money(mortgage)} − {money(costs)} = {money(net)}.",
            ],
            ["math"],
        ))

    # Prorations, 360-day, seller owns closing day, taxes prepaid
    prorations = [
        (3600, "July 1", "June 30", "September 15", 75),
        (7200, "July 1", "June 30", "October 10", 100),
        (2400, "January 1", "December 31", "April 20", 110),
        (5400, "July 1", "June 30", "August 1", 31),
    ]
    for annual, start, end, close, seller_days in prorations:
        daily = annual / 360
        seller_share = daily * seller_days
        buyer_days = 360 - seller_days
        credit = daily * buyer_days
        q.append(math_item(
            f"Annual taxes of {money(annual)} are paid in full for a tax year running {start} through {end}. Closing is {close}. Use a 360-day year and 30-day months, and the seller owns the day of closing. The seller has owned {seller_days} days of the tax year. How much does the buyer reimburse the seller for the buyer's share of the prepaid taxes?",
            money(credit),
            unique_wrongs(money(credit), [
                money(seller_share),
                money(annual),
                money(daily * seller_days / 2) if seller_share / 2 != credit else money(daily * 30),
                money(credit + daily),
            ]),
            f"Daily tax is {money(annual)} ÷ 360 = {money(daily)}. The buyer owns {buyer_days} days, so the credit to the seller is {money(credit)}.",
            [
                f"Daily tax: {money(annual)} ÷ 360 = {money(daily)}.",
                f"Seller's days, including the closing day: {seller_days}.",
                f"Buyer's days: 360 − {seller_days} = {buyer_days}.",
                f"Buyer reimburses the seller: {buyer_days} × {money(daily)} = {money(credit)}.",
            ],
            ["math"],
        ))

    # Rent proration: rent paid in advance for the month, buyer owns closing day
    rents = [
        (1800, 30, 10),
        (2400, 30, 16),
        (1500, 30, 1),
        (2100, 30, 21),
    ]
    for rent, month_days, close_day in rents:
        # seller owns days 1 through close_day-1 if buyer owns closing day
        seller_days = close_day - 1
        buyer_days = month_days - seller_days
        daily = rent / month_days
        credit_buyer = daily * buyer_days
        q.append(math_item(
            f"A tenant paid {money(rent)} rent for a 30-day month. Closing is on day {close_day}, and the buyer owns the day of closing. How much of this prepaid rent is credited to the buyer?",
            money(credit_buyer),
            unique_wrongs(money(credit_buyer), [
                money(daily * seller_days),
                money(rent),
                money(daily * close_day),
                money(credit_buyer / 2 if credit_buyer / 2 != daily * seller_days else rent / 3),
            ]),
            f"The buyer is credited for each day of the month from closing forward. That credit is {money(credit_buyer)}.",
            [
                f"Daily rent: {money(rent)} ÷ 30 = {money(daily)}.",
                f"Buyer owns the closing day, so the seller's days are day 1 through day {seller_days} ({seller_days} days).",
                f"Buyer's days: 30 − {seller_days} = {buyer_days}.",
                f"Credit to the buyer: {buyer_days} × {money(daily)} = {money(credit_buyer)}.",
            ],
            ["math"],
        ))

    # CT conveyance
    conv_prices = [250000, 400000, 560000, 800000, 900000, 1200000, 2500000, 2600000, 150000]
    for price in conv_prices:
        state = ct_state_tax(price)
        muni = muni_tax(price)
        total = state + muni
        q.append(math_item(
            f"A Connecticut residential dwelling sells for {money(price)}. The town charges only the base municipal conveyance tax and has not adopted an extra local tax. Using Conn. Gen. Stat. § 12-494, what is the total state plus municipal conveyance tax?",
            money(total),
            unique_wrongs(money(total), [
                money(state),
                money(muni),
                money(price * 0.01),
                money(price * 0.0125),
                money(total * 2),
            ]),
            f"State tax is {money(state)} and base municipal tax is {money(muni)}. Together they are {money(total)}. The seller pays this to the town clerk. Consideration of at least $2,000 is the threshold for the tax to apply.",
            _conv_steps(price, state, muni, total),
            ["math", "ct-laws"],
            event=True,
        ))

    # Nonresidential
    for price in (300000, 750000):
        state = price * 0.0125
        muni = price * 0.0025
        total = state + muni
        q.append(math_item(
            f"A Connecticut property used for a nonresidential purpose, and not unimproved land, sells for {money(price)}. The town charges only the base municipal rate. What is the total conveyance tax?",
            money(total),
            unique_wrongs(money(total), [
                money(price * 0.0075 + muni),
                money(state),
                money(price * 0.01),
                money(muni),
            ]),
            f"Section 12-494(b)(1) sets the state rate at 1.25% for property used for a nonresidential purpose, except unimproved land. Municipal tax at 0.25% is {money(muni)}. Total: {money(total)}.",
            [
                f"State tax: {money(price)} × 0.0125 = {money(state)}.",
                f"Municipal tax: {money(price)} × 0.0025 = {money(muni)}.",
                f"Total: {money(state)} + {money(muni)} = {money(total)}.",
            ],
            ["math", "ct-laws"],
        ))

    # Under 2000 exempt
    q.append(math_item(
        "A Connecticut deed shows consideration of $1,500. How much state and municipal conveyance tax does § 12-494 impose?",
        "$0",
        ["$15", "$30", "$11.25"],
        "The tax applies when consideration equals or exceeds $2,000. At $1,500, no conveyance tax is imposed. Section 12-498 also exempts deeds under $2,000.",
        [
            "Compare the consideration with the $2,000 threshold in § 12-494.",
            "$1,500 is below $2,000, so the tax is not imposed.",
            "Do not multiply a below-threshold price by 0.75% or 0.25%.",
        ],
        ["math", "ct-laws"],
    ))

    # LTV
    ltvs = [
        (240000, 300000),
        (180000, 200000),
        (356000, 445000),
        (150000, 250000),
        (276000, 345000),
        (412000, 515000),
    ]
    for loan, value in ltvs:
        ratio = loan / value * 100
        q.append(math_item(
            f"A lender will loan {money(loan)} on a property valued at {money(value)}. What is the loan-to-value ratio?",
            pct(ratio),
            unique_wrongs(pct(ratio), [
                pct(value / loan * 100 if loan else 0),
                pct(ratio / 10),
                pct(100 - ratio),
                pct(ratio + 10),
            ]),
            f"LTV = loan ÷ value. {money(loan)} ÷ {money(value)} = {pct(ratio)}.",
            [
                f"Divide the loan by the value: {money(loan)} ÷ {money(value)} = {loan / value:.4f}.",
                f"Convert to a percent: {pct(ratio)}.",
            ],
            ["math"],
        ))

    # Down payment from LTV
    for price, ltv in ((320000, 0.80), (275000, 0.90), (410000, 0.95), (198000, 0.75)):
        loan = price * ltv
        down = price - loan
        q.append(math_item(
            f"The price is {money(price)} and the lender's maximum LTV is {pct(ltv * 100)}. Assuming the price is the value used, what down payment does the borrower need?",
            money(down),
            unique_wrongs(money(down), [
                money(loan),
                money(price * (1 - ltv) / 2),
                money(price * ltv * 0.2),
                money(down + 1000),
            ]),
            f"The loan is {pct(ltv * 100)} of price, so the down payment is the rest: {money(down)}.",
            [
                f"Maximum loan: {money(price)} × {ltv} = {money(loan)}.",
                f"Down payment: {money(price)} − {money(loan)} = {money(down)}.",
            ],
            ["math"],
        ))

    # Points
    for loan, points in ((250000, 2), (180000, 1), (420000, 1.5), (315000, 3), (200000, 2.5), (275500, 1)):
        cost = loan * points / 100
        q.append(math_item(
            f"A borrower pays {points:g} discount point(s) on a {money(loan)} loan. What do the points cost?",
            money(cost),
            unique_wrongs(money(cost), [
                money(points * 100),
                money(loan * points / 1000),
                money(cost * 2),
                money(loan * (points / 100) * 0.1) if cost * 0.1 != points * 100 else money(cost + 250),
            ]),
            f"One point is 1% of the loan. {points:g} point(s) cost {money(cost)}.",
            [
                "One discount point = 1% of the loan amount, not 1% of the price.",
                f"Cost: {money(loan)} × {points / 100} = {money(cost)}.",
            ],
            ["math"],
        ))

    # Equity
    for value, debt in ((340000, 210000), (500000, 500000), (275000, 190000), (630000, 250000), (415000, 300000), (260000, 80000)):
        equity = value - debt
        q.append(math_item(
            f"A home is worth {money(value)} and the only lien is a mortgage with a balance of {money(debt)}. What is the owner's equity?",
            money(equity),
            unique_wrongs(money(equity), [
                money(value),
                money(debt),
                money(value + debt),
                money(abs(equity - 10000)),
            ]),
            f"Equity is value minus liens. {money(value)} − {money(debt)} = {money(equity)}.",
            [
                "Equity = market value − outstanding liens.",
                f"{money(value)} − {money(debt)} = {money(equity)}.",
            ],
            ["math"],
        ))

    # PITI
    pitis = [
        (1420, 4800, 1200),
        (980, 3600, 840),
        (2100, 7200, 1800),
        (1650, 5400, 960),
        (1100, 2400, 600),
        (1875, 6000, 1440),
    ]
    for pi, taxes, ins in pitis:
        monthly = pi + taxes / 12 + ins / 12
        q.append(math_item(
            f"Monthly principal and interest are {money(pi)}. Annual property taxes are {money(taxes)} and annual homeowners insurance is {money(ins)}. What is the monthly PITI payment?",
            money(monthly),
            unique_wrongs(money(monthly), [
                money(pi),
                money(pi + taxes + ins),
                money(pi + taxes / 12),
                money(pi + ins / 12),
            ]),
            f"Convert taxes and insurance to monthly amounts and add them to principal and interest. PITI is {money(monthly)}.",
            [
                f"Monthly taxes: {money(taxes)} ÷ 12 = {money(taxes / 12)}.",
                f"Monthly insurance: {money(ins)} ÷ 12 = {money(ins / 12)}.",
                f"PITI: {money(pi)} + {money(taxes / 12)} + {money(ins / 12)} = {money(monthly)}.",
            ],
            ["math"],
        ))

    # Interest-only monthly
    for loan, rate in ((200000, 0.06), (150000, 0.07), (360000, 0.05), (240000, 0.045), (100000, 0.08)):
        annual = loan * rate
        monthly = annual / 12
        q.append(math_item(
            f"An interest-only loan of {money(loan)} has a {pct(rate * 100)} annual rate. What is the interest due for one month?",
            money(monthly),
            unique_wrongs(money(monthly), [
                money(annual),
                money(monthly * 12),
                money(loan * rate / 365 * 30),
                money(monthly / 2),
            ]),
            f"Annual interest is {money(annual)}. One month is one-twelfth: {money(monthly)}. An interest-only payment does not reduce principal.",
            [
                f"Annual interest: {money(loan)} × {rate} = {money(annual)}.",
                f"Monthly interest: {money(annual)} ÷ 12 = {money(monthly)}.",
            ],
            ["math"],
        ))

    # Area
    areas = [
        (40, 100, "rectangular lot"),
        (50, 120, "rectangular lot"),
        (30, 80, "rectangular room, in feet"),
        (25, 40, "rectangular living room, in feet"),
        (60, 110, "rectangular parcel, in feet"),
    ]
    for length, width, label in areas:
        sq = length * width
        q.append(math_item(
            f"A {label} measures {length} feet by {width} feet. What is its area?",
            f"{sq:,} square feet",
            unique_wrongs(f"{sq:,} square feet", [
                f"{length + width:,} square feet",
                f"{sq * 2:,} square feet",
                f"{int(sq / 2):,} square feet",
                f"{(length + width) * 2:,} square feet",
            ]),
            f"Area of a rectangle is length × width. {length} × {width} = {sq:,} square feet.",
            [
                "Use area = length × width.",
                f"{length} × {width} = {sq:,} square feet.",
                "Perimeter would add the sides. This question asks for area.",
            ],
            ["math"],
        ))

    # Acres
    for sqft in (87120, 43560, 21780, 130680, 65340):
        acres = sqft / 43560
        q.append(math_item(
            f"A parcel contains {sqft:,} square feet. How many acres is that? One acre is 43,560 square feet.",
            f"{acres:g} acre" if acres == 1 else f"{acres:g} acres",
            unique_wrongs(
                f"{acres:g} acre" if acres == 1 else f"{acres:g} acres",
                [
                    f"{acres * 2:g} acres",
                    f"{sqft / 4356:g} acres",
                    "1 acre" if acres != 1 else "2 acres",
                    f"{acres / 2:g} acres",
                ],
            ),
            f"Divide square feet by 43,560. {sqft:,} ÷ 43,560 = {acres:g} acres.",
            [
                "Acres = square feet ÷ 43,560.",
                f"{sqft:,} ÷ 43,560 = {acres:g}.",
            ],
            ["math"],
        ))

    # Triangle
    q.append(math_item(
        "A triangular lot has a base of 100 feet and a height of 80 feet. What is its area?",
        "4,000 square feet",
        ["8,000 square feet", "180 square feet", "2,000 square feet"],
        "Triangle area is one-half × base × height. Half of 8,000 is 4,000 square feet.",
        [
            "Area = ½ × base × height.",
            "½ × 100 × 80 = 4,000 square feet.",
        ],
        ["math"],
    ))

    # Cap rate
    caps = [
        (24000, 0.08),
        (36000, 0.09),
        (45000, 0.06),
        (30000, 0.10),
        (18000, 0.06),
        (50000, 0.08),
    ]
    for noi, cap in caps:
        value = noi / cap
        q.append(math_item(
            f"A small income property has net operating income of {money(noi)}. The market capitalization rate is {pct(cap * 100)}. What value does the income approach indicate?",
            money(value),
            unique_wrongs(money(value), [
                money(noi * cap),
                money(noi),
                money(value / 2),
                money(noi / (cap + 0.02)),
            ]),
            f"Value = NOI ÷ cap rate. {money(noi)} ÷ {cap} = {money(value)}. Mortgage payments are not deducted in NOI.",
            [
                f"Value = net operating income ÷ capitalization rate.",
                f"{money(noi)} ÷ {cap} = {money(value)}.",
            ],
            ["math"],
        ))

    for value, noi in ((400000, 32000), (250000, 20000), (600000, 42000)):
        cap = noi / value * 100
        q.append(math_item(
            f"A property worth {money(value)} produces net operating income of {money(noi)}. What is the capitalization rate?",
            pct(cap),
            unique_wrongs(pct(cap), [
                pct(value / noi),
                pct(cap * 10),
                pct(cap / 2),
                pct(noi / 1000),
            ]),
            f"Cap rate = NOI ÷ value. {money(noi)} ÷ {money(value)} = {pct(cap)}.",
            [
                "Cap rate = NOI ÷ value.",
                f"{money(noi)} ÷ {money(value)} = {noi / value:.4f} = {pct(cap)}.",
            ],
            ["math"],
        ))

    # Buyer funds
    buyers = [
        (300000, 0.90, 6000, 5000),
        (240000, 0.80, 4500, 4000),
        (450000, 0.95, 8000, 10000),
        (180000, 0.90, 3000, 2000),
        (520000, 0.80, 9000, 15000),
    ]
    for price, ltv, closing_costs, deposit in buyers:
        loan = price * ltv
        down = price - loan
        cash = down + closing_costs - deposit
        q.append(math_item(
            f"The price is {money(price)}. The loan is {pct(ltv * 100)} of the price. Buyer closing costs are {money(closing_costs)}, and the buyer has already paid a {money(deposit)} deposit. How much additional cash must the buyer bring to closing?",
            money(cash),
            unique_wrongs(money(cash), [
                money(down),
                money(down + closing_costs),
                money(down + closing_costs + deposit),
                money(cash + deposit),
            ]),
            f"The buyer needs the down payment plus closing costs, minus the deposit already paid: {money(cash)}.",
            [
                f"Loan: {money(price)} × {ltv} = {money(loan)}.",
                f"Down payment: {money(price)} − {money(loan)} = {money(down)}.",
                f"Add closing costs and subtract the deposit already paid: {money(down)} + {money(closing_costs)} − {money(deposit)} = {money(cash)}.",
            ],
            ["math"],
            event=True,
        ))

    # Commission from a known net, simple
    q.append(math_item(
        "A brokerage earns a 6% commission and the total commission check is $18,000. What was the sale price?",
        "$300,000",
        ["$180,000", "$108,000", "$318,000"],
        "Sale price = commission ÷ rate. $18,000 ÷ 0.06 = $300,000.",
        [
            "Price = commission ÷ commission rate.",
            "$18,000 ÷ 0.06 = $300,000.",
        ],
        ["math"],
    ))

    # Square footage of a house from price per foot
    q.append(math_item(
        "A house sold for $420,000, which the parties treat as $210 per square foot. How many square feet is the house?",
        "2,000",
        ["1,000", "4,200", "210"],
        "Square feet = price ÷ price per square foot. $420,000 ÷ $210 = 2,000.",
        [
            "Divide the price by the price per square foot.",
            "420,000 ÷ 210 = 2,000 square feet.",
        ],
        ["math"],
    ))

    # Assessment and tax
    q.append(math_item(
        "A town assesses property at 70% of market value. The market value is $200,000 and the tax rate is 20 mills. What is the annual tax? A mill is $1 of tax per $1,000 of assessed value.",
        "$2,800",
        ["$4,000", "$2,000", "$1,400"],
        "Assessed value is $140,000. Twenty mills is $20 per $1,000, so the tax is 140 × $20 = $2,800.",
        [
            "Assessed value: $200,000 × 0.70 = $140,000.",
            "Number of thousands: 140,000 ÷ 1,000 = 140.",
            "Tax: 140 × $20 = $2,800.",
        ],
        ["math"],
    ))

    q.append(math_item(
        "The same mill calculation another way: assessed value is $150,000 and the rate is 25 mills. What is the annual property tax?",
        "$3,750",
        ["$1,500", "$3,075", "$6,000"],
        "Twenty-five mills means $25 per $1,000 of assessed value. $150,000 ÷ $1,000 = 150, and 150 × $25 = $3,750.",
        [
            "Mills: 25 mills = $25 of tax per $1,000 of assessed value.",
            "$150,000 ÷ $1,000 = 150.",
            "150 × $25 = $3,750.",
        ],
        ["math"],
    ))

    return q


def _conv_steps(price, state, muni, total):
    steps = [
        "Municipal base rate is 0.25% of the full consideration when the town has not adopted an extra local tax.",
        f"Municipal tax: {money(price)} × 0.0025 = {money(muni)}.",
    ]
    if price <= 800000:
        steps.append(f"State tax on a residential dwelling at or under $800,000 is 0.75%: {money(price)} × 0.0075 = {money(state)}.")
    else:
        first = 800000 * 0.0075
        steps.append(f"State tax on the first $800,000 is 0.75%: {money(first)}.")
        if price <= 2500000:
            mid = (price - 800000) * 0.0125
            steps.append(f"State tax on the portion above $800,000 is 1.25%: {money(price - 800000)} × 0.0125 = {money(mid)}.")
        else:
            mid = (2500000 - 800000) * 0.0125
            top = (price - 2500000) * 0.0225
            steps.append(f"State tax from $800,000 to $2,500,000 is 1.25%: {money(mid)}.")
            steps.append(f"State tax above $2,500,000 is 2.25%: {money(top)}.")
        steps.append(f"State tax total: {money(state)}.")
    steps.append(f"Add state and municipal tax: {money(state)} + {money(muni)} = {money(total)}.")
    steps.append("The person conveying the property pays the town clerk. This problem assumes no exemption.")
    return steps


TOPICS = [
    {
        "id": "ownership",
        "name": "Property Ownership",
        "town": "Milford",
        "blurb": "What is real, who owns it, and what sticks to the title.",
        "portion": "national",
        "weight": 8,
    },
    {
        "id": "landuse",
        "name": "Land Use Controls",
        "town": "Stratford",
        "blurb": "Zoning, taxes, takings, and private rules.",
        "portion": "national",
        "weight": 4,
    },
    {
        "id": "valuation",
        "name": "Valuation",
        "town": "Bridgeport",
        "blurb": "Appraisals, CMAs, and the three approaches to value.",
        "portion": "national",
        "weight": 6,
    },
    {
        "id": "financing",
        "name": "Financing",
        "town": "Fairfield",
        "blurb": "Loans, points, RESPA, and the closing disclosure clock.",
        "portion": "national",
        "weight": 8,
    },
    {
        "id": "contracts",
        "name": "Contracts",
        "town": "Trumbull",
        "blurb": "Offers, contingencies, and what makes a deal real.",
        "portion": "national",
        "weight": 15,
    },
    {
        "id": "agency",
        "name": "Agency",
        "town": "Monroe",
        "blurb": "Who you work for, and what you owe them.",
        "portion": "national",
        "weight": 10,
    },
    {
        "id": "disclosures",
        "name": "Property Disclosures",
        "town": "Shelton",
        "blurb": "Material facts, lead paint, and red flags.",
        "portion": "national",
        "weight": 6,
    },
    {
        "id": "management",
        "name": "Leasing and Property Management",
        "town": "Derby",
        "blurb": "Leases, landlords, and the owner's money.",
        "portion": "national",
        "weight": 2,
    },
    {
        "id": "title",
        "name": "Transfer of Title",
        "town": "New Haven",
        "blurb": "Deeds, title insurance, and the closing table.",
        "portion": "national",
        "weight": 5,
    },
    {
        "id": "practice",
        "name": "Practice of Real Estate",
        "town": "Hamden",
        "blurb": "Fair housing, antitrust, advertising, and trust money.",
        "portion": "national",
        "weight": 10,
    },
    {
        "id": "ct-license",
        "name": "Connecticut Licensing",
        "town": "Wallingford",
        "blurb": "The exam, the license, and the guaranty fund.",
        "portion": "state",
        "weight": 7,
    },
    {
        "id": "ct-conduct",
        "name": "Licensee Conduct",
        "town": "Meriden",
        "blurb": "Deposits, ads, compensation, and records.",
        "portion": "state",
        "weight": 11,
    },
    {
        "id": "ct-agency",
        "name": "Connecticut Agency",
        "town": "Middletown",
        "blurb": "First meetings, dual agency, and designated agents.",
        "portion": "state",
        "weight": 9,
    },
    {
        "id": "ct-laws",
        "name": "Connecticut Property Law",
        "town": "Hartford",
        "blurb": "Condition reports, fair housing, deposits, and conveyance tax.",
        "portion": "state",
        "weight": 8,
    },
    {
        "id": "math",
        "name": "Math Pass",
        "town": "Waterbury",
        "blurb": "Commission, proration, conveyance tax, and the rest of the calculator work.",
        "portion": "national",
        "weight": 6,
    },
]


def finalize(raw):
    questions = []
    stems = set()
    for index, raw_q in enumerate(raw, start=1):
        stem = raw_q["stem"]
        if stem in stems:
            raise SystemExit(f"Duplicate stem: {stem[:120]}")
        stems.add(stem)
        rng = random.Random(f"ctlt-{index}-{stem[:40]}")
        choices = [raw_q["correct"], *raw_q["wrongs"]]
        rng.shuffle(choices)
        answer = choices.index(raw_q["correct"])
        qid = f"{raw_q['topic']}-{index:04d}"
        questions.append({
            "id": qid,
            "topic": raw_q["topic"],
            "chapter": classify_question(raw_q["topic"], stem, raw_q["explanation"]),
            "pools": raw_q["pools"],
            "stem": stem,
            "choices": choices,
            "answer": answer,
            "explanation": raw_q["explanation"],
            "steps": raw_q["steps"],
            "math": raw_q["math"],
            "event": raw_q["event"],
            "source": raw_q["source"],
        })
    return questions


def main():
    raw = []
    raw.extend(national_questions())
    raw.extend(more_national())
    raw.extend(ct_questions())
    raw.extend(math_questions())
    questions = finalize(raw)

    state_topics = {"ct-license", "ct-conduct", "ct-agency", "ct-laws"}
    missing = []
    for q in questions:
        if q["topic"] in state_topics or "ct-laws" in q["pools"]:
            if not q["source"]:
                missing.append(q["id"] + " " + q["stem"][:80])
        if q["math"] and not q["steps"]:
            missing.append("steps " + q["id"])
        if len(q["choices"]) != 4:
            missing.append("choices " + q["id"])
    if missing:
        raise SystemExit("Validation failed:\n" + "\n".join(missing[:20]))

    counts = {}
    math_n = 0
    for q in questions:
        counts[q["topic"]] = counts.get(q["topic"], 0) + 1
        if q["math"]:
            math_n += 1

    payload = {
        "version": "2026.1",
        "title": "CT License Trail",
        "disclaimer": "Unofficial study aid. Not affiliated with PSI, the Connecticut Department of Consumer Protection, or the Connecticut Real Estate Commission.",
        "exam": {
            "nationalCount": 80,
            "nationalMinutes": 120,
            "stateCount": 35,
            "stateMinutes": 45,
            "bothMinutes": 165,
            "passingPercent": 70,
            "sourceLabel": "PSI Connecticut Real Estate Candidate Information Bulletin, updated November 13, 2025",
            "sourceUrl": "https://test-takers.psiexams.com/ctre",
        },
        "topics": TOPICS,
        "questions": questions,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(questions)} questions ({math_n} math) to {OUT}")
    for topic in TOPICS:
        print(f"  {topic['id']:12} {counts.get(topic['id'], 0):4}  weight {topic['weight']:2}  {topic['town']}")
    if len(questions) < 400 or math_n < 80:
        raise SystemExit(f"Bank too small: {len(questions)} questions, {math_n} math")


if __name__ == "__main__":
    main()
