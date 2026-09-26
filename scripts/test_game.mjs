import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import {
  createState, levelInfo, daysUntil, todayKey, previousDay, masteryPercent,
  answerQuestion, dueReviews, sampleExam, scoreExam, recordExam, roadTopics,
  puzzleForDate, awardCrossword, completedChapters, pickQuestions,
  displayStem, ctLawEventsForStop, themeId,
  portionOf, portionReadiness, chapterStudyPlan, hydratePortions, EXAM_SHAPE,
  cleanDogName, companion, companionCheer, DEFAULT_DOG_NAME, liveStreak,
  searchBuddy, tutorUrl, spokenLetters, trailBuddyLines,
} from "../js/logic.js";

const bank = JSON.parse(readFileSync(new URL("../data/questions.json", import.meta.url), "utf8"));
const questions = bank.questions;
const byId = Object.fromEntries(questions.map((q) => [q.id, q]));

assert.ok(questions.length >= 400, `need 400+ questions, got ${questions.length}`);
const math = questions.filter((q) => q.math);
assert.ok(math.length >= 80, `need 80+ math, got ${math.length}`);

const stems = new Set();
for (const q of questions) {
  assert.equal(q.choices.length, 4, q.id);
  assert.equal(new Set(q.choices).size, 4, q.id);
  assert.ok(q.answer >= 0 && q.answer < 4, q.id);
  assert.ok(q.explanation && q.explanation.length > 20, q.id);
  assert.ok(!stems.has(q.stem), `duplicate stem ${q.id}`);
  stems.add(q.stem);
  if (q.math) assert.ok(Array.isArray(q.steps) && q.steps.length >= 2, q.id);
  if (q.topic.startsWith("ct-") || (q.pools || []).includes("ct-laws")) {
    assert.ok(q.source && q.source.url && q.source.label, `missing source ${q.id}`);
  }
}

const national = bank.topics.filter((t) => t.portion === "national");
const state = bank.topics.filter((t) => t.portion === "state");
assert.equal(national.reduce((n, t) => n + t.weight, 0), 80);
assert.equal(state.reduce((n, t) => n + t.weight, 0), 35);
assert.equal(roadTopics(bank.topics).some((t) => t.id === "math"), false);

for (const topic of bank.topics) {
  const pool = questions.filter((q) => q.pools.includes(topic.id));
  assert.ok(pool.length >= topic.weight, `${topic.id} pool ${pool.length} < weight ${topic.weight}`);
}

const rng = () => 0.5;
const nationalExam = sampleExam(questions, bank.topics, "national", rng);
const stateExam = sampleExam(questions, bank.topics, "state", rng);
const both = sampleExam(questions, bank.topics, "both", rng);
assert.equal(nationalExam.ids.length, 80);
assert.equal(nationalExam.minutes, 120);
assert.equal(stateExam.ids.length, 35);
assert.equal(stateExam.minutes, 45);
assert.equal(both.ids.length, 115);
assert.equal(both.minutes, 165);
assert.equal(new Set(both.ids).size, 115);

const q = questions.find((item) => item.topic === "ownership");
let state0 = createState();
const wrong = answerQuestion(state0, q, (q.answer + 1) % 4, 1_700_000_000_000, "2026-09-26");
assert.equal(wrong.correct, false);
assert.equal(wrong.xpGain, 3);
assert.equal(wrong.state.supplies.coffee, 5);
assert.equal(wrong.state.stats.answered, 1);
assert.equal(wrong.state.streak.count, 1);
assert.ok(dueReviews(wrong.state, 1_700_000_000_000).includes(q.id));

let rightState = wrong.state;
for (let i = 0; i < 3; i += 1) {
  const again = answerQuestion(rightState, q, q.answer, 1_700_000_000_000 + i + 1, "2026-09-26");
  assert.equal(again.correct, true);
  rightState = again.state;
  if (i === 2) assert.equal(again.supplyDelta, 1);
}
assert.equal(rightState.answerStreak, 3);
assert.equal(dueReviews(rightState, 1_700_000_000_000 + 10).includes(q.id), false);

