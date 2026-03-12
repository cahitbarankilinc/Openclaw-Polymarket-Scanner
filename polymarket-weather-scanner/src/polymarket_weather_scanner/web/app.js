const state = { items: [], summary: null };
const summaryCards = document.getElementById('summaryCards');
const summaryCardTemplate = document.getElementById('summaryCardTemplate');
const walletList = document.getElementById('walletList');
const searchInput = document.getElementById('searchInput');
const qualifiedOnly = document.getElementById('qualifiedOnly');
const sortSelect = document.getElementById('sortSelect');
const refreshButton = document.getElementById('refreshButton');

async function load() {
  const [summaryRes, resultsRes] = await Promise.all([
    fetch('/api/summary'),
    fetch('/api/results?limit=500'),
  ]);
  state.summary = await summaryRes.json();
  state.items = await resultsRes.json();
  renderSummary();
  renderList();
}

function renderSummary() {
  summaryCards.innerHTML = '';
  const cards = [
    ['Toplam sonuç', state.summary.total],
    ['Qualified', state.summary.qualified],
    ['Ort. win rate', formatPercent(state.summary.avg_win_rate)],
    ['Ort. PnL', formatMoney(state.summary.avg_pnl)],
    ['Ort. weather ratio', formatPercent(state.summary.avg_weather_ratio)],
    ['En yüksek markets', formatInt(state.summary.top_markets)],
  ];
  for (const [label, value] of cards) {
    const node = summaryCardTemplate.content.firstElementChild.cloneNode(true);
    node.querySelector('.stat-label').textContent = label;
    node.querySelector('.stat-value').textContent = value;
    summaryCards.appendChild(node);
  }
}

function filteredItems() {
  let items = [...state.items];
  const query = searchInput.value.trim().toLowerCase();
  const mode = qualifiedOnly.value;
  const sortKey = sortSelect.value;
  if (query) {
    items = items.filter((item) => [item.username, item.address, item.source, item.qualification_reason]
      .filter(Boolean).some((value) => String(value).toLowerCase().includes(query)));
  }
  if (mode === 'qualified') items = items.filter((item) => item.qualified);
  if (mode === 'rejected') items = items.filter((item) => !item.qualified);
  items.sort((a, b) => valueForSort(b, sortKey) - valueForSort(a, sortKey));
  return items;
}

function valueForSort(item, key) {
  if (key === 'win_rate') return item.win_stats?.win_rate ?? 0;
  return item[key] ?? 0;
}

function renderList() {
  walletList.innerHTML = filteredItems().map(renderWalletCard).join('');
}

function renderWalletCard(item) {
  const win = item.win_stats || {};
  const grouped = win.grouped_buckets || [];
  const statusClass = item.qualified ? 'good' : 'bad';
  return `
    <a class="panel wallet-card" href="/wallet/${item.address}">
      <div class="wallet-main">
        <div>
          <div class="wallet-title-row">
            <strong>${escapeHtml(item.username || item.address)}</strong>
            <span class="badge ${statusClass}">${item.qualified ? 'qualified' : 'rejected'}</span>
          </div>
          <div class="address">${escapeHtml(item.address)}</div>
          <div class="wallet-metrics muted">
            <span>Genel win rate: <strong>${formatPercent(win.win_rate)}</strong></span>
            <span>Won: ${formatInt(win.wins)}</span>
            <span>Lost: ${formatInt(win.losses)}</span>
            <span>Sample: ${formatInt(win.analyzed_closed_positions)}</span>
            <span>PnL: ${formatMoney(item.pnl)}</span>
          </div>
        </div>
        <div class="bucket-grid">
          ${grouped.map(renderGroupedBucket).join('')}
        </div>
      </div>
    </a>
  `;
}

function renderGroupedBucket(bucket) {
  const cls = bucket.win_rate > 0.5 ? 'bucket-good' : 'bucket-bad';
  return `
    <div class="bucket-card ${cls}">
      <div class="bucket-label">${escapeHtml(bucket.label)}</div>
      <div class="bucket-rate">${formatPercent(bucket.win_rate)}</div>
      <div class="muted">Won: ${formatInt(bucket.wins)}</div>
      <div class="muted">Lost: ${formatInt(bucket.losses)}</div>
    </div>
  `;
}

function formatMoney(value) {
  if (value == null) return '—';
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(value);
}
function formatPercent(value) {
  if (value == null) return '—';
  return `%${(value * 100).toFixed(1)}`;
}
function formatInt(value) {
  if (value == null) return '—';
  return new Intl.NumberFormat('en-US').format(value);
}
function escapeHtml(value) {
  return String(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#39;');
}

[searchInput, qualifiedOnly, sortSelect].forEach((el) => el.addEventListener('input', renderList));
refreshButton.addEventListener('click', load);
load().catch((error) => { console.error(error); walletList.innerHTML = '<div class="panel empty-state">Veri yüklenemedi</div>'; });
