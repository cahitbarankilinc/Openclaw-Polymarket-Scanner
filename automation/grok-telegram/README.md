# Grok / X.ai API otomasyonu

Bu klasör artık eski browser relay akışının değil, yeni X.ai API tabanlı Grok iş akışının talimatlarını içerir.

## Yeni mimari

Akış merkezi:
- `~/Desktop/x_search`

Temel mantık:
1. Baz prompt korunur (`prompt.base.txt`)
2. Son raporlardan kısa hafıza özeti çıkarılır
3. Bu özet `prompt.txt` içine eklenir
4. `node x-search-save-md.js` ile X.ai API request atılır
5. Cevap tarihli `grok-output-*.md` dosyasına yazılır
6. Kullanıcı follow-up soru sorarsa `node send-followup.js "soru"` ile son rapor bağlamlı yeni istek atılır

## Dosyalar

Bu klasörde:
- `agent-prompt.md` → Grok agent’ın ana sistem/talimat dosyası
- `cron-agent-message.md` → günlük rapor + follow-up görev akışı

`~/Desktop/x_search` içinde:
- `prompt.base.txt` → korunmuş baz prompt
- `prompt.txt` → güncel, hafıza eklenmiş aktif prompt
- `build-prompt.js` → son raporlardan kısa geçmiş özeti üretir ve `prompt.txt` dosyasını günceller
- `x-search-save-md.js` → X.ai API isteğini atar ve sonucu `.md` kaydeder
- `send-followup.js` → kullanıcının follow-up sorusunu son rapor bağlamıyla X.ai API’ye yollar
- `grok-output-*.md` → cevap arşivi

## Görev kuralları

### Günlük rapor
- Önce `node build-prompt.js`
- Sonra `node x-search-save-md.js`
- Gelen cevabı kullanıcıya düz metin olarak ilet

### Detay / follow-up
- `node send-followup.js "<kullanıcının sorusu>"`
- Sonucu kullanıcıya ilet

### Manuel test komutu
- Kullanıcı `test raporu` yazarsa bunu manuel günlük rapor tetikleme komutu olarak yorumla
- Çalıştırılacak akış:
  - `node build-prompt.js`
  - `node x-search-save-md.js`

## Önemli

- Browser / relay / grok.com akışı artık kullanılmayacak.
- Kaynak artık doğrudan X.ai API çağrısıdır.
- Kullanıcı detay istediğinde agent bunu otomatik follow-up request olarak yürütmelidir.