const day = "2026-09-26";
assert.equal(previousDay(day), "2026-09-25");
assert.equal(daysUntil("2026-09-28", day), 2);
assert.equal(daysUntil(day, day), 0);
assert.equal(levelInfo(0).name, "Student");
assert.equal(levelInfo(80).name, "Notebook Rider");
assert.equal(levelInfo(3000).name, "Licensed Agent");
assert.equal(masteryPercent(rightState, q.topic) > 0, true);

const examState = createState();
const answers = {};
both.ids.forEach((id, index) => { answers[id] = index % 7 === 0 ? (byId[id].answer + 1) % 4 : byId[id].answer; });
const recorded = recordExam(examState, both.ids, answers, byId, 1_700_000_000_000, day);
assert.equal(recorded.result.total, 115);
assert.equal(recorded.result.percent >= 70, recorded.result.passed);
assert.equal(recorded.state.streak.count, 1);
assert.ok(dueReviews(recorded.state, 1_700_000_000_000).length > 0);

const scored = scoreExam(both.ids, Object.fromEntries(both.ids.map((id) => [id, byId[id].answer])), byId, both.sections);
assert.equal(scored.percent, 100);
assert.equal(scored.passed, true);
assert.equal(scored.portions.length, 2);
assert.ok(scored.portions.every((row) => row.passed));
const splitAnswers = Object.fromEntries(both.ids.map((id) => [id, byId[id].answer]));
both.sections.find((section) => section.id === "state").ids.forEach((id) => {
  splitAnswers[id] = (byId[id].answer + 1) % 4;
});
const split = scoreExam(both.ids, splitAnswers, byId, both.sections);
assert.equal(split.portions.find((row) => row.id === "national").passed, true);
assert.equal(split.portions.find((row) => row.id === "state").passed, false);
assert.equal(split.passed, false);

const course = JSON.parse(readFileSync(new URL("../data/course.json", import.meta.url), "utf8"));
const pack = JSON.parse(readFileSync(new URL("../data/crosswords.json", import.meta.url), "utf8"));
const chapterNumbers = course.chapters.map((row) => row.n);
assert.deepEqual(chapterNumbers, Array.from({ length: 21 }, (_, index) => index + 1));
assert.deepEqual(course.defaultCompleted, [2, 3, 6, 7, 14, 15, 16, 17, 20]);
assert.deepEqual(completedChapters(createState(), course), course.defaultCompleted);
const custom = createState();
custom.completedChapters = [16, 2, 99];
assert.deepEqual(completedChapters(custom, course), [2, 16]);
custom.completedChapters = [];
assert.deepEqual(completedChapters(custom, course), []);
for (const item of questions) {
  assert.equal(item.unit, undefined, `${item.id} unit`);
  assert.ok(chapterNumbers.includes(item.chapter), `${item.id} chapter`);
}
const ctLayer = questions.filter((q) => q.ctLaw);
assert.ok(ctLayer.length >= 30, `ct law layer ${ctLayer.length}`);
const eventChapters = new Set(ctLayer.filter((q) => q.event).map((q) => q.chapter));
for (const n of [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21]) {
  assert.ok(eventChapters.has(n), `missing CT law event for chapter ${n}`);
}
for (const q of ctLayer) {
  assert.ok(q.source && q.source.url && q.source.label, q.id);
  assert.ok(q.flavor.outdoors && q.flavor.adventure && q.flavor.history, q.id);
  assert.equal(q.flavor.classic, undefined, q.id);
  assert.equal(displayStem(q, "classic"), q.stem);
  const outdoors = displayStem(q, "outdoors");
  assert.equal(outdoors, `${q.flavor.outdoors} ${q.stem}`);
  assert.equal(outdoors.includes(q.choices[q.answer]), false);
}
assert.equal(themeId(createState()), "outdoors");
assert.equal(createState().settings.dogName, DEFAULT_DOG_NAME);
assert.equal(cleanDogName("  <Hudson!> "), "Hudson");
assert.equal(cleanDogName(""), DEFAULT_DOG_NAME);
assert.equal(companion(createState()).on, true);
assert.equal(companion({ settings: { dog: false, dogName: "Moss" } }).on, false);
assert.equal(companionCheer({ settings: { dog: false } }, "2026-09-26"), "");
assert.ok(companionCheer(createState(), "2026-09-26").includes("Hudson"));
assert.equal(liveStreak({ count: 4, lastDay: "2026-09-25" }, "2026-09-26"), 4);
assert.equal(liveStreak({ count: 4, lastDay: "2026-09-01" }, "2026-09-26"), 0);
const ownershipEvents = ctLawEventsForStop(questions, "ownership", [3, 4, 5], []);
assert.ok(ownershipEvents.some((q) => q.chapter === 3 && q.ctLaw && q.event));
assert.equal(ctLawEventsForStop(questions, "ownership", [2], []).length, 0);

