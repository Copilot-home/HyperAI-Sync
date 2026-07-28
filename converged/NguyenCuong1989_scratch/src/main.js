// Developer Cockpit Interaction Controller

document.addEventListener('DOMContentLoaded', () => {
  // Initialize Widgets
  initClock();
  initTheme();
  renderDiagnostics();
  renderMCPServers();
  renderCommands();
  initGitHub();
  initAIChat();
  
  // Register Search Event
  const searchInput = document.getElementById('command-search');
  if (searchInput) {
    searchInput.addEventListener('input', filterCommands);
  }
});

/* ==========================================================================
   REAL-TIME CLOCK & DATE WIDGET
   ========================================================================== */
function initClock() {
  const timeEl = document.getElementById('time-display');
  const dateEl = document.getElementById('date-display');
  
  if (!timeEl || !dateEl) return;
  
  const updateTime = () => {
    const now = new Date();
    
    // Format Time: HH:MM:SS
    const timeStr = now.toLocaleTimeString('en-US', {
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
    
    // Format Date: Day, Month Date, Year
    const dateStr = now.toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
    
    timeEl.textContent = timeStr;
    dateEl.textContent = dateStr;
  };
  
  updateTime();
  setInterval(updateTime, 1000);
}

/* ==========================================================================
   LIGHT / DARK THEME MANAGER
   ========================================================================== */
function initTheme() {
  const themeToggle = document.getElementById('theme-toggle');
  if (!themeToggle) return;
  
  const savedTheme = localStorage.getItem('theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeIcon(themeToggle, savedTheme);
  
  themeToggle.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(themeToggle, newTheme);
    showToast(`Switched to ${newTheme === 'dark' ? 'Dark Sleek' : 'Light Comfort'} Mode`);
  });
}

function updateThemeIcon(btn, theme) {
  btn.innerHTML = theme === 'dark' ? '☀️' : '🌙';
}

/* ==========================================================================
   ENVIRONMENT SPEC DIAGNOSTICS (Hardcoded with scanned data)
   ========================================================================== */
const DIAGNOSTIC_DATA = [
  { icon: '💻', title: 'Operating System', value: 'macOS' },
  { icon: '🟢', title: 'Node.js Version', value: 'v26.0.0' },
  { icon: '📦', title: 'NPM Version', value: 'v11.12.1' },
  { icon: '🐍', title: 'Python Version', value: '3.14.5' },
  { icon: '⚡', title: 'UV Version', value: 'v0.9.4' },
  { icon: '🌿', title: 'Git Version', value: '2.52.0' },
  { icon: '🍺', title: 'Homebrew', value: 'v5.1.14' },
  { icon: '🦖', title: 'Cloud Deployers', value: 'Vercel, Cloudflare, Netlify' }
];

function renderDiagnostics() {
  const container = document.getElementById('spec-list');
  if (!container) return;
  
  container.innerHTML = DIAGNOSTIC_DATA.map(spec => `
    <div class="spec-card">
      <span class="spec-icon">${spec.icon}</span>
      <span class="spec-title">${spec.title}</span>
      <span class="spec-value">${spec.value}</span>
    </div>
  `).join('');
}

/* ==========================================================================
   MCP SERVER CONNECTORS
   ========================================================================== */
const MCP_SERVERS = [
  { name: 'AlloyDB Remote', desc: 'Remote AlloyDB cluster access', status: 'idle' },
  { name: 'BigQuery Remote', desc: 'Read/write BigQuery datasets', status: 'idle' },
  { name: 'Cloud-SQL Remote', desc: 'Cloud SQL Instance operations', status: 'idle' },
  { name: 'Dataproc Remote', desc: 'Spark & Hadoop cluster runner', status: 'idle' },
  { name: 'Spanner Remote', desc: 'Global Spanner DB transactions', status: 'idle' },
  { name: 'Knowledge Catalog', desc: 'Data product annotations lookup', status: 'idle' }
];

function renderMCPServers() {
  const container = document.getElementById('mcp-list');
  const countEl = document.getElementById('mcp-count');
  if (!container) return;
  
  if (countEl) countEl.textContent = MCP_SERVERS.length;
  
  container.innerHTML = MCP_SERVERS.map(srv => `
    <div class="mcp-item">
      <div class="mcp-info">
        <span class="mcp-name">${srv.name}</span>
        <span class="mcp-status">
          <span class="status-dot ${srv.status}"></span>
          ${srv.status.toUpperCase()} — ${srv.desc}
        </span>
      </div>
      <button class="btn-toggle" onclick="toggleMcpStatus(this, '${srv.name}')">⚡</button>
    </div>
  `).join('');
}

window.toggleMcpStatus = function(btn, name) {
  const item = btn.closest('.mcp-item');
  const dot = item.querySelector('.status-dot');
  const statusText = item.querySelector('.mcp-status');
  
  const isActive = dot.classList.contains('active');
  
  if (isActive) {
    dot.className = 'status-dot idle';
    statusText.innerHTML = `<span class="status-dot idle"></span>IDLE — connection standby`;
    showToast(`Disconnected from ${name}`);
  } else {
    dot.className = 'status-dot active';
    statusText.innerHTML = `<span class="status-dot active"></span>ACTIVE — connected via lazy load`;
    showToast(`Connected to ${name} MCP server!`);
  }
};

/* ==========================================================================
   DEVELOPER COMMAND CLIPBOARD TOOLBOX
   ========================================================================== */
const DEVELOPER_COMMANDS = [
  { tag: 'git', code: 'git init && git add . && git commit -m "initial commit"', desc: 'Initialize standard repository & commit' },
  { tag: 'git', code: 'git checkout -b feature/amazing-feature', desc: 'Create and switch to new feature branch' },
  { tag: 'node', code: 'npm install', desc: 'Install project package dependencies' },
  { tag: 'node', code: 'npm run dev', desc: 'Launch Vite development hot-reloading server' },
  { tag: 'node', code: 'npm run build', desc: 'Compile optimized production build assets' },
  { tag: 'python', code: 'uv venv && source .venv/bin/activate', desc: 'Create & activate virtual env using superfast UV' },
  { tag: 'python', code: 'uv pip install numpy pandas requests', desc: 'Install base pip packages using UV' },
  { tag: 'cloudflare', code: 'npx wrangler dev', desc: 'Run Cloudflare worker functions locally' },
  { tag: 'vercel', code: 'vercel deploy', desc: 'Deploy app workspace directly to Vercel production' },
  { tag: 'agent', code: '/goal build a complete modern weather app', desc: 'Launch extra-thorough autonomous goals' }
];

function renderCommands() {
  const container = document.getElementById('command-list');
  if (!container) return;
  
  container.innerHTML = DEVELOPER_COMMANDS.map((cmd, idx) => `
    <div class="command-card" data-tag="${cmd.tag}" data-code="${cmd.code.toLowerCase()}" data-desc="${cmd.desc.toLowerCase()}">
      <div class="command-info">
        <span class="command-tag tag-${cmd.tag}">${cmd.tag}</span>
        <p class="command-desc">${cmd.desc}</p>
      </div>
      <div class="command-code-wrapper">
        <span class="command-code" title="${cmd.code}">${cmd.code}</span>
        <button class="btn-copy" onclick="copyCommand(this, '${btoa(cmd.code)}')">📋</button>
      </div>
    </div>
  `).join('');
}

function filterCommands(e) {
  const query = e.target.value.toLowerCase().trim();
  const cards = document.querySelectorAll('.command-card');
  
  cards.forEach(card => {
    const tag = card.getAttribute('data-tag');
    const code = card.getAttribute('data-code');
    const desc = card.getAttribute('data-desc');
    
    if (tag.includes(query) || code.includes(query) || desc.includes(query)) {
      card.style.display = 'flex';
    } else {
      card.style.display = 'none';
    }
  });
}

window.copyCommand = function(btn, encodedCode) {
  const code = atob(encodedCode);
  navigator.clipboard.writeText(code).then(() => {
    btn.classList.add('copied');
    btn.innerHTML = '✅';
    showToast(`Copied: "${code.substring(0, 30)}..."`);
    
    setTimeout(() => {
      btn.classList.remove('copied');
      btn.innerHTML = '📋';
    }, 1500);
  }).catch(err => {
    console.error('Clipboard copy failed', err);
  });
};

/* ==========================================================================
   TOAST NOTIFICATION TRIGGER
   ========================================================================== */
function showToast(message) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `<span>🚀</span> <span>${message}</span>`;
  
  container.appendChild(toast);
  
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(15px)';
    toast.style.transition = 'all 0.4s ease';
    setTimeout(() => toast.remove(), 400);
  }, 3000);
}

