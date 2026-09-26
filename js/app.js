import {
  STORAGE_KEY, SUPPLIES, SUPPLY_MAX, createState, levelInfo, daysUntil, todayKey,
  masteryPercent, answerQuestion, dueReviews, pickQuestions, sampleExam, recordExam,
  roadTopics, puzzleForDate, awardCrossword, completedChapters,
  themeId, displayStem, ctLawEventsForStop, THEMES,
  EXAM_SHAPE, portionReadiness, hydratePortions, chapterStudyPlan,
} from "./logic.js";

const main = document.querySelector("#main");
const live = document.querySelector("#live");
const tabButtons = [...document.querySelectorAll(".tabs button")];
const levelName = document.querySelector("#level-name");
const streakPill = document.querySelector("#streak-pill");
const countPill = document.querySelector("#count-pill");

let bank = null;
let byId = {};
let crosswords = null;
let course = null;
let state = loadState();
let screen = "home";
let calcValue = "0";
let calcFresh = true;
let timerHandle = 0;

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return createState();
    const saved = JSON.parse(raw);
    const fresh = createState();
    return {
      ...fresh,
      ...saved,
      supplies: { ...fresh.supplies, ...(saved.supplies || {}) },
      settings: { sound: false, ...(saved.settings || {}) },
      streak: { ...fresh.streak, ...(saved.streak || {}) },
      stats: { ...fresh.stats, ...(saved.stats || {}) },
      portions: saved.portions || fresh.portions,
      chapterLoops: { ...(saved.chapterLoops || {}) },
      crossword: {
        streak: { ...fresh.crossword.streak, ...(saved.crossword?.streak || {}) },
        solved: { ...(saved.crossword?.solved || {}) },
        progress: { ...(saved.crossword?.progress || {}) },
      },
    };
  } catch {
    return createState();
  }
}

function save() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  paintChrome();
}

function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (ch) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[ch]));
}

function topicById(id) {
  return bank.topics.find((topic) => topic.id === id);
}

function say(text) {
  live.textContent = "";
  window.setTimeout(() => { live.textContent = text; }, 30);
}

function beep(ok) {
  if (!state.settings.sound) return;
  const Ctx = window.AudioContext || window.webkitAudioContext;
  if (!Ctx) return;
  const ctx = beep.ctx || new Ctx();
  beep.ctx = ctx;
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.type = "sine";
  osc.frequency.value = ok ? 587 : 196;
  gain.gain.value = 0.035;
  osc.connect(gain);
  gain.connect(ctx.destination);
  osc.start();
  osc.stop(ctx.currentTime + 0.09);
}

function paintChrome() {
  const level = levelInfo(state.xp);
  levelName.textContent = level.name;
  const day = state.streak.lastDay === todayKey() ? state.streak.count : state.streak.count;
  streakPill.textContent = `${state.streak.count || 0}-day streak`;
  countPill.textContent = `${state.stats.correct}/${state.stats.answered || 0} correct`;
  tabButtons.forEach((button) => {
    const tab = button.dataset.tab;
    const quizKind = state.session?.kind;
    const on = (tab === "home" && (screen === "home" || (screen === "question" && quizKind !== "math" && quizKind !== "review")))
      || (tab === "map" && (screen === "map" || screen === "loop"))
      || (tab === "math" && (screen === "math" || (screen === "question" && quizKind === "math")))
      || (tab === "exam" && ["exam", "mock"].includes(screen))
      || (tab === "review" && (screen === "review" || (screen === "question" && quizKind === "review")))
      || (tab === "daily" && screen === "daily");
    if (on) button.setAttribute("aria-current", "page");
    else button.removeAttribute("aria-current");
  });
}

function go(next) {
  if (screen === "daily" && next !== "daily") freezeDaily();
  if (screen === "mock" && next !== "mock") freezeMock();
  screen = next;
  state.lastScreen = next;
  save();
  render();
}

function currentQuestion() {
  if (!state.session) return null;
  return byId[state.session.ids[state.session.index]];
}

function startSession(kind, ids, topicId) {
  state.session = { kind, topicId, ids, index: 0, phase: "ask", choice: null, note: "" };
  go("question");
}

function chapterList() {
  return completedChapters(state, course);
}

function openRoad() {
  return roadTopics(bank.topics, bank.questions, chapterList());
}

function chapterTitle(number) {
  const row = course?.chapters?.find((item) => item.n === number);
  return row ? `Ch ${number} · ${row.name}` : `Chapter ${number}`;
}

function startJourney(topicId) {
  const road = openRoad();
  const chapters = chapterList();
  if (!road.length) {
    say("Check at least one course chapter to open a town.");
    go("settings");
    return;
  }
  if (!topicId) {
    const topic = road[(state.routeIndex || 0) % road.length];
    topicId = topic.id;
  } else {
    const index = road.findIndex((topic) => topic.id === topicId);
    if (index >= 0) state.routeIndex = index;
  }
  const ids = pickQuestions(bank.questions, topicId, 3, state, Math.random, chapters);
  if (!ids.length) {
    say("That town has no questions in the chapters you've completed.");
    return;
  }
  const ctEvents = ctLawEventsForStop(bank.questions, topicId, chapters, ids);
  if (ctEvents.length && ids.length > 1) {
    const event = ctEvents[Math.floor(Math.random() * ctEvents.length)];
    ids.splice(1, 1, event.id);
  } else {
    const events = bank.questions.filter((q) => q.event && q.topic === topicId && chapters.includes(q.chapter) && !ids.includes(q.id));
    if (events.length && Math.random() < 0.75 && ids.length > 1) {
      const event = events[Math.floor(Math.random() * events.length)];
      ids.splice(1, 1, event.id);
    }
  }
  startSession("journey", ids, topicId);
}

function freezeMock(now = Date.now()) {
  if (!state.mock || state.mock.submitted || !state.mock.running) return;
  state.mock.elapsedMs += Math.max(0, now - state.mock.lastTick);
  state.mock.running = false;
  state.mock.lastTick = now;
  save();
}

function resumeMock(now = Date.now()) {
  if (!state.mock || state.mock.submitted) return;
  state.mock.running = true;
  state.mock.lastTick = now;
  save();
}

function mockLeft(now = Date.now()) {
  if (!state.mock) return 0;
  let elapsed = state.mock.elapsedMs;
  if (state.mock.running) elapsed += now - state.mock.lastTick;
  return Math.max(0, state.mock.limitMs - elapsed);
}

