import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

DEFAULT_URL = "https://tr.wikipedia.org/wiki/2019_T%C3%BCrkiye_yerel_se%C3%A7imleri_i%C3%A7in_yap%C4%B1lan_anketler"

TR_PROVINCES = [
    "Adana","Adıyaman","Afyonkarahisar","Ağrı","Aksaray","Amasya","Ankara","Antalya","Ardahan","Artvin",
    "Aydın","Balıkesir","Bartın","Batman","Bayburt","Bilecik","Bingöl","Bitlis","Bolu","Burdur","Bursa",
    "Çanakkale","Çankırı","Çorum","Denizli","Diyarbakır","Düzce","Edirne","Elazığ","Erzincan","Erzurum",
    "Eskişehir","Gaziantep","Giresun","Gümüşhane","Hakkâri","Hatay","Iğdır","Isparta","İstanbul","İzmir",
    "Kahramanmaraş","Karabük","Karaman","Kars","Kastamonu","Kayseri","Kırıkkale","Kırklareli","Kırşehir",
    "Kilis","Kocaeli","Konya","Kütahya","Malatya","Manisa","Mardin","Mersin","Muğla","Muş","Nevşehir",
    "Niğde","Ordu","Osmaniye","Rize","Sakarya","Samsun","Siirt","Sinop","Sivas","Şanlıurfa","Şırnak",
    "Tekirdağ","Tokat","Trabzon","Tunceli","Uşak","Van","Yalova","Yozgat","Zonguldak"
]

# 2019 dönemi için yaygın parti eşadları (alias)
PARTY_ALIASES = {
    "AKP": [r"AKP", r"AK Parti", r"Adalet ve Kalkınma"],
    "CHP": [r"CHP", r"Cumhuriyet Halk"],
    "MHP": [r"MHP", r"Milliyetçi Hareket"],
    "İYİ": [r"İYİ", r"İYİ Parti"],
    "HDP": [r"HDP", r"Halkların Demokratik"],
    "SP":  [r"SP", r"Saadet"],
    "BBP": [r"BBP", r"Büyük Birlik"],
    "DSP": [r"DSP", r"Demokratik Sol"],
    "DP":  [r"DP", r"Demokrat Parti"],
    "TKP": [r"TKP", r"Türkiye Komünist"],
    "VP":  [r"Vatan Partisi", r"VP"],
    "BTP": [r"BTP", r"Bağımsız Türkiye"],
}
# Alians/sentez başlıkları (parti değil) — hariç tut
EXCLUDE_TERMS = [r"Cumhur İttifakı", r"Millet İttifakı", r"İttifakı", r"Blok"]

# Kararsız/benzeri sütun adayları
UNDECIDED_ALIASES = [
    r"Kararsız", r"Fikri?m?\s*yok", r"Cevap\s*yok", r"Tercih\s*yok",
    r"Oy\s*kullan(mayacak|mam)", r"Protesto\s*oy", r"Boş\s*oy"
]

# --- Yardımcılar ---

