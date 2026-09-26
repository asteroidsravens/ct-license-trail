import {
  STORAGE_KEY, SUPPLIES, SUPPLY_MAX, createState, levelInfo, daysUntil, todayKey,
  masteryPercent, answerQuestion, dueReviews, pickQuestions, sampleExam, recordExam,
  roadTopics,
} from "./logic.js";

const main = document.querySelector("#main");
const live = document.querySelector("#live");
const tabButtons = [...document.querySelectorAll(".tabs button")];
const levelName = document.querySelector("#level-name");
const streakPill = document.querySelector("#streak-pill");
const countPill = document.querySelector("#count-pill");

let bank = null;
let byId = {};
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
    return {
      ...createState(),
      ...saved,
      supplies: { ...createState().supplies, ...(saved.supplies || {}) },
      settings: { sound: false, ...(saved.settings || {}) },
      streak: { ...createState().streak, ...(saved.streak || {}) },
      stats: { ...createState().stats, ...(saved.stats || {}) },
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
      || (tab === "map" && screen === "map")
      || (tab === "math" && (screen === "math" || (screen === "question" && quizKind === "math")))
      || (tab === "exam" && ["exam", "mock"].includes(screen))
      || (tab === "review" && (screen === "review" || (screen === "question" && quizKind === "review")));
    if (on) button.setAttribute("aria-current", "page");
    else button.removeAttribute("aria-current");
  });
}

