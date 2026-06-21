"""
FamCare Sync — Habit Tracker Web App Generator
------------------------------------------------
Run this script to produce famcare_sync.html — a fully self-contained
single-file web app you can open in any browser or host anywhere.

Usage:
    python generate_habit_tracker.py

Output:
    famcare_sync.html  (same directory as this script)
"""

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1" />
<title>FamCare Sync</title>
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
  position: relative;
  min-height: 580px;
}

/* ── Welcome screen ── */
.welcome {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 580px;
  padding: 48px 24px;
  text-align: center;
  background: #111;
  border-radius: 20px;
}

.logo-ring {
  width: 76px;
  height: 76px;
  border-radius: 50%;
  background: #1a1a1a;
  border: 1.5px solid #2a2a2a;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 26px;
  font-size: 32px;
}

.welcome h1 {
  font-size: 24px;
  font-weight: 500;
  color: #fff;
  margin-bottom: 12px;
  line-height: 1.35;
}

.welcome p {
  font-size: 14px;
  color: #666;
  max-width: 260px;
  line-height: 1.65;
  margin-bottom: 40px;
}

.start-btn {
  background: #5DCAA5;
  color: #04342C;
  border: none;
  border-radius: 12px;
  padding: 15px 34px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  font-family: inherit;
  letter-spacing: .01em;
  transition: opacity .15s, transform .12s;
}
.start-btn:hover  { opacity: .9; }
.start-btn:active { transform: scale(.97); }

/* ── Tracker screen ── */
.tracker {
  display: none;
  flex-direction: column;
  background: #111;
  border-radius: 20px;
  padding: 24px;
  min-height: 580px;
}