def polite_get(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; AnketScraper/2.0; +https://example.com/)"}
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.text

def slugify(text: str) -> str:
    text = (text or "").strip()
    text = re.sub(r"\s+", "_", text, flags=re.UNICODE)
    text = re.sub(r"[^\w\-.]+", "", text, flags=re.UNICODE)
    return text[:80] or "cikti"

def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        new_cols = []
        for tpl in df.columns.values:
            parts = [str(x) for x in tpl if str(x) != "nan"]
            new_cols.append(" ".join(parts).strip())
        df.columns = new_cols
    df.columns = [re.sub(r"\s+", " ", str(c)).strip() for c in df.columns]
    # benzersizleştir
    seen, out = {}, []
    for c in df.columns:
        if c in seen:
            seen[c] += 1
            out.append(f"{c}.{seen[c]}")
        else:
            seen[c] = 0
            out.append(c)
    df.columns = out
    return df

def parse_pct(x):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return np.nan
    s = str(x).strip()
    if s in {"", "—", "–", "-", "N/A", "NaN"}:
        return np.nan
    s = s.replace("%", "").replace(" ", "")
    s = s.replace(",", ".")
    # "34.5±2.1" gibi değerleri kırp
    s = re.split(r"[±\(\[]", s)[0]
    try:
        return float(s)
    except Exception:
        return np.nan

def any_regex(patterns):
    return re.compile("|".join(f"(?:{p})" for p in patterns), flags=re.IGNORECASE | re.UNICODE)

PARTY_PATTERNS = {canon: any_regex(aliases) for canon, aliases in PARTY_ALIASES.items()}
EXCLUDE_REGEX = any_regex(EXCLUDE_TERMS)
UNDECIDED_REGEX = any_regex(UNDECIDED_ALIASES)

def detect_party_from_header(h: str):
    """Sütun başlığından (varsa) parti tespit et. Önce parantez içi, yoksa tüm başlık."""
    if not h:
        return None
    # Önce parantez içini dene: "Aday (CHP)" gibi
    m = re.search(r"\(([^)]+)\)", h)
    candidates = [m.group(1)] if m else []
    candidates.append(h)
    for text in candidates:
        if EXCLUDE_REGEX.search(text or ""):
            return None
        for canon, pat in PARTY_PATTERNS.items():
            if pat.search(text or ""):
                return canon
    return None

def is_undecided_header(h: str):
    return bool(UNDECIDED_REGEX.search(h or ""))

def map_tables_to_headings(soup: BeautifulSoup):
    content = soup.find("div", id="mw-content-text")
    if not content:
        return []
    pairs, last_heading = [], "Genel"
    for el in content.descendants:
        name = getattr(el, "name", None)
        if name in {"h2", "h3", "h4"}:
            title = el.get_text(" ", strip=True)
            title = re.sub(r"\s*\[.*?düzenle.*?\]\s*", "", title, flags=re.IGNORECASE)
            last_heading = title or last_heading
        elif name == "table" and "wikitable" in (el.get("class") or []):
            pairs.append((last_heading, el))
    return pairs

def find_province_in_text(text: str):
    if not text:
        return None
    for p in TR_PROVINCES:
        if re.search(rf"\b{re.escape(p)}\b", text, flags=re.IGNORECASE | re.UNICODE):
            return p
    return None

def split_df_by_province_from_column(df: pd.DataFrame):
    """Tablonun içindeki herhangi bir sütundan il adı yakalanırsa o değerlere göre böler."""
    buckets = {}
    for col in df.columns:
        ser = df[col].astype(str)
        # hızlıca benzersiz değerlere bakıp il var mı kontrol et
        for v in pd.unique(ser.dropna()):
            prov = find_province_in_text(str(v))
            if prov:
                mask = ser.str.contains(rf"\b{re.escape(prov)}\b", case=False, regex=True)
                part = df[mask].copy()
                if not part.empty:
                    buckets.setdefault(prov, []).append(part)
    return buckets

def reduce_to_party_and_undecided(df: pd.DataFrame) -> pd.DataFrame:
    """
    DataFrame'den sadece parti sütunlarını (kanonik isimlerle) ve tek bir 'Kararsız' sütununu üretir.
    Değerler yüzde (float) olarak döner.
    """
    party_cols = {}
    undecided_sources = []

    for col in df.columns:
        canon = detect_party_from_header(col)
        if canon:
            party_cols.setdefault(canon, []).append(col)
        elif is_undecided_header(col):
            undecided_sources.append(col)

    # Hiç parti yoksa, tüm satırlar boş dönebilir
    if not party_cols and not undecided_sources:
        return pd.DataFrame()

    out = pd.DataFrame(index=df.index)

    # Partiler: aynı partiye denk gelen birden çok sütun varsa topla (örn. 1. tur / 2. tur vb. karışık tablolar)
    for canon, cols in party_cols.items():
        vals = df[cols].applymap(parse_pct)
        out[canon] = vals.sum(axis=1, skipna=True, min_count=1)

    # Kararsız: tüm kaynakları topla
    if undecided_sources:
        vals_u = df[undecided_sources].applymap(parse_pct)
        out["Kararsız"] = vals_u.sum(axis=1, skipna=True, min_count=1)
    else:
        out["Kararsız"] = np.nan

    # Tümü NaN olan satırları at
    if not out.empty:
        out = out.dropna(how="all").reset_index(drop=True)
    return out

# --- Ana akış ---

def scrape_and_write(url: str, outdir: Path):
    html = polite_get(url)
    soup = BeautifulSoup(html, "lxml")

    pairs = map_tables_to_headings(soup)
    if not pairs:
        raise RuntimeError("Bu sayfada 'wikitable' bulunamadı.")

    outdir.mkdir(parents=True, exist_ok=True)

    buckets = {p: [] for p in TR_PROVINCES}
    unknown = []

    for heading, tbl in pairs:
        dfs = pd.read_html(str(tbl), flavor="lxml")
        if not dfs:
            continue
        raw = flatten_columns(dfs[0])

        # İli başlıktan yakala; yoksa tablo içinden böl
        prov = find_province_in_text(heading)
        if prov:
            reduced = reduce_to_party_and_undecided(raw)
            if not reduced.empty:
                buckets[prov].append(reduced)
        else:
            split = split_df_by_province_from_column(raw)
            if split:
                for p, parts in split.items():
                    merged = pd.concat(parts, ignore_index=True)
                    reduced = reduce_to_party_and_undecided(merged)
                    if not reduced.empty:
                        buckets[p].append(reduced)
            else:
                # il tespit edilemeyen, ama yine de parti/kararsız çıkarılabilen satırlar
                reduced = reduce_to_party_and_undecided(raw)
                if not reduced.empty:
                    unknown.append(reduced)

    # İller için yaz
    for p, frames in buckets.items():
        if not frames:
            continue
        combined = pd.concat(frames, ignore_index=True)
        # sadece parti+kararsız kalsın; tümü NaN olan kolonları (hiç görünmeyen parti) at
        combined = combined.dropna(axis=1, how="all")
        if combined.empty:
            continue
        path = outdir / f"{slugify(p).lower()}_2019_oy_oranlari.csv"
        combined.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"[✓] {p}: {path}")

    # İl tespit edilemeyenler atlanıyor (sadece il bazlı veriler kaydediliyor)

def main():
    ap = argparse.ArgumentParser(description="2019 yerel anketler: il il CSV (sadece parti oy oranları + Kararsız).")
    ap.add_argument("-u", "--url", default=DEFAULT_URL, help="Wikipedia sayfa URL'si")
    ap.add_argument("-o", "--outdir", default="anketler", help="Çıktı klasörü")
    args = ap.parse_args()

    scrape_and_write(args.url, Path(args.outdir))

if __name__ == "__main__":
    main()
