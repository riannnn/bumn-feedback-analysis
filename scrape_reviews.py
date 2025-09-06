from google_play_scraper import reviews, Sort
import pandas as pd
import os

# Buat folder data kalau belum ada
if not os.path.exists("data"):
    os.makedirs("data")

# Daftar aplikasi BUMN dengan App ID terbaru
apps = {
    "BRImo": "id.co.bri.brimo",
    "LivinMandiri": "id.bmri.livin",             # ✅ ID terbaru
    "MyTelkomsel": "com.telkomsel.telkomselcm"
}

def scrape_app(app_name, app_id, n=1000):
    """Scrape review dengan continuation_token supaya lebih lengkap"""
    all_reviews = []
    token = None

    while len(all_reviews) < n:
        result, token = reviews(
            app_id,
            lang="id",        # Bahasa Indonesia
            country="id",     # Review dari Indonesia
            sort=Sort.NEWEST, # Review terbaru
            count=200,        # Batch size
            continuation_token=token
        )
        all_reviews.extend(result)

        print(f"{app_name}: {len(all_reviews)} review terkumpul")

        if not token:  # kalau sudah habis
            break

    # Simpan hasil ke DataFrame
    df = pd.DataFrame(all_reviews)
    df["app"] = app_name

    # Simpan ke CSV per aplikasi
    csv_path = f"data/{app_name}_reviews.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"✅ {app_name} selesai, {len(df)} review tersimpan di {csv_path}\n")

    return df


# Scrape semua aplikasi
all_data = []
for app_name, app_id in apps.items():
    print(f"🔍 Sedang scraping {app_name}...")
    df = scrape_app(app_name, app_id, n=1000)
    all_data.append(df)

# Gabungkan semua aplikasi jadi 1 file
combined_df = pd.concat(all_data, ignore_index=True)
combined_df.to_csv("data/bumn_reviews.csv", index=False, encoding="utf-8-sig")

print(f"\n🎉 Semua selesai! Total {len(combined_df)} review tersimpan di data/bumn_reviews.csv")