function formatClock(ms) {
  const total = Math.ceil(ms / 1000);
  const m = Math.floor(total / 60);
  const s = total % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

function render() {
  window.clearInterval(timerHandle);
  paintChrome();
  const views = {
    home: viewHome,
    question: viewQuestion,
    map: viewMap,
    math: viewMathHome,
    mathrun: viewQuestion,
    exam: viewExamHome,
    loop: viewLoop,
    mock: viewMock,
    review: viewReviewHome,
    settings: viewSettings,
    about: viewAbout,
    daily: viewDaily,
  };
  (views[screen] || viewHome)();
  const heading = main.querySelector("h2, .stem");
  if (heading) heading.setAttribute("tabindex", "-1");
}

function viewHome() {
  const level = levelInfo(state.xp);
  const days = daysUntil(state.examDate);
  const due = dueInChapters().length;
  const road = openRoad();
  const town = road.length ? road[(state.routeIndex || 0) % road.length] : null;
  let dateLine = "Set your own exam date whenever you know it. Change it any time.";
  if (days === 0) dateLine = "Exam day is today. A short review still counts.";
  else if (days > 0) dateLine = `${days} day${days === 1 ? "" : "s"} until the date you chose.`;
  else if (days < 0) dateLine = "That exam date has passed. Pick another whenever you are ready.";
  const resumeMock = state.mock && !state.mock.submitted;
  const resumeQuiz = state.session && state.session.phase;
  main.innerHTML = `
    <section class="card">
      <p class="kicker">${town ? esc(town.town) : "Course chapters"}</p>
      <h2>${resumeQuiz ? "Pick up the same question" : town ? `Next stop: ${esc(town.name)}` : "No town in these chapters yet"}</h2>
      <p class="lede">${town ? `${esc(town.blurb)} Three questions is a full stop between rides.` : "The road uses only chapters you've completed. Check the ones you have finished."}</p>
      <div class="stack">
        ${resumeMock ? `<button class="btn btn-primary" data-act="resume-mock">Resume mock exam</button>` : ""}
        <button class="btn btn-primary" data-act="continue" ${!resumeQuiz && !town ? "disabled" : ""}>${resumeQuiz ? "Continue this question" : "Start three questions"}</button>
        <button class="btn btn-pine" data-act="study-list">Study a chapter</button>
        <button class="btn btn-quiet" data-act="daily">${dailyHomeLabel()}</button>
        <button class="btn btn-quiet" data-act="settings">Chapters, exam date, and sound</button>
      </div>
    </section>
    <section class="card">
      <h2>${esc(level.name)}</h2>
      <p class="muted">${state.xp} XP${level.nextAt ? ` · ${level.nextAt - state.xp} to ${esc(level.nextName)}` : ""}</p>
      <div class="meter" aria-hidden="true"><span style="width:${level.pct}%"></span></div>
      <div class="meters" style="margin-top:12px">
        ${SUPPLIES.map((row) => `
          <div class="supply">
            <strong>${esc(row.label)}</strong>
            <span class="muted">${state.supplies[row.id]}/${SUPPLY_MAX}</span>
            <div class="bar" aria-hidden="true"><span style="width:${(state.supplies[row.id] / SUPPLY_MAX) * 100}%"></span></div>
          </div>`).join("")}
      </div>
      <p class="muted">A miss spends a supply. Three correct answers in a row put one back. Hitting empty is a pull-over, not the end of the trip.</p>
    </section>
    <section class="card">
      <h2>Your date</h2>
      <p>${esc(dateLine)}</p>
      <p>${due ? `${due} missed question${due === 1 ? "" : "s"} ready for another look.` : "The review pile is clear."}</p>
    </section>
      <p class="fine">Unofficial study aid for the Connecticut salesperson exam. Not affiliated with PSI or the Department of Consumer Protection.</p>
    ${readinessCard()}`;
}

function viewQuestion() {
  const session = state.session;
  if (!session || !session.ids.length) {
    go("home");
    return;
  }
  const question = byId[session.ids[session.index]];
  const topic = topicById(question.topic);
  const answered = session.phase === "explain";
  const keys = ["1", "2", "3", "4"];
  const where = session.kind === "review" ? "Review"
    : session.kind === "math" ? "Math Pass"
    : session.kind === "chapter-principles" ? "Principles and practices"
    : session.kind === "chapter-ct" ? "Connecticut law"
    : session.kind === "chapter-quiz" ? "Chapter quiz"
    : topic?.town || "Chapter";
  const quizMode = session.kind === "chapter-quiz";
  const quizChoice = quizMode ? session.answers?.[question.id] : null;
  const chapterBit = question.chapter ? chapterTitle(question.chapter) : "";
  const lawBadge = question.ctLaw ? `<span class="badge-ct">CT Law</span>` : "";
  main.innerHTML = `
    <article class="card">
      <p class="kicker">${lawBadge}${esc(where)}${chapterBit ? ` · ${esc(chapterBit)}` : ""} · ${session.index + 1} of ${session.ids.length}${question.event && session.kind === "journey" ? " · road stop" : ""}</p>
      <h2 class="stem" id="stem">${esc(displayStem(question, themeId(state)))}</h2>
      <div class="stack" role="group" aria-labelledby="stem">
        ${question.choices.map((choice, index) => {
          let cls = "choice";
          if (quizMode && quizChoice === index) cls += " picked";
          if (!quizMode && answered && index === question.answer) cls += " good";
          else if (!quizMode && answered && index === session.choice && index !== question.answer) cls += " bad";
          return `<button class="${cls}" data-choice="${index}" ${!quizMode && answered ? "disabled" : ""}>
            <span class="key" aria-hidden="true">${keys[index]}</span>
            <span>${esc(choice)}</span>
          </button>`;
        }).join("")}
      </div>
      ${!quizMode && answered ? explainBlock(question, session.choice) : ""}
      ${session.note ? `<div class="note">${esc(session.note)}</div>` : ""}
      <div class="dock">
        ${question.math ? `<button class="btn btn-quiet" data-act="calc">Calculator</button>` : ""}
        ${quizMode ? `<button class="btn btn-primary" data-act="quiz-next">${session.index + 1 >= session.ids.length ? "Finish quiz" : "Next question"}</button>` : ""}
        ${!quizMode && answered ? `<button class="btn btn-primary" data-act="next-q">${session.index + 1 >= session.ids.length ? "Finish this step" : "Next question"}</button>` : ""}
        <button class="btn btn-quiet" data-act="park">Park and save</button>
      </div>
    </article>`;
  if (!answered) say(question.stem);
}

function explainBlock(question, choice) {
  const correct = choice === question.answer;
  const source = question.source
    ? `<p class="source"><a href="${esc(question.source.url)}" target="_blank" rel="noopener noreferrer">Source: ${esc(question.source.label)}</a></p>`
    : "";
  const steps = question.steps?.length
    ? `<ol class="steps">${question.steps.map((step) => `<li>${esc(step)}</li>`).join("")}</ol>`
    : "";
  return `<section class="explain ${correct ? "" : "miss"}">
    <h3>${correct ? "That holds up." : "Useful miss."}</h3>
    <p>${correct ? "Nice. The rule is worth keeping." : "Missing it is how this sticks. The rule:"}</p>
    <p>${esc(question.explanation)}</p>
    ${steps}
    ${source}
  </section>`;
}

function readinessCard() {
  const rows = portionReadiness(state);
  return `
    <section class="card">
      <h2>Progress</h2>
      <p class="lede">The salesperson exam is two sittings. The ${EXAM_SHAPE.bulletin} lists ${EXAM_SHAPE.nationalCount} general questions in ${EXAM_SHAPE.nationalMinutes} minutes and ${EXAM_SHAPE.stateCount} Connecticut questions in ${EXAM_SHAPE.stateMinutes} minutes. Each portion needs ${EXAM_SHAPE.passingPercent}%.</p>
      <div class="meters">
        ${rows.map((row) => `
          <div class="supply">
            <strong>${esc(row.label)}</strong>
            <span class="muted">${row.correct}/${row.seen || 0} · ${row.percent}% · ${esc(row.status)}</span>
            <div class="bar" aria-hidden="true"><span style="width:${row.seen ? row.percent : 0}%"></span></div>
            <span class="muted">Bulletin: ${row.count} questions, ${row.minutes} minutes. ${row.status === "Early" ? "Ten answers before this reads as a pace." : row.status === "On pace" ? "Recent answers are at or above 70%." : row.status === "Below the line" ? "Recent answers are under 70%." : "No answers in this portion yet."}</span>
          </div>`).join("")}
      </div>
    </section>`;
}

function viewMap() {
  const road = openRoad();
  const mathCount = bank.questions.filter((q) => q.math && chapterList().includes(q.chapter)).length;
  main.innerHTML = `
    ${readinessCard()}
    <section class="card">
      <h2>The road</h2>
      <p class="lede">Towns with questions in the chapters you've completed. The suggested stop is marked.</p>
      <div class="roadline stack">
        ${road.map((topic, index) => {
          const pct = masteryPercent(state, topic.id);
          const row = state.topics[topic.id] || { seen: 0, correct: 0 };
          const here = index === ((state.routeIndex || 0) % road.length);
          return `<button class="btn town" data-topic="${esc(topic.id)}">
            <span class="dot ${here ? "on" : ""}" aria-hidden="true"></span>
            <span>
              <strong>${esc(topic.town)}</strong> · ${esc(topic.name)}
              <span class="muted" style="display:block">${row.correct}/${row.seen} correct · ${pct}% on answered items</span>
              <span class="meter" aria-hidden="true"><span style="width:${pct}%"></span></span>
            </span>
          </button>`;
        }).join("")}
        <button class="btn town" data-act="math-tab" ${mathCount ? "" : "disabled"}>
          <span class="dot" aria-hidden="true"></span>
          <span><strong>Waterbury</strong> · Math Pass<span class="muted" style="display:block">${mathCount ? `${mathCount} drills in your completed chapters.` : "No math drills in the chapters you've completed."}</span></span>
        </button>
      </div>
      <div class="stack" style="margin-top:12px">
        <button class="btn btn-pine" data-act="study-list">Study a chapter</button>
      </div>
    </section>`;
}

function viewMathHome() {
  const mathCount = bank.questions.filter((q) => q.math && chapterList().includes(q.chapter)).length;
  main.innerHTML = `
    <section class="card">
      <p class="kicker">Waterbury · Math Pass</p>
      <h2>Numbers, then the reason</h2>
      <p class="lede">${mathCount} drills from chapters you've completed. Commission, prorations, conveyance tax, loans, area, and value show up when that chapter is checked. Every one shows the steps after you answer.</p>
      <div class="stack">
        <button class="btn btn-primary" data-act="math-start" ${mathCount ? "" : "disabled"}>Work three math items</button>
        <button class="btn btn-quiet" data-act="calc">Open the calculator</button>
      </div>
      <p class="muted">Day-count and who owns closing day are written into each proration, so you are practicing a stated method. Conveyance items use Conn. Gen. Stat. § 12-494 and say when the town has not added an extra local tax.</p>
    </section>`;
}

function mockDraw(mode) {
  const chapters = state.mockAllChapters ? null : chapterList();
  return sampleExam(bank.questions, bank.topics, mode, () => 0.5, chapters);
}

function viewExamHome() {
  const paused = state.mock && !state.mock.submitted;
  const all = Boolean(state.mockAllChapters);
  const national = mockDraw("national");
  const stateDraw = mockDraw("state");
  const both = mockDraw("both");
  const scopeLine = all
    ? "Every chapter is included, including chapters you have not completed. Counts and timing match the candidate bulletin."
    : "Completed chapters only. Chapters you have not checked are left out, so the set can be shorter than the bulletin.";
  main.innerHTML = `
    <section class="card">
      <h2>Mock exam</h2>
      <p class="lede">The ${esc(EXAM_SHAPE.bulletin)} lists two salesperson portions: general principles, ${EXAM_SHAPE.nationalCount} questions and ${EXAM_SHAPE.nationalMinutes} minutes; Connecticut, ${EXAM_SHAPE.stateCount} questions and ${EXAM_SHAPE.stateMinutes} minutes. A full run is ${EXAM_SHAPE.nationalCount + EXAM_SHAPE.stateCount} questions and ${EXAM_SHAPE.bothMinutes} minutes. The passing score is ${EXAM_SHAPE.passingPercent}% on each portion, and both have to pass.</p>
      <p>The clock pauses when you leave this page or lock the phone. On the real exam day, it will not.</p>
      <button class="btn btn-pine" data-act="mock-scope" aria-pressed="${all ? "true" : "false"}">${all ? "Every chapter" : "Completed chapters only"}</button>
      <p>${scopeLine}</p>
      <p class="muted">General ${national.ids.length} items, ${national.minutes} min. Connecticut ${stateDraw.ids.length} items, ${stateDraw.minutes} min. Both ${both.ids.length} items, ${both.minutes} min.</p>
      <div class="stack">
        ${paused ? `<button class="btn btn-primary" data-act="resume-mock">Resume saved mock (${state.mock.ids.length} items)</button>` : ""}
        <button class="btn btn-pine" data-mode="national" ${national.ids.length ? "" : "disabled"}>General portion</button>
        <button class="btn btn-pine" data-mode="state" ${stateDraw.ids.length ? "" : "disabled"}>Connecticut portion</button>
        <button class="btn btn-primary" data-mode="both" ${both.ids.length ? "" : "disabled"}>Both portions</button>
      </div>
      <p class="muted">You can flag items and change answers until you submit or time runs out. Feedback waits until the end, like the real sitting. This is practice, not a PSI exam.</p>
    </section>`;
}

function viewMock() {
  const mock = state.mock;
  if (!mock) {
    go("exam");
    return;
  }
  if (mock.submitted) {
    viewMockResult();
    return;
  }
  const left = mockLeft();
  if (left <= 0) {
    finishMock();
    return;
  }
  const question = byId[mock.ids[mock.index]];
  const topic = topicById(question.topic);
  const chosen = mock.answers[question.id];
  main.innerHTML = `
    <article class="card">
      <p class="kicker">${question.ctLaw ? `<span class="badge-ct">CT Law</span>` : ""}${esc(topic.name)}${question.chapter ? ` · ${esc(chapterTitle(question.chapter))}` : ""} · ${mock.index + 1} of ${mock.ids.length}${mock.everyChapter ? " · every chapter" : " · completed chapters"}</p>
      <p class="timer ${left < 5 * 60 * 1000 ? "low" : ""}" style="color:${left < 5 * 60 * 1000 ? "var(--bad)" : "var(--pine)"}" aria-live="off">Time left ${formatClock(left)}</p>
      <h2 class="stem" id="stem">${esc(displayStem(question, themeId(state)))}</h2>
      <div class="stack" role="group" aria-labelledby="stem">
        ${question.choices.map((choice, index) => `
          <button class="choice ${chosen === index ? "picked" : ""}" data-mock-choice="${index}" aria-pressed="${chosen === index ? "true" : "false"}">
            <span class="key" aria-hidden="true">${index + 1}</span><span>${esc(choice)}</span>
          </button>`).join("")}
      </div>
      <div class="row" style="margin-top:12px">
        <button class="btn btn-quiet" data-act="mock-prev" ${mock.index === 0 ? "disabled" : ""}>Back</button>
        <button class="btn btn-quiet" data-act="mock-flag">${mock.flagged[question.id] ? "Unflag" : "Flag"}</button>
        <button class="btn btn-quiet" data-act="calc">Calc</button>
      </div>
      <div class="dock">
        ${mock.index + 1 < mock.ids.length
          ? `<button class="btn btn-primary" data-act="mock-next">Next</button>`
          : `<button class="btn btn-primary" data-act="mock-submit">Submit exam</button>`}
        <button class="btn btn-quiet" data-act="mock-grid">Question list</button>
        <button class="btn btn-quiet" data-act="park-mock">Pause and save</button>
      </div>
    </article>`;
  timerHandle = window.setInterval(() => {
    const remain = mockLeft();
    const node = main.querySelector(".timer");
    if (node) node.textContent = `Time left ${formatClock(remain)}`;
    if (remain <= 0) finishMock();
  }, 500);
}

function viewMockResult() {
  const mock = state.mock;
  const result = mock.result;
  const portions = result.portions || [];
  const portionLines = portions.map((row) => (
    `<p><strong>${esc(row.label)}</strong> · ${row.correct}/${row.total} · ${row.percent}% · ${row.passed ? "70% or better" : "under 70%"}</p>`
  )).join("");
  const lines = bank.topics.map((topic) => {
    const row = result.byTopic[topic.id];
    if (!row) return "";
    return `<p><strong>${esc(topic.name)}</strong> · ${row.correct}/${row.total}</p>`;
  }).join("");
  const both = portions.length > 1;
  const headline = both
    ? (result.passed ? "Both portions reached 70%." : "Both portions have to reach 70%.")
    : (result.passed ? "You cleared 70%." : "Not 70% this time.");
  main.innerHTML = `
    <section class="card">
      <h2>${headline}</h2>
      <p class="lede">${both ? "Each portion is scored on its own." : `${result.correct} of ${result.total} · ${result.percent}%.`} The salesperson passing score in the PSI bulletin is ${EXAM_SHAPE.passingPercent}%. ${mock.everyChapter ? "This sitting included every chapter." : "This sitting used only chapters you've completed."} ${result.passed ? "Hold onto what worked." : "The misses are already in your review pile."}</p>
      ${portionLines}
      ${lines}
      <div class="stack">
        <button class="btn btn-primary" data-act="review-tab">Review the misses</button>
        <button class="btn btn-quiet" data-act="mock-clear">Leave this result</button>
      </div>
    </section>`;
}

function loopRow(chapter) {
  return state.chapterLoops?.[chapter] || {};
}

function viewLoop() {
  const loop = state.loop;
  if (loop?.phase === "between") {
    viewLoopBetween();
    return;
  }
  if (loop?.phase === "result") {
    viewLoopResult();
    return;
  }
  const chapters = chapterList();
  const rows = (course?.chapters || []).filter((row) => chapters.includes(row.n));
  main.innerHTML = `
    <section class="card">
      <h2>Chapter study</h2>
      <p class="lede">Each chapter follows the class order: principles and practices, then the Connecticut law for that chapter, then a short quiz. The quiz holds the answers until the end.</p>
      ${rows.length ? "" : `<p>Check at least one chapter you have finished. The loop uses those chapters.</p>`}
      <div class="stack">
        ${rows.map((row) => {
          const done = loopRow(row.n);
          const bits = [
            done.principles ? "Principles done" : "Principles",
            done.ct ? "Connecticut law done" : "Connecticut law",
            done.quizPercent !== undefined ? `Quiz ${done.quizPercent}%` : "Quiz",
          ];
          return `<button class="btn btn-quiet" data-act="study-chapter" data-chapter="${row.n}">
            <strong>Ch ${row.n}</strong> ${esc(row.name)}
            <span class="muted" style="display:block">${esc(bits.join(" · "))}</span>
          </button>`;
        }).join("")}
      </div>
    </section>`;
}

function viewLoopBetween() {
  const loop = state.loop;
  const title = chapterTitle(loop.chapter);
  const next = loop.next;
  let heading = "Connecticut law is next";
  let body = "Same chapter, different rules. These items are Connecticut statutes and regulations. The general principles you just reviewed stay as they were.";
  if (next === "quiz" && !loop.ct.length) {
    heading = "No Connecticut items in this chapter";
    body = "The bank has no Connecticut-law questions tagged to this chapter. The chapter quiz is next, and it uses the principles items.";
  } else if (next === "quiz") {
    heading = "Chapter quiz";
    body = "A short mix from this chapter. Pick an answer on each item. The explanation waits until you finish.";
  }
  main.innerHTML = `
    <section class="card">
      <p class="kicker">${esc(title)}</p>
      <h2>${heading}</h2>
      <p class="lede">${body}</p>
      <div class="stack">
        <button class="btn btn-primary" data-act="loop-continue">${next === "ct" ? "Start Connecticut law" : "Start the quiz"}</button>
        <button class="btn btn-quiet" data-act="study-list">Back to chapters</button>
      </div>
    </section>`;
}

function viewLoopResult() {
  const loop = state.loop;
  const quiz = loop.quiz || { correct: 0, total: 0, percent: 0 };
  const misses = (loop.quizIds || []).map((id) => {
    const question = byId[id];
    const choice = quiz.answers?.[id];
    if (!question || choice === question.answer) return "";
    return `<p><strong>${esc(question.stem)}</strong> ${esc(question.explanation)}</p>`;
  }).join("");
  main.innerHTML = `
    <section class="card">
      <p class="kicker">${esc(chapterTitle(loop.chapter))}</p>
      <h2>${quiz.percent >= EXAM_SHAPE.passingPercent ? "Chapter quiz is at 70% or better." : "Chapter quiz is under 70%."}</h2>
      <p class="lede">${quiz.correct} of ${quiz.total} · ${quiz.percent}%. This is a chapter check, not the PSI exam. The bulletin still asks for ${EXAM_SHAPE.passingPercent}% on each full portion.</p>
      ${misses}
      <div class="stack">
        <button class="btn btn-primary" data-act="study-chapter" data-chapter="${loop.chapter}">Run this chapter again</button>
        <button class="btn btn-quiet" data-act="study-list">Back to chapters</button>
      </div>
    </section>`;
}

function startChapterStudy(chapter) {
  const plan = chapterStudyPlan(bank.questions, chapter, Math.random);
  if (!plan.principles.length && !plan.ct.length && !plan.quiz.length) {
    say("That chapter has no questions yet.");
    return;
  }
  state.loop = {
    chapter,
    principles: plan.principles,
    ct: plan.ct,
    quizIds: plan.quiz,
    phase: "run",
  };
  if (plan.principles.length) startSession("chapter-principles", plan.principles, null);
  else if (plan.ct.length) startSession("chapter-ct", plan.ct, null);
  else beginChapterQuiz();
}

function beginChapterQuiz() {
  const loop = state.loop;
  if (!loop?.quizIds?.length) {
    loop.phase = "result";
    loop.quiz = { correct: 0, total: 0, percent: 0, answers: {} };
    state.loop = loop;
    go("loop");
    return;
  }
  startSession("chapter-quiz", loop.quizIds, null);
  state.session.answers = {};
  save();
}

function finishLoopStep(session) {
  const loop = state.loop || { chapter: null, ct: [], quizIds: [] };
  if (!state.chapterLoops) state.chapterLoops = {};
  const row = { ...(state.chapterLoops[loop.chapter] || {}) };
  if (session.kind === "chapter-principles") row.principles = true;
  if (session.kind === "chapter-ct") row.ct = true;
  state.chapterLoops[loop.chapter] = row;
  state.session = null;
  if (session.kind === "chapter-principles") {
    loop.phase = "between";
    loop.next = loop.ct?.length ? "ct" : "quiz";
  } else {
    loop.phase = "between";
    loop.next = "quiz";
  }
  state.loop = loop;
  save();
  go("loop");
}

function finishChapterQuiz(session) {
  const answers = session.answers || {};
  let correct = 0;
  session.ids.forEach((id) => {
    const question = byId[id];
    const choice = answers[id];
    const outcome = answerQuestion(state, question, choice ?? -1);
    state = outcome.state;
    if (outcome.correct) correct += 1;
  });
  const total = session.ids.length;
  const percent = total ? Math.round((correct / total) * 100) : 0;
  if (!state.chapterLoops) state.chapterLoops = {};
  state.chapterLoops[state.loop.chapter] = {
    ...(state.chapterLoops[state.loop.chapter] || {}),
    quizPercent: percent,
  };
  state.loop.quiz = { correct, total, percent, answers };
  state.loop.phase = "result";
  state.session = null;
  save();
  go("loop");
}

function continueLoop() {
  const loop = state.loop;
  if (!loop) {
    go("loop");
    return;
  }
  if (loop.next === "ct" && loop.ct?.length) startSession("chapter-ct", loop.ct, null);
  else beginChapterQuiz();
}

function dueInChapters() {
  const allowed = new Set(chapterList());
  return dueReviews(state).filter((id) => allowed.has(byId[id]?.chapter));
}

function viewReviewHome() {
  const due = dueInChapters();
  const waiting = Object.values(state.review).filter((row) => row.due > Date.now()).length;
  main.innerHTML = `
    <section class="card">
      <h2>Another look</h2>
      <p class="lede">${due.length ? `${due.length} question${due.length === 1 ? "" : "s"} due now.` : "Nothing is due right now."} ${waiting} more ${waiting === 1 ? "is" : "are"} scheduled later. A correct answer waits longer next time. A miss comes back immediately.</p>
      <div class="stack">
        <button class="btn btn-primary" data-act="review-start" ${due.length ? "" : "disabled"}>Review what is due</button>
      </div>
    </section>`;
}

function viewSettings() {
  const checked = new Set(chapterList());
  const chapters = course?.chapters || [];
  main.innerHTML = `
    <section class="card">
      <h2>Chapters I've completed</h2>
      <p>Classes rotate, so check every chapter you have already finished. The road and the daily crossword use only those chapters.</p>
      <div class="stack chapter-list">
        ${chapters.map((row) => `
          <button type="button" class="checkline" data-act="toggle-chapter" data-chapter="${row.n}" aria-pressed="${checked.has(row.n) ? "true" : "false"}">
            <span class="box" aria-hidden="true"></span>
            <span><strong>Ch ${row.n}</strong> ${esc(row.name)}</span>
          </button>`).join("")}
      </div>
      <div class="stack" style="margin-top:12px">
        <button class="btn btn-quiet" data-act="reset-chapters">Use the starting chapters</button>
      </div>
    </section>
    <section class="card">
      <h2>Your exam date</h2>
      <p>Type the date you are aiming for. It is only a countdown. Change it whenever the plan changes.</p>
      <label class="field" for="exam-date">Exam date</label>
      <input id="exam-date" type="date" value="${esc(state.examDate || "")}">
      <div class="stack" style="margin-top:12px">
        <button class="btn btn-primary" data-act="save-date">Save date</button>
        <button class="btn btn-quiet" data-act="clear-date">Clear date</button>
      </div>
    </section>
    <section class="card">
      <h2>Theme</h2>
      <p>Outdoors, Adventure, and History add a scene around a question. Classic leaves the question as written. The scene never changes the facts, the choices, or the rule.</p>
      <div class="stack">
        ${THEMES.map((row) => `
          <button class="btn ${themeId(state) === row.id ? "btn-pine" : "btn-quiet"}" data-act="theme" data-theme="${row.id}" aria-pressed="${themeId(state) === row.id ? "true" : "false"}">${esc(row.name)}</button>`).join("")}
      </div>
      <p class="muted">${esc(THEMES.find((row) => row.id === themeId(state))?.note || "")}</p>
    </section>
    <section class="card">
      <h2>Sound</h2>
      <p>Optional, and off unless you turn it on. A short tone marks right and wrong answers.</p>
      <button class="btn btn-pine" data-act="toggle-sound" aria-pressed="${state.settings.sound ? "true" : "false"}">${state.settings.sound ? "Sound is on" : "Sound is off"}</button>
    </section>
    <section class="card">
      <h2>Reset this phone</h2>
      <p>Clears XP, supplies, streaks, review, and any paused exam stored in this browser.</p>
      <button class="btn btn-quiet" data-act="reset">Reset progress</button>
    </section>
    <button class="btn btn-quiet" data-act="about">Sources and disclaimer</button>`;
}

function viewAbout() {
  main.innerHTML = `
    <section class="card">
      <h2>What this is</h2>
      <p>CT License Trail is an unofficial study aid for an adult preparing for the Connecticut real estate salesperson exam. The road, town names, and drawings are original. It is not a PSI product and it is not affiliated with the Department of Consumer Protection.</p>
      <p>Questions were written for this project from public official sources. They are not copied from a textbook or a commercial prep course. If a Connecticut figure could not be checked, it was left out.</p>
      <p>The daily crossword is original too: new grid each calendar day, written for this game, with no newspaper puzzle or name behind it. A Connecticut fact in a clue uses the same public sources as the questions.</p>
      <h2>Sources</h2>
      <ul>
        <li><a href="https://test-takers.psiexams.com/ctre">PSI Connecticut real estate candidate bulletin</a> (content outline and exam timing, updated November 13, 2025)</li>
        <li><a href="https://portal.ct.gov/dcp/license-services-division/all-license-applications/real-estate-salesperson---initialexam">DCP salesperson initial exam page</a></li>
        <li><a href="https://portal.ct.gov/dcp/continuing-education/real-estate-salesperson---continuing-education">DCP salesperson continuing education</a></li>
        <li><a href="https://www.cga.ct.gov/current/pub/chap_392.htm">Connecticut General Statutes, Chapter 392</a></li>
        <li><a href="https://eregulations.ct.gov/eRegsPortal/Browse/RCSA/Title_20Subtitle_20-328Section_20-328-1a.html">Regulations of Connecticut State Agencies, real estate licensee conduct</a></li>
        <li><a href="https://www.cga.ct.gov/current/pub/chap_223.htm">Chapter 223, real estate conveyance tax</a></li>
        <li><a href="https://www.cga.ct.gov/current/pub/chap_814c.htm">Chapter 814c, discriminatory housing practices</a></li>
        <li><a href="https://www.cga.ct.gov/current/pub/chap_831.htm">Chapter 831, security deposits</a></li>
        <li><a href="https://www.cga.ct.gov/current/pub/chap_822.htm#sec_47-37">Section 47-37, prescriptive easements</a> and <a href="https://www.cga.ct.gov/current/pub/chap_926.htm#sec_52-575">section 52-575</a></li>
      </ul>
      <p class="fine">Federal items in the national portion cite the Fair Housing Act, RESPA, ECOA, the lead-paint disclosure statute, Regulation Z, the Sherman Act, the ADA, or the FTC Telemarketing Sales Rule when a specific rule is used.</p>
      <button class="btn btn-primary" data-act="home">Back to the road</button>
    </section>`;
}

function viewGrid() {
  window.clearInterval(timerHandle);
  const mock = state.mock;
  main.innerHTML = `
    <section class="card">
      <h2>All items</h2>
      <p class="muted">Amber ring means flagged. Green means answered.</p>
      <div class="grid">
        ${mock.ids.map((id, index) => {
          const cls = [
            mock.answers[id] !== undefined ? "answered" : "",
            mock.flagged[id] ? "flagged" : "",
          ].filter(Boolean).join(" ");
          return `<button class="${cls}" data-jump="${index}" aria-label="Question ${index + 1}${mock.flagged[id] ? ", flagged" : ""}">${index + 1}</button>`;
        }).join("")}
      </div>
      <div class="stack" style="margin-top:12px">
        <button class="btn btn-primary" data-act="mock-submit">Submit exam</button>
        <button class="btn btn-quiet" data-act="mock-back-q">Return to the question</button>
      </div>
    </section>`;
}

function viewCalc() {
  window.clearInterval(timerHandle);
  main.innerHTML = `
    <section class="card">
      <h2>Calculator</h2>
      <div class="calc" id="calc">
        <div class="readout" aria-live="polite">${esc(calcValue)}</div>
        ${["7", "8", "9", "÷", "4", "5", "6", "×", "1", "2", "3", "−", "0", ".", "C", "+"].map((key) =>
          `<button type="button" data-key="${esc(key)}">${esc(key)}</button>`).join("")}
        <button type="button" data-key="=" style="grid-column: span 4">Equals</button>
      </div>
      <button class="btn btn-quiet" style="margin-top:12px" data-act="calc-close">Close</button>
    </section>`;
}

let calcReturn = "home";

function crosswordBook() {
  if (!state.crossword) state.crossword = createState().crossword;
  return state.crossword;
}

function chapterPhrase(numbers) {
  const list = [...(numbers || [])].sort((a, b) => a - b);
  if (!list.length) return "No chapters checked";
  if (list.length === 1) return chapterTitle(list[0]);
  return `Chapters ${list.join(", ")}`;
}

function dailyHomeLabel() {
  if (state.crossword?.solved?.[todayKey()]) return "Today's crossword · solved";
  if (!chapterList().length) return "Today's crossword · check a chapter";
  return "Today's crossword · completed chapters";
}

function todayPuzzle() {
  if (!crosswords) return null;
  return puzzleForDate(crosswords, new Date(), chapterList());
}

function slotKey(picked) {
  return `${picked.dateKey}:${picked.puzzle.id}`;
}

function isBlack(puzzle, r, c) {
  return puzzle.grid[r][c] === "#";
}

function cellsOf(entry, dir) {
  const cells = [];
  for (let i = 0; i < entry.answer.length; i += 1) {
    cells.push(dir === "across" ? [entry.row, entry.col + i] : [entry.row + i, entry.col]);
  }
  return cells;
}

function entryAt(puzzle, r, c, dir) {
  const list = dir === "across" ? puzzle.across : puzzle.down;
  return list.find((entry) => cellsOf(entry, dir).some(([rr, cc]) => rr === r && cc === c)) || null;
}

function firstWhite(puzzle) {
  for (let r = 0; r < puzzle.size; r += 1) {
    for (let c = 0; c < puzzle.size; c += 1) {
      if (!isBlack(puzzle, r, c)) return { r, c };
    }
  }
  return { r: 0, c: 0 };
}

function ensureProgress(puzzle, key, calendarDay) {
  const book = crosswordBook();
  let prog = book.progress[key];
  const size = puzzle.size * puzzle.size;
  if (!prog || prog.id !== puzzle.id || !Array.isArray(prog.letters) || prog.letters.length !== size) {
    const start = firstWhite(puzzle);
    prog = {
      id: puzzle.id,
      letters: Array(size).fill(""),
      bad: Array(size).fill(false),
      revealed: Array(size).fill(false),
      revealedAny: false,
      row: start.r,
      col: start.c,
      dir: "across",
      seconds: 0,
      running: false,
      lastTick: Date.now(),
      done: false,
    };
    book.progress[key] = prog;
  }
  const solvedToday = book.solved[calendarDay];
  if (solvedToday && solvedToday.id === puzzle.id && !prog.done) {
    prog.done = true;
    prog.running = false;
    for (let r = 0; r < puzzle.size; r += 1) {
      for (let c = 0; c < puzzle.size; c += 1) {
        if (!isBlack(puzzle, r, c)) prog.letters[r * puzzle.size + c] = puzzle.grid[r][c];
      }
    }
  }
  if (!entryAt(puzzle, prog.row, prog.col, prog.dir)) {
    const other = prog.dir === "across" ? "down" : "across";
    if (entryAt(puzzle, prog.row, prog.col, other)) prog.dir = other;
  }
  return prog;
}

function dailyElapsed(prog, now = Date.now()) {
  let seconds = prog.seconds || 0;
  if (prog.running) seconds += Math.max(0, Math.floor((now - prog.lastTick) / 1000));
  return seconds;
}

function formatSeconds(total) {
  const safe = Math.max(0, total || 0);
  const m = Math.floor(safe / 60);
  const s = safe % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

function rollDaily(now = Date.now()) {
  if (!crosswords || !course) return;
  const picked = todayPuzzle();
  if (!picked) return;
  const prog = state.crossword?.progress?.[slotKey(picked)];
  if (!prog?.running) return;
  const add = Math.max(0, Math.floor((now - prog.lastTick) / 1000));
  if (add > 0) {
    prog.seconds += add;
    prog.lastTick = now;
  }
}

function freezeDaily(now = Date.now()) {
  if (!crosswords || !course) return;
  const picked = todayPuzzle();
  if (!picked) return;
  const prog = state.crossword?.progress?.[slotKey(picked)];
  if (!prog?.running) return;
  rollDaily(now);
  prog.running = false;
  prog.lastTick = now;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  paintChrome();
}

function resumeDaily(now = Date.now()) {
  if (!crosswords) return;
  const picked = todayPuzzle();
  if (!picked) return;
  const prog = ensureProgress(picked.puzzle, slotKey(picked), picked.dateKey);
  if (prog.done) return;
  prog.running = true;
  prog.lastTick = now;
}

function paintDaily() {
  const picked = todayPuzzle();
  if (!picked) return;
  const puzzle = picked.puzzle;
  const prog = ensureProgress(puzzle, slotKey(picked), picked.dateKey);
  const entry = entryAt(puzzle, prog.row, prog.col, prog.dir);
  const wordCells = new Set((entry ? cellsOf(entry, prog.dir) : []).map(([r, c]) => `${r},${c}`));
  main.querySelectorAll(".xw-cell[data-r]").forEach((cell) => {
    const r = Number(cell.dataset.r);
    const c = Number(cell.dataset.c);
    const index = r * puzzle.size + c;
    const face = cell.querySelector(".xw-face");
    if (face) face.textContent = prog.letters[index] || "";
    cell.classList.toggle("xw-on", wordCells.has(`${r},${c}`));
    cell.classList.toggle("xw-cur", r === prog.row && c === prog.col);
    cell.classList.toggle("xw-bad", Boolean(prog.bad[index]));
    cell.classList.toggle("xw-revealed", Boolean(prog.revealed[index]));
    const num = puzzle.numbers[r][c] ? ` ${puzzle.numbers[r][c]}` : "";
    cell.setAttribute("aria-label", `Row ${r + 1}, column ${c + 1}${num}, ${prog.letters[index] || "empty"}`);
    if (r === prog.row && c === prog.col) cell.setAttribute("aria-selected", "true");
    else cell.removeAttribute("aria-selected");
  });
  const clue = main.querySelector(".xw-clue");
  if (clue && entry) {
    const source = entry.source
      ? ` <a href="${esc(entry.source.url)}" target="_blank" rel="noopener noreferrer">${esc(entry.source.label)}</a>`
      : "";
    clue.innerHTML = `<strong>${entry.n} ${prog.dir === "across" ? "Across" : "Down"}.</strong> ${esc(entry.clue)}${source}`;
  }
  const time = main.querySelector(".xw-time");
  if (time) time.textContent = formatSeconds(dailyElapsed(prog));
  const banner = main.querySelector(".xw-banner");
  if (banner) {
    const solved = state.crossword.solved[picked.dateKey];
    banner.hidden = !prog.done;
    if (prog.done && solved && solved.id === puzzle.id) {
      banner.textContent = solved.clean
        ? `Solved clean. +${solved.xp} XP, and a supply wherever one fit.`
        : `Solved. +${solved.xp} XP. A reveal skips the supply bonus.`;
    } else if (prog.done && solved) {
      banner.textContent = "Solved. Today's crossword XP was already counted.";
    } else if (prog.done) {
      banner.textContent = "Solved.";
    }
  }
  const streak = main.querySelector(".xw-streak");
  if (streak) streak.textContent = `crossword streak ${state.crossword.streak?.count || 0}`;
}

function viewDaily() {
  if (!crosswords) {
    main.innerHTML = `<section class="card"><h2>The crossword file did not load.</h2><p>Check that data/crosswords.json is next to this page, then reload.</p></section>`;
    return;
  }
  const picked = todayPuzzle();
  if (!picked) {
    const checked = chapterList();
    const detail = checked.length
      ? "Nothing in the puzzle library stays inside just these chapters. Add another completed chapter, or use the starting set."
      : "Check the chapters you have completed. The grid is built only from those chapters.";
    main.innerHTML = `<section class="card"><h2>No crossword for these chapters yet</h2><p>${detail}</p><button class="btn btn-primary" data-act="settings">Choose chapters</button></section>`;
    return;
  }
  const puzzle = picked.puzzle;
  const prog = ensureProgress(puzzle, slotKey(picked), picked.dateKey);
  if (!prog.done) resumeDaily();
  const n = puzzle.size;
  const cells = [];
  for (let r = 0; r < n; r += 1) {
    for (let c = 0; c < n; c += 1) {
      if (isBlack(puzzle, r, c)) {
        cells.push(`<div class="xw-cell xw-black" role="presentation"></div>`);
      } else {
        const num = puzzle.numbers[r][c];
        cells.push(`<button type="button" class="xw-cell" data-r="${r}" data-c="${c}" data-cell="${r},${c}">${num ? `<span class="xw-num">${num}</span>` : ""}<span class="xw-face"></span></button>`);
      }
    }
  }
  const list = (dir) => (dir === "across" ? puzzle.across : puzzle.down)
    .map((entry) => `<li><strong>${entry.n}.</strong> ${esc(entry.clue)}</li>`)
    .join("");
  const keyRows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"];
  main.innerHTML = `
    <div class="xw">
      <div class="xw-scroll">
        <section class="card xw-head">
          <p class="kicker">${esc(picked.weekday)} · ${esc(picked.dateKey)} · ${esc(chapterPhrase(picked.chapters))}</p>
          <h2>${esc(puzzle.title)}</h2>
          <p class="lede">${esc(puzzle.blurb)} Only chapters you've completed.</p>
          <p class="xw-meta"><span class="xw-time" aria-label="Elapsed time">0:00</span> · <span class="xw-streak">crossword streak 0</span></p>
          <p class="xw-banner note" hidden></p>
        </section>
        <div class="xw-grid" role="grid" aria-label="${esc(puzzle.title)}" style="grid-template-columns: repeat(${n}, minmax(0, 1fr))">${cells.join("")}</div>
        <details class="card xw-all">
          <summary>All clues</summary>
          <h3>Across</h3>
          <ol class="xw-list">${list("across")}</ol>
          <h3>Down</h3>
          <ol class="xw-list">${list("down")}</ol>
        </details>
      </div>
      <div class="xw-dock">
        <p class="xw-clue"></p>
        <div class="xw-board" aria-label="Keyboard">
          ${keyRows.map((row) => `<div class="xw-keyrow">${[...row].map((ch) => `<button type="button" data-xw="${ch}" aria-label="${ch}">${ch}</button>`).join("")}</div>`).join("")}
          <div class="xw-keyrow xw-keyrow-wide">
            <button type="button" data-xw="dir" aria-label="Toggle direction">Direction</button>
            <button type="button" data-xw="bksp" aria-label="Backspace">Delete</button>
          </div>
        </div>
        <div class="xw-tools">
          <button type="button" data-act="xw-check-letter">Check letter</button>
          <button type="button" data-act="xw-check-word">Check word</button>
          <button type="button" data-act="xw-check-puzzle">Check puzzle</button>
          <button type="button" data-act="xw-reveal-letter">Reveal letter</button>
          <button type="button" data-act="xw-reveal-word">Reveal word</button>
          <button type="button" data-act="xw-reveal-puzzle">Reveal puzzle</button>
        </div>
      </div>
    </div>`;
  paintDaily();
  window.clearInterval(timerHandle);
  timerHandle = window.setInterval(() => {
    if (screen !== "daily") return;
    const current = state.crossword?.progress?.[slotKey(picked)];
    if (!current?.running) return;
    rollDaily();
    const time = main.querySelector(".xw-time");
    if (time) time.textContent = formatSeconds(current.seconds || 0);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }, 1000);
}

function moveInEntry(puzzle, prog, delta) {
  const entry = entryAt(puzzle, prog.row, prog.col, prog.dir);
  if (!entry) return;
  const cells = cellsOf(entry, prog.dir);
  const at = cells.findIndex(([r, c]) => r === prog.row && c === prog.col);
  const next = cells[at + delta];
  if (!next) return;
  prog.row = next[0];
  prog.col = next[1];
}

function markChecked(puzzle, prog, cells) {
  for (const [r, c] of cells) {
    const index = r * puzzle.size + c;
    const have = prog.letters[index];
    prog.bad[index] = Boolean(have) && have !== puzzle.grid[r][c];
  }
}

function revealCells(puzzle, prog, cells) {
  for (const [r, c] of cells) {
    const index = r * puzzle.size + c;
    const need = puzzle.grid[r][c];
    if (prog.letters[index] !== need) prog.revealedAny = true;
    prog.letters[index] = need;
    prog.revealed[index] = true;
    prog.bad[index] = false;
  }
}

function allWhiteCells(puzzle) {
  const cells = [];
  for (let r = 0; r < puzzle.size; r += 1) {
    for (let c = 0; c < puzzle.size; c += 1) {
      if (!isBlack(puzzle, r, c)) cells.push([r, c]);
    }
  }
  return cells;
}

function gridComplete(puzzle, prog) {
  for (let r = 0; r < puzzle.size; r += 1) {
    for (let c = 0; c < puzzle.size; c += 1) {
      if (isBlack(puzzle, r, c)) continue;
      if (prog.letters[r * puzzle.size + c] !== puzzle.grid[r][c]) return false;
    }
  }
  return true;
}

function finishIfSolved(puzzle, prog, day) {
  if (prog.done || !gridComplete(puzzle, prog)) return;
  rollDaily();
  prog.done = true;
  prog.running = false;
  const result = awardCrossword(state, day, !prog.revealedAny, puzzle.id);
  state = result.state;
  if (result.awarded) {
    const supply = result.supplyDelta ? ` Supplies +${result.supplyDelta}.` : "";
    say(result.clean
      ? `Crossword solved. +${result.xpGain} XP.${supply}`
      : `Crossword solved with reveals. +${result.xpGain} XP.`);
  } else {
    say("Solved. Today's crossword XP was already counted.");
  }
}

function selectCell(r, c) {
  const picked = todayPuzzle();
  const puzzle = picked.puzzle;
  const prog = ensureProgress(puzzle, slotKey(picked), picked.dateKey);
  if (isBlack(puzzle, r, c)) return;
  if (prog.row === r && prog.col === c) {
    const other = prog.dir === "across" ? "down" : "across";
    if (entryAt(puzzle, r, c, other)) prog.dir = other;
  } else {
    prog.row = r;
    prog.col = c;
    if (!entryAt(puzzle, r, c, prog.dir)) {
      const other = prog.dir === "across" ? "down" : "across";
      if (entryAt(puzzle, r, c, other)) prog.dir = other;
    }
  }
  save();
  paintDaily();
}

function xwType(letter) {
  const picked = todayPuzzle();
  const puzzle = picked.puzzle;
  const prog = ensureProgress(puzzle, slotKey(picked), picked.dateKey);
  if (prog.done) return;
  const index = prog.row * puzzle.size + prog.col;
  prog.letters[index] = letter;
  prog.bad[index] = false;
  if (letter !== puzzle.grid[prog.row][prog.col]) prog.revealed[index] = false;
  moveInEntry(puzzle, prog, 1);
  finishIfSolved(puzzle, prog, picked.dateKey);
  save();
  paintDaily();
}

function xwBackspace() {
  const picked = todayPuzzle();
  const puzzle = picked.puzzle;
  const prog = ensureProgress(puzzle, slotKey(picked), picked.dateKey);
  if (prog.done) return;
  const index = prog.row * puzzle.size + prog.col;
  if (prog.letters[index]) {
    prog.letters[index] = "";
    prog.bad[index] = false;
    prog.revealed[index] = false;
  } else {
    moveInEntry(puzzle, prog, -1);
    const prev = prog.row * puzzle.size + prog.col;
    prog.letters[prev] = "";
    prog.bad[prev] = false;
    prog.revealed[prev] = false;
  }
  save();
  paintDaily();
}

function xwToggle() {
  const picked = todayPuzzle();
  const prog = ensureProgress(picked.puzzle, slotKey(picked), picked.dateKey);
  const other = prog.dir === "across" ? "down" : "across";
  if (entryAt(picked.puzzle, prog.row, prog.col, other)) prog.dir = other;
  save();
  paintDaily();
}

function xwTool(kind) {
  const picked = todayPuzzle();
  const puzzle = picked.puzzle;
  const prog = ensureProgress(puzzle, slotKey(picked), picked.dateKey);
  if (prog.done && kind.startsWith("check")) {
    paintDaily();
    return;
  }
  const entry = entryAt(puzzle, prog.row, prog.col, prog.dir);
  const one = [[prog.row, prog.col]];
  const word = entry ? cellsOf(entry, prog.dir) : one;
  if (kind === "check-letter") markChecked(puzzle, prog, one);
  else if (kind === "check-word") markChecked(puzzle, prog, word);
  else if (kind === "check-puzzle") markChecked(puzzle, prog, allWhiteCells(puzzle));
  else if (kind === "reveal-letter") revealCells(puzzle, prog, one);
  else if (kind === "reveal-word") revealCells(puzzle, prog, word);
  else if (kind === "reveal-puzzle") revealCells(puzzle, prog, allWhiteCells(puzzle));
  if (kind.startsWith("reveal")) finishIfSolved(puzzle, prog, picked.dateKey);
  save();
  paintDaily();
}

function xwArrow(key) {
  const picked = todayPuzzle();
  if (!picked) return;
  const puzzle = picked.puzzle;
  const prog = ensureProgress(puzzle, slotKey(picked), picked.dateKey);
  const step = { ArrowLeft: [0, -1], ArrowRight: [0, 1], ArrowUp: [-1, 0], ArrowDown: [1, 0] }[key];
  const nr = prog.row + step[0];
  const nc = prog.col + step[1];
  if (nr < 0 || nc < 0 || nr >= puzzle.size || nc >= puzzle.size || isBlack(puzzle, nr, nc)) return;
  prog.row = nr;
  prog.col = nc;
  prog.dir = key === "ArrowLeft" || key === "ArrowRight" ? "across" : "down";
  save();
  paintDaily();
}

function onClick(event) {
  const button = event.target.closest("button");
  if (!button) return;
  const act = button.dataset.act;
  const tab = button.dataset.tab;
  if (tab) {
    if (screen === "mock") freezeMock();
    if (tab === "home") go("home");
    else if (tab === "math") go("math");
    else if (tab === "exam") go("exam");
    else go(tab);
    return;
  }
  if (button.dataset.choice !== undefined) chooseAnswer(Number(button.dataset.choice));
  if (button.dataset.mockChoice !== undefined) chooseMock(Number(button.dataset.mockChoice));
  if (button.dataset.topic) startJourney(button.dataset.topic);
  if (button.dataset.mode) beginMock(button.dataset.mode);
  if (button.dataset.jump !== undefined) {
    state.mock.index = Number(button.dataset.jump);
    save();
    screen = "mock";
    render();
  }
  if (button.dataset.key) pressCalc(button.dataset.key);
  if (button.dataset.cell) {
    const [r, c] = button.dataset.cell.split(",").map(Number);
    selectCell(r, c);
    return;
  }
  if (button.dataset.xw) {
    if (button.dataset.xw === "bksp") xwBackspace();
    else if (button.dataset.xw === "dir") xwToggle();
    else xwType(button.dataset.xw);
    return;
  }
  if (!act) return;
  if (act === "continue") {
    if (state.session) go("question");
    else startJourney();
  } else if (act === "study-list") {
    state.loop = null;
    go("loop");
  } else if (act === "study-chapter") {
    startChapterStudy(Number(button.dataset.chapter));
  } else if (act === "loop-continue") {
    continueLoop();
  } else if (act === "quiz-next") {
    const session = state.session;
    const id = session?.ids?.[session.index];
    if (!session || session.answers?.[id] === undefined) {
      say("Pick an answer first.");
      return;
    }
    if (session.index + 1 >= session.ids.length) finishChapterQuiz(session);
    else {
      session.index += 1;
      session.choice = session.answers[session.ids[session.index]] ?? null;
      state.session = session;
      save();
      viewQuestion();
    }
  } else if (act === "resume-mock") {
    resumeMock();
    go("mock");
  } else if (act === "settings") go("settings");
  else if (act === "park") go("home");
  else if (act === "next-q") advanceSession();
  else if (act === "calc") {
    calcReturn = screen;
    viewCalc();
  } else if (act === "calc-close") go(calcReturn);
  else if (act === "math-tab" || act === "math-start") {
    if (act === "math-start") {
      const ids = bank.questions.filter((q) => q.math && chapterList().includes(q.chapter)).map((q) => q.id);
      if (!ids.length) {
        say("No math drills in the chapters you've completed.");
        return;
      }
      for (let i = ids.length - 1; i > 0; i -= 1) {
        const j = Math.floor(Math.random() * (i + 1));
        [ids[i], ids[j]] = [ids[j], ids[i]];
      }
      startSession("math", ids.slice(0, 3), "math");
    } else go("math");
  } else if (act === "toggle-chapter") {
    const number = Number(button.dataset.chapter);
    const next = new Set(chapterList());
    if (next.has(number)) next.delete(number);
    else next.add(number);
    state.completedChapters = [...next].sort((a, b) => a - b);
    save();
    viewSettings();
  } else if (act === "reset-chapters") {
    state.completedChapters = null;
    save();
    say("Starting chapters restored.");
    viewSettings();
  } else if (act === "mock-scope") {
    state.mockAllChapters = !state.mockAllChapters;
    save();
    viewExamHome();
  } else if (act === "save-date") {
    const value = document.querySelector("#exam-date").value;
    state.examDate = value || null;
    save();
    say(value ? "Exam date saved." : "Exam date cleared.");
    go("home");
  } else if (act === "clear-date") {
    state.examDate = null;
    save();
    go("settings");
  } else if (act === "theme") {
    const next = THEMES.some((row) => row.id === button.dataset.theme) ? button.dataset.theme : "classic";
    state.settings.theme = next;
    save();
    viewSettings();
  } else if (act === "toggle-sound") {
    state.settings.sound = !state.settings.sound;
    save();
    if (state.settings.sound) beep(true);
    viewSettings();
  } else if (act === "reset") {
    if (window.confirm("Reset all progress stored on this phone?")) {
      state = createState();
      state.introSeen = true;
      save();
      go("home");
    }
  }   else if (act === "about") go("about");
  else if (act === "home") go("home");
  else if (act === "daily") go("daily");
  else if (act.startsWith("xw-")) xwTool(act.slice(3));
  else if (act === "mock-prev") stepMock(-1);
  else if (act === "mock-next") stepMock(1);
  else if (act === "mock-flag") {
    const id = state.mock.ids[state.mock.index];
    state.mock.flagged[id] = !state.mock.flagged[id];
    save();
    viewMock();
  } else if (act === "mock-grid") viewGrid();
  else if (act === "mock-back-q") {
    screen = "mock";
    render();
  } else if (act === "mock-submit") {
    if (window.confirm("Submit this mock exam?")) finishMock();
  } else if (act === "park-mock") {
    freezeMock();
    go("home");
  } else if (act === "review-tab" || act === "review-start") {
    if (act === "review-start") {
      const ids = dueInChapters().slice(0, 5);
      if (ids.length) startSession("review", ids, null);
    } else go("review");
  } else if (act === "mock-clear") {
    state.mock = null;
    save();
    go("exam");
  }
}

function chooseAnswer(choice) {
  const session = state.session;
  if (!session || session.phase !== "ask") return;
  if (session.kind === "chapter-quiz") {
    session.answers = session.answers || {};
    session.answers[session.ids[session.index]] = choice;
    session.choice = choice;
    state.session = session;
    save();
    viewQuestion();
    return;
  }
  const question = byId[session.ids[session.index]];
  const outcome = answerQuestion(state, question, choice);
  state = outcome.state;
  session.phase = "explain";
  session.choice = choice;
  const supplyName = SUPPLIES.find((row) => row.id === outcome.supplyId)?.label;
  if (outcome.restStop) {
    session.note = `Pulled over. ${supplyName} was empty, so it is refilled to 3. The trip continues.`;
  } else if (outcome.supplyDelta < 0) {
    session.note = `${supplyName} −1. Still moving.`;
  } else if (outcome.supplyDelta > 0) {
    session.note = `Three in a row. ${supplyName} +1.`;
  } else session.note = "";
  state.session = session;
  beep(outcome.correct);
  save();
  say(outcome.correct ? "Correct. " + question.explanation : "Not this time. " + question.explanation);
  viewQuestion();
  main.querySelector(".explain")?.scrollIntoView({ block: "start" });
}

function advanceSession() {
  const session = state.session;
  if (session.index + 1 >= session.ids.length) {
    if (session.kind === "chapter-principles" || session.kind === "chapter-ct") {
      finishLoopStep(session);
      return;
    }
    const finishedTown = topicById(session.topicId);
    state.session = null;
    if (session.kind === "journey") {
      const road = openRoad();
      if (road.length) state.routeIndex = (state.routeIndex + 1) % road.length;
    }
    save();
    say(finishedTown ? `${finishedTown.town} stop saved.` : "Stop saved.");
    go("home");
    return;
  }
  session.index += 1;
  session.phase = "ask";
  session.choice = null;
  session.note = "";
  state.session = session;
  save();
  viewQuestion();
}

function beginMock(mode) {
  const chapters = state.mockAllChapters ? null : chapterList();
  const drawn = sampleExam(bank.questions, bank.topics, mode, Math.random, chapters);
  if (!drawn.ids.length) {
    say("No questions in that set.");
    return;
  }
  state.session = null;
  state.mock = {
    mode,
    everyChapter: drawn.everyChapter,
    ids: drawn.ids,
    sections: drawn.sections,
    answers: {},
    flagged: {},
    index: 0,
    elapsedMs: 0,
    running: true,
    lastTick: Date.now(),
    limitMs: drawn.limitMs,
    submitted: false,
    result: null,
  };
  save();
  go("mock");
}

function chooseMock(choice) {
  const id = state.mock.ids[state.mock.index];
  state.mock.answers[id] = choice;
  save();
  viewMock();
}

function stepMock(delta) {
  state.mock.index = Math.min(state.mock.ids.length - 1, Math.max(0, state.mock.index + delta));
  save();
  viewMock();
}

function finishMock() {
  if (!state.mock || state.mock.submitted) return;
  freezeMock();
  const recorded = recordExam(state, state.mock.ids, state.mock.answers, byId, Date.now(), todayKey(), state.mock.sections);
  state = recorded.state;
  state.mock.submitted = true;
  state.mock.running = false;
  state.mock.result = recorded.result;
  state.lastScreen = "mock";
  screen = "mock";
  save();
  say(recorded.result.passed ? "Mock exam passed the 70 percent mark." : "Mock exam saved. Misses were added for review.");
  render();
}

function pressCalc(key) {
  if (key === "C") {
    calcValue = "0";
    calcFresh = true;
  } else if (key === "=") {
    calcValue = compute(calcValue);
    calcFresh = true;
  } else {
    const map = { "÷": "/", "×": "*", "−": "-" };
    const token = map[key] || key;
    if (calcFresh && "0123456789.".includes(token)) calcValue = token === "." ? "0." : token;
    else calcValue = (calcValue === "0" && token !== ".") ? token : calcValue + token;
    calcFresh = false;
  }
  const readout = main.querySelector(".readout");
  if (readout) readout.textContent = calcValue;
}

function compute(expr) {
  if (expr.length > 80 || !/^[-+/*0-9.\s]+$/.test(expr)) return "0";
  try {
    const value = Function(`"use strict"; return (${expr})`)();
    if (!Number.isFinite(value)) return "0";
    return String(Math.round(value * 10000) / 10000);
  } catch {
    return "0";
  }
}

function onKey(event) {
  if (screen === "daily" && !event.metaKey && !event.ctrlKey && !event.altKey) {
    if (!todayPuzzle()) return;
    if (event.target && (event.target.tagName === "INPUT" || event.target.tagName === "TEXTAREA")) return;
    if (event.key === "Backspace") {
      event.preventDefault();
      xwBackspace();
      return;
    }
    if (event.key === " ") {
      event.preventDefault();
      xwToggle();
      return;
    }
    if (event.key.startsWith("Arrow")) {
      event.preventDefault();
      xwArrow(event.key);
      return;
    }
    if (/^[a-zA-Z]$/.test(event.key)) {
      event.preventDefault();
      xwType(event.key.toUpperCase());
      return;
    }
  }
  if (screen === "question" && state.session?.phase === "ask" && ["1", "2", "3", "4"].includes(event.key)) {
    chooseAnswer(Number(event.key) - 1);
  }
}

document.querySelector(".tabs").addEventListener("click", onClick);
main.addEventListener("click", onClick);
document.addEventListener("keydown", onKey);
document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    freezeMock();
    freezeDaily();
  } else if (screen === "mock") resumeMock();
  else if (screen === "daily") resumeDaily();
});

async function boot() {
  const [questionResponse, crosswordResponse, courseResponse] = await Promise.all([
    fetch("./data/questions.json"),
    fetch("./data/crosswords.json"),
    fetch("./data/course.json"),
  ]);
  bank = await questionResponse.json();
  crosswords = await crosswordResponse.json();
  course = await courseResponse.json();
  byId = Object.fromEntries(bank.questions.map((q) => [q.id, q]));
  state = hydratePortions(state, bank.questions);
  if (state.mock && !state.mock.submitted && state.mock.running) {
    state.mock.running = false;
    state.mock.lastTick = Date.now();
  }
  Object.values(state.crossword?.progress || {}).forEach((prog) => {
    prog.running = false;
  });
  const saved = state.lastScreen || "home";
  if (saved === "question" && state.session?.ids?.length) screen = "question";
  else if (saved === "mock" && state.mock) {
    if (!state.mock.submitted) resumeMock();
    screen = "mock";
  } else if (["home", "map", "math", "exam", "review", "settings", "about", "daily", "loop"].includes(saved)) screen = saved;
  else screen = "home";
  render();
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("./sw.js").catch(() => {});
  }
}

boot().catch(() => {
  main.innerHTML = `<section class="card"><h2>The question file did not load.</h2><p>Check that data/questions.json is next to this page, then reload.</p></section>`;
});
