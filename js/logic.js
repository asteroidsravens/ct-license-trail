/** Pure game rules for CT License Trail. No DOM. */

export const STORAGE_KEY = "ct-license-trail-v1";
export const SUPPLY_MAX = 8;
export const SUPPLIES = [
  { id: "coffee", label: "Coffee", hint: "Focus for the next question" },
  { id: "fuel", label: "Fuel", hint: "Miles left in this sitting" },
  { id: "calm", label: "Calm", hint: "Room to miss one and keep going" },
  { id: "notes", label: "Notes", hint: "The pages you can still trust" },
];

export const LEVELS = [
  [0, "Student"],
  [80, "Notebook Rider"],
  [200, "Town Reader"],
  [400, "Clause Spotter"],
  [700, "Disclosure Scout"],
  [1100, "Road Scholar"],
  [1600, "Closing Crew"],
  [2200, "License Ready"],
  [3000, "Licensed Agent"],
];

const SUPPLY_FOR_TOPIC = {
  math: "notes",
  financing: "fuel",
  contracts: "calm",
  agency: "calm",
  "ct-agency": "calm",
  disclosures: "notes",
  "ct-laws": "notes",
  practice: "coffee",
  "ct-conduct": "coffee",
};

export function createState() {
  return {
    v: 1,
    xp: 0,
    supplies: { coffee: 6, fuel: 6, calm: 6, notes: 6 },
    streak: { count: 0, lastDay: null },
    answerStreak: 0,
    bestStreak: 0,
    stats: { answered: 0, correct: 0 },
    topics: {},
    review: {},
    journey: null,
    routeIndex: 0,
    examDate: null,
    settings: { sound: false, theme: "outdoors", dog: true, dogName: "Hudson" },
    mock: null,
    session: null,
    portions: {
      national: { seen: 0, correct: 0 },
      state: { seen: 0, correct: 0 },
    },
    chapterLoops: {},
    introSeen: false,
    lastScreen: "home",
    completedChapters: null,
    mockAllChapters: false,
    crossword: {
      streak: { count: 0, lastDay: null },
      solved: {},
      progress: {},
    },
  };
}

const WEEKDAY_NAMES = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];

export const FALLBACK_COMPLETED = [2, 3, 6, 7, 14, 15, 16, 17, 20];

export const THEMES = [
  { id: "classic", name: "Classic", note: "The question, with no extra scene." },
  { id: "outdoors", name: "Outdoors", note: "A trail, shore, or field around the same facts." },
  { id: "adventure", name: "Adventure", note: "A road or ridge around the same facts." },
  { id: "history", name: "History", note: "An older town setting around the same facts." },
];

export function themeId(state) {
  const id = state?.settings?.theme;
  return THEMES.some((row) => row.id === id) ? id : "outdoors";
}

export const DEFAULT_DOG_NAME = "Hudson";

