#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const BASE_PROMPT = '/Users/baran/Desktop/grok/promt.md';
const OUT_PROMPT = '/Users/baran/.openclaw/workspace/automation/grok-telegram/generated-prompt.md';
const REPORTS_DIR = '/Users/baran/.openclaw/workspace/automation/grok-telegram/reports';
const LAST_RESPONSE = '/Users/baran/.openclaw/workspace/automation/grok-telegram/last-response.md';
const MAX_REPORTS = 10;
const MAX_BULLETS = 2;

function ensureDir(dir) { fs.mkdirSync(dir, { recursive: true }); }
function readIfExists(p) { try { return fs.readFileSync(p, 'utf8'); } catch { return null; } }
function listReports() {
  ensureDir(REPORTS_DIR);
  const files = fs.readdirSync(REPORTS_DIR)
    .filter(name => name.endsWith('.md'))
    .map(name => ({ name, path: path.join(REPORTS_DIR, name), mtimeMs: fs.statSync(path.join(REPORTS_DIR, name)).mtimeMs }))
    .sort((a,b)=>b.mtimeMs-a.mtimeMs)
    .slice(0, MAX_REPORTS);
  if (files.length === 0) {
    const last = readIfExists(LAST_RESPONSE);
    if (last && last.trim()) return [{ name: 'last-response.md', path: LAST_RESPONSE, mtimeMs: Date.now(), inline: last }];
  }
  return files;
}
function extractDateLabel(fileName) {
  const m = fileName.match(/(\d{4}-\d{2}-\d{2})/);
  return m ? m[1] : fileName.replace(/\.md$/, '');
}
function summarizeReport(text, label) {
  const lines = text.split(/\r?\n/).map(x => x.trim()).filter(Boolean);
  const bullets = [];
  let inSummary = false;
  for (const line of lines) {
    if (/^1\.\s*GÜNLÜK ÖZET/i.test(line)) { inSummary = true; continue; }
    if (/^2\./.test(line)) break;
    if (inSummary) {
      if (/^[\-•]/.test(line)) bullets.push(line.replace(/^[\-•]\s*/, ''));
      else if (bullets.length === 0 && line.length > 30) bullets.push(line);
    }
    if (bullets.length >= MAX_BULLETS) break;
  }
  const resultLine = lines.find(line => /Bugün en çok /i.test(line));
  return {
    label,
    compact: bullets.slice(0, MAX_BULLETS).map(s => s.replace(/\s+/g, ' ').slice(0, 110)),
    result: resultLine ? resultLine.replace(/\s+/g, ' ').slice(0, 110) : ''
  };
}

const base = readIfExists(BASE_PROMPT);
if (!base) throw new Error(`Base prompt not found: ${BASE_PROMPT}`);
const reports = listReports().map(r => ({ ...summarizeReport(r.inline ?? fs.readFileSync(r.path,'utf8'), extractDateLabel(r.name)) }));
const seenSection = reports.length
  ? ['## BENİM GÖRDÜKLERİM', ...reports.flatMap(r => {
      const head = `- ${r.label}: ${r.compact.join(' | ')}`.slice(0, 260);
      return r.result ? [head, `  sonuç: ${r.result}`.slice(0, 140)] : [head];
    }),
    '',
    'Bunları uzun tekrar etme; yeni olanı, değişeni ve farklı açıyı bul.',
    'Aynı konu sürüyorsa sadece yeni kısmını yaz.',
    ''].join('\n')
  : '';
const extraSection = [
  '## EK İLGİ ALANLARI',
  '- sosyal medya monetization',
  '- n8n',
  '- polymarket',
  '',
  'Bunlarda özellikle: para modeli, yükselen use-case, TR’ye uyarlanabilir fırsat, hızlı test edilecek mikro ürün.'
].join('\n');
const finalPrompt = `${base.trim()}\n\n${seenSection}${extraSection}\n\nEk yönlendirme:\n- Daha önce gördüğüm şeyleri tekrar etme.\n- Yeni olanı ve para kazanma açısından en önemli farkı bul.\n`;
fs.writeFileSync(OUT_PROMPT, finalPrompt.trim() + '\n');
console.log(JSON.stringify({ ok: true, out: OUT_PROMPT, reportsUsed: reports.length }, null, 2));
