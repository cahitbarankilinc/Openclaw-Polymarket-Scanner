const pathParts = window.location.pathname.split('/');
const address = pathParts[pathParts.length - 1].toLowerCase();
const walletTitle = document.getElementById('walletTitle');
const walletAddress = document.getElementById('walletAddress');
const walletSummary = document.getElementById('walletSummary');
const detailBody = document.getElementById('detailBody');

async function loadWallet() {
  const res = await fetch(`/api/wallet?address=${encodeURIComponent(address)}`);
  if (!res.ok) throw new Error('wallet not found');
  const item = await res.json();
  const win = item.win_stats || {};
  walletTitle.textContent = item.username || item.address;
  walletAddress.textContent = item.address;

  const summaryCards = [
    ['Genel win rate', formatPercent(win.win_rate)],
    ['Won', formatInt(win.wins)],
    ['Lost', formatInt(win.losses)],
    ['Closed sample', formatInt(win.analyzed_closed_positions)],
    ['PnL', formatMoney(item.pnl)],
    ['Markets', formatInt(item.distinct_markets_traded)],
  ];
  walletSummary.innerHTML = summaryCards.map(([label, value]) => `
    <article class="panel stat-card">
      <span class="muted stat-label">${label}</span>
      <strong class="stat-value">${value}</strong>
    </article>
  `).join('');

  detailBody.innerHTML = (win.five_cent_buckets || []).map((bucket) => `
    <tr>
      <td>${bucket.label}</td>
      <td>${formatPercent(bucket.win_rate)}</td>
      <td>${formatInt(bucket.wins)}</td>
      <td>${formatInt(bucket.losses)}</td>
      <td>${formatInt(bucket.total)}</td>
    </tr>
  `).join('');
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

loadWallet().catch((error) => {
  console.error(error);
  walletTitle.textContent = 'Wallet bulunamadı';
});
