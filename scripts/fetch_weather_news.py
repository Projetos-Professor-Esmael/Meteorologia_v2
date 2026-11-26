"""Gera news.json com notícias do tempo (Brasil, Mundo, Tempestades tropicais) a partir de RSS. Sem API paga."""
import json, sys, re, datetime as dt, urllib.request, xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

UA = {"User-Agent": "Mozilla/5.0 (compatible; meteomapa-bot)"}
FEEDS = [
    ("Brasil", "Google Notícias", "https://news.google.com/rss/search?q=previs%C3%A3o+do+tempo+OR+INMET+OR+%22frente+fria%22+OR+tempestade+OR+%22onda+de+calor%22+when:2d&hl=pt-BR&gl=BR&ceid=BR:pt-419"),
    ("Mundo", "Google Notícias", "https://news.google.com/rss/search?q=weather+forecast+OR+hurricane+OR+storm+OR+heatwave+when:2d&hl=en-US&gl=US&ceid=US:en"),
    ("Tempestades", "NOAA NHC (Atlântico)", "https://www.nhc.noaa.gov/index-at.xml"),
]
def parse_date(s):
    try: return parsedate_to_datetime(s).astimezone(dt.timezone.utc)
    except Exception: return None
def fetch(scope, name, url):
    out = []
    try:
        root = ET.fromstring(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25).read())
        for it in root.iter("item"):
            t = (it.findtext("title") or "").strip(); l = (it.findtext("link") or "").strip(); d = parse_date(it.findtext("pubDate") or "")
            src = (it.findtext("source") or name).strip()
            if name == "Google Notícias": t = re.sub(r"\s+-\s+[^-]+$", "", t)
            if t and l.startswith("http") and d: out.append({"title": t, "link": l, "source": src, "published": d.isoformat(), "scope": scope})
    except Exception as e:
        print("falha em", scope, name, e)
    print(f"{scope} / {name}: {len(out)} itens")
    return out
def main():
    items, seen = [], set()
    for f in FEEDS:
        for i in sorted(fetch(*f), key=lambda x: x["published"], reverse=True)[:25]:
            k = re.sub(r"\W+", "", i["title"].lower())[:60]
            if k not in seen: seen.add(k); items.append(i)
    if not items: sys.exit("Nenhuma notícia coletada: veja as mensagens de falha acima.")
    json.dump({"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(), "items": items}, open("news.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(items), "itens")
if __name__ == "__main__": main()