const starter = course.defaultCompleted;
const towns = roadTopics(bank.topics, questions, starter);
assert.ok(towns.length > 0);
assert.equal(roadTopics(bank.topics, questions, []).length, 0);
for (const town of towns) {
  const ids = pickQuestions(questions, town.id, 3, createState(), () => 0.2, starter);
  assert.ok(ids.length > 0, town.id);
  ids.forEach((id) => assert.ok(starter.includes(byId[id].chapter), `${town.id} ${id}`));
}
const limited = sampleExam(questions, bank.topics, "national", rng, starter);
assert.ok(limited.ids.length > 0 && limited.ids.length <= 80);
assert.equal(limited.everyChapter, false);
limited.ids.forEach((id) => assert.ok(starter.includes(byId[id].chapter), id));
const fullNational = sampleExam(questions, bank.topics, "both", rng, null);
assert.equal(fullNational.everyChapter, true);
assert.equal(fullNational.ids.length, 115);
const days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"];
const banned = /new york times|\bnyt\b|wall street journal/i;
let puzzleCount = 0;
assert.ok(pack.packs.default, "default pack");
assert.ok(pack.packs.all, "all-chapters pack");
assert.deepEqual([...pack.packs.default.chapters].sort((a, b) => a - b), starter);
assert.deepEqual(pack.packs.all.chapters, chapterNumbers);
for (const [packId, range] of Object.entries(pack.packs)) {
  const allowed = new Set([...range.chapters, 0]);
  for (const day of days) {
    const need = packId === "default" || packId === "all" ? 8 : 4;
    assert.ok(range.days[day].length >= need, `${packId} ${day}`);
    for (const puzzle of range.days[day]) {
      puzzleCount += 1;
      assert.equal(banned.test(JSON.stringify(puzzle)), false, puzzle.id);
      const n = puzzle.size;
      const grid = puzzle.grid;
      assert.equal(grid.length, n);
      const seen = new Set();
      for (const entry of [...puzzle.across, ...puzzle.down]) {
        assert.ok(entry.answer.length >= 3, puzzle.id);
        assert.equal(seen.has(entry.answer), false, `${puzzle.id} ${entry.answer}`);
        seen.add(entry.answer);
        assert.equal(course.words[entry.answer], entry.chapter, `${puzzle.id} ${entry.answer}`);
        assert.ok(allowed.has(entry.chapter), `${puzzle.id} chapter ${entry.chapter}`);
        let r = entry.row;
        let c = entry.col;
        const across = puzzle.across.includes(entry);
        let built = "";
        for (const ch of entry.answer) {
          assert.notEqual(grid[r][c], "#");
          built += grid[r][c];
          if (across) c += 1;
          else r += 1;
        }
        assert.equal(built, entry.answer, puzzle.id);
        const clue = entry.clue.toLowerCase();
        if (clue.includes("connecticut") || clue.includes("dcp") || clue.includes("psi ")) {
          assert.ok(entry.source && entry.source.url, `${puzzle.id} ${entry.clue}`);
        }
      }
      for (let r = 0; r < n; r += 1) {
        for (let c = 0; c < n; c += 1) {
          assert.equal(grid[r][c] === "#", grid[n - 1 - r][n - 1 - c] === "#", puzzle.id);
          if (grid[r][c] === "#") continue;
          const across = puzzle.across.some((entry) => entry.row === r && c >= entry.col && c < entry.col + entry.answer.length);
          const down = puzzle.down.some((entry) => entry.col === c && r >= entry.row && r < entry.row + entry.answer.length);
          assert.equal(across && down, true, `${puzzle.id} ${r},${c}`);
        }
      }
    }
  }
  const sizes = Object.fromEntries(days.map((day) => [day, range.days[day][0].size]));
  assert.ok(sizes.sunday >= sizes.saturday, `${packId} sunday`);
  if (range.tier === "full") {
    assert.ok(sizes.monday < sizes.thursday, packId);
    assert.ok(sizes.saturday < sizes.sunday, packId);
  }
  if (range.tier === "mini") {
    assert.ok(sizes.monday <= 5 && sizes.saturday <= 5, packId);
  }
}
for (const day of days) {
  for (const puzzle of pack.packs.default.days[day]) {
    const chapters = new Set([...puzzle.across, ...puzzle.down].map((entry) => entry.chapter));
    assert.equal(chapters.has(12), false, puzzle.id);
    assert.equal(chapters.has(1), false, puzzle.id);
  }
}

