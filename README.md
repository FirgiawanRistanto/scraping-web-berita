# Web Scraping Berita

Proyek ini adalah skrip Python untuk melakukan web scraping berita dari beberapa portal online dan menganalisis data yang terkumpul.

## Daftar Portal Web yang Di-scrape

*   **Detik Travel:** Mengambil artikel berita dari kategori travel (`https://travel.detik.com/`).
*   **Liputan6 Global:** Mengambil artikel berita dari kategori global (`https://www.liputan6.com/global`).

## Cara Menjalankan Proyek

Ikuti langkah-langkah berikut untuk menjalankan skrip scraping dan notebook analisis:

### 1. Persiapan Lingkungan Virtual

Sangat disarankan untuk menggunakan lingkungan virtual untuk mengelola dependensi proyek.

```bash
# Buat lingkungan virtual baru
python -m venv .venv

# Aktifkan lingkungan virtual
# Di Windows:
.venv\Scripts\activate
# Di macOS/Linux:
source .venv/bin/activate
```

### 2. Instalasi Dependensi

Setelah lingkungan virtual aktif, instal semua pustaka Python yang diperlukan dari `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Menjalankan Skrip Scraping

Untuk menjalankan skrip scraping dan mengumpulkan data berita ke dalam `hasil_crawling_berita.csv`:

```bash
python detik_liputan_scraper.py
```

### 4. Menjalankan Analisis Data

Untuk melihat analisis data dan visualisasi, buka notebook Jupyter `analisis.ipynb`:

```bash
jupyter notebook analisis.ipynb
```
Di dalam Jupyter Notebook, jalankan semua sel untuk melihat hasil analisis.

## Catatan Kendala & Solusi Singkat

Selama pengembangan skrip scraping dan analisis, beberapa kendala ditemui dan telah diatasi:

*   **Inkonsistensi Format Tanggal:**
    *   **Kendala:** Portal berita yang berbeda memiliki format tanggal yang tidak seragam, menyebabkan kesalahan parsing.
    *   **Solusi:** Mengimplementasikan logika parsing tanggal yang lebih robust di `detik_liputan_scraper.py` untuk menstandardisasi semua tanggal ke format `YYYY-MM-DD HH:MM:SS`.
*   **Anomali Kategori Detik Travel:**
    *   **Kendala:** Terkadang, link dari Detik Travel mengarah ke subdomain lain (misalnya `20.detik.com`) yang bukan kategori travel.
    *   **Solusi:** Menambahkan filter URL di `detik_liputan_scraper.py` untuk hanya memproses link yang berasal dari `travel.detik.com` dan mengeset kategori secara langsung sebagai "Travel".
*   **Kesalahan Parsing/Plotting di Jupyter Notebook:**
    *   **Kendala:** Notebook `analisis.ipynb` memiliki logika parsing tanggal yang usang dan variabel yang belum didefinisikan untuk plotting.
    *   **Solusi:** Memperbarui fungsi `parse_waktu` agar sesuai dengan format tanggal yang sudah distandardisasi dan menambahkan perhitungan `jumlah_per_source` sebelum visualisasi grafik.
