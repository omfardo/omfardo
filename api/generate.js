const RSS_FEEDS = [
  "https://feeds.reuters.com/Reuters/worldNews",
  "https://rsshub.app/apnews/topics/apf-topnews",
];

function decodeHtml(str) {
  return str
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");
}

function cleanText(text) {
  return decodeHtml(text)
    .replace(/\s+/g, " ")
    .replace(/\s*[-|]\s*Reuters$/i, "")
    .trim();
}

function extractTitles(xml) {
  const titles = [];
  const regex = /<item[\s\S]*?<title>([\s\S]*?)<\/title>[\s\S]*?<\/item>/gi;
  let match;
  while ((match = regex.exec(xml)) !== null) {
    const t = cleanText(match[1].replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, "$1"));
    if (t) titles.push(t);
  }
  return titles;
}

function dedupe(lines) {
  const seen = new Set();
  const out = [];
  for (const line of lines) {
    const key = line.toLowerCase().replace(/[^a-z0-9]+/g, "");
    if (key && !seen.has(key)) {
      seen.add(key);
      out.push(line);
    }
  }
  return out;
}

function makeSketches(headlines, count = 4) {
  return headlines.slice(0, count).map((h, i) => ({
    id: i + 1,
    konu: h,
    catisma: "Vatandaşın günlük derdi ile küresel sistemin soğuk dili çarpışıyor.",
    surpriz: "Çözmesi beklenen kurum, karikatürde sorunun kaynağına dönüşüyor.",
    punchline: "Biz haberi izliyoruz sanıyorduk, meğer haber bizi izliyormuş.",
    kompozisyon: "Tek panel; ön planda 2 karakter, arkada tek güçlü sembol.",
  }));
}

export default async function handler(req, res) {
  if (req.method !== "GET") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const allTitles = [];
    for (const feed of RSS_FEEDS) {
      try {
        const r = await fetch(feed, { headers: { "User-Agent": "omfardo-web-agent/1.0" } });
        const xml = await r.text();
        allTitles.push(...extractTitles(xml));
      } catch {
        allTitles.push(`[feed unavailable] ${feed}`);
      }
    }

    const unique = dedupe(allTitles).slice(0, 12);
    const briefing = unique.slice(0, 8);
    const sketches = makeSketches(unique, 4);

    return res.status(200).json({
      date: new Date().toISOString().slice(0, 10),
      briefing,
      sketches,
    });
  } catch (err) {
    return res.status(500).json({ error: "Generation failed", detail: String(err) });
  }
}
