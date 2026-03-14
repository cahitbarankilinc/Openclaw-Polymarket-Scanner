const GROUPED_BUCKET_LABELS = ['0-15¢', '15-35¢', '35-65¢', '65-85¢', '85-100¢'];
const FAVORITES_STORAGE_KEY = 'polymarket-weather-scanner:favs';
const CATEGORY_ALIASES = {
  business: 'finance',
  pop_culture: 'culture',
};
const STATIC_CATEGORY_ORDER = ['favs', 'all', 'politics', 'sports', 'crypto', 'finance', 'culture', 'mentions', 'weather', 'economics', 'tech', 'custom'];

const state = {
  items: [],
  summary: null,
  scanState: null,
  bucketSort: null,
  activeCategory: 'all',
  favorites: new Set(loadFavorites()),
  loading: false,
  lastFullLoadAt: 0,
};
const summaryCards = document.getElementById('summaryCards');
const summaryCardTemplate = document.getElementById('summaryCardTemplate');
const walletList = document.getElementById('walletList');
const searchInput = document.getElementById('searchInput');
const outcomeInput = document.getElementById('outcomeInput');
const qualifiedOnly = document.getElementById('qualifiedOnly');
const sortSelect = document.getElementById('sortSelect');
const refreshButton = document.getElementById('refreshButton');
const refreshProgress = document.getElementById('refreshProgress');
const bucketFiltersGrid = document.getElementById('bucketFiltersGrid');
const resetBucketFiltersButton = document.getElementById('resetBucketFilters');
const categoryList = document.getElementById('categoryList');
const walletAddressInput = document.getElementById('walletAddressInput');
const addWalletButton = document.getElementById('addWalletButton');
const addWalletStatus = document.getElementById('addWalletStatus');

initBucketFilters();
renderCategories();

function setRefreshProgress(value, text = '') {
  refreshProgress.textContent = text || (value > 0 && value < 100 ? `%${value}` : '');
}

function renderScanProgress() {
  const scan = state.scanState;
  if (!scan) {
    setRefreshProgress(0, '');
    return;
  }
  if (scan.running) {
    const percent = Number(scan.percent || 0);
    const activeCategory = categoryLabel(normalizeCategory(scan.active_category || ''));
    const completed = Number(scan.completed_candidates || 0);
    const total = Number(scan.total_candidates || 0);
    const detail = activeCategory && activeCategory !== 'Unknown'
      ? ` · ${activeCategory} ${completed}/${total}`
      : ` · ${completed}/${total}`;
    setRefreshProgress(percent, `%${percent}${detail}`);
    return;
  }
  if (Number(scan.percent || 0) >= 100 && Number(scan.total_candidates || 0) > 0) {
    setRefreshProgress(100, '%100');
    setTimeout(() => {
      if (!state.scanState?.running) setRefreshProgress(0, '');
    }, 1200);
    return;
  }
  setRefreshProgress(0, '');
}

async function load(force = false) {
  if (state.loading) return;
  state.loading = true;
  refreshButton.disabled = true;
  try {
    setRefreshProgress(10);
    const summaryRes = await fetch('/api/summary');
    setRefreshProgress(35);
    const resultsRes = await fetch('/api/results?limit=5000');
    setRefreshProgress(60);
    const scanStateRes = await fetch('/api/scan-state');
    setRefreshProgress(80);
    state.summary = await summaryRes.json();
    state.items = await resultsRes.json();
    state.scanState = await scanStateRes.json();
    state.lastFullLoadAt = Date.now();
    if (!availableCategories().includes(state.activeCategory)) state.activeCategory = 'all';
    renderSummary();
    renderCategories();
    renderList();
    renderScanProgress();
  } finally {
    state.loading = false;
    refreshButton.disabled = false;
  }
}

function loadFavorites() {
  try {
    const raw = localStorage.getItem(FAVORITES_STORAGE_KEY);
    const items = raw ? JSON.parse(raw) : [];
    return Array.isArray(items) ? items : [];
  } catch {
    return [];
  }
}

function persistFavorites() {
  localStorage.setItem(FAVORITES_STORAGE_KEY, JSON.stringify([...state.favorites]));
}

function normalizeCategory(category) {
  const normalized = String(category || 'unknown').toLowerCase();
  return CATEGORY_ALIASES[normalized] || normalized;
}

