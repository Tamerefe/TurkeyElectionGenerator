import argparse
import re
from pathlib import Path

import requests
import pandas as pd
from bs4 import BeautifulSoup

DEFAULT_URLS = [
    # 2023 Cumhurbaşkanlığı anketleri
    "https://tr.wikipedia.org/wiki/2023_T%C3%BCrkiye_cumhurba%C5%9Fkanl%C4%B1%C4%9F%C4%B1_se%C3%A7imi_i%C3%A7in_yap%C4%B1lan_anketler",
    # Ülke çapında 2023 genel seçim anketleri
    "https://tr.wikipedia.org/wiki/%C3%9Clke_%C3%A7ap%C4%B1nda_2023_T%C3%BCrkiye_genel_se%C3%A7imleri_i%C3%A7in_yap%C4%B1lan_anketler",
]

def polite_get(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; AnketScraper/1.0; +https://example.com/)"
    }
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.text

def slugify_filename(text: str) -> str:
    # Dosya adı için güvenli, kısa bir slug
    text = text.strip()
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"[^\w\-.]+", "", text, flags=re.UNICODE)
    return (text or "cikti")[:120]

def make_unique_columns(cols):
    seen = {}
    out = []
    for c in cols:
        key = str(c)
        if key not in seen:
            seen[key] = 0
            out.append(key)
        else:
            seen[key] += 1
            out.append(f"{key}.{seen[key]}")
    return out

def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        new_cols = []
        for tpl in df.columns.values:
            parts = [str(x) for x in tpl if str(x) != "nan"]
            new_cols.append(" ".join(parts).strip())
        df.columns = new_cols
    df.columns = [re.sub(r"\s+", " ", str(c)).strip() for c in df.columns]
    df.columns = make_unique_columns(df.columns)
    return df

def map_tables_to_headings(soup: BeautifulSoup):
    """mw-content-text içindeki wikitable tablolarını, en yakın önceki h2/h3 başlığıyla eşleştir."""
    content = soup.find("div", id="mw-content-text")
    if not content:
        return []
    pairs = []
    last_heading = "Genel"
    for el in content.descendants:
        if getattr(el, "name", None) in {"h2", "h3"}:
            title = el.get_text(" ", strip=True)
            title = re.sub(r"\s*\[.*?düzenle.*?\]\s*", "", title, flags=re.IGNORECASE)
            last_heading = title or last_heading
        elif getattr(el, "name", None) == "table" and "wikitable" in (el.get("class") or []):
            pairs.append((last_heading, el))
    return pairs

def scrape_page_to_csv(url: str, outdir: Path) -> Path:
    html = polite_get(url)
    soup = BeautifulSoup(html, "lxml")

    # Başlık -> tablo eşleşmeleri
    pairs = map_tables_to_headings(soup)
    if not pairs:
        raise RuntimeError("Bu sayfada 'wikitable' bulunamadı.")

    # Sayfa başlığından dosya adı üret
    title_tag = soup.find("h1", id="firstHeading")
    page_title = title_tag.get_text(" ", strip=True) if title_tag else "wikipedia_sayfa"
    csv_name = slugify_filename(page_title) + ".csv"
    csv_path = outdir / csv_name

    all_frames = []
    for heading, table_el in pairs:
        # Tek tabloyu pandas ile oku
        dfs = pd.read_html(str(table_el), flavor="lxml")
        if not dfs:
            continue
        df = dfs[0]
        df = flatten_columns(df)
        # Ek bağlam sütunları
        df.insert(0, "Bölüm", heading)
        df.insert(1, "KaynakURL", url)
        all_frames.append(df)

    if not all_frames:
        raise RuntimeError("Tablolar okunamadı.")

    combined = pd.concat(all_frames, ignore_index=True)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(csv_path, index=False, encoding="utf-8-sig")
    return csv_path

def main():
    ap = argparse.ArgumentParser(description="Wikipedia anket tablolarını iki sayfa için ayrı CSV'lere dök.")
    ap.add_argument("-o", "--outdir", default="output", help="Çıktı klasörü")
    ap.add_argument("-u", "--urls", nargs="*", default=DEFAULT_URLS, help="İşlenecek sayfa URL listesi")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    for url in args.urls:
        print(f"[i] İşleniyor: {url}")
        try:
            path = scrape_page_to_csv(url, outdir)
            print(f"[✓] Kaydedildi: {path}")
        except Exception as e:
            print(f"[!] Hata ({url}): {e}")

if __name__ == "__main__":
    main()
