// ============================================================
// APP LOGIC
// ============================================================
const solved = new Set(JSON.parse(localStorage.getItem('sql_solved') || '[]'));
let currentQ = 0;

function renderTable(tbl) {
  const t = TABLES[tbl];
  if (!t) return '';
  let h = `<div class="table-section"><h3>📋 Table: ${t.name}</h3><table class="schema-table"><tr>`;
  t.cols.forEach(c => h += `<th>${c}</th>`);
  h += '</tr>';
  t.rows.forEach(r => {
    h += '<tr>';
    r.forEach(v => h += `<td>${v === null ? '<em style="color:#484f58">NULL</em>' : v}</td>`);
    h += '</tr>';
  });
  h += '</table></div>';
  return h;
}

function diffBadge(d) {
  const cls = d === 'easy' ? 'badge-easy' : d === 'medium' ? 'badge-medium' : 'badge-hard';
  return `<span class="badge ${cls}">${d}</span>`;
}

function renderSidebar() {
  const list = document.getElementById('qList');
  let html = '';
  let lastSection = '';
  QUESTIONS.forEach((q, i) => {
    if (q.section !== lastSection) {
      html += `<div class="section-label">${q.section}</div>`;
      lastSection = q.section;
    }
    const s = solved.has(q.id) ? 'solved' : '';
    const a = i === currentQ ? 'active' : '';
    html += `<ul class="q-list"><li class="${s} ${a}" onclick="goTo(${i})"><span class="dot"></span><span class="num">${q.id}.</span>${q.concept}</li></ul>`;
  });
  list.innerHTML = html;

  document.getElementById('progressFill').style.width = (solved.size / QUESTIONS.length * 100) + '%';
  document.getElementById('progressText').textContent = `${solved.size} / ${QUESTIONS.length} solved`;
}

function renderQuestion() {
  const q = QUESTIONS[currentQ];
  const main = document.getElementById('main');
  let html = `
    <div class="q-header">
      <h1>Q${q.id}.</h1>
      ${diffBadge(q.difficulty)}
      <span class="concept-tag">${q.concept}</span>
      ${solved.has(q.id) ? '<span class="badge badge-easy">✓ Solved</span>' : ''}
    </div>
    <div class="q-description">${q.question}</div>
  `;

  q.tables.forEach(t => html += renderTable(t));

  html += `
    <div class="editor-section">
      <div class="editor-label">YOUR SQL QUERY</div>
      <textarea class="sql-input" id="sqlInput" placeholder="Write your SQL here..." spellcheck="false">${localStorage.getItem('sql_draft_' + q.id) || ''}</textarea>
    </div>
    <div class="btn-row">
      <button class="btn btn-primary" onclick="checkAnswer()">▶ Check Answer</button>
      <button class="btn btn-hint" onclick="showHint()">💡 Hint</button>
      <button class="btn btn-answer" onclick="showAnswer()">👁 Show Answer</button>
      <button class="btn" onclick="clearInput()">🗑 Clear</button>
    </div>
    <div id="feedback"></div>
    <div class="nav-row">
      ${currentQ > 0 ? '<button class="btn" onclick="goTo(' + (currentQ - 1) + ')">← Previous</button>' : ''}
      ${currentQ < QUESTIONS.length - 1 ? '<button class="btn btn-primary" onclick="goTo(' + (currentQ + 1) + ')">Next →</button>' : '<button class="btn badge-easy" style="padding:8px 18px;font-size:13px">🎉 All Done!</button>'}
    </div>
  `;

  main.innerHTML = html;
  main.scrollTop = 0;

  // Auto-save drafts
  document.getElementById('sqlInput').addEventListener('input', e => {
    localStorage.setItem('sql_draft_' + q.id, e.target.value);
  });
}

function checkAnswer() {
  const q = QUESTIONS[currentQ];
  const input = document.getElementById('sqlInput').value.trim();
  const fb = document.getElementById('feedback');

  if (!input) {
    fb.className = 'feedback wrong';
    fb.innerHTML = 'Please write a query first.';
    return;
  }

  if (q.validate(input)) {
    fb.className = 'feedback correct';
    fb.innerHTML = '✅ Correct! Well done. Your query matches the expected pattern.';
    solved.add(q.id);
    localStorage.setItem('sql_solved', JSON.stringify([...solved]));
    renderSidebar();
  } else {
    fb.className = 'feedback wrong';
    fb.innerHTML = '❌ Not quite. Check your syntax and try again. Use the hint if you\'re stuck.';
  }
}

function showHint() {
  const q = QUESTIONS[currentQ];
  const fb = document.getElementById('feedback');
  fb.className = 'feedback hint';
  fb.innerHTML = '💡 <strong>Hint:</strong> ' + q.hint;
}

function showAnswer() {
  const q = QUESTIONS[currentQ];
  const fb = document.getElementById('feedback');
  fb.className = 'feedback answer';
  fb.innerHTML = '👁 <strong>Answer:</strong><br><code>' + q.answer.replace(/</g, '&lt;') + '</code>';
}

function clearInput() {
  document.getElementById('sqlInput').value = '';
  document.getElementById('feedback').className = 'feedback';
  document.getElementById('feedback').innerHTML = '';
  localStorage.removeItem('sql_draft_' + QUESTIONS[currentQ].id);
}

function goTo(i) {
  currentQ = i;
  renderSidebar();
  renderQuestion();
}

// Keyboard shortcuts
document.addEventListener('keydown', e => {
  if (e.ctrlKey && e.key === 'Enter') checkAnswer();
});

// Init
renderSidebar();
renderQuestion();