function dynamicCategories() {
  const categories = new Set((state.items || []).map((item) => normalizeCategory(item.source_category)).filter(Boolean));
  return [...categories].filter((category) => !STATIC_CATEGORY_ORDER.includes(category)).sort();
}

function availableCategories() {
  return [...STATIC_CATEGORY_ORDER, ...dynamicCategories()];
}

function categoryLabel(category) {
  if (category === 'favs') return 'Favs';
  if (category === 'all') return 'All';
  if (category === 'custom') return 'Custom';
  if (category === 'weather_deep') return 'Weather Deep';
  if (category === 'custom_deep') return 'Custom Deep';
  if (category.endsWith('_deep')) return `${categoryLabel(category.slice(0, -5))} Deep`;
  return category.replaceAll('_', ' ').replace(/\b\w/g, (char) => char.toUpperCase());
}

function categoryCount(category) {
  if (category === 'favs') return state.items.filter((item) => state.favorites.has(item.address.toLowerCase())).length;
  if (category === 'all') return state.items.length;
  return state.items.filter((item) => normalizeCategory(item.source_category) === category).length;
}

function renderCategories() {
  categoryList.innerHTML = availableCategories().map((category) => `
    <button
      type="button"
      class="category-item${state.activeCategory === category ? ' active' : ''}"
      data-category="${category}"
    >
      <span>${categoryLabel(category)}</span>
      <span class="category-count">${formatInt(categoryCount(category))}</span>
    </button>
  `).join('');
}

function initBucketFilters() {
  bucketFiltersGrid.innerHTML = `
    <div class="bucket-filter-side">
      <div class="bucket-filter-side-inner">
        <div class="bucket-filter-row-labels">
          <div class="bucket-filter-row-label">Win Rate</div>
          <div class="bucket-filter-row-label">Activity</div>
        </div>
      </div>
    </div>
    <div class="bucket-filter-card-grid">
      ${GROUPED_BUCKET_LABELS.map((label, index) => renderBucketFilterCard(index, label)).join('')}
    </div>
  `;
}

function renderBucketFilterCard(index, label) {
  const winrateSortState = getBucketSortState(index, 'winrate');
  const activitySortState = getBucketSortState(index, 'activity');
  return `
    <div class="bucket-card bucket-filter-card" aria-label="${escapeHtml(label)} filtreleri">
      <div class="bucket-label">${escapeHtml(label)}</div>
      <div class="bucket-filter-card-body">
        <div class="bucket-filter-row">
          <input
            id="bucket-${index}-winrate-min"
            data-bucket-index="${index}"
            data-filter-kind="winrate-min"
            class="bucket-mini-input"
            type="number"
            min="0"
            max="100"
            step="0.1"
            placeholder="min"
          />
          <div class="bucket-max-cell">
            <input
              id="bucket-${index}-winrate-max"
              data-bucket-index="${index}"
              data-filter-kind="winrate-max"
              class="bucket-mini-input"
              type="number"
              min="0"
              max="100"
              step="0.1"
              placeholder="max"
            />
            <button
              type="button"
              class="bucket-sort-button${winrateSortState ? ' active' : ''}"
              data-sort-bucket-index="${index}"
              data-sort-metric="winrate"
              title="Win rate sıralama"
            >${sortButtonLabel(winrateSortState)}</button>
          </div>
        </div>
        <div class="bucket-filter-row">
          <input
            id="bucket-${index}-activity-min"
            data-bucket-index="${index}"
            data-filter-kind="activity-min"
            class="bucket-mini-input"
            type="number"
            min="0"
            step="1"
            placeholder="min"
          />
          <div class="bucket-max-cell">
            <input
              id="bucket-${index}-activity-max"
              data-bucket-index="${index}"
              data-filter-kind="activity-max"
              class="bucket-mini-input"
              type="number"
              min="0"
              step="1"
              placeholder="max"
            />
            <button
              type="button"
              class="bucket-sort-button${activitySortState ? ' active' : ''}"
              data-sort-bucket-index="${index}"
              data-sort-metric="activity"
              title="Activity sıralama"
            >${sortButtonLabel(activitySortState)}</button>
          </div>
        </div>
      </div>
    </div>
  `;
}

function isDeepCategory(category) {
  return String(category || '').endsWith('_deep') || category === 'weather_deep' || category === 'custom_deep';
}

