const state = {
  items: [],
  summary: null,
};

const summaryCards = document.getElementById('summaryCards');
const summaryCardTemplate = document.getElementById('summaryCardTemplate');
const resultsBody = document.getElementById('resultsBody');
const resultCount = document.getElementById('resultCount');
const sourceList = document.getElementById('sourceList');
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
  renderTable();
}

function renderSummary() {
  summaryCards.innerHTML = '';
  const cards = [
    ['Toplam sonuç', state.summary.total],
    ['Qualified', state.summary.qualified],
    ['Ort. PnL', formatMoney(state.summary.avg_pnl)],
    ['Ort. weather ratio', formatPercent(state.summary.avg_weather_ratio)],
    ['En yüksek PnL', formatMoney(state.summary.top_pnl)],
    ['En yüksek markets', formatInt(state.summary.top_markets)],
  ];

  for (const [label, value] of cards) {
    const node = summaryCardTemplate.content.firstElementChild.cloneNode(true);
    node.querySelector('.stat-label').textContent = label;
    node.querySelector('.stat-value').textContent = value;
    summaryCards.appendChild(node);
  }

  sourceList.textContent = `Sources: ${state.summary.sources.join(', ')}`;
}

function renderTable() {
  let items = [...state.items];
  const query = searchInput.value.trim().toLowerCase();
  const mode = qualifiedOnly.value;
  const sortKey = sortSelect.value;

  if (query) {
    items = items.filter((item) =>
      [item.username, item.address, item.source, item.qualification_reason]
        .filter(Boolean)
        .some((value) => String(value).toLowerCase().includes(query))
    );
  }

  if (mode === 'qualified') items = items.filter((item) => item.qualified);
  if (mode === 'rejected') items = items.filter((item) => !item.qualified);

  items.sort((a, b) => {
    const av = a[sortKey] ?? 0;
    const bv = b[sortKey] ?? 0;
    return bv - av;
  });

  resultCount.textContent = `${items.length} sonuç`;
  resultsBody.innerHTML = items.map(renderRow).join('');
}

function renderRow(item) {
  const statusClass = item.qualified ? 'good' : 'bad';
  const statusText = item.qualified ? 'qualified' : 'rejected';
  return `
    <tr>
      <td>${escapeHtml(item.username || '—')}</td>
      <td class="address">${escapeHtml(item.address)}</td>
      <td>${formatMoney(item.pnl)}</td>
      <td>${formatInt(item.distinct_markets_traded)}</td>
      <td>${formatInt(item.buy_trade_count)}</td>
      <td>${formatInt(item.sell_trade_count)}</td>
      <td>${formatInt(item.weather_trade_count)}</td>
      <td>${formatPercent(item.weather_trade_ratio)}</td>
      <td><span class="badge ${statusClass}">${statusText}</span></td>
      <td>${escapeHtml(item.qualification_reason)}</td>
    </tr>
  `;
}

function formatMoney(value) {
  if (value == null) return '—';
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(value);
}

function formatPercent(value) {
  if (value == null) return '—';
  return `${(value * 100).toFixed(2)}%`;
}

function formatInt(value) {
  if (value == null) return '—';
  return new Intl.NumberFormat('en-US').format(value);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

[searchInput, qualifiedOnly, sortSelect].forEach((el) => el.addEventListener('input', renderTable));
refreshButton.addEventListener('click', load);

load().catch((error) => {
  console.error(error);
  resultCount.textContent = 'Veri yüklenemedi';
});
