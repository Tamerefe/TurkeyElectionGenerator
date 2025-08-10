import argparse
import os
import re
import time
from pathlib import Path

import requests
import pandas as pd
from bs4 import BeautifulSoup

WIKI_URL_DEFAULT = "https://tr.wikipedia.org/wiki/2024_Türkiye_yerel_seçimleri_için_yapılan_anketler"

def slugify(text: str) -> str:
    text = re.sub(r"\s+", "_", text.strip())
    text = re.sub(r"[^\w\-\.]+", "", text, flags=re.UNICODE)
    return text[:120] if text else "bolum"

def fetch_html(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; AnketScraper/1.0; +https://example.com/)"
    }
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.text

def map_tables_to_headings(soup: BeautifulSoup):
    """
    Sayfadaki <table> öğelerini, en yakın önceki h2/h3 başlık metni ile eşle.
    Dönen liste: [(heading_text, table_element), ...]
    """
    results = []
    last_heading = "Genel"
    for el in soup.find("div", id="mw-content-text").descendants:
        if el.name in {"h2", "h3"}:
            # H2/H3 başlık içindeki görünür metni al
            title = el.get_text(" ", strip=True)
            # "Düzenle" vs. kırp
            title = re.sub(r"\s*\[.*?düzenle.*?\]\s*", "", title, flags=re.IGNORECASE)
            last_heading = title or last_heading
        elif el.name == "table" and "wikitable" in el.get("class", []):
            results.append((last_heading, el))
    return results

def read_table(elem) -> pd.DataFrame:
    # Tek tablo html'ini pandas ile oku
    df_list = pd.read_html(str(elem), flavor="lxml")
    if not df_list:
        return pd.DataFrame()
    df = df_list[0]
    # Çok seviyeli kolonları düzleştir
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [" ".join([str(c) for c in col if str(c) != "nan"]).strip() for col in df.columns.values]
    df.columns = [re.sub(r"\s+", " ", str(c)).strip() for c in df.columns]
    return df

def extract_province_name(heading: str) -> str:
    """
    Başlık metninden il adını çıkar.
    Örnek: "İstanbul anketleri" -> "istanbul"
    """
    # Türkiye'nin il isimleri (küçük harfle)
    provinces = [
        "adana", "adıyaman", "afyonkarahisar", "afyon", "ağrı", "amasya", "ankara", "antalya", 
        "artvin", "aydın", "balıkesir", "bilecik", "bingöl", "bitlis", "bolu", 
        "burdur", "bursa", "çanakkale", "çankırı", "çorum", "denizli", "diyarbakır", 
        "edirne", "elazığ", "erzincan", "erzurum", "eskişehir", "gaziantep", "giresun", 
        "gümüşhane", "hakkari", "hatay", "isparta", "mersin", "istanbul", "izmir", 
        "kars", "kastamonu", "kayseri", "kırklareli", "kırşehir", "kocaeli", "konya", 
        "kütahya", "malatya", "manisa", "kahramanmaraş", "mardin", "muğla", "muş", 
        "nevşehir", "niğde", "ordu", "rize", "sakarya", "samsun", "siirt", "sinop", 
        "sivas", "tekirdağ", "tokat", "trabzon", "tunceli", "şanlıurfa", "uşak", 
        "van", "yozgat", "zonguldak", "aksaray", "bayburt", "karaman", "kırıkkale", 
        "batman", "şırnak", "bartın", "ardahan", "iğdır", "yalova", "karabük", "kilis", 
        "osmaniye", "düzce"
    ]
    
    heading_lower = heading.lower()
    # İ ve ı karakterleri için normalize et
    heading_normalized = heading_lower.replace('ı', 'i').replace('ğ', 'g').replace('ş', 's').replace('ç', 'c').replace('ö', 'o').replace('ü', 'u')
    
    for province in provinces:
        province_normalized = province.replace('ı', 'i').replace('ğ', 'g').replace('ş', 's').replace('ç', 'c').replace('ö', 'o').replace('ü', 'u')
        if province in heading_lower or province_normalized in heading_normalized:
            return province
    return None

def main():
    ap = argparse.ArgumentParser(description="Wikipedia anket tablolarını çek")
    ap.add_argument("-u", "--url", default=WIKI_URL_DEFAULT, help="Wikipedia sayfa URL'si")
    ap.add_argument("-o", "--outdir", default="anket_cikti", help="Çıktı klasörü")
    ap.add_argument("--sleep", type=float, default=0.5, help="Kibar gecikme (sn)")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    print(f"[i] Sayfa indiriliyor: {args.url}")
    html = fetch_html(args.url)
    soup = BeautifulSoup(html, "lxml")

    pairs = map_tables_to_headings(soup)
    if not pairs:
        print("[!] Uyarı: wikitable bulunamadı.")
        return

    all_rows = []
    province_data = {}  # İl bazında veri toplamak için

    for idx, (heading, table_el) in enumerate(pairs, start=1):
        df = read_table(table_el)
        if df.empty:
            continue

        # Kaynak URL ve bölüm bilgisini ek sütun olarak koy
        df.insert(0, "Bölüm", heading)
        df.insert(1, "KaynakURL", args.url)

        # İl adını tespit et
        province_name = extract_province_name(heading)
        
        if province_name:
            # İl bazında gruplanmış veri sakla
            if province_name not in province_data:
                province_data[province_name] = []
            province_data[province_name].append(df)
            print(f"[i] {province_name.capitalize()} ili için veri toplandı: {heading}")
        else:
            # İl tespit edilemeyenler için genel kayıt
            section_slug = slugify(heading)
            section_path = outdir / f"{section_slug}_genel.csv"
            df.to_csv(section_path, index=False, encoding="utf-8-sig")
            print(f"[✓] Genel kayıt: {section_path}")

        # Birleştirme için sakla
        all_rows.append(df)

        time.sleep(args.sleep)

    # Her il için ayrı CSV dosyası oluştur
    for province_name, dfs in province_data.items():
        if dfs:
            combined_province_df = pd.concat(dfs, ignore_index=True)
            province_file = outdir / f"{province_name}_2024_anketler.csv"
            combined_province_df.to_csv(province_file, index=False, encoding="utf-8-sig")
            print(f"[✓] {province_name.capitalize()} ili kaydedildi: {province_file}")

    # Hepsini tek CSV'de birleştir (isteğe bağlı)
    if all_rows:
        combined = pd.concat(all_rows, ignore_index=True)
        combined_path = outdir / "tum_anketler_birlesik.csv"
        combined.to_csv(combined_path, index=False, encoding="utf-8-sig")
        print(f"[✓] Birleşik CSV: {combined_path}")

        # İsteğe bağlı: Excel çıktı (il bazında sayfalar)
        if province_data:
            try:
                xlsx_path = outdir / "iller_bazinda_anketler.xlsx"
                with pd.ExcelWriter(xlsx_path, engine="xlsxwriter") as xw:
                    for province_name, dfs in province_data.items():
                        if dfs:
                            combined_province_df = pd.concat(dfs, ignore_index=True)
                            sheet_name = province_name.capitalize()[:31]
                            combined_province_df.to_excel(xw, sheet_name=sheet_name, index=False)
                print(f"[✓] Excel çıktı (il bazında): {xlsx_path}")
            except ImportError:
                print("[!] Excel çıktı için xlsxwriter modülü gerekli (pip install xlsxwriter)")

    print(f"[i] Toplam {len(province_data)} il için veri toplandı.")
    print("[i] Tamamlandı.")

if __name__ == "__main__":
    main()