function getStageProgress(stage) {
  const scan = state.scanState || {};
  const totals = scan.category_totals || {};
  const completed = scan.category_completed || {};
  const entries = Object.keys(totals).filter((key) => stage === 1 ? !isDeepCategory(key) : isDeepCategory(key));
  const total = entries.reduce((sum, key) => sum + Number(totals[key] || 0), 0);
  const done = entries.reduce((sum, key) => sum + Math.min(Number(completed[key] || 0), Number(totals[key] || 0)), 0);
  const percent = total ? Math.floor((done / total) * 100) : 0;
  return { done, total, percent };
}

function renderSummary() {
  if (!state.summary) return;
  summaryCards.innerHTML = '';
  const stage1 = getStageProgress(1);
  const stage2 = getStageProgress(2);
  const cards = [
    ['Toplam sonuç', state.summary.total],
    ['Qualified', state.summary.qualified],
    ['Stage 1', `${stage1.percent}%`],
    ['Stage 2', `${stage2.percent}%`],
  ];
  for (const [label, value] of cards) {
    const node = summaryCardTemplate.content.firstElementChild.cloneNode(true);
    node.querySelector('.stat-label').textContent = label;
    node.querySelector('.stat-value').textContent = value;
    summaryCards.appendChild(node);
  }
}

function currentOutcomeFilter() {
  return outcomeInput ? outcomeInput.value.trim().toLowerCase() : '';
}

function emptyWinStats() {
  return {
    analyzed_positions: 0,
    analyzed_closed_positions: 0,
    analyzed_open_loss_positions: 0,
    wins: 0,
    losses: 0,
    win_rate: 0,
    grouped_buckets: GROUPED_BUCKET_LABELS.map((label) => ({ label, total: 0, wins: 0, losses: 0, win_rate: 0 })),
  };
}

function displayWinStats(item) {
  const outcome = currentOutcomeFilter();
  const base = item.win_stats || emptyWinStats();
  if (!outcome) return base;
  return base.outcome_stats?.[outcome] || emptyWinStats();
}

function filteredItems() {
  let items = [...state.items];
  const query = searchInput.value.trim().toLowerCase();
  const mode = qualifiedOnly.value;
  const sortKey = sortSelect.value;
  const outcome = currentOutcomeFilter();

  if (state.activeCategory === 'favs') {
    items = items.filter((item) => state.favorites.has(item.address.toLowerCase()));
  } else if (state.activeCategory !== 'all') {
    items = items.filter((item) => normalizeCategory(item.source_category) === state.activeCategory);
  }

  if (query) {
    items = items.filter((item) => [item.username, item.address, item.source, item.source_category, item.qualification_reason]
      .filter(Boolean).some((value) => String(value).toLowerCase().includes(query)));
  }
  if (outcome) {
    items = items.filter((item) => (displayWinStats(item).analyzed_positions || 0) > 0);
  }
  if (mode === 'qualified') items = items.filter((item) => item.qualified);
  if (mode === 'rejected') items = items.filter((item) => !item.qualified);
  items = items.filter(matchesBucketFilters);
  items.sort((a, b) => compareItems(a, b, sortKey));
  return items;
}

function matchesBucketFilters(item) {
  const groupedBuckets = displayWinStats(item).grouped_buckets || [];
  return GROUPED_BUCKET_LABELS.every((label, index) => {
    const bucket = groupedBuckets.find((entry) => entry.label === label) || groupedBuckets[index] || null;
    const activity = bucket?.total ?? 0;
    const winRatePercent = (bucket?.win_rate ?? 0) * 100;
    const activityMin = getNumericFilterValue(index, 'activity-min');
    const activityMax = getNumericFilterValue(index, 'activity-max');
    const winRateMin = getNumericFilterValue(index, 'winrate-min');
    const winRateMax = getNumericFilterValue(index, 'winrate-max');

    if (activityMin != null && activity < activityMin) return false;
    if (activityMax != null && activity > activityMax) return false;
    if (winRateMin != null && winRatePercent < winRateMin) return false;
    if (winRateMax != null && winRatePercent > winRateMax) return false;
    return true;
  });
}

