# CT License Trail

An unofficial, mobile-first study game for the Connecticut real estate **salesperson** exam given by PSI. You drive a short road from Student to Licensed Agent, one Connecticut town at a time. Each town is an exam topic. Sessions are built for a few minutes between rides: three questions, one thumb, and the same question still waiting when you come back.

This is a study aid. It is not a PSI exam, not a Department of Consumer Protection product, and not a substitute for the statutes, the regulations, or the candidate bulletin.

## Play

Open the site, or run it locally (see below). Progress stays in this browser (`localStorage`). Nothing is sent to a server.

- **Road.** Three questions at the next town. A miss spends Coffee, Fuel, Calm, or Notes. Three correct answers in a row put a supply back. An empty supply is a pull-over refill, not a failed trip.
- **Towns.** Milford through Hartford, plus Waterbury for math. A town appears when it has questions in the chapters you've completed. The mastery meter is your score on items you have already answered.
- **Math Pass.** Commission, splits, seller proceeds, prorations, Connecticut conveyance tax, loan-to-value, PITI, area, cap rate, equity, points, and a few related drills. The steps appear after you answer.
- **Mock exam.** National portion: 80 questions, 120 minutes. Connecticut portion: 35 questions, 45 minutes. Both: 115 questions, 165 minutes, when every chapter is included. Each portion is scored on its own, and both have to reach 70 percent. The default sitting uses only chapters you've completed and says so; it can be shorter. The clock pauses if you leave the page. The real exam clock does not.
- **Chapter study.** Open Study a chapter. The loop is principles and practices, then that chapter's Connecticut law, then a short quiz.
- **Progress.** The trailhead home screen is the hub: town trail, crossword, exam countdown, readiness for the 80-question general portion and the 35-question Connecticut portion, chapter count, review queue, ranger badge, and a math drill. An optional trail dog walks along; the default name is Hudson and can be changed on this phone.
- **Theme.** Outdoors is the default scene around questions that have one. Adventure, History, and Classic are in settings. The scene never changes the facts.
- **Screens.** The layout is built for a phone around 390 pixels wide. On a wide window the shell stops at 1080 pixels, the trailhead tiles sit in a wider grid, and the crossword grid sits beside its clues. Crossword keys: letters, arrows, and Tab for the next clue. Quiz and mock answers: keys 1 to 4.
- **Trail Buddy.** The Buddy tab is an offline study helper with a trail-guide voice. It searches this app's glossary, Connecticut notes, and question explanations. No API key. A match can start a three-question quiz. It is a study helper, not a counselor. Turn on Read aloud and it speaks answers and questions, choices included, for a parked hands-free round.
- **Talk to my tutor.** `data/tutor.json` holds `talkTutorUrl`. Leave it empty and the button stays hidden on the trailhead and in Trail Buddy. Set an http or https link when you have a tutor page.
- **Hands-free tips.** The trailhead card opens a short page on the microphone key for iPhone and Android keyboards, plus Trail Buddy's mic and read-aloud. Where the browser supports the Web Speech API, a mic sits on Trail Buddy, the crossword, and the trail dog's name. A spoken Trail Buddy question is sent for you. Saying a word fills the current crossword entry. If the browser has no speech button, the page says to use the keyboard microphone key.
- **Review.** Missed questions come back immediately. A correct answer waits longer the next time.
- **Daily crossword.** A new original grid each calendar day, built only from course chapters you have checked. The starting checklist is chapters 2, 3, 6, 7, 14, 15, 16, 17, and 20. A single chapter uses a smaller mini grid when its word list is short. With every chapter checked, Monday is the smallest, clues get harder through Saturday, and Sunday is larger. Tap a square to select it, tap again to switch across and down. Check or reveal a letter, a word, or the whole puzzle. The timer pauses when you leave. A clean solve adds 40 XP and one of each supply that is not already full. A solve that used a reveal adds 12 XP. The crossword streak and the in-progress grid stay on this phone. XP for the crossword counts once per calendar day.
- **Course chapters.** The chapter list lives in `data/course.json`. Check the ones you have finished under Chapters I've completed. The road follows that checklist. Connecticut-law questions carry a CT Law badge and are tagged to those chapters, so a stop can include a Connecticut-law event from a checked chapter. Replace the chapter list to match a syllabus, retag `words` and each question's `chapter`, then rebuild the crossword library.
- **Exam date.** Type your own date under Chapters, exam date, and sound. Change it whenever you want. Sound is off until you turn it on.

The app is an installable PWA. Add it to your home screen after it loads once; the service worker keeps the question bank available offline.

## Run locally

No build step is required to play. From this folder:

```bash
python3 -m http.server 8080
```

Then open `http://127.0.0.1:8080/`.

Check the game rules, the bank, and the crossword library:

```bash
node scripts/test_game.mjs
python3 scripts/course_units.py
python3 scripts/build_crosswords.py
python3 scripts/build_glossary.py
```

## Add questions

Questions live in `scripts/bank_ct.py`, `scripts/bank_national.py`, `scripts/bank_national_b.py`, and the math generator in `scripts/build_bank.py`. Rebuild the file the site actually loads:

```bash
python3 scripts/build_bank.py
```