/* ==========================================================================
   GIT COMMIT & MERGE HUB GENERATOR LOGIC
   ========================================================================== */
function initGitHub() {
  const tabs = document.querySelectorAll('.git-tab');
  const panes = document.querySelectorAll('.git-pane');
  const commandOut = document.getElementById('git-compiled-command');
  const copyBtn = document.getElementById('btn-copy-git');

  if (!tabs.length || !panes.length || !commandOut || !copyBtn) return;

  let activeMode = 'commit';

  // Input elements
  const commitMsgEl = document.getElementById('commit-msg');
  const commitAddAllEl = document.getElementById('commit-add-all');
  const mergeTargetEl = document.getElementById('merge-target');
  const mergeSourceEl = document.getElementById('merge-source');
  const mergeNoFfEl = document.getElementById('merge-no-ff');
  const mergeSquashEl = document.getElementById('merge-squash');
  const branchNameEl = document.getElementById('branch-name');
  const branchCheckoutEl = document.getElementById('branch-checkout');

  // Tab switching
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      activeMode = tab.getAttribute('data-mode');
      
      panes.forEach(pane => {
        const id = pane.id;
        if (id === `pane-${activeMode}`) {
          pane.style.display = 'block';
        } else {
          pane.style.display = 'none';
        }
      });

      updateGitCommand();
    });
  });

  // Reactive compilation on keyup/change
  const inputs = [
    commitMsgEl, commitAddAllEl,
    mergeTargetEl, mergeSourceEl, mergeNoFfEl, mergeSquashEl,
    branchNameEl, branchCheckoutEl
  ];

  inputs.forEach(input => {
    if (input) {
      const eventType = input.type === 'checkbox' ? 'change' : 'input';
      input.addEventListener(eventType, updateGitCommand);
    }
  });

  // Dynamic compiler function
  function updateGitCommand() {
    let command = '';

    if (activeMode === 'commit') {
      const msg = commitMsgEl.value.trim().replace(/"/g, '\\"');
      const finalMsg = msg || 'update workspace';
      const addAll = commitAddAllEl.checked;
      
      command = addAll 
        ? `git add . && git commit -m "${finalMsg}"` 
        : `git commit -am "${finalMsg}"`;

    } else if (activeMode === 'merge') {
      const target = mergeTargetEl.value.trim() || 'main';
      const source = mergeSourceEl.value.trim() || 'feature-branch';
      const noFf = mergeNoFfEl.checked ? ' --no-ff' : '';
      const squash = mergeSquashEl.checked ? ' --squash' : '';
      
      command = `git checkout ${target} && git merge ${source}${noFf}${squash}`;

    } else if (activeMode === 'branch') {
      const name = branchNameEl.value.trim().toLowerCase().replace(/\s+/g, '-');
      const finalName = name || 'feature/new-branch';
      const checkout = branchCheckoutEl.checked;
      
      command = checkout 
        ? `git checkout -b ${finalName}` 
        : `git branch ${finalName}`;
    }

    commandOut.textContent = command;
  }

  // Copy button
  copyBtn.addEventListener('click', () => {
    const commandText = commandOut.textContent;
    navigator.clipboard.writeText(commandText).then(() => {
      showToast(`Copied Git command to clipboard!`);
    }).catch(err => {
      console.error('Failed to copy', err);
    });
  });

  // Initial compile
  updateGitCommand();
}

