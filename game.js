// =========================================
//   ROCK PAPER SCISSORS — BATTLE ARENA
//   Game Logic & Animation Controller
// =========================================

// ---------- State ----------
const state = {
  playerScore: 0,
  cpuScore: 0,
  round: 1,
  history: [],
  isPlaying: false,
};

const CHOICES = ['rock', 'paper', 'scissors'];
const EMOJIS = { rock: '🪨', paper: '📄', scissors: '✂️' };
const BEATS = { rock: 'scissors', paper: 'rock', scissors: 'paper' };
const BEATS_DESC = {
  rock: 'Rock crushes Scissors',
  paper: 'Paper covers Rock',
  scissors: 'Scissors cut Paper',
};

// ---------- DOM Refs ----------
const playerEmojiEl    = document.getElementById('player-emoji');
const cpuEmojiEl       = document.getElementById('cpu-emoji');
const playerDisplayEl  = document.getElementById('player-display');
const cpuDisplayEl     = document.getElementById('cpu-display');
const playerChoiceName = document.getElementById('player-choice-name');
const cpuChoiceName    = document.getElementById('cpu-choice-name');
const resultBadge      = document.getElementById('result-badge');
const resultText       = document.getElementById('result-text');
const playerScoreEl    = document.getElementById('player-score');
const cpuScoreEl       = document.getElementById('cpu-score');
const roundInfoEl      = document.getElementById('round-info');
const instructionEl    = document.getElementById('instruction');
const actionsEl        = document.getElementById('actions');
const historySection   = document.getElementById('history-section');
const historyList      = document.getElementById('history-list');
const resultOverlay    = document.getElementById('result-overlay');
const modalEmoji       = document.getElementById('modal-emoji');
const modalTitle       = document.getElementById('modal-title');
const modalSubtitle    = document.getElementById('modal-subtitle');
const choiceBtns       = document.querySelectorAll('.choice-btn');

// ---------- Particle System ----------
function createParticles() {
  const container = document.getElementById('particles');
  const colors = ['#8b5cf6', '#ec4899', '#06b6d4', '#f59e0b', '#10b981', '#f97316'];
  for (let i = 0; i < 25; i++) {
    const p = document.createElement('div');
    p.classList.add('particle');
    const size = Math.random() * 5 + 2;
    p.style.cssText = `
      width: ${size}px;
      height: ${size}px;
      background: ${colors[Math.floor(Math.random() * colors.length)]};
      left: ${Math.random() * 100}%;
      --duration: ${Math.random() * 10 + 6}s;
      --delay: ${Math.random() * 8}s;
    `;
    container.appendChild(p);
  }
}

// ---------- Core Game ----------
function play(playerChoice) {
  if (state.isPlaying) return;
  state.isPlaying = true;

  // Disable buttons
  choiceBtns.forEach(b => b.disabled = true);
  actionsEl.style.display = 'none';

  // Show player's choice immediately
  playerEmojiEl.textContent = EMOJIS[playerChoice];
  playerChoiceName.textContent = playerChoice;
  playerDisplayEl.classList.add('revealed');

  // CPU "thinking" animation
  cpuEmojiEl.textContent = '🎲';
  cpuChoiceName.textContent = '...';
  cpuDisplayEl.classList.remove('revealed');

  // Update result badge to thinking
  resultBadge.className = 'result-badge';
  resultText.textContent = '⚡';
  instructionEl.textContent = 'CPU is choosing...';

  let thinkTicks = 0;
  const thinkInterval = setInterval(() => {
    cpuEmojiEl.textContent = EMOJIS[CHOICES[Math.floor(Math.random() * 3)]];
    thinkTicks++;
    if (thinkTicks > 10) {
      clearInterval(thinkInterval);
      revealResult(playerChoice);
    }
  }, 80);
}

function revealResult(playerChoice) {
  const cpuChoice = CHOICES[Math.floor(Math.random() * 3)];

  // Show CPU choice
  cpuEmojiEl.textContent = EMOJIS[cpuChoice];
  cpuChoiceName.textContent = cpuChoice;
  cpuDisplayEl.classList.add('revealed');

  // Determine winner
  let outcome;
  if (playerChoice === cpuChoice) {
    outcome = 'tie';
  } else if (BEATS[playerChoice] === cpuChoice) {
    outcome = 'win';
  } else {
    outcome = 'lose';
  }

  // Update scores
  if (outcome === 'win') {
    state.playerScore++;
    updateScore(playerScoreEl);
  } else if (outcome === 'lose') {
    state.cpuScore++;
    updateScore(cpuScoreEl);
  }

  playerScoreEl.textContent = state.playerScore;
  cpuScoreEl.textContent    = state.cpuScore;
  roundInfoEl.textContent   = `Round ${state.round}`;

  // Update result badge
  const badgeMap = {
    win: { cls:'win', label:'YOU WIN!' },
    lose: { cls:'lose', label:'YOU LOSE' },
    tie: { cls:'tie', label:'TIE!' },
  };
  const badge = badgeMap[outcome];
  resultBadge.className = `result-badge ${badge.cls}`;
  resultText.textContent = badge.label;

  // Instruction
  const instrMap = {
    win: BEATS_DESC[playerChoice] + ' — You win this round! 🎉',
    lose: BEATS_DESC[cpuChoice] + ' — CPU wins this round! 😞',
    tie: 'Great minds think alike! It\'s a tie! 🤝',
  };
  instructionEl.textContent = instrMap[outcome];

  // Shake loser display
  if (outcome === 'win') shakeEl(cpuDisplayEl);
  else if (outcome === 'lose') shakeEl(playerDisplayEl);

  // Flash overlay
  showOverlay(outcome, playerChoice, cpuChoice);

  // Log history
  addHistory(playerChoice, cpuChoice, outcome);

  // Increment round
  state.round++;

  // Show follow-up actions
  setTimeout(() => {
    choiceBtns.forEach(b => b.disabled = false);
    actionsEl.style.display = 'flex';
    historySection.style.display = 'block';
    state.isPlaying = false;
  }, 1200);
}

