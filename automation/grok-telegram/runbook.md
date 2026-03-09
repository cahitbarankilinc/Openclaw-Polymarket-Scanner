# Runbook

## Sabitler

- Chrome profil yolu: `~/.openclaw/chrome-grok-profile`
- Hedef URL: `https://grok.com/`
- Prompt kaynağı: `/Users/baran/Desktop/grok/promt.md`
- Son çıktı dosyası: `/Users/baran/.openclaw/workspace/automation/grok-telegram/last-response.md`

## UI bulma stratejisi

### 1. Modal kapatma
Önce şu buton varyasyonlarını ara:
- `Close`
- `Schließen`
- `Kapat`

### 2. Prompt giriş alanı
Öncelik sırası:
1. `[contenteditable="true"]`
2. Placeholder / görünen metin:
   - `Ask Grok`
   - `Frag Grok`
   - `Grok'a sor`

### 3. Gönder butonu
Etiket varyasyonları:
- `Send`
- `Absenden`
- `Gönder`

Fallback:
- `aria-label` içinde yukarı ok / send benzeri gönderim butonu

### 4. Cevap tamamlandı kontrolü
Birden fazla sinyal kullan:
- Son assistant mesajı mevcut mu?
- Metin 2 kontrol üst üste aynı mı?
- Copy butonu göründü mü?
- Stop generating benzeri buton kayboldu mu?

## DOM'dan son cevap çekme
Tercih sırası:
1. Assistant message container
2. `article`, `.message`, `.prose`, `[data-message-author-role]`
3. Son kullanıcı mesajını ayıklayıp en alttaki assistant bloğunu seç

## Kalıcılık

Akış sonunda her zaman:
- `last-response.md` güncellenir
- sonra aynı içerik Telegram'a yollanır

## Neden copy butonunu yedek yol yaptık?

Çünkü aynı işlev DOM okuma ile daha kararlı yapılabiliyor. Copy butonu UI değişikliklerinden daha çok etkilenebilir.
