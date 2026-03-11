#!/usr/bin/env node
import fs from 'node:fs';
import { spawnSync } from 'node:child_process';

const JOBS_PATH = process.env.OPENCLAW_CRON_JOBS || '/Users/baran/.openclaw/cron/jobs.json';
const TARGET_JOB_ID = process.env.GROK_REPORT_JOB_ID || '5b030397-7df3-421b-82b4-b6f6cde88056';
const TZ = 'Europe/Istanbul';
const RECOVER_AFTER_HOUR = 7;
const RECOVER_AFTER_MINUTE = 10;

function partsFor(ms) {
  const fmt = new Intl.DateTimeFormat('en-CA', {
    timeZone: TZ,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  });
  const parts = Object.fromEntries(fmt.formatToParts(new Date(ms)).filter(p => p.type !== 'literal').map(p => [p.type, p.value]));
  return {
    date: `${parts.year}-${parts.month}-${parts.day}`,
    hour: Number(parts.hour),
    minute: Number(parts.minute),
    second: Number(parts.second),
  };
}

function shouldRecover(nowParts, job) {
  if (!job?.enabled) return { ok: false, reason: 'job-disabled' };
  if (job.state?.runningAtMs) return { ok: false, reason: 'job-running' };
  if (nowParts.hour < RECOVER_AFTER_HOUR || (nowParts.hour === RECOVER_AFTER_HOUR && nowParts.minute < RECOVER_AFTER_MINUTE)) {
    return { ok: false, reason: 'before-recovery-window' };
  }
  const lastRunAtMs = job.state?.lastRunAtMs;
  const lastStatus = job.state?.lastRunStatus || job.state?.lastStatus;
  if (typeof lastRunAtMs === 'number') {
    const lastParts = partsFor(lastRunAtMs);
    if (lastParts.date === nowParts.date && lastStatus === 'ok') {
      return { ok: false, reason: 'already-ran-today' };
    }
    if (lastParts.date === nowParts.date && lastStatus !== 'ok') {
      return { ok: true, reason: `retry-today-after-${lastStatus}` };
    }
  }
  return { ok: true, reason: 'missed-today' };
}

const now = Date.now();
const nowParts = partsFor(now);
const raw = fs.readFileSync(JOBS_PATH, 'utf8');
const store = JSON.parse(raw);
const job = store.jobs.find(j => j.id === TARGET_JOB_ID);
if (!job) {
  console.log(JSON.stringify({ action: 'skip', reason: 'job-not-found', jobId: TARGET_JOB_ID }));
  process.exit(0);
}

const decision = shouldRecover(nowParts, job);
if (!decision.ok) {
  console.log(JSON.stringify({ action: 'skip', reason: decision.reason, jobId: TARGET_JOB_ID, localDate: nowParts.date, localTime: `${String(nowParts.hour).padStart(2,'0')}:${String(nowParts.minute).padStart(2,'0')}` }));
  process.exit(0);
}

const run = spawnSync('openclaw', ['cron', 'run', TARGET_JOB_ID], { encoding: 'utf8' });
const result = {
  action: run.status === 0 ? 'recovered' : 'error',
  reason: decision.reason,
  jobId: TARGET_JOB_ID,
  status: run.status,
  stdout: (run.stdout || '').trim(),
  stderr: (run.stderr || '').trim(),
};
console.log(JSON.stringify(result));
process.exit(run.status ?? 1);