const monday = new Date(2024, 0, 1);
const first = puzzleForDate(pack, monday, starter);
assert.equal(first.weekday, "monday");
assert.equal(first.dateKey, "2024-01-01");
assert.ok(first.chapters.length > 0);
assert.ok(first.chapters.every((n) => starter.includes(n)));
const nextMonday = new Date(2024, 0, 8);
assert.equal(puzzleForDate(pack, nextMonday, starter).puzzle.id !== first.puzzle.id, true);
assert.equal(puzzleForDate(pack, monday, starter).puzzle.id, first.puzzle.id);
assert.ok(puzzleForDate(pack, monday).chapters.every((n) => starter.includes(n)));
assert.equal(puzzleForDate(pack, monday, []), null);
const onlyTwo = puzzleForDate(pack, monday, [2]);
assert.ok(onlyTwo);
assert.deepEqual(onlyTwo.chapters, [2]);
const saturday = new Date(2024, 0, 6);
const sunday = new Date(2024, 0, 7);
assert.equal(puzzleForDate(pack, sunday, chapterNumbers).weekday, "sunday");
assert.ok(puzzleForDate(pack, sunday, chapterNumbers).puzzle.size > puzzleForDate(pack, saturday, chapterNumbers).puzzle.size);

let fresh = createState();
const clean = awardCrossword(fresh, "2026-09-26", true, "monday-1");
assert.equal(clean.awarded, true);
assert.equal(clean.xpGain, 40);
assert.equal(clean.state.xp, 40);
assert.equal(clean.state.supplies.coffee, 7);
assert.equal(clean.state.supplies.fuel, 7);
assert.equal(clean.supplyDelta, 4);
assert.equal(clean.state.streak.count, 1);
assert.equal(clean.state.crossword.streak.count, 1);
const again = awardCrossword(clean.state, "2026-09-26", true, "monday-1");
assert.equal(again.awarded, false);
assert.equal(again.state.xp, 40);
const dirty = awardCrossword(createState(), "2026-09-26", false, "monday-1");
assert.equal(dirty.xpGain, 12);
assert.equal(dirty.state.supplies.coffee, 6);
assert.equal(dirty.supplyDelta, 0);
const nextDay = awardCrossword(clean.state, "2026-09-27", true, "tuesday-1");
assert.equal(nextDay.state.crossword.streak.count, 2);
const skipped = awardCrossword(clean.state, "2026-09-28", true, "wednesday-1");
assert.equal(skipped.state.crossword.streak.count, 1);

