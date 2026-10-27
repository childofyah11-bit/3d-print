:root {
  --bg: #0b1120;
  --bg-soft: #111827;
  --panel: rgba(17, 24, 39, 0.9);
  --panel-strong: #111827;
  --card: #0f172a;
  --card-alt: #172033;
  --line: rgba(148, 163, 184, 0.2);
  --text: #e2e8f0;
  --text-muted: #94a3b8;
  --primary: #60a5fa;
  --primary-strong: #2563eb;
  --success: #34d399;
  --warning: #fbbf24;
  --danger: #f87171;
  --shadow: 0 18px 35px rgba(2, 6, 23, 0.45);
}

* {
  box-sizing: border-box;
}

html {
  background: var(--bg);
  color: var(--text);
  scroll-behavior: smooth;
}

body {
  margin: 0;
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(96, 165, 250, 0.14), transparent 25%),
    radial-gradient(circle at bottom right, rgba(52, 211, 153, 0.1), transparent 20%),
    var(--bg);
  color: var(--text);
  font-family: "Inter", sans-serif;
}

button,
input,
select {
  font: inherit;
}

button {
  cursor: pointer;
}

.app-shell {
  max-width: 1280px;
  margin: 0 auto;
  padding: 24px 18px 60px;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 18px 20px;
  border: 1px solid var(--line);
  background: rgba(15, 23, 42, 0.86);
  border-radius: 18px;
  box-shadow: var(--shadow);
  backdrop-filter: blur(14px);
}

.brand-wrap {
  display: flex;
  align-items: center;
  gap: 14px;
}

.brand-mark {
  display: grid;
  place-items: center;
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--primary), var(--primary-strong));
  color: #f8fafc;
  font-weight: 800;
}

.eyebrow {
  margin: 0;
  color: var(--text-muted);
  text-transform: uppercase;
  font-size: 0.7rem;
  letter-spacing: 0.12em;
}

h1,
h2,
h3,
p {
  margin: 0;
}

h1 {
  font-size: clamp(1.4rem, 2vw, 2.1rem);
}

.primary-button,
.ghost-button,
.danger-button,
.tab-button {
  border: 1px solid transparent;
  border-radius: 12px;
  transition: transform 0.2s ease, border-color 0.2s ease, background 0.2s ease;
}

.primary-button,
.ghost-button,
.danger-button {
  padding: 0.75rem 1rem;
  font-weight: 600;
}

.primary-button {
  color: #f8fafc;
  background: linear-gradient(135deg, var(--primary), var(--primary-strong));
  box-shadow: 0 10px 20px rgba(37, 99, 235, 0.3);
}

.ghost-button {
  background: transparent;
  color: var(--text);
  border-color: var(--line);
}

.danger-button {
  background: rgba(248, 113, 113, 0.12);
  color: #fecaca;
  border-color: rgba(248, 113, 113, 0.25);
}

.primary-button:hover,
.ghost-button:hover,
.danger-button:hover,
.tab-button:hover {
  transform: translateY(-1px);
}

.tab-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 22px 0 18px;
}

.tab-button {
  background: rgba(15, 23, 42, 0.75);
  color: var(--text-muted);
  border-color: var(--line);
  padding: 0.8rem 1.1rem;
  font-weight: 600;
}

.tab-button.active {
  background: rgba(96, 165, 250, 0.14);
  border-color: rgba(96, 165, 250, 0.42);
  color: var(--text);
}

.content-area {
  min-height: 560px;
}

.tab-panel {
  display: none;
}

