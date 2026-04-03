# Omfardo Daily Cartoon Agent

Bu repo, her gün dünya gündeminden başlıkları toplayıp **Omfardo'nun çizgi evrenine uygun** karikatür esprisi/eskiz promptları üreten hafif bir ajan içerir.

## Ne yapar?
- Reuters World ve AP News RSS akışlarını çeker.
- Başlıkları sadeleştirir, tekrarları azaltır.
- Omfardo evrenine göre 10 maddelik bir "günlük briefing" ve 8 adet karikatür eskiz promptu üretir.
- Sonucu Markdown olarak `output/` klasörüne kaydeder.

## Çalıştırma

```bash
python3 agent/omfardo_daily_cartoon_agent.py
```

Opsiyonel ayarlar:

```bash
python3 agent/omfardo_daily_cartoon_agent.py \
  --profile prompts/omfardo_universe_profile.md \
  --out output/bugun.md \
  --max-headlines 16
```

## Otomatik günlük çalışma (cron)

UTC 07:00 için örnek cron:

```cron
0 7 * * * cd /workspace/omfardo && /usr/bin/python3 agent/omfardo_daily_cartoon_agent.py >> /workspace/omfardo/output/cron.log 2>&1
```

Bu sayede her gün hazır briefing + espri eskiz promptlarına sahip olursun.


## Tablet kullanımı (en kolay yol: GitHub)

Bilgisayar şart değil. Repo'yu GitHub'a atıp ajanı **GitHub Actions** ile çalıştırabilirsin.

1. Bu repoyu GitHub'a push et.
2. GitHub'da repo içinde **Actions** sekmesine gir.
3. "Daily Omfardo Cartoon Agent" workflow'unu aç.
4. İstersen **Run workflow** ile elle çalıştır, istersen günlük otomatik çalışsın (UTC 07:00).
5. Üretilen dosyalar `reports/` klasörüne commitlenir ve ayrıca artifact olarak indirilebilir.

Bu sayede tablette sadece GitHub uygulaması/Safari üzerinden çıktıyı okuyup çizime geçebilirsin.


Not: Workflow artık her gün raporu GitHub'da otomatik **Issue** olarak da açar; böylece tablette direkt Issues sekmesinden okuyabilirsin.


## Tek komutla GitHub kurulum (en kolay)

Aşağıdaki komut remote ayarını yapar ve `work` branch'ini GitHub'a push eder:

```bash
bash scripts/setup_github_easy.sh omfardo/omfardo-ajan
```

Bittikten sonra tablette direkt şu linkleri aç:
- `https://github.com/omfardo/omfardo-ajan/actions`
- `https://github.com/omfardo/omfardo-ajan/issues`


## Vercel web sürümü

Bu repo artık `index.html` + `api/generate.js` ile Vercel'de web arayüzü olarak çalışır.

- Buton: **Gündemi Tara & Esprile**
- API: `GET /api/generate`
- Çıktı: güncel briefing + 4 eskiz kartı

Vercel'de deploy sonrası doğrudan URL'den tabletle kullanabilirsin.
