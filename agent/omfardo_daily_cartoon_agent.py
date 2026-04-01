#!/usr/bin/env python3
"""Generate daily world-news-based cartoon sketch prompts for Omfardo universe."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import textwrap
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable

RSS_FEEDS = [
    "https://feeds.reuters.com/Reuters/worldNews",
    "https://rsshub.app/apnews/topics/apf-topnews",
]


def fetch_rss_titles(url: str, timeout: int = 15) -> list[str]:
    req = urllib.request.Request(url, headers={"User-Agent": "omfardo-agent/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    root = ET.fromstring(data)
    items = root.findall(".//item/title")
    return [clean_text(i.text or "") for i in items if (i.text or "").strip()]


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s*[-|]\s*Reuters$", "", text, flags=re.IGNORECASE)
    return text


def dedupe_keep_order(lines: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for line in lines:
        key = re.sub(r"[^a-z0-9]+", "", line.lower())
        if key and key not in seen:
            seen.add(key)
            out.append(line)
    return out


def load_profile(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def build_briefing(headlines: list[str], max_items: int = 10) -> str:
    picks = headlines[:max_items]
    lines = [f"{i+1}. {h}" for i, h in enumerate(picks)]
    return "\n".join(lines)


def make_prompt_blocks(headlines: list[str], count: int = 8) -> str:
    selected = headlines[:count]
    blocks = []
    for i, h in enumerate(selected, 1):
        block = f"""### Eskiz {i}: {h}
- **Konu:** {h}
- **Çatışma:** Vatandaşın gündelik derdi ile küresel sistemin soğuk dili çarpışıyor.
- **Sürpriz Dönüş:** Sorunu çözmesi beklenen kurum, sorunun bizzat karikatürize edilmiş kaynağı çıkıyor.
- **Punchline (öneri):** "Biz haberi izliyoruz sanıyorduk, meğer haber bizi izliyormuş."
- **Kompozisyon Notu:** Tek panel; ön planda iki karakter, arka planda durumu özetleyen tek sembol; metin kısa.
"""
        blocks.append(block)
    return "\n".join(blocks)


def render_output(profile: str, briefing: str, prompts: str) -> str:
    today = dt.datetime.utcnow().strftime("%Y-%m-%d")
    return textwrap.dedent(
        f"""
        # Omfardo Günlük Karikatür Ajan Çıktısı ({today})

        > Bu doküman otomatik üretildi. Başlıklar güncel dünya gündeminden derlendi.

        ## Evren Profili (Özet)
        {profile}

        ## Günlük Dünya Gündemi Briefing
        {briefing}

        ## Karikatür Espri Eskizi Promptları
        {prompts}
        """
    ).strip() + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Omfardo daily cartoon prompt agent")
    p.add_argument("--profile", default="prompts/omfardo_universe_profile.md")
    p.add_argument("--out", default=None, help="Output markdown path")
    p.add_argument("--max-headlines", type=int, default=20)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    all_titles: list[str] = []
    for feed in RSS_FEEDS:
        try:
            all_titles.extend(fetch_rss_titles(feed))
        except Exception as exc:  # keep pipeline alive even if one feed fails
            all_titles.append(f"[feed unavailable] {feed} ({exc.__class__.__name__})")

    unique_titles = dedupe_keep_order(all_titles)
    unique_titles = unique_titles[: args.max_headlines]

    profile = load_profile(Path(args.profile))
    briefing = build_briefing(unique_titles, max_items=min(10, len(unique_titles)))
    prompts = make_prompt_blocks(unique_titles, count=min(8, len(unique_titles)))
    output = render_output(profile, briefing, prompts)

    out_path = Path(args.out) if args.out else Path("output") / f"omfardo_daily_{dt.datetime.utcnow():%Y%m%d}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output, encoding="utf-8")

    print(f"Wrote: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