export function cleanDogName(raw) {
  const cleaned = String(raw ?? "")
    .replace(/[^A-Za-z .'-]/g, "")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 20)
    .trim();
  return cleaned || DEFAULT_DOG_NAME;
}

export function companion(state) {
  const settings = state?.settings || {};
  return {
    on: settings.dog !== false,
    name: cleanDogName(settings.dogName || DEFAULT_DOG_NAME),
  };
}

export function liveStreak(streak, today) {
  if (!streak?.lastDay || !streak.count) return 0;
  if (streak.lastDay === today || streak.lastDay === previousDay(today)) return streak.count;
  return 0;
}

export function companionCheer(state, today) {
  const pal = companion(state);
  if (!pal.on) return "";
  const name = pal.name;
  const solved = Boolean(state?.crossword?.solved?.[today]);
  const study = liveStreak(state?.streak, today);
  const grid = liveStreak(state?.crossword?.streak, today);
  if (solved) return `${name} wags. Today's grid is done.`;
  if (study >= 3) return `${name} likes this run of days.`;
  if (grid >= 2) return `${name} is keeping the crossword streak.`;
  const lines = [
    `${name} waits at the trailhead.`,
    `${name} found shade under the pines.`,
    `${name} noses the next blaze.`,
    `${name} is ready when you are.`,
  ];
  const n = Number(String(today || "0").replace(/\D/g, "").slice(-2)) || 0;
  return lines[n % lines.length];
}

export function displayStem(question, theme = "classic") {
  const flavor = theme && theme !== "classic" ? question?.flavor?.[theme] : "";
  if (!flavor) return question?.stem || "";
  return `${flavor} ${question.stem}`;
}

export function ctLawEventsForStop(questions, topicId, chapters, avoidIds = []) {
  const allowed = new Set(chapters || []);
  const avoid = new Set(avoidIds);
  const stopChapters = new Set(
    (questions || [])
      .filter((q) => q.topic === topicId && allowed.has(q.chapter))
      .map((q) => q.chapter),
  );
  return (questions || []).filter((q) => (
    q.ctLaw && q.event && allowed.has(q.chapter) && stopChapters.has(q.chapter) && !avoid.has(q.id)
  ));
}

export function completedChapters(state, course) {
  const known = new Set((course?.chapters || []).map((row) => row.n));
  const fallback = (course?.defaultCompleted || FALLBACK_COMPLETED).filter((n) => !known.size || known.has(n));
  if (!Array.isArray(state?.completedChapters)) return [...fallback];
  return state.completedChapters
    .map((n) => Number(n))
    .filter((n) => !known.size || known.has(n))
    .sort((a, b) => a - b);
}

function puzzleChapters(puzzle) {
  const used = new Set();
  [...(puzzle.across || []), ...(puzzle.down || [])].forEach((entry) => {
    if (entry.chapter) used.add(entry.chapter);
  });
  return [...used].sort((a, b) => a - b);
}

export function puzzleForDate(pack, date = new Date(), checked) {
  const utc = Date.UTC(date.getFullYear(), date.getMonth(), date.getDate());
  const epoch = Date.UTC(2024, 0, 1);
  const days = Math.floor((utc - epoch) / 86400000);
  const week = Math.floor(days / 7);
  const weekday = WEEKDAY_NAMES[date.getDay()];
  const wanted = Array.isArray(checked) ? [...checked] : [...(pack.defaultCompleted || FALLBACK_COMPLETED)];
  const allowed = new Set(wanted);
  if (!allowed.size) return null;
  const eligible = [];
  Object.values(pack.packs || {}).forEach((row) => {
    (row.days?.[weekday] || []).forEach((puzzle) => {
      const chapters = puzzleChapters(puzzle);
      if (!chapters.length) return;
      if (chapters.every((n) => allowed.has(n))) eligible.push({ puzzle, chapters });
    });
  });
  if (!eligible.length) return null;
  eligible.sort((a, b) => b.chapters.length - a.chapters.length || a.puzzle.id.localeCompare(b.puzzle.id));
  const top = eligible[0].chapters.length;
  const near = eligible.filter((item) => item.chapters.length >= top - 1);
  const pool = near.length >= 4 ? near : eligible.slice(0, Math.min(8, eligible.length));
  const index = ((week % pool.length) + pool.length) % pool.length;
  const chosen = pool[index];
  return {
    puzzle: chosen.puzzle,
    weekday,
    dateKey: todayKey(date),
    index,
    chapters: chosen.chapters,
  };
}

export function awardCrossword(state, day, clean, puzzleId) {
  const next = structuredClone(state);
  if (!next.crossword) {
    next.crossword = { streak: { count: 0, lastDay: null }, solved: {}, progress: {} };
  }
  const book = next.crossword;
  book.streak = book.streak || { count: 0, lastDay: null };
  book.solved = book.solved || {};
  if (book.solved[day]) {
    return { state: next, awarded: false, xpGain: 0, supplyDelta: 0, clean: Boolean(book.solved[day].clean) };
  }
  const xpGain = clean ? 40 : 12;
  next.xp += xpGain;
  let supplyDelta = 0;
  if (clean) {
    for (const row of SUPPLIES) {
      if (next.supplies[row.id] < SUPPLY_MAX) {
        next.supplies[row.id] += 1;
        supplyDelta += 1;
      }
    }
  }
  const streak = book.streak;
  if (streak.lastDay !== day) {
    if (streak.lastDay === previousDay(day)) streak.count += 1;
    else streak.count = 1;
    streak.lastDay = day;
  }
  book.solved[day] = { id: puzzleId, clean, xp: xpGain };
  touchStreak(next, day);
  return { state: next, awarded: true, xpGain, supplyDelta, clean };
}

export function todayKey(date = new Date()) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

export function previousDay(key) {
  const [y, m, d] = key.split("-").map(Number);
  const dt = new Date(y, m - 1, d);
  dt.setDate(dt.getDate() - 1);
  return todayKey(dt);
}

export function levelInfo(xp) {
  let current = LEVELS[0];
  let next = LEVELS[1] || null;
  for (let i = 0; i < LEVELS.length; i += 1) {
    if (xp >= LEVELS[i][0]) {
      current = LEVELS[i];
      next = LEVELS[i + 1] || null;
    }
  }
  const floor = current[0];
  const ceil = next ? next[0] : floor + 1;
  const pct = next ? Math.min(100, Math.round(((xp - floor) / (ceil - floor)) * 100)) : 100;
  return { name: current[1], xp, nextName: next ? next[1] : null, nextAt: next ? next[0] : null, pct };
}

export function daysUntil(examDate, today = todayKey()) {
  if (!examDate) return null;
  const [y, m, d] = examDate.split("-").map(Number);
  const [ty, tm, td] = today.split("-").map(Number);
  const exam = Date.UTC(y, m - 1, d);
  const now = Date.UTC(ty, tm - 1, td);
  return Math.round((exam - now) / 86400000);
}

export function topicStats(state, topicId) {
  return state.topics[topicId] || { seen: 0, correct: 0 };
}

export function masteryPercent(state, topicId) {
  const row = topicStats(state, topicId);
  if (!row.seen) return 0;
  return Math.round((row.correct / row.seen) * 100);
}

export const EXAM_SHAPE = {
  nationalCount: 80,
  nationalMinutes: 120,
  stateCount: 35,
  stateMinutes: 45,
  bothMinutes: 165,
  passingPercent: 70,
  bulletin: "PSI Connecticut Real Estate Candidate Information Bulletin, updated November 13, 2025",
};

export function portionOf(question) {
  if (question?.ctLaw || String(question?.topic || "").startsWith("ct-")) return "state";
  return "national";
}

function emptyPortions() {
  return {
    national: { seen: 0, correct: 0 },
    state: { seen: 0, correct: 0 },
  };
}

function bumpPortion(state, question, correct) {
  if (!state.portions) state.portions = emptyPortions();
  const key = portionOf(question);
  const row = state.portions[key] || { seen: 0, correct: 0 };
  row.seen += 1;
  if (correct) row.correct += 1;
  state.portions[key] = row;
}

export function hydratePortions(state, questions) {
  if (!state.portions) state.portions = emptyPortions();
  if (state.portions.hydrated) return state;
  const byId = Object.fromEntries((questions || []).map((q) => [q.id, q]));
  const tally = emptyPortions();
  let any = false;
  Object.entries(state.review || {}).forEach(([id, row]) => {
    const question = byId[id];
    if (!question || !row) return;
    const seen = (row.reps || 0) + (row.lapses || 0);
    if (!seen) return;
    any = true;
    const key = portionOf(question);
    tally[key].seen += seen;
    tally[key].correct += row.reps || 0;
  });
  if (any && !state.portions.national.seen && !state.portions.state.seen) {
    state.portions.national = tally.national;
    state.portions.state = tally.state;
  }
  state.portions.hydrated = true;
  return state;
}

export function portionReadiness(state) {
  const portions = state.portions || emptyPortions();
  const shape = [
    ["national", "General principles", EXAM_SHAPE.nationalCount, EXAM_SHAPE.nationalMinutes],
    ["state", "Connecticut law", EXAM_SHAPE.stateCount, EXAM_SHAPE.stateMinutes],
  ];
  return shape.map(([id, label, count, minutes]) => {
    const stats = portions[id] || { seen: 0, correct: 0 };
    const percent = stats.seen ? Math.round((stats.correct / stats.seen) * 100) : 0;
    let status = "Not started";
    if (stats.seen > 0 && stats.seen < 10) status = "Early";
    else if (stats.seen >= 10 && percent >= EXAM_SHAPE.passingPercent) status = "On pace";
    else if (stats.seen >= 10) status = "Below the line";
    return { id, label, seen: stats.seen, correct: stats.correct, percent, status, count, minutes };
  });
}

function shuffled(list, rng) {
  const copy = [...list];
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rng() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

export function chapterStudyPlan(questions, chapter, rng = Math.random) {
  const pool = (questions || []).filter((q) => q.chapter === chapter);
  const principles = shuffled(pool.filter((q) => portionOf(q) === "national"), rng);
  const ct = shuffled(pool.filter((q) => portionOf(q) === "state"), rng);
  const principleIds = principles.slice(0, 4).map((q) => q.id);
  const ctIds = ct.slice(0, 4).map((q) => q.id);
  const used = new Set([...principleIds, ...ctIds]);
  let rest = shuffled(pool.filter((q) => !used.has(q.id)), rng);
  if (rest.length < Math.min(4, pool.length)) rest = shuffled(pool, rng);
  const quizCt = rest.filter((q) => portionOf(q) === "state").slice(0, 2);
  const quizNat = rest.filter((q) => portionOf(q) === "national").slice(0, 4);
  let quiz = shuffled([...quizNat, ...quizCt], rng).slice(0, 6);
  if (quiz.length < Math.min(4, pool.length)) quiz = shuffled(pool, rng).slice(0, Math.min(6, pool.length));
  return {
    principles: principleIds,
    ct: ctIds,
    quiz: quiz.map((q) => q.id),
  };
}

function touchStreak(state, day) {
  if (state.streak.lastDay === day) return;
  if (state.streak.lastDay === previousDay(day)) state.streak.count += 1;
  else state.streak.count = 1;
  state.streak.lastDay = day;
}

function clampSupply(state, id) {
  state.supplies[id] = Math.max(0, Math.min(SUPPLY_MAX, state.supplies[id]));
}

function lowestSupply(state) {
  return SUPPLIES.reduce((best, row) => (
    state.supplies[row.id] < state.supplies[best] ? row.id : best
  ), SUPPLIES[0].id);
}

function schedule(state, questionId, correct, now) {
  const prior = state.review[questionId] || { ease: 2.3, interval: 0, reps: 0, lapses: 0, due: now };
  if (!correct) {
    state.review[questionId] = {
      ease: Math.max(1.3, prior.ease - 0.2),
      interval: 0,
      reps: 0,
      lapses: prior.lapses + 1,
      due: now,
    };
    return;
  }
  const interval = prior.reps === 0 ? 1 : Math.max(1, Math.round(prior.interval * prior.ease));
  state.review[questionId] = {
    ease: prior.ease,
    interval,
    reps: prior.reps + 1,
    lapses: prior.lapses,
    due: now + interval * 86400000,
  };
}

export function answerQuestion(state, question, choiceIndex, now = Date.now(), day = todayKey()) {
  const next = structuredClone(state);
  const correct = choiceIndex === question.answer;
  touchStreak(next, day);
  next.stats.answered += 1;
  if (correct) {
    next.stats.correct += 1;
    next.answerStreak += 1;
    next.bestStreak = Math.max(next.bestStreak, next.answerStreak);
  } else {
    next.answerStreak = 0;
  }
  const row = topicStats(next, question.topic);
  row.seen += 1;
  if (correct) row.correct += 1;
  next.topics[question.topic] = row;
  bumpPortion(next, question, correct);

  const xpGain = correct ? 10 + Math.min(next.answerStreak, 5) * 2 : 3;
  next.xp += xpGain;

  let supplyId = null;
  let supplyDelta = 0;
  let restStop = null;
  if (!correct) {
    supplyId = SUPPLY_FOR_TOPIC[question.topic] || "coffee";
    if (next.supplies[supplyId] <= 0) {
      supplyId = SUPPLIES.find((row) => next.supplies[row.id] > 0)?.id || supplyId;
    }
    if (next.supplies[supplyId] > 0) {
      next.supplies[supplyId] -= 1;
      supplyDelta = -1;
    }
    if (next.supplies[supplyId] <= 0) {
      next.supplies[supplyId] = 3;
      restStop = supplyId;
    }
  } else if (next.answerStreak > 0 && next.answerStreak % 3 === 0) {
    supplyId = lowestSupply(next);
    if (next.supplies[supplyId] < SUPPLY_MAX) {
      next.supplies[supplyId] += 1;
      supplyDelta = 1;
    }
  }
  if (supplyId) clampSupply(next, supplyId);
  schedule(next, question.id, correct, now);
  return { state: next, correct, xpGain, supplyId, supplyDelta, restStop };
}

export function dueReviews(state, now = Date.now()) {
  return Object.entries(state.review)
    .filter(([, row]) => row.due <= now)
    .map(([id]) => id);
}

export function pickQuestions(questions, topicId, count, state, rng = Math.random, chapters = null) {
  const allowed = chapters ? new Set(chapters) : null;
  const pool = questions.filter((q) => q.topic === topicId && (!allowed || allowed.has(q.chapter)));
  const unseen = pool.filter((q) => !state.topics[topicId] || !state.review[q.id]);
  const missed = pool.filter((q) => state.review[q.id] && state.review[q.id].lapses > 0 && state.review[q.id].reps === 0);
  const ranked = [...missed, ...unseen.filter((q) => !missed.includes(q)), ...pool];
  const unique = [];
  const seen = new Set();
  for (const q of ranked) {
    if (seen.has(q.id)) continue;
    seen.add(q.id);
    unique.push(q);
  }
  for (let i = unique.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rng() * (i + 1));
    [unique[i], unique[j]] = [unique[j], unique[i]];
  }
  // Keep missed questions near the front, then fill.
  const front = missed.map((q) => q.id);
  const rest = unique.filter((q) => !front.includes(q.id));
  const ordered = [...unique.filter((q) => front.includes(q.id)), ...rest];
  return ordered.slice(0, count).map((q) => q.id);
}

function shuffleIds(ids, rng) {
  const copy = [...ids];
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rng() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

export function sampleExam(questions, topics, mode, rng = Math.random, chapters = null) {
  const used = new Set();
  const allowed = chapters ? new Set(chapters) : null;
  const source = allowed ? questions.filter((q) => allowed.has(q.chapter)) : questions;
  const sections = [];
  const take = (topicId, count) => {
    const pool = source.filter((q) => q.pools.includes(topicId) && !used.has(q.id));
    const copy = [...pool];
    for (let i = copy.length - 1; i > 0; i -= 1) {
      const j = Math.floor(rng() * (i + 1));
      [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    const chosen = copy.slice(0, count);
    chosen.forEach((q) => used.add(q.id));
    return chosen.map((q) => q.id);
  };
  const want = (portion) => topics.filter((t) => t.portion === portion);
  if (mode === "national" || mode === "both") {
    const ids = [];
    want("national").forEach((topic) => ids.push(...take(topic.id, topic.weight)));
    sections.push({ id: "national", label: "General portion", minutes: 120, ids: shuffleIds(ids, rng) });
  }
  if (mode === "state" || mode === "both") {
    const ids = [];
    want("state").forEach((topic) => ids.push(...take(topic.id, topic.weight)));
    sections.push({ id: "state", label: "Connecticut portion", minutes: 45, ids: shuffleIds(ids, rng) });
  }
  const ids = sections.flatMap((section) => section.ids);
  const bulletinCount = mode === "both" ? 115 : mode === "state" ? 35 : 80;
  const bulletinMinutes = mode === "both" ? 165 : mode === "state" ? 45 : 120;
  const minutes = chapters && ids.length < bulletinCount
    ? Math.max(5, Math.round(bulletinMinutes * ids.length / bulletinCount))
    : bulletinMinutes;
  return {
    ids,
    sections,
    minutes,
    limitMs: minutes * 60 * 1000,
    everyChapter: !chapters,
    bulletinCount,
  };
}

function scoreIds(ids, answers, questionsById) {
  let correct = 0;
  const byTopic = {};
  (ids || []).forEach((id) => {
    const q = questionsById[id];
    if (!q) return;
    const ok = answers[id] === q.answer;
    if (ok) correct += 1;
    if (!byTopic[q.topic]) byTopic[q.topic] = { correct: 0, total: 0 };
    byTopic[q.topic].total += 1;
    if (ok) byTopic[q.topic].correct += 1;
  });
  const total = (ids || []).length;
  const percent = total ? Math.round((correct / total) * 100) : 0;
  return {
    correct,
    total,
    percent,
    passed: total > 0 && percent >= EXAM_SHAPE.passingPercent,
    byTopic,
  };
}

export function scoreExam(ids, answers, questionsById, sections = null) {
  const overall = scoreIds(ids, answers, questionsById);
  const portions = (sections || [])
    .filter((section) => section.ids?.length)
    .map((section) => {
      const scored = scoreIds(section.ids, answers, questionsById);
      return {
        id: section.id,
        label: section.label,
        correct: scored.correct,
        total: scored.total,
        percent: scored.percent,
        passed: scored.passed,
      };
    });
  const passed = portions.length ? portions.every((section) => section.passed) : overall.passed;
  return { ...overall, passed, portions };
}

export function recordExam(state, ids, answers, questionsById, now = Date.now(), day = todayKey(), sections = null) {
  const next = structuredClone(state);
  touchStreak(next, day);
  const result = scoreExam(ids, answers, questionsById, sections);
  ids.forEach((id) => {
    const q = questionsById[id];
    const ok = answers[id] === q.answer;
    bumpPortion(next, q, ok);
    const row = topicStats(next, q.topic);
    row.seen += 1;
    if (ok) row.correct += 1;
    next.topics[q.topic] = row;
    if (!ok) schedule(next, id, false, now);
  });
  next.xp += result.correct * 4;
  next.stats.answered += result.total;
  next.stats.correct += result.correct;
  return { state: next, result };
}

export function roadTopics(topics, questions = null, chapters = null) {
  const base = topics.filter((topic) => topic.id !== "math");
  if (!questions || !chapters) return base;
  const allowed = new Set(chapters);
  return base.filter((topic) => questions.some((q) => q.topic === topic.id && allowed.has(q.chapter)));
}