function go(next) {
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

function startJourney(topicId) {
  const road = roadTopics(bank.topics);
  if (!topicId) {
    const topic = road[(state.routeIndex || 0) % road.length];
    topicId = topic.id;
  } else {
    const index = road.findIndex((topic) => topic.id === topicId);
    if (index >= 0) state.routeIndex = index;
  }
  const ids = pickQuestions(bank.questions, topicId, 3, state);
  const events = bank.questions.filter((q) => q.event && !ids.includes(q.id));
  if (events.length && Math.random() < 0.75 && ids.length > 1) {
    const event = events[Math.floor(Math.random() * events.length)];
    ids.splice(1, 1, event.id);
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
    mock: viewMock,
    review: viewReviewHome,
    settings: viewSettings,
    about: viewAbout,
  };
  (views[screen] || viewHome)();
  const heading = main.querySelector("h2, .stem");
  if (heading) heading.setAttribute("tabindex", "-1");
}

function viewHome() {
  const level = levelInfo(state.xp);
  const days = daysUntil(state.examDate);
  const due = dueReviews(state).length;
  const road = roadTopics(bank.topics);
  const town = road[(state.routeIndex || 0) % road.length];
  let dateLine = "Set your own exam date whenever you know it. Change it any time.";
  if (days === 0) dateLine = "Exam day is today. A short review still counts.";
  else if (days > 0) dateLine = `${days} day${days === 1 ? "" : "s"} until the date you chose.`;
  else if (days < 0) dateLine = "That exam date has passed. Pick another whenever you are ready.";
  const resumeMock = state.mock && !state.mock.submitted;
  const resumeQuiz = state.session && state.session.phase;
  main.innerHTML = `
    <section class="card">
      <p class="kicker">${esc(town.town)}</p>
      <h2>${resumeQuiz ? "Pick up the same question" : `Next stop: ${esc(town.name)}`}</h2>
      <p class="lede">${esc(town.blurb)} Three questions is a full stop between rides.</p>
      <div class="stack">
        ${resumeMock ? `<button class="btn btn-primary" data-act="resume-mock">Resume mock exam</button>` : ""}
        <button class="btn btn-primary" data-act="continue">${resumeQuiz ? "Continue this question" : "Start three questions"}</button>
        <button class="btn btn-quiet" data-act="settings">Exam date and sound</button>
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
    <p class="fine">Unofficial study aid for the Connecticut salesperson exam. Not affiliated with PSI or the Department of Consumer Protection.</p>`;
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
  const where = session.kind === "review" ? "Review" : session.kind === "math" ? "Math Pass" : topic.town;
  main.innerHTML = `
    <article class="card">
      <p class="kicker">${esc(where)} · ${session.index + 1} of ${session.ids.length}${question.event && session.kind === "journey" ? " · road stop" : ""}</p>
      <h2 class="stem" id="stem">${esc(question.stem)}</h2>
      <div class="stack" role="group" aria-labelledby="stem">
        ${question.choices.map((choice, index) => {
          let cls = "choice";
          if (answered && index === question.answer) cls += " good";
          else if (answered && index === session.choice && index !== question.answer) cls += " bad";
          return `<button class="${cls}" data-choice="${index}" ${answered ? "disabled" : ""}>
            <span class="key" aria-hidden="true">${keys[index]}</span>
            <span>${esc(choice)}</span>
          </button>`;
        }).join("")}
      </div>
      ${answered ? explainBlock(question, session.choice) : ""}
      ${session.note ? `<div class="note">${esc(session.note)}</div>` : ""}
      <div class="dock">
        ${question.math ? `<button class="btn btn-quiet" data-act="calc">Calculator</button>` : ""}
        ${answered ? `<button class="btn btn-primary" data-act="next-q">${session.index + 1 >= session.ids.length ? "Finish this stop" : "Next question"}</button>` : ""}
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

function viewMap() {
  const road = roadTopics(bank.topics);
  main.innerHTML = `
    <section class="card">
      <h2>The road</h2>
      <p class="lede">Each town is an outline topic. Open any of them. The suggested stop is marked.</p>
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
        <button class="btn town" data-act="math-tab">
          <span class="dot" aria-hidden="true"></span>
          <span><strong>Waterbury</strong> · Math Pass<span class="muted" style="display:block">Calculator drills, with the steps written out.</span></span>
        </button>
      </div>
    </section>`;
}

function viewMathHome() {
  const mathCount = bank.questions.filter((q) => q.math).length;
  main.innerHTML = `
    <section class="card">
      <p class="kicker">Waterbury · Math Pass</p>
      <h2>Numbers, then the reason</h2>
      <p class="lede">${mathCount} drills: commission, splits, seller proceeds, prorations, Connecticut conveyance tax, LTV, PITI, area, cap rate, equity, and points. Every one shows the steps after you answer.</p>
      <div class="stack">
        <button class="btn btn-primary" data-act="math-start">Work three math items</button>
        <button class="btn btn-quiet" data-act="calc">Open the calculator</button>
      </div>
      <p class="muted">Day-count and who owns closing day are written into each proration, so you are practicing a stated method. Conveyance items use Conn. Gen. Stat. § 12-494 and say when the town has not added an extra local tax.</p>
    </section>`;
}

function viewExamHome() {
  const paused = state.mock && !state.mock.submitted;
  main.innerHTML = `
    <section class="card">
      <h2>Mock exam</h2>
      <p class="lede">Built to the PSI salesperson shape in the November 13, 2025 candidate bulletin: national 80 items / 120 minutes, Connecticut 35 items / 45 minutes, 70% to pass each sitting here. A full run is 115 items and 165 minutes.</p>
      <p>The clock pauses when you leave this page or lock the phone. On the real exam day, it will not.</p>
      <div class="stack">
        ${paused ? `<button class="btn btn-primary" data-act="resume-mock">Resume saved mock (${state.mock.ids.length} items)</button>` : ""}
        <button class="btn btn-pine" data-mode="national">National portion</button>
        <button class="btn btn-pine" data-mode="state">Connecticut portion</button>
        <button class="btn btn-primary" data-mode="both">Both portions</button>
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
      <p class="kicker">${esc(topic.name)} · ${mock.index + 1} of ${mock.ids.length}</p>
      <p class="timer ${left < 5 * 60 * 1000 ? "low" : ""}" style="color:${left < 5 * 60 * 1000 ? "var(--bad)" : "var(--pine)"}" aria-live="off">Time left ${formatClock(left)}</p>
      <h2 class="stem" id="stem">${esc(question.stem)}</h2>
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
  const lines = bank.topics.map((topic) => {
    const row = result.byTopic[topic.id];
    if (!row) return "";
    return `<p><strong>${esc(topic.name)}</strong> · ${row.correct}/${row.total}</p>`;
  }).join("");
  main.innerHTML = `
    <section class="card">
      <h2>${result.passed ? "You cleared 70%." : "Not 70% this time."}</h2>
      <p class="lede">${result.correct} of ${result.total} · ${result.percent}%. A salesperson passing score on the PSI bulletin is 70%. ${result.passed ? "Hold onto what worked." : "The misses are already in your review pile."}</p>
      ${lines}
      <div class="stack">
        <button class="btn btn-primary" data-act="review-tab">Review the misses</button>
        <button class="btn btn-quiet" data-act="mock-clear">Leave this result</button>
      </div>
    </section>`;
}

function viewReviewHome() {
  const due = dueReviews(state);
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
  main.innerHTML = `
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
  if (!act) return;
  if (act === "continue") {
    if (state.session) go("question");
    else startJourney();
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
      const ids = bank.questions.filter((q) => q.math).map((q) => q.id);
      for (let i = ids.length - 1; i > 0; i -= 1) {
        const j = Math.floor(Math.random() * (i + 1));
        [ids[i], ids[j]] = [ids[j], ids[i]];
      }
      startSession("math", ids.slice(0, 3), "math");
    } else go("math");
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
  } else if (act === "about") go("about");
  else if (act === "home") go("home");
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
      const ids = dueReviews(state).slice(0, 5);
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
    const finishedTown = topicById(session.topicId);
    state.session = null;
    if (session.kind === "journey") {
      const road = roadTopics(bank.topics);
      state.routeIndex = (state.routeIndex + 1) % road.length;
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
  const drawn = sampleExam(bank.questions, bank.topics, mode);
  state.session = null;
  state.mock = {
    mode,
    ids: drawn.ids,
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
  const recorded = recordExam(state, state.mock.ids, state.mock.answers, byId);
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
  if (screen === "question" && state.session?.phase === "ask" && ["1", "2", "3", "4"].includes(event.key)) {
    chooseAnswer(Number(event.key) - 1);
  }
}

document.querySelector(".tabs").addEventListener("click", onClick);
main.addEventListener("click", onClick);
document.addEventListener("keydown", onKey);
document.addEventListener("visibilitychange", () => {
  if (document.hidden) freezeMock();
  else if (screen === "mock") resumeMock();
});

async function boot() {
  const response = await fetch("./data/questions.json");
  bank = await response.json();
  byId = Object.fromEntries(bank.questions.map((q) => [q.id, q]));
  if (state.mock && !state.mock.submitted && state.mock.running) {
    state.mock.running = false;
    state.mock.lastTick = Date.now();
  }
  const saved = state.lastScreen || "home";
  if (saved === "question" && state.session?.ids?.length) screen = "question";
  else if (saved === "mock" && state.mock) {
    if (!state.mock.submitted) resumeMock();
    screen = "mock";
  } else if (["home", "map", "math", "exam", "review", "settings", "about"].includes(saved)) screen = saved;
  else screen = "home";
  render();
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("./sw.js").catch(() => {});
  }
}

boot().catch(() => {
  main.innerHTML = `<section class="card"><h2>The question file did not load.</h2><p>Check that data/questions.json is next to this page, then reload.</p></section>`;
});
