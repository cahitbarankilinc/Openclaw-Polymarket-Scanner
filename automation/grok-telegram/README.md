# Grok → Telegram otomasyonu

Bu klasör, Grok cevabını tarayıcıdan alıp Telegram'a ileten akış için çalışma dosyalarını içerir.

## Mimari

Bu akışın tarayıcı tıklama kısmı **OpenClaw agent** içinde çalışır.
Sebep: `browser` ve `message` yetkileri doğrudan agent araçlarıdır; düz bir yerel script bunlara doğal olarak erişmez.

Akış:

1. Sabit Chrome profili kullanılır: `~/.openclaw/chrome-grok-profile`
2. Her çalışmada `https://grok.com/` açılır veya mevcut Grok sekmesi bu URL'ye yönlendirilir
3. Agent, önce temel prompt + kısa geçmiş özetlerinden derlenmiş kompakt promptu üretir
4. Browser Relay üzerinden Grok sekmesine bağlanır
5. Prompt'u yapıştırır ve gönderir
6. Yanıt tamamlanana kadar bekler
7. Son assistant mesajını DOM'dan çeker
8. Sonucu dosyaya kaydeder ve arşive atar
9. Sonucu Telegram'a düz metin olarak yollar; mesaj çok uzunsa birkaç parçaya böler

## Dosyalar

- `agent-prompt.md` → agent'e verilecek operasyon talimatı
- `runbook.md` → tarayıcı tarafında hangi öğelerin nasıl bulunduğu
- `schedule-example.sh` → örnek cron kayıt komutu
- `/Users/baran/Desktop/grok/promt.md` → temel prompt kaynağı
- `build-prompt.mjs` → son raporlardan kısa “Benim gördüklerim” özeti üretip kompakt prompt oluşturur
- `generated-prompt.md` → Grok'a giden nihai prompt
- `archive-last-report.mjs` → son raporu tarih damgasıyla arşive yazar
- `reports/` → geçmiş rapor arşivi

## Kullanım şekilleri

### 1) Manuel tetikleme
Bir agent turn veya sub-agent, `agent-prompt.md` talimatını izleyerek akışı çalıştırır.

### 2) Cron ile otomatik
`schedule-example.sh` içindeki komutu kendine göre düzenleyip çalıştır.

## Gerekenler

- Chrome'da doğru profil: `~/.openclaw/chrome-grok-profile`
- Grok oturumu açık
- İlgili sekmede Browser Relay bağlı
- Telegram hesabı OpenClaw tarafında bağlı
- Bu akış için gönderici hesabı: `grok` (`@cbaranksgrok_bot`)
- Telegram hedef chat id / kullanıcı adı belli

## Not

Bu yapıda "Copy" butonu birincil yol değildir. Önce DOM'dan son Grok yanıtı çekilir.
Gerekirse kopyalama butonu yedek yol olarak kullanılabilir. Bu, UI değişikliklerine karşı daha dayanıklıdır.
