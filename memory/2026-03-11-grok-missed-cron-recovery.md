# Grok missed cron recovery — 2026-03-11

- Kullanıcı isteği: Elektrik kesintisi / kapanma sonrası Grok günlük cron kaçarsa, sistem açılınca eksik işi bulup otomatik telafi etsin ve raporu o anda göndersin.
- İnceleme: OpenClaw içinde startup catch-up mantığı mevcut görünüyor, fakat yalnız buna güvenmek yerine Grok için ek emniyet katmanı kuruldu.
- Eklenen dosya: `automation/grok-telegram/recover-missed-report.mjs`
  - `jobs.json` içinden ana Grok günlük job'unu (`5b030397-7df3-421b-82b4-b6f6cde88056`) kontrol ediyor.
  - Europe/Istanbul bazında, 07:10 sonrası bugün başarılı run yoksa recovery tetikliyor.
  - Bugün zaten başarılı çalıştıysa skip ediyor.
  - Job çalışıyorsa skip ediyor.
  - Gerekirse `openclaw cron run <jobId>` ile telafi çalıştırıyor.
- Eklenen cron job:
  - id: `90aa3924-e1f6-4ac9-bbe3-115049d83b6b`
  - name: `grok-missed-report-recovery`
  - sıklık: her 15 dakikada bir
  - session: isolated
  - delivery: none
  - failure alert: Telegram / account `grok` / hedef `5046117769`
- Amaç: Sistem elektrik kesintisinden sonra geç açılırsa, periyodik recovery checker eksik günlük Grok raporunu fark edip ana job'u yeniden tetiklesin; rapor normal Grok hattından gelsin.