function getNumericFilterValue(bucketIndex, kind) {
  const input = document.querySelector(`[data-bucket-index="${bucketIndex}"][data-filter-kind="${kind}"]`);
  if (!input) return null;
  const value = input.value.trim();
  if (!value) return null;
  const num = Number(value);
  return Number.isFinite(num) ? num : null;
}

function getBucketSortState(bucketIndex, metric) {
  return state.bucketSort && state.bucketSort.bucketIndex === bucketIndex && state.bucketSort.metric === metric
    ? state.bucketSort.direction
    : null;
}

function sortButtonLabel(direction) {
  if (direction === 'desc') return '↓';
  if (direction === 'asc') return '↑';
  return '↕';
}

function getGroupedBucket(item, bucketIndex) {
  const groupedBuckets = displayWinStats(item).grouped_buckets || [];
  return groupedBuckets.find((entry) => entry.label === GROUPED_BUCKET_LABELS[bucketIndex]) || groupedBuckets[bucketIndex] || null;
}

function bucketMetricValue(item, bucketIndex, metric) {
  const bucket = getGroupedBucket(item, bucketIndex);
  if (!bucket) return 0;
  if (metric === 'winrate') return bucket.win_rate ?? 0;
  if (metric === 'activity') return bucket.total ?? 0;
  return 0;
}

function compareItems(a, b, key) {
  if (state.bucketSort) {
    const av = bucketMetricValue(a, state.bucketSort.bucketIndex, state.bucketSort.metric);
    const bv = bucketMetricValue(b, state.bucketSort.bucketIndex, state.bucketSort.metric);
    return state.bucketSort.direction === 'asc' ? av - bv : bv - av;
  }
  const av = key === 'win_rate' ? (displayWinStats(a).win_rate ?? 0) : (a[key] ?? 0);
  const bv = key === 'win_rate' ? (displayWinStats(b).win_rate ?? 0) : (b[key] ?? 0);
  return bv - av;
}

function renderList() {
  const items = filteredItems();
  walletList.innerHTML = items.length
    ? items.map(renderWalletCard).join('')
    : '<div class="panel empty-state">Bu kategoride/filtrede wallet bulunamadı.</div>';
}

function renderWalletCard(item) {
  const win = displayWinStats(item);
  const grouped = win.grouped_buckets || [];
  const statusClass = item.qualified ? 'good' : 'bad';
  const favorite = isFavorite(item.address);
  const rejectedReason = !item.qualified ? (item.qualification_reason || 'No rejection reason available') : '';
  return `
    <div class="panel wallet-card">
      <div class="wallet-main">
        <div>
          <div class="wallet-title-row">
            <button
              type="button"
              class="favorite-button${favorite ? ' active' : ''}"
              data-favorite-address="${escapeHtml(item.address)}"
              title="Favorilere ekle/kaldır"
              aria-label="Favorilere ekle/kaldır"
            >★</button>
            <strong>${escapeHtml(item.username || item.address)}</strong>
            <span class="badge ${statusClass}"${!item.qualified ? ` data-tooltip="${escapeHtml(rejectedReason)}" title="${escapeHtml(rejectedReason)}"` : ''}>${item.qualified ? 'qualified' : 'rejected'}</span>
            <span class="badge source-category">${escapeHtml(categoryLabel(normalizeCategory(item.source_category)))}</span>
          </div>
          <div class="address">${escapeHtml(item.address)}</div>
          <div class="wallet-metrics muted">
            <span>Genel win rate: <strong>${formatPercent(win.win_rate)}</strong></span>
            <span>Won: ${formatInt(win.wins)}</span>
            <span>Lost: ${formatInt(win.losses)}</span>
            <span>Sample: ${formatInt(win.analyzed_positions)}</span>
            <span>Closed: ${formatInt(win.analyzed_closed_positions)}</span>
            <span>Open loss: ${formatInt(win.analyzed_open_loss_positions)}</span>
            <span>PnL: ${formatMoney(item.pnl)}</span>
            <span>Trades: ${formatInt(item.last_trade_count)}</span>
            <span>Source: ${escapeHtml(item.source || '—')}</span>
          </div>
        </div>
        <div class="bucket-grid">
          ${grouped.map(renderGroupedBucket).join('')}
        </div>
      </div>
    </div>
  `;
}

