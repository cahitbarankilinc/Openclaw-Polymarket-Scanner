# Etsy + Canva + Sticker Automation Research Brief

Amaç: Etsy'de dijital sticker ürünlerini ölçekli şekilde listelemek için, Canva'daki ürünlerden başlayıp Etsy listing oluşturma akışını araştır.

Her çalıştırmada şunları yap:
1. Etsy listing upload automation için güncel kaynakları tara.
2. Özellikle şu başlıklarda yeni bilgi ara:
   - Etsy seller upload / listing creation automation
   - Browser automation with human-like UI interaction
   - Canva export/download automation possibilities and limits
   - VPS/Windows üzerinde kalıcı tarayıcı profili ile çalışma
   - Anti-bot / account safety / rate limiting / CAPTCHA riskleri
   - Yarı otomatik onay akışları vs tam otomatik akışlar
   - Paralel satılabilecek yüksek hacimli sticker / digital download marketplace'leri
   - GitHub projeleri, X tartışmaları, bloglar, forumlar, Google sonuçları
3. Mümkünse GitHub ve web kaynaklarını kullan.
4. X araştırması için /Users/baran/Desktop/x_search içindeki script altyapısını kullan; semantik arama ile bu alanın güncel durumunu kontrol et.
5. Bulduğun önemli sonuçları kısa maddeler halinde özetle.
6. Çıktıyı şu dosyaya append et: /Users/baran/.openclaw/workspace/research/etsy-sticker/hourly-log.md
7. Eğer gerçekten kritik bir gelişme varsa ayrıca aynı log içine "CRITICAL:" başlığıyla belirt.

Odak karar soruları:
- En güvenli mimari tam otomatik mi, yarı otomatik mi?
- Windows VPS + kalıcı browser profile + Playwright/Browser-use yaklaşımı uygun mu?
- Canva'dan ürün varlıklarını almak için resmi API, export otomasyonu, ya da insan-onaylı bir ara katman mı daha mantıklı?
- Etsy dışında Gumroad, Creative Market, Ko-fi, Design Bundles, Creative Fabrica, Shopify/Etsy kombinasyonu gibi kanallar ne kadar mantıklı?

Çıktı formatı:
- Başta ISO timestamp
- 5-12 madde
- Varsa linkler
- En sonda kısa verdict: "şimdilik öneri"