.tab-panel.active {
  display: block;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.section-label {
  color: var(--text-muted);
  font-size: 0.75rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 6px;
}

.panel-grid {
  display: grid;
  gap: 18px;
}

.two-column {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.one-column {
  grid-template-columns: 1fr;
}

.wide-gap {
  gap: 25px;
}

.panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 20px;
  border: 1px solid var(--line);
  border-radius: 18px;
  background: rgba(15, 23, 42, 0.86);
  box-shadow: var(--shadow);
}

.form-panel {
  padding-bottom: 18px;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.panel-header.compact {
  align-items: center;
}

.chip {
  display: inline-flex;
  align-items: center;
  padding: 0.4rem 0.7rem;
  border-radius: 999px;
  background: rgba(52, 211, 153, 0.1);
  color: #a7f3d0;
  border: 1px solid rgba(52, 211, 153, 0.2);
  font-size: 0.72rem;
  font-weight: 700;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.stat-card {
  padding: 20px;
  border: 1px solid var(--line);
  border-radius: 18px;
  background: linear-gradient(180deg, rgba(17, 24, 39, 0.8), rgba(15, 23, 42, 0.94));
}

.stat-label {
  color: var(--text-muted);
  font-size: 0.8rem;
  margin-bottom: 6px;
}

.stat-value {
  font-size: clamp(1.5rem, 2vw, 2.5rem);
  font-weight: 800;
}

.recommendation-panel {
  display: grid;
  gap: 12px;
}

.recommendation-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.big-score {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 800;
}

.meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.meta-pill {
  padding: 0.4rem 0.7rem;
  border-radius: 999px;
  background: rgba(96, 165, 250, 0.12);
  color: #bfdbfe;
  border: 1px solid rgba(96, 165, 250, 0.2);
  font-size: 0.76rem;
}

.bullet-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 12px;
  color: var(--text-muted);
}

.bullet-list li {
  position: relative;
  padding-left: 1.1rem;
}

.bullet-list li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: var(--primary);
}

.field-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.field-grid.single-column {
  grid-template-columns: 1fr;
}

label {
  display: flex;
  flex-direction: column;
  gap: 8px;
  color: var(--text-muted);
  font-size: 0.82rem;
}

input,
select {
  background: rgba(15, 23, 42, 0.9);
  color: var(--text);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 0.8rem 0.9rem;
}

input:focus,
select:focus {
  outline: 2px solid rgba(96, 165, 250, 0.35);
  border-color: rgba(96, 165, 250, 0.42);
}

.search-input {
  max-width: 260px;
  width: 100%;
}

.form-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 12px;
}

.stack-list {
  display: grid;
  gap: 12px;
}

.profile-item,
.queue-item,
.filament-card {
  border: 1px solid var(--line);
  border-radius: 16px;
  background: rgba(15, 23, 42, 0.72);
}

.profile-item,
.queue-item {
  padding: 16px;
}

.profile-item-header,
.queue-item-header {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  align-items: center;
  margin-bottom: 10px;
}

.profile-item h4,
.queue-item h4,
.filament-card h4 {
  margin: 0;
  font-size: 1.05rem;
}

.item-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 10px;
}

.action-button {
  border: 1px solid var(--line);
  background: rgba(15, 23, 42, 0.8);
  color: var(--text);
  border-radius: 10px;
  padding: 0.5rem 0.8rem;
  font-size: 0.8rem;
}

.action-button.delete {
  color: #fecaca;
  border-color: rgba(248, 113, 113, 0.4);
}

.meta-line {
  color: var(--text-muted);
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 0.82rem;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.filament-card {
  padding: 16px;
}

.filament-card .badge {
  display: inline-flex;
  margin-bottom: 10px;
  padding: 0.35rem 0.6rem;
  border-radius: 999px;
  background: rgba(52, 211, 153, 0.12);
  color: #a7f3d0;
  border: 1px solid rgba(52, 211, 153, 0.2);
  font-size: 0.72rem;
  font-weight: 700;
}

.priority-tag {
  font-size: 0.72rem;
  padding: 0.3rem 0.6rem;
  border-radius: 999px;
  border: 1px solid var(--line);
  color: var(--text-muted);
}

.priority-tag.high { background: rgba(248, 113, 113, 0.12); color: #fecaca; }
.priority-tag.normal { background: rgba(96, 165, 250, 0.12); color: #bfdbfe; }
.priority-tag.low { background: rgba(52, 211, 153, 0.12); color: #a7f3d0; }

.toggle-row {
  flex-direction: row !important;
  align-items: center;
  justify-content: space-between;
  padding: 0.8rem 0.9rem;
  border: 1px solid var(--line);
  border-radius: 12px;
  background: rgba(15, 23, 42, 0.9);
}

.toggle-row input {
  width: 18px;
  height: 18px;
}

.empty-state {
  padding: 18px;
  border: 1px dashed var(--line);
  border-radius: 12px;
  color: var(--text-muted);
  text-align: center;
}

@media (max-width: 860px) {
  .stats-grid,
  .two-column,
  .field-grid {
    grid-template-columns: 1fr;
  }

  .topbar {
    flex-wrap: wrap;
  }

  .brand-wrap {
    width: 100%;
  }

  .primary-button,
  .ghost-button,
  .danger-button {
    width: 100%;
  }

  .tab-nav {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 480px) {
  .app-shell {
    padding-left: 12px;
    padding-right: 12px;
  }

  .topbar,
  .panel {
    padding: 16px;
  }

  .tab-nav {
    grid-template-columns: 1fr;
  }
}