function updateScore(el) {
  el.classList.remove('score-bump');
  void el.offsetWidth; // reflow to restart animation
  el.classList.add('score-bump');
}

function shakeEl(el) {
  el.classList.remove('shake');
  void el.offsetWidth;
  el.classList.add('shake');
}

// ---------- Overlay Flash ----------
function showOverlay(outcome, playerChoice, cpuChoice) {
  const cfg = {
    win: {
      emoji: '🎉',
      title: 'Victory!',
      titleColor: '#10b981',
      subtitle: BEATS_DESC[playerChoice],
    },
    lose: {
      emoji: '💀',
      title: 'Defeated!',
      titleColor: '#ef4444',
      subtitle: BEATS_DESC[cpuChoice],
    },
    tie: {
      emoji: '🤝',
      title: 'Tie Game!',
      titleColor: '#f59e0b',
      subtitle: 'Both picked ' + playerChoice,
    },
  };

  const c = cfg[outcome];
  modalEmoji.textContent = c.emoji;
  modalTitle.textContent = c.title;
  modalTitle.style.background = `linear-gradient(135deg, ${c.titleColor}, white)`;
  modalTitle.style.webkitBackgroundClip = 'text';
  modalTitle.style.webkitTextFillColor = 'transparent';
  modalTitle.style.backgroundClip = 'text';
  modalSubtitle.textContent = c.subtitle;

  resultOverlay.style.display = 'flex';
  setTimeout(() => {
    resultOverlay.style.display = 'none';
  }, 1400);
}

// ---------- History ----------
function addHistory(playerChoice, cpuChoice, outcome) {
  const round = state.round;
  state.history.unshift({ round, playerChoice, cpuChoice, outcome });

  const item = document.createElement('div');
  item.classList.add('history-item');
  item.innerHTML = `
    <span class="history-round">Round ${round}</span>
    <span class="history-choices">
      <span class="emoji" title="Your choice">${EMOJIS[playerChoice]}</span>
      <span>${playerChoice}</span>
      <span class="arrow">vs</span>
      <span class="emoji" title="CPU choice">${EMOJIS[cpuChoice]}</span>
      <span>${cpuChoice}</span>
    </span>
    <span class="history-result ${outcome}">${outcome === 'win' ? 'WIN' : outcome === 'lose' ? 'LOSE' : 'TIE'}</span>
  `;
  historyList.prepend(item);

  // Keep max 10 entries in DOM
  while (historyList.children.length > 10) {
    historyList.removeChild(historyList.lastChild);
  }
}

// ---------- Play Again ----------
function playAgain() {
  // Reset displays
  playerEmojiEl.textContent = '❓';
  cpuEmojiEl.textContent = '❓';
  playerChoiceName.textContent = '—';
  cpuChoiceName.textContent = '—';
  playerDisplayEl.classList.remove('revealed', 'shake');
  cpuDisplayEl.classList.remove('revealed', 'shake');

  resultBadge.className = 'result-badge';
  resultText.textContent = 'Choose!';
  instructionEl.textContent = 'Select your weapon to begin the battle!';

  // Hide actions
  actionsEl.style.display = 'none';

  // Enable buttons
  choiceBtns.forEach(b => b.disabled = false);
}

// ---------- Reset Scores ----------
function resetGame() {
  state.playerScore = 0;
  state.cpuScore = 0;
  state.round = 1;
  state.history = [];

  playerScoreEl.textContent = '0';
  cpuScoreEl.textContent = '0';
  roundInfoEl.textContent = 'Round 1';

  historyList.innerHTML = '';
  historySection.style.display = 'none';

  playAgain();
}

// ---------- Keyboard Support ----------
document.addEventListener('keydown', (e) => {
  if (state.isPlaying) return;
  const m = { r: 'rock', p: 'paper', s: 'scissors' };
  if (m[e.key]) play(m[e.key]);
});

// ---------- Init ----------
createParticles();
