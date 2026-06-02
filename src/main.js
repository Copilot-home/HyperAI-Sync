// Developer Cockpit Interaction Controller

document.addEventListener('DOMContentLoaded', () => {
  // Initialize Widgets
  initClock();
  initTheme();
  renderDiagnostics();
  renderMCPServers();
  renderCommands();
  
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