function renderGroupedBucket(bucket) {
  const cls = bucket.win_rate > 0.5 ? 'bucket-good' : 'bucket-bad';
  return `
    <div class="bucket-card ${cls}">
      <div class="bucket-label">${escapeHtml(bucket.label)}</div>
      <div class="bucket-rate">${formatPercent(bucket.win_rate)}</div>
      <div class="muted">Activity: ${formatInt(bucket.total)}</div>
      <div class="muted">Won: ${formatInt(bucket.wins)}</div>
      <div class="muted">Lost: ${formatInt(bucket.losses)}</div>
    </div>
  `;
}

function isFavorite(address) {
  return state.favorites.has(String(address).toLowerCase());
}

function toggleFavorite(address) {
  const key = String(address).toLowerCase();
  if (state.favorites.has(key)) state.favorites.delete(key);
  else state.favorites.add(key);
  persistFavorites();
  renderCategories();
  renderList();
}

function cycleBucketSort(bucketIndex, metric) {
  const current = getBucketSortState(bucketIndex, metric);
  let next = 'desc';
  if (current === 'desc') next = 'asc';
  else if (current === 'asc') next = null;

  state.bucketSort = next ? { bucketIndex, metric, direction: next } : null;
  updateBucketSortButtons();
  renderList();
}

function updateBucketSortButtons() {
  document.querySelectorAll('[data-sort-bucket-index]').forEach((button) => {
    const bucketIndex = Number(button.dataset.sortBucketIndex);
    const metric = button.dataset.sortMetric;
    const direction = getBucketSortState(bucketIndex, metric);
    button.textContent = sortButtonLabel(direction);
    button.classList.toggle('active', Boolean(direction));
  });
}

function resetBucketFilters() {
  document.querySelectorAll('[data-bucket-index]').forEach((input) => {
    input.value = '';
  });
  renderList();
}

async function addWallet() {
  const address = walletAddressInput.value.trim().toLowerCase();
  if (!address) {
    addWalletStatus.textContent = 'Wallet address gir.';
    return;
  }
  addWalletStatus.textContent = 'Analiz ediliyor...';
  addWalletButton.disabled = true;
  walletAddressInput.disabled = true;
  try {
    const res = await fetch('/api/custom-wallets', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ address }),
    });
    const payload = await res.json();
    if (!res.ok) throw new Error(payload.error || 'wallet eklenemedi');
    addWalletStatus.textContent = `Eklendi: ${payload.address}`;
    walletAddressInput.value = '';
    await load();
  } catch (error) {
    addWalletStatus.textContent = error.message || 'wallet eklenemedi';
  } finally {
    addWalletButton.disabled = false;
    walletAddressInput.disabled = false;
  }
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

[searchInput, outcomeInput, qualifiedOnly, sortSelect].filter(Boolean).forEach((el) => el.addEventListener('input', renderList));
document.addEventListener('input', (event) => {
  if (event.target.matches('[data-bucket-index]')) renderList();
});
document.addEventListener('click', (event) => {
  const favoriteButton = event.target.closest('[data-favorite-address]');
  if (favoriteButton) {
    event.preventDefault();
    event.stopPropagation();
    toggleFavorite(favoriteButton.dataset.favoriteAddress);
    return;
  }

  const categoryButton = event.target.closest('[data-category]');
  if (categoryButton) {
    state.activeCategory = categoryButton.dataset.category;
    renderCategories();
    renderList();
    return;
  }

  const button = event.target.closest('[data-sort-bucket-index]');
  if (!button) return;
  cycleBucketSort(Number(button.dataset.sortBucketIndex), button.dataset.sortMetric);
});
refreshButton.addEventListener('click', load);
resetBucketFiltersButton.addEventListener('click', resetBucketFilters);
addWalletButton.addEventListener('click', addWallet);
walletAddressInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    event.preventDefault();
    addWallet();
  }
});
setInterval(async () => {
  try {
    if (state.loading) return;
    const res = await fetch('/api/scan-state');
    state.scanState = await res.json();
    renderScanProgress();
    renderSummary();
    const shouldRefreshData = state.scanState?.running && (Date.now() - state.lastFullLoadAt > 10000);
    if (shouldRefreshData) {
      await load();
    }
  } catch (error) {
    console.error(error);
  }
}, 2500);

load().catch((error) => { console.error(error); walletList.innerHTML = '<div class="panel empty-state">Veri yüklenemedi</div>'; });
