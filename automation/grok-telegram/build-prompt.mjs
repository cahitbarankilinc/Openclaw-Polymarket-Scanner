#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const BASE_PROMPT = '/Users/baran/Desktop/grok/promt.md';
const OUT_PROMPT = '/Users/baran/.openclaw/workspace/automation/grok-telegram/generated-prompt.md';
const REPORTS_DIR = '/Users/baran/.openclaw/workspace/automation/grok-telegram/reports';
const LAST_RESPONSE = '/Users/baran/.openclaw/workspace/automation/grok-telegram/last-response.md';
const MAX_REPORTS = 10;
const MAX_BULLETS = 3;

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
  const resultLine = lines.find(line => /Bugün en çok /i.test(line) || /Günün tek cümlelik ana sonucu/i.test(line));
  const compact = bullets.slice(0, MAX_BULLETS).map(s => s.replace(/\s+/g, ' ').slice(0, 140));
  const result = resultLine ? resultLine.replace(/\s+/g, ' ').slice(0, 140) : '';
  return { label, compact, result };
}

const base = readIfExists(BASE_PROMPT);
if (!base) throw new Error(`Base prompt not found: ${BASE_PROMPT}`);
const reports = listReports().map(r => ({ ...summarizeReport(r.inline ?? fs.readFileSync(r.path,'utf8'), extractDateLabel(r.name)) }));
const seenSection = reports.length
  ? ['## BENİM GÖRDÜKLERİM (son raporların çok kısa özeti)', ...reports.flatMap(r => {
      const head = `- ${r.label}: ${r.compact.join(' | ')}`.slice(0, 420);
      return r.result ? [head, `  sonuç: ${r.result}`.slice(0, 180)] : [head];
    }), '',
    'Bu bölüm daha önce önüme gelen şeylerin kısa hafızasıdır.',
    'Yeni raporda bu listedekileri kör tekrar etme.',
    'Öncelik: bu listedekilerin DIŞINDA son 24 saatte ortaya çıkan yeni sinyal, yeni açı, yeni para kazanma yöntemi, yeni araç, yeni kullanım şekli veya önceki güne göre anlamlı değişim.',
    'Eğer aynı konu tekrar gündemdeyse, sadece gerçekten yeni olan kısmını yaz; eskiyi yeniden uzun uzun anlatma.',
    ''].join('\n')
  : '';
const extraSection = `\n## EK İLGİ ALANLARIM\n- sosyal medya üzerinden para kazanma\n- n8n\n- polymarket\n\nBu alanlarda da özellikle şunları ara:\n- para kazanma modeli\n- yükselen use-case\n- Türkiye\'ye uyarlanabilir fırsat\n- hızlı test edilebilecek mikro ürün / servis fikri\n`;
const finalPrompt = `${base.trim()}\n\n${seenSection}${extraSection}\nEk yönlendirme:\n- Bana daha önce gördüğüm şeyleri tekrarlama; yeni olanı, değişeni ve gözden kaçırmış olabileceğim kısmı bul.\n- Özellikle sosyal medya monetization, n8n otomasyonları ve polymarket etrafındaki para kazanma fırsatlarını da tarayıp rapora yedir.\n`;
fs.writeFileSync(OUT_PROMPT, finalPrompt.trim() + '\n');
console.log(JSON.stringify({ ok: true, out: OUT_PROMPT, reportsUsed: reports.length }, null, 2));