That writes `data/questions.json`. Each item needs a stem, one correct answer, three wrong answers, and an explanation. Connecticut items need a `source` with a `label` and a `url` pointing at a public official page. Math items need `steps`. The rebuild also stamps a `chapter` number from `scripts/course_units.py`. Chapter titles in `data/course.json` are topic tags only. Do not name a textbook. Questions, crossword clues, and definitions must stay original and grounded in the PSI outline, Connecticut statutes, and DCP sources. Do not copy or closely paraphrase textbook wording, questions, glossary definitions, or figures, and do not copy a paid prep course or PSI's sample items.

Topic weights in `TOPICS` must keep adding up to 80 for the national portion and 35 for the Connecticut portion. Those weights are how the mock exam draws its mix. The Math Pass topic supplies the national calculations block (weight 6) and is not a stop on the road.

## Sources

Questions were written for this project from public official materials:

- PSI Connecticut Real Estate candidate information, updated November 13, 2025: [test-takers.psiexams.com/ctre](https://test-takers.psiexams.com/ctre)
- Connecticut Department of Consumer Protection, [salesperson initial exam](https://portal.ct.gov/dcp/license-services-division/all-license-applications/real-estate-salesperson---initialexam), [continuing education](https://portal.ct.gov/dcp/continuing-education/real-estate-salesperson---continuing-education), and the [guaranty fund](https://portal.ct.gov/dcp/common-elements/consumer-facts-and-contacts/real-estate-guaranty-fund)
- [Connecticut General Statutes, Chapter 392](https://www.cga.ct.gov/current/pub/chap_392.htm) (real estate brokers and salespersons)
- [Regulations of Connecticut State Agencies](https://eregulations.ct.gov/eRegsPortal/Browse/RCSA/Title_20Subtitle_20-328Section_20-328-1a.html) on licensee conduct (sections 20-328-1a through 20-328-10a)
- [Chapter 223](https://www.cga.ct.gov/current/pub/chap_223.htm) (real estate conveyance tax, §§ 12-494 to 12-498)
- [Chapter 814c](https://www.cga.ct.gov/current/pub/chap_814c.htm) (discriminatory housing practices)
- [Chapter 831](https://www.cga.ct.gov/current/pub/chap_831.htm) (security deposits, § 47a-21)
- [§ 47-37](https://www.cga.ct.gov/current/pub/chap_822.htm#sec_47-37) (prescriptive easements) and [§ 52-575](https://www.cga.ct.gov/current/pub/chap_926.htm#sec_52-575)
- Federal rules used only on national items: Fair Housing Act (42 USC 3604), lead-based paint disclosure (42 USC 4852d), RESPA (12 USC 2607), Regulation Z / TRID (12 CFR 1026.19), ECOA (15 USC 1691), Sherman Act (15 USC 1), ADA Title III, and the FTC Telemarketing Sales Rule

Conveyance-tax math uses the rates in § 12-494 and assumes the town has **not** adopted an extra local tax. Continuing-education dates in the bank follow the DCP page for the cycle March 1, 2026 through February 28, 2028. Recheck that page when the cycle changes.

Figures that could not be pinned to a stable official text were left out. That includes the current security-deposit interest rate (it is reset from the deposit index), any dollar cap on the guaranty-fund balance, Connecticut recording priority, the common-interest resale-certificate cancellation window, and an appraisal de minimis dollar cutoff. Leasing and property management is the shortest national topic because the outline gives it the smallest share of the exam. Connecticut agency is covered, with fewer items than licensing or conduct.

## Credits

Third-party code used to publish the site is listed in [`LICENSES/credits`](LICENSES/credits). The study text, crossword, and art in this repository are original. The deploy workflow calls MIT-licensed GitHub Actions (`actions/checkout`, `actions/configure-pages`, `actions/upload-pages-artifact`, and `actions/deploy-pages`). No copyrighted game art or textbook content is included.

Layout patterns come from the owner's other public repositories. Those sites were not copied. See the credits file for which pattern came from which repo.

## Deploy

Pushes to `main` run `.github/workflows/pages.yml`, the same Actions shape as [the-immortal-case](https://github.com/asteroidsravens/the-immortal-case): checkout, configure Pages with no enablement flag, upload the site root, deploy. A newer push cancels an in-progress deploy. `.nojekyll` is included the way [asteroidsravens.github.io](https://github.com/asteroidsravens/asteroidsravens.github.io) does, so a branch publish will not run Jekyll on this tree.

The site uses relative paths so it can live at a project URL, the same kind of address as [the-slow-boil](https://asteroidsravens.github.io/the-slow-boil/). The intended address is `https://asteroidsravens.github.io/ct-license-trail/`. The user-site root, `https://asteroidsravens.github.io/`, stays the existing site. This app does not replace that index.

The repository is meant to stay private. GitHub Pages on a private repository needs a paid plan (GitHub Pro, Team, or Enterprise). An admin has to set **Settings → Pages → Build and deployment → Source: GitHub Actions** once. The workflow cannot create that site on its own. Do not switch the repository back to public if Pages then fails for billing.

## Disclaimer

CT License Trail is an unofficial study aid. Exam rules, fees, tax rates, and license deadlines change. Read the current PSI bulletin, the Department of Consumer Protection pages, the General Statutes, and the regulations before you rely on a number. Nothing here is legal advice or a promise about an exam result.
