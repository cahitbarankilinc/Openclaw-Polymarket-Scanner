# Polymarket Weather Scanner

Polymarket wallet scanner ve lokal dashboard.

Ana amaç:
- wallet adaylarını keşfetmek
- her wallet için trade / PnL / win-rate / bucket istatistiklerini hesaplamak
- **closed positions** ve seçilmiş **open position losses** verilerini birlikte dashboard'da göstermek

## Ne hesaplar?

Scanner her wallet için özetle şunları toplar:
- distinct markets traded
- son aktivitelerde BUY / SELL dağılımı
- closed positions win/loss istatistikleri
- grouped bucket win-rate'leri
- uygun open positions için ek loss/activity hesabı

## Open position handling

Open position verileri doğrudan genel win-rate akışına dahil edilir.

Kurallar:
- sadece `percentPnl` değeri **-101 ile -95** arasında olan open positions hesaba katılır
- bu kayıtlar **loss** kabul edilir
- bucket eşleşmesi için `avgPrice` kullanılır
- bu kayıtlar **activity / sample** sayısına eklenir
- bu aralık dışındaki open positions tamamen ignore edilir

Yani sonuçta wallet için görülen `Sample`, `Lost` ve bucket activity değerleri:
- closed positions
- + qualifying open-loss positions
birleşiminden oluşur.

## Wallet qualification logic

Bir wallet varsayılan olarak şu koşullarla qualified olur:
1. `distinct_markets_traded >= 200`
2. son `TRADE` aktivitelerinde `SELL` sayısı `0`
3. genel PnL pozitif

## Mimari notlar

Güncel sürümde:
- listede görünen wallet'lar gerçek analizden geçer
- seed-only placeholder kayıtlar dashboard sonuçlarında gösterilmez
- wallet değerlendirmesi sırasında şu istekler **paralel** çekilir:
  - `total_markets_traded`
  - `user_activity`
  - `closed_positions_all`
  - `open_positions`
- frontend asset cache problemi azaltmak için static dosyalarda no-cache header kullanılır

## Proje yapısı

- `src/polymarket_weather_scanner/` — ana uygulama
- `tests/` — testler
- `data/` — sqlite db, export dosyaları, scan state

## Gereksinimler

Sıfır bir bilgisayarda sadece şunların kurulu olması yeterli:
- Python 3
- Node.js

Not:
- Bu proje şu an Python tarafında ek üçüncü parti paket gerektirmiyor
- Node.js zorunlu çalışma bağımlılığı değil; ortamda kurulu olması yeterli

## Sıfırdan kurulum

### 1) Repoyu klonla

```bash
git clone <REPO_URL>
cd polymarket-weather-scanner
```

### 2) Python sürümünü kontrol et

```bash
python3 --version
```

### 3) İsteğe bağlı sanal ortam oluştur

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Bu proje standart kütüphane ile çalıştığı için ekstra `pip install -r requirements.txt` adımı gerekmiyor.

### 4) Testleri çalıştır

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Windows PowerShell:

```powershell
$env:PYTHONPATH = 'src'
python -m unittest discover -s tests -v
```

## Çalıştırma

### Full scan başlat

```bash
PYTHONPATH=src python3 -m polymarket_weather_scanner scan
```

### Sonuç raporu gör

```bash
PYTHONPATH=src python3 -m polymarket_weather_scanner report --limit 25
```

### JSON export

```bash
PYTHONPATH=src python3 -m polymarket_weather_scanner export --format json --out data/latest-wallets.json
```

### CSV export

```bash
PYTHONPATH=src python3 -m polymarket_weather_scanner export --format csv --out data/latest-wallets.csv
```

### Dashboard / local web UI aç

```bash
PYTHONPATH=src python3 -m polymarket_weather_scanner serve --host 127.0.0.1 --port 8765
```

Ardından tarayıcıda aç:

```text
http://127.0.0.1:8765
```

## En hızlı günlük kullanım

Bir terminalde dashboard server:

```bash
cd polymarket-weather-scanner
PYTHONPATH=src python3 -m polymarket_weather_scanner serve --host 127.0.0.1 --port 8765
```

Başka terminalde scan:

```bash
cd polymarket-weather-scanner
PYTHONPATH=src python3 -m polymarket_weather_scanner scan
```

## Kullanışlı notlar

- `data/scanner.db` içinde sonuçlar tutulur
- `data/scan-state.json` aktif scan progress bilgisini taşır
- dashboard `Yenile` ile son sonuçları tekrar okur
- stale frontend sorunu yaşamamak için static asset cache kapatılmıştır

## Sorun giderme

### Dashboard açık ama veri eski görünüyor

Şunları sırayla dene:

1. server'ı yeniden başlat
2. sayfayı hard refresh yap
3. yeni scan çalıştır

### Port kullanımda

Farklı port ile aç:

```bash
PYTHONPATH=src python3 -m polymarket_weather_scanner serve --host 127.0.0.1 --port 8787
```

### Test / import hatası

Komutlarda `PYTHONPATH=src` kullandığından emin ol.

## Lisans / not

Dahili kullanım için geliştirildi; ihtiyaç oldukça genişletilebilir.
