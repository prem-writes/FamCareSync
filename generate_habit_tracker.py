"""
Habit Tracker Web App Generator
--------------------------------
Run this script to produce habit_tracker.html — a fully self-contained
single-file web app you can open in any browser or host anywhere.

Usage:
    python generate_habit_tracker.py

Output:
    habit_tracker.html  (same directory as this script)
"""

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Habit Tracker</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: #0d0d0d;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    min-height: 100vh;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    padding: 32px 16px 48px;
    color: #e8e8e8;
  }

  .app {
    width: 100%;
    max-width: 420px;
  }

  /* Header */
  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 28px;
  }
  .header h1 { font-size: 18px; font-weight: 500; color: #fff; }
  .date-label { font-size: 13px; color: #555; }

  /* Stats */
  .stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 24px;
  }
  .stat {
    background: #181818;
    border-radius: 10px;
    padding: 14px 10px;
    text-align: center;
  }
  .stat-n { font-size: 24px; font-weight: 500; color: #fff; }
  .stat-l {
    font-size: 10px;
    color: #555;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: .05em;
  }

  /* Habit rows */
  .habit-list { display: flex; flex-direction: column; }

  .habit-row {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 17px 0;
    border-bottom: 1px solid #1c1c1c;
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
    user-select: none;
  }
  .habit-row:last-child { border-bottom: none; }

  /* Checkbox */
  .cb {
    width: 28px;
    height: 28px;
    border-radius: 8px;
    border: 1.5px solid #333;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    position: relative;
    overflow: hidden;
    transition: background .18s, border-color .18s, transform .12s;
  }
  .cb.done { background: #5DCAA5; border-color: #5DCAA5; }
  .cb svg {
    opacity: 0;
    transform: scale(0) rotate(-15deg);
    transition: opacity .18s, transform .22s cubic-bezier(.34,1.56,.64,1);
  }
  .cb.done svg { opacity: 1; transform: scale(1) rotate(0deg); }

  /* Ripple */
  .ripple {
    position: absolute;
    width: 70px; height: 70px;
    border-radius: 50%;
    background: rgba(93,202,165,.3);
    top: 50%; left: 50%;
    transform: translate(-50%,-50%) scale(0);
    animation: ripple .5s linear forwards;
    pointer-events: none;
  }
  @keyframes ripple { to { transform: translate(-50%,-50%) scale(3.5); opacity: 0; } }

  /* Pop */
  .pop { animation: pop .22s cubic-bezier(.34,1.56,.64,1); }
  @keyframes pop {
    0%   { transform: scale(1); }
    50%  { transform: scale(1.18); }
    100% { transform: scale(1); }
  }

  /* Habit info */
  .habit-info { flex: 1; min-width: 0; }
  .habit-name {
    font-size: 15px;
    color: #e0e0e0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    transition: color .18s;
  }
  .habit-row.done .habit-name { color: #5DCAA5; }

  /* Streak dots */
  .dots-row {
    display: flex;
    align-items: center;
    gap: 5px;
    margin-top: 6px;
  }
  .dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #222;
    transition: background .25s, transform .2s;
  }
  .dot.lit { background: #5DCAA5; }
  .dot.pop-dot { animation: dotpop .3s cubic-bezier(.34,1.56,.64,1); }
  @keyframes dotpop {
    0%   { transform: scale(1); }
    50%  { transform: scale(2); }
    100% { transform: scale(1); }
  }
  .streak-txt {
    font-size: 11px;
    color: #444;
    margin-left: 4px;
  }
  .streak-txt.active { color: #5DCAA5; }

  /* Edit button */
  .edit-btn {
    background: none;
    border: none;
    color: #444;
    cursor: pointer;
    font-size: 13px;
    padding: 2px 4px;
    margin-top: 18px;
    float: right;
    font-family: inherit;
    transition: color .15s;
  }
  .edit-btn:hover { color: #888; }

  /* Edit modal */
  .modal-bg {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,.6);
    align-items: center;
    justify-content: center;
    z-index: 100;
    padding: 16px;
  }
  .modal-bg.open { display: flex; }
  .modal {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 14px;
    padding: 24px;
    width: 100%;
    max-width: 360px;
  }
  .modal h2 { font-size: 15px; font-weight: 500; margin-bottom: 16px; color: #e8e8e8; }
  .modal input {
    background: #111;
    border: 1px solid #2a2a2a;
    border-radius: 8px;
    padding: 10px 12px;
    color: #e8e8e8;
    font-size: 14px;
    width: 100%;
    margin-bottom: 8px;
    outline: none;
    font-family: inherit;
    transition: border-color .15s;
  }
  .modal input:focus { border-color: #5DCAA5; }
  .modal-actions { display: flex; gap: 8px; justify-content: flex-end; margin-top: 12px; }
  .btn-cancel {
    background: none;
    border: 1px solid #2a2a2a;
    border-radius: 8px;
    padding: 8px 18px;
    color: #888;
    cursor: pointer;
    font-size: 13px;
    font-family: inherit;
  }
  .btn-save {
    background: #5DCAA5;
    border: none;
    border-radius: 8px;
    padding: 8px 18px;
    color: #04342C;
    cursor: pointer;
    font-size: 13px;
    font-weight: 500;
    font-family: inherit;
  }
  .btn-save:active { opacity: .85; }
</style>
</head>
<body>
<div class="app">
  <div class="header">
    <h1>Daily habits</h1>
    <span class="date-label" id="dateLabel"></span>
  </div>
  <div class="stats">
    <div class="stat"><div class="stat-n" id="sToday">0/5</div><div class="stat-l">Today</div></div>
    <div class="stat"><div class="stat-n" id="sBest">0</div><div class="stat-l">Best streak</div></div>
    <div class="stat"><div class="stat-n" id="sWeek">0%</div><div class="stat-l">This week</div></div>
  </div>
  <div class="habit-list" id="habitList"></div>
  <button class="edit-btn" onclick="openEdit()">&#9998; edit habits</button>
</div>

<!-- Edit modal -->
<div class="modal-bg" id="modalBg">
  <div class="modal">
    <h2>Edit habits</h2>
    <div id="editInputs"></div>
    <div class="modal-actions">
      <button class="btn-cancel" onclick="closeEdit()">Cancel</button>
      <button class="btn-save" onclick="saveEdit()">Save</button>
    </div>
  </div>
</div>

<script>
const DEFAULTS = [
  'Morning workout',
  'Read for 30 min',
  'Drink 8 glasses of water',
  'No social media before noon',
  'Meditate 10 min'
];

function dateKey(offset) {
  const d = new Date();
  d.setDate(d.getDate() + offset);
  return d.toISOString().slice(0, 10);
}
function todayKey() { return dateKey(0); }

function loadState() {
  try { const s = localStorage.getItem('habitApp'); return s ? JSON.parse(s) : null; }
  catch(e) { return null; }
}
function saveState(st) {
  try { localStorage.setItem('habitApp', JSON.stringify(st)); } catch(e) {}
}

let state = loadState() || { habits: DEFAULTS.slice(), completions: {} };

function getStreak(idx) {
  let n = 0;
  for (let i = 0; i >= -365; i--) {
    const c = state.completions[dateKey(i)] || {};
    if (c[idx]) n++;
    else break;
  }
  return n;
}
function getLast7(idx) {
  return Array.from({length: 7}, (_, i) => {
    const c = state.completions[dateKey(i - 6)] || {};
    return !!c[idx];
  });
}
function getBest(idx) {
  const keys = Object.keys(state.completions).sort();
  let best = 0, cur = 0;
  keys.forEach(k => {
    if (state.completions[k] && state.completions[k][idx]) { cur++; best = Math.max(best, cur); }
    else cur = 0;
  });
  return best;
}
function weekRate() {
  let total = 0, done = 0;
  for (let i = -6; i <= 0; i++) {
    total += state.habits.length;
    const c = state.completions[dateKey(i)] || {};
    done += Object.values(c).filter(Boolean).length;
  }
  return total ? Math.round(done / total * 100) : 0;
}
function todayDone() {
  const c = state.completions[todayKey()] || {};
  return Object.values(c).filter(Boolean).length;
}

function toggleHabit(idx) {
  const k = todayKey();
  if (!state.completions[k]) state.completions[k] = {};
  const nowDone = !state.completions[k][idx];
  state.completions[k][idx] = nowDone;
  saveState(state);
  render();
  if (nowDone) {
    const cb = document.querySelector('[data-cb="' + idx + '"]');
    if (cb) {
      const r = document.createElement('span');
      r.className = 'ripple';
      cb.appendChild(r);
      setTimeout(() => r.remove(), 600);
      cb.classList.add('pop');
      setTimeout(() => cb.classList.remove('pop'), 300);
    }
    const lastDot = document.querySelector('[data-dot="' + idx + '7"]');
    if (lastDot) {
      lastDot.classList.add('pop-dot');
      setTimeout(() => lastDot.classList.remove('pop-dot'), 400);
    }
  }
}

function render() {
  const todayComp = state.completions[todayKey()] || {};
  const today = new Date().toLocaleDateString('en-US', {weekday:'short', month:'short', day:'numeric'});
  document.getElementById('dateLabel').textContent = today;

  const done = todayDone();
  document.getElementById('sToday').textContent = done + '/' + state.habits.length;
  const overallBest = Math.max(0, ...state.habits.map((_, i) => getBest(i)));
  document.getElementById('sBest').textContent = overallBest;
  document.getElementById('sWeek').textContent = weekRate() + '%';

  const list = document.getElementById('habitList');
  list.innerHTML = state.habits.map((h, i) => {
    const isDone = !!todayComp[i];
    const dots = getLast7(i);
    const streak = getStreak(i);
    const streakTxt = streak > 0 ? streak + ' day' + (streak !== 1 ? 's' : '') + ' streak' : 'no streak yet';
    return '<div class="habit-row' + (isDone ? ' done' : '') + '" onclick="toggleHabit(' + i + ')" role="checkbox" aria-checked="' + isDone + '" tabindex="0">'
      + '<div class="cb' + (isDone ? ' done' : '') + '" data-cb="' + i + '">'
      + '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="#04342C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
      + '<polyline points="2,7 6,11 12,3"></polyline></svg></div>'
      + '<div class="habit-info">'
      + '<div class="habit-name">' + h + '</div>'
      + '<div class="dots-row">'
      + dots.map((lit, di) => '<div class="dot' + (lit ? ' lit' : '') + '" data-dot="' + i + (di + 1) + '"></div>').join('')
      + '<span class="streak-txt' + (streak > 0 ? ' active' : '') + '">' + streakTxt + '</span>'
      + '</div></div></div>';
  }).join('');

  list.querySelectorAll('[role=checkbox]').forEach((el, i) => {
    el.addEventListener('keydown', e => {
      if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); toggleHabit(i); }
    });
  });
}

function openEdit() {
  const inp = document.getElementById('editInputs');
  inp.innerHTML = state.habits.map((h, i) =>
    '<input type="text" id="ei' + i + '" value="' + h.replace(/"/g, '&quot;') + '" placeholder="Habit ' + (i+1) + '" />'
  ).join('');
  document.getElementById('modalBg').classList.add('open');
}
function closeEdit() { document.getElementById('modalBg').classList.remove('open'); }
function saveEdit() {
  state.habits = state.habits.map((h, i) => {
    const v = document.getElementById('ei' + i).value.trim();
    return v || h;
  });
  saveState(state);
  closeEdit();
  render();
}

document.getElementById('modalBg').addEventListener('click', e => {
  if (e.target === document.getElementById('modalBg')) closeEdit();
});

render();
</script>
</body>
</html>
"""

def main():
    output_path = "habit_tracker.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(HTML)
    print(f"Generated: {output_path}")
    print()
    print("To preview locally, open the file in any browser.")
    print("To serve it over your local network (e.g. to your iPhone):")
    print("  python -m http.server 8080")
    print("Then on your iPhone browser, go to:")
    print("  http://<your-computer-ip>:8080/habit_tracker.html")

if __name__ == "__main__":
    main()