const ctQuestion = questions.find((q) => q.ctLaw);
const nationalQuestion = questions.find((q) => q.topic === "contracts" && !q.ctLaw);
assert.equal(portionOf(ctQuestion), "state");
assert.equal(portionOf(nationalQuestion), "national");
let pace = createState();
pace = answerQuestion(pace, nationalQuestion, nationalQuestion.answer).state;
pace = answerQuestion(pace, ctQuestion, (ctQuestion.answer + 1) % 4).state;
const ready = portionReadiness(pace);
assert.equal(ready.find((row) => row.id === "national").correct, 1);
assert.equal(ready.find((row) => row.id === "state").correct, 0);
assert.equal(ready.find((row) => row.id === "state").seen, 1);
assert.equal(ready.find((row) => row.id === "national").status, "Early");
const plan3 = chapterStudyPlan(questions, 3, () => 0.2);
assert.ok(plan3.principles.length > 0);
assert.ok(plan3.ct.length > 0);
assert.ok(plan3.quiz.length > 0);
assert.ok(plan3.ct.every((id) => portionOf(byId[id]) === "state"));
assert.ok(plan3.principles.every((id) => portionOf(byId[id]) === "national"));
const plan2 = chapterStudyPlan(questions, 2, () => 0.2);
assert.equal(plan2.ct.length, 0);
assert.ok(plan2.principles.length > 0);
const seeded = hydratePortions(createState(), questions);
assert.equal(portionReadiness(seeded)[0].seen, 0);

const glossary = JSON.parse(readFileSync(new URL("../data/glossary.json", import.meta.url), "utf8")).entries;
const tutor = JSON.parse(readFileSync(new URL("../data/tutor.json", import.meta.url), "utf8"));
assert.equal(tutor.talkTutorUrl, "");
assert.equal(tutorUrl(tutor), "");
assert.equal(tutorUrl({ talkTutorUrl: "javascript:alert(1)" }), "");
assert.equal(tutorUrl({ askTutorUrl: "https://example.com/tutor" }), "https://example.com/tutor");
assert.equal(tutorUrl({ talkTutorUrl: "https://example.com/trail" }), "https://example.com/trail");
assert.equal(createState().settings.readAloud, false);
assert.equal(spokenLetters("an easement."), "EASEMENT");
assert.equal(spokenLetters("the deed"), "DEED");
const easement = searchBuddy("what is an easement", glossary, questions);
assert.equal(easement.kind, "glossary");
assert.equal(easement.term, "EASEMENT");
assert.match(easement.text, /right to use/i);
assert.equal(easement.related.length, 3);
assert.ok(easement.related.every((id) => /easement/i.test(`${byId[id].stem} ${byId[id].explanation}`)));
const dual = searchBuddy("CT dual agency", glossary, questions);
assert.equal(dual.kind, "law");
assert.match(`${dual.title} ${dual.text}`, /dual[- ]agency/i);
assert.ok(dual.source?.url && dual.source.label);
assert.equal(dual.related.length, 3);
assert.ok(dual.related.every((id) => /dual[- ]agency/i.test(`${byId[id].stem} ${byId[id].explanation}`)));
const voice = trailBuddyLines("what is an easement", easement);
assert.match(voice.lead, /pack|notes|map/i);
assert.match(voice.nudge, /Quiz me on this/i);
const miss = trailBuddyLines("zzzznotaterm", null);
assert.match(miss.lead, /glossary|pack/i);
assert.equal(/counselor/i.test(`${voice.lead} ${voice.nudge} ${miss.lead} ${miss.nudge}`), false);
const appSource = readFileSync(new URL("../js/app.js", import.meta.url), "utf8");
assert.match(appSource, /study helper, not a counselor/);
assert.match(appSource, /Hands-free tips/);
assert.match(appSource, /Talk to my tutor/);
assert.match(appSource, /speechSynthesis/);

console.log(`ok ${questions.length} questions, ${math.length} math, ${puzzleCount} crosswords, ${chapterNumbers.length} chapters`);