.tr-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 22px;
}
.tr-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 500;
  color: #5DCAA5;
  letter-spacing: .01em;
}
.tr-date { font-size: 12px; color: #555; }

/* Stats */
.stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin-bottom: 22px;
}
.stat { background: #181818; border-radius: 10px; padding: 12px; text-align: center; }
.stat-n { font-size: 22px; font-weight: 500; color: #fff; }
.stat-l { font-size: 10px; color: #555; margin-top: 3px; text-transform: uppercase; letter-spacing: .05em; }

/* Habit rows */
.habit-row {
  display: flex;
  align-items: center;
  gap: 13px;
  padding: 15px 0;
  border-bottom: 1px solid #1c1c1c;
  cursor: pointer;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
}
.habit-row:last-child { border-bottom: none; }

/* Checkbox */
.cb {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  border: 1.5px solid #2e2e2e;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  position: relative;
  overflow: hidden;
  transition: background .17s, border-color .17s;
}
.cb.done { background: #5DCAA5; border-color: #5DCAA5; }
.cb svg {
  opacity: 0;
  transform: scale(0) rotate(-15deg);
  transition: opacity .17s, transform .22s cubic-bezier(.34,1.56,.64,1);
}
.cb.done svg { opacity: 1; transform: scale(1) rotate(0); }

/* Ripple */
.ripple {
  position: absolute;
  width: 70px; height: 70px;
  border-radius: 50%;
  background: rgba(93,202,165,.28);
  top: 50%; left: 50%;
  transform: translate(-50%,-50%) scale(0);
  animation: rpl .48s linear forwards;
  pointer-events: none;
}
@keyframes rpl { to { transform: translate(-50%,-50%) scale(3.5); opacity: 0; } }

.pop-cb { animation: popcb .22s cubic-bezier(.34,1.56,.64,1); }
@keyframes popcb {
  0%   { transform: scale(1); }
  50%  { transform: scale(1.18); }
  100% { transform: scale(1); }
}

/* Info */
.habit-info { flex: 1; min-width: 0; }
.habit-name {
  font-size: 14px;
  color: #ddd;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: color .17s;
}
.habit-row.done .habit-name { color: #5DCAA5; }

/* Streak dots */
.dots { display: flex; align-items: center; gap: 4px; margin-top: 6px; }
.dot { width: 6px; height: 6px; border-radius: 50%; background: #222; transition: background .22s; }
.dot.lit { background: #5DCAA5; }
.streak-txt { font-size: 11px; color: #444; margin-left: 4px; }
.streak-txt.on { color: #5DCAA5; }

/* Footer */
.tr-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 18px;
  padding-top: 14px;
  border-top: 1px solid #1c1c1c;
}
.back-btn, .edit-btn {
  background: none;
  border: none;
  color: #555;
  font-size: 12px;
  cursor: pointer;
  font-family: inherit;
  padding: 0;
  transition: color .15s;
}
.back-btn:hover, .edit-btn:hover { color: #888; }

/* Edit modal */
.modal-bg {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.65);
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
.modal h2 { font-size: 15px; font-weight: 500; color: #e8e8e8; margin-bottom: 16px; }
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

  <!-- Welcome screen -->
  <div class="welcome" id="welcomeScreen">
    <div class="logo-ring">&#129340;</div>
    <h1>Welcome to<br>FamCare Sync</h1>
    <p>Build healthy habits together. Track your daily routines and keep your streaks alive.</p>
    <button class="start-btn" onclick="goTracker()">&#8594; Start logging your daily habits</button>
  </div>

  <!-- Tracker screen -->
  <div class="tracker" id="trackerScreen">
    <div class="tr-head">
      <div class="tr-brand">&#129340; FamCare Sync</div>
      <span class="tr-date" id="dateLabel"></span>
    </div>
    <div class="stats">
      <div class="stat"><div class="stat-n" id="sToday">0/5</div><div class="stat-l">Today</div></div>
      <div class="stat"><div class="stat-n" id="sBest">0</div><div class="stat-l">Best streak</div></div>
      <div class="stat"><div class="stat-n" id="sWeek">0%</div><div class="stat-l">This week</div></div>
    </div>
    <div id="habitList"></div>
    <div class="tr-footer">
      <button class="back-btn" onclick="goWelcome()">&#8592; Home</button>
      <button class="edit-btn" onclick="openEdit()">&#9998; Edit habits</button>
    </div>
  </div>

</div>

<!-- Edit modal -->
<div class="modal-bg" id="modalBg">
  <div class="modal">
    <h2>Edit your habits</h2>
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
const STORE_KEY = 'famcaresync_v1';

function loadState() {
  try { const s = localStorage.getItem(STORE_KEY); return s ? JSON.parse(s) : null; }
  catch(e) { return null; }
}
function saveState(st) {
  try { localStorage.setItem(STORE_KEY, JSON.stringify(st)); } catch(e) {}
}

let state = loadState() || { habits: DEFAULTS.slice(), completions: {}, lastScreen: 'welcome' };

function dateKey(off) {
  const d = new Date();
  d.setDate(d.getDate() + (off || 0));
  return d.toISOString().slice(0, 10);
}
function todayKey() { return dateKey(0); }

function getStreak(idx) {
  let n = 0;
  for (let x = 0; x >= -365; x--) {
    const c = state.completions[dateKey(x)] || {};
    if (c[idx]) n++; else break;
  }
  return n;
}
function getLast7(idx) {
  return Array.from({ length: 7 }, (_, x) => {
    const c = state.completions[dateKey(x - 6)] || {};
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
  for (let x = -6; x <= 0; x++) {
    total += state.habits.length;
    const c = state.completions[dateKey(x)] || {};
    done += Object.values(c).filter(Boolean).length;
  }
  return total ? Math.round(done / total * 100) : 0;
}
function todayDone() {
  const c = state.completions[todayKey()] || {};
  return Object.values(c).filter(Boolean).length;
}

function goWelcome() {
  document.getElementById('welcomeScreen').style.display = 'flex';
  document.getElementById('trackerScreen').style.display = 'none';
  state.lastScreen = 'welcome';
  saveState(state);
}
function goTracker() {
  document.getElementById('welcomeScreen').style.display = 'none';
  document.getElementById('trackerScreen').style.display = 'flex';
  state.lastScreen = 'tracker';
  saveState(state);
  render();
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
      setTimeout(() => r.remove(), 550);
      cb.classList.add('pop-cb');
      setTimeout(() => cb.classList.remove('pop-cb'), 300);
    }
  }
}

function render() {
  const today = new Date().toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
  document.getElementById('dateLabel').textContent = today;

  const done = todayDone();
  document.getElementById('sToday').textContent = done + '/' + state.habits.length;
  const best = Math.max(0, ...state.habits.map((_, i) => getBest(i)));
  document.getElementById('sBest').textContent = best;
  document.getElementById('sWeek').textContent = weekRate() + '%';

  const todayComp = state.completions[todayKey()] || {};
  document.getElementById('habitList').innerHTML = state.habits.map((h, i) => {
    const isDone = !!todayComp[i];
    const dots = getLast7(i);
    const streak = getStreak(i);
    const streakTxt = streak > 0 ? streak + ' day' + (streak !== 1 ? 's' : '') + ' streak' : 'no streak yet';
    return '<div class="habit-row' + (isDone ? ' done' : '') + '" onclick="toggleHabit(' + i + ')" role="checkbox" aria-checked="' + isDone + '" tabindex="0">'
      + '<div class="cb' + (isDone ? ' done' : '') + '" data-cb="' + i + '">'
      + '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="#04342C" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
      + '<polyline points="2,7 6,11 12,3"></polyline></svg></div>'
      + '<div class="habit-info"><div class="habit-name">' + h + '</div>'
      + '<div class="dots">'
      + dots.map(lit => '<div class="dot' + (lit ? ' lit' : '') + '"></div>').join('')
      + '<span class="streak-txt' + (streak > 0 ? ' on' : '') + '">' + streakTxt + '</span>'
      + '</div></div></div>';
  }).join('');

  document.querySelectorAll('[role=checkbox]').forEach((el, i) => {
    el.addEventListener('keydown', e => {
      if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); toggleHabit(i); }
    });
  });
}

function openEdit() {
  document.getElementById('editInputs').innerHTML = state.habits.map((h, i) =>
    '<input type="text" id="ei' + i + '" value="' + h.replace(/"/g, '&quot;') + '" placeholder="Habit ' + (i + 1) + '" />'
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

// Restore last screen on load
if (state.lastScreen === 'tracker') goTracker();
</script>
</body>
</html>
"""

def main():
    output_path = "famcare_sync.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(HTML)
    print(f"Generated: {output_path}")
    print()
    print("Open famcare_sync.html in any browser to use the app.")
    print()
    print("To host on your iPhone via local network:")
    print("  python -m http.server 8080")
    print("  Then visit http://<your-ip>:8080/famcare_sync.html on Safari")
    print()
    print("Or drag famcare_sync.html to netlify.com/drop for a free public URL.")

if __name__ == "__main__":
    main()
