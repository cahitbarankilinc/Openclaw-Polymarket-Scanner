#!/usr/bin/env node
import fs from 'node:fs';

const SRC = '/Users/baran/.openclaw/workspace/automation/grok-telegram/last-response.md';
const DIR = '/Users/baran/.openclaw/workspace/automation/grok-telegram/reports';
fs.mkdirSync(DIR, { recursive: true });
const text = fs.readFileSync(SRC, 'utf8').trim();
if (!text) throw new Error('last-response.md is empty');
const now = new Date();
const stamp = now.toISOString().replace(/[:]/g, '-').replace(/\.\d{3}Z$/, 'Z');
const out = `${DIR}/${stamp}.md`;
fs.writeFileSync(out, text + '\n');
console.log(JSON.stringify({ ok: true, out }, null, 2));