/* ==========================================================================
   AI CHAT PANEL — Gemini Cloud + Ollama Local
   ========================================================================== */
function initAIChat() {
  const messagesEl    = document.getElementById('ai-chat-messages');
  const inputEl       = document.getElementById('ai-chat-input');
  const sendBtn       = document.getElementById('btn-ai-send');
  const modelBtns     = document.querySelectorAll('.ai-model-btn');
  const configGemini  = document.getElementById('config-gemini');
  const configOllama  = document.getElementById('config-ollama');
  const geminiKeyEl   = document.getElementById('gemini-api-key');
  const saveKeyBtn    = document.getElementById('btn-save-gemini-key');
  const ollamaStatus  = document.getElementById('ollama-status');
  const geminiModel   = document.getElementById('gemini-model-select');
  const ollamaModel   = document.getElementById('ollama-model-select');

  if (!messagesEl || !inputEl || !sendBtn) return;

  let activeProvider = 'gemini';
  const GEMINI_KEY_STORAGE = 'cockpit_gemini_api_key';

  // --- Load saved Gemini key ---
  const savedKey = localStorage.getItem(GEMINI_KEY_STORAGE);
  if (savedKey && geminiKeyEl) geminiKeyEl.value = savedKey;

  // --- Save key button ---
  if (saveKeyBtn) {
    saveKeyBtn.addEventListener('click', () => {
      const key = geminiKeyEl.value.trim();
      if (!key) { showToast('⚠️ Nhập API key trước!'); return; }
      localStorage.setItem(GEMINI_KEY_STORAGE, key);
      showToast('✅ Gemini API key đã lưu!');
    });
  }

  // --- Provider Switch ---
  modelBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      modelBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeProvider = btn.dataset.provider;

      if (activeProvider === 'gemini') {
        configGemini.style.display = 'flex';
        configOllama.style.display = 'none';
      } else {
        configGemini.style.display = 'none';
        configOllama.style.display = 'flex';
        checkOllamaStatus();
      }
    });
  });

  // --- Check Ollama is running ---
  async function checkOllamaStatus() {
    if (!ollamaStatus) return;
    ollamaStatus.textContent = '⏳ Checking Ollama...';
    ollamaStatus.className = 'ollama-status-badge';
    try {
      const res = await fetch('http://localhost:11434/api/tags', { signal: AbortSignal.timeout(2500) });
      if (res.ok) {
        ollamaStatus.textContent = '🟢 Ollama Online';
        ollamaStatus.className = 'ollama-status-badge online';
      } else throw new Error();
    } catch {
      ollamaStatus.textContent = '🔴 Ollama Offline';
      ollamaStatus.className = 'ollama-status-badge offline';
    }
  }

  // --- Auto-grow textarea ---
  inputEl.addEventListener('input', () => {
    inputEl.style.height = 'auto';
    inputEl.style.height = Math.min(inputEl.scrollHeight, 160) + 'px';
  });

  // --- Enter to send, Shift+Enter = newline ---
  inputEl.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  sendBtn.addEventListener('click', sendMessage);

  // --- Append message bubble ---
  function appendMessage(role, content, streaming = false) {
    const isUser = role === 'user';
    const avatar = isUser ? '👤' : (activeProvider === 'gemini' ? '✨' : '🦙');
    
    const msgEl = document.createElement('div');
    msgEl.className = `ai-msg ${isUser ? 'user' : 'assistant'}`;
    
    const bubble = document.createElement('div');
    bubble.className = `ai-msg-bubble${streaming ? ' streaming' : ''}`;
    bubble.textContent = content;
    
    const avatarEl = document.createElement('div');
    avatarEl.className = 'ai-msg-avatar';
    avatarEl.textContent = avatar;
    
    msgEl.appendChild(avatarEl);
    msgEl.appendChild(bubble);
    messagesEl.appendChild(msgEl);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    
    return bubble;
  }

  // --- Send message logic ---
  async function sendMessage() {
    const text = inputEl.value.trim();
    if (!text) return;

    inputEl.value = '';
    inputEl.style.height = 'auto';
    appendMessage('user', text);
    
    sendBtn.classList.add('sending');
    document.getElementById('send-icon').textContent = '⏳';

    try {
      if (activeProvider === 'gemini') {
        await sendToGemini(text);
      } else {
        await sendToOllama(text);
      }
    } catch (err) {
      appendMessage('assistant', `❌ Lỗi: ${err.message}`);
    } finally {
      sendBtn.classList.remove('sending');
      document.getElementById('send-icon').textContent = '📤';
    }
  }

  // --- Gemini Streaming via REST ---
  async function sendToGemini(text) {
    const apiKey = localStorage.getItem(GEMINI_KEY_STORAGE) || geminiKeyEl?.value?.trim();
    if (!apiKey) {
      appendMessage('assistant', '⚠️ Chưa có Gemini API key! Bố nhập key rồi nhấn "Save Key" nhé.');
      return;
    }

    const model = geminiModel?.value || 'gemini-2.5-flash';
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:streamGenerateContent?alt=sse&key=${apiKey}`;

    const bubble = appendMessage('assistant', '', true);

    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{ role: 'user', parts: [{ text }] }],
        generationConfig: { temperature: 0.7, maxOutputTokens: 2048 }
      })
    });

    if (!res.ok) {
      const err = await res.json();
      bubble.classList.remove('streaming');
      bubble.textContent = `❌ Gemini error ${res.status}: ${err?.error?.message || 'Unknown'}`;
      return;
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let accumulated = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        const jsonStr = line.slice(6).trim();
        if (!jsonStr || jsonStr === '[DONE]') continue;
        try {
          const data = JSON.parse(jsonStr);
          const part = data?.candidates?.[0]?.content?.parts?.[0]?.text || '';
          accumulated += part;
          bubble.textContent = accumulated;
          messagesEl.scrollTop = messagesEl.scrollHeight;
        } catch {}
      }
    }

    bubble.classList.remove('streaming');
    if (!accumulated) bubble.textContent = '(Không có phản hồi)';
  }

  // --- Ollama via OpenAI-compatible streaming ---
  async function sendToOllama(text) {
    const model = ollamaModel?.value || 'qwen3:8b';
    const bubble = appendMessage('assistant', '', true);

    const res = await fetch('http://localhost:11434/v1/chat/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model,
        stream: true,
        messages: [{ role: 'user', content: text }]
      })
    });

    if (!res.ok) {
      bubble.classList.remove('streaming');
      bubble.textContent = `❌ Ollama error ${res.status}. Kiểm tra Ollama đang chạy chưa?`;
      return;
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let accumulated = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        const jsonStr = line.slice(6).trim();
        if (!jsonStr || jsonStr === '[DONE]') continue;
        try {
          const data = JSON.parse(jsonStr);
          const delta = data?.choices?.[0]?.delta?.content || '';
          accumulated += delta;
          bubble.textContent = accumulated;
          messagesEl.scrollTop = messagesEl.scrollHeight;
        } catch {}
      }
    }

    bubble.classList.remove('streaming');
    if (!accumulated) bubble.textContent = '(Không có phản hồi từ Ollama)';
  }
}
