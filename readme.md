# Panduan Penggunaan WebScraper

## Deskripsi
`WebScraper` adalah sebuah kelas Python yang dirancang untuk melakukan web scraping terhadap data jurnal dari situs **SINTA (Science and Technology Index)**. Program ini dapat mengambil informasi jurnal berdasarkan kata kunci tertentu, menyimpan data ke dalam file CSV, dan membuat visualisasi data.

## Fitur Utama
1. **Scraping Data Jurnal**: Mengambil data jurnal termasuk nama jurnal, afiliasi, akreditasi, dan tautan.
2. **Penyimpanan Data**: Data yang diambil akan disimpan dalam format CSV.
3. **Visualisasi Data**: Membuat grafik distribusi data berdasarkan afiliasi dan akreditasi.
4. **Log Aktivitas**: Menyimpan log proses scraping untuk melacak kesalahan dan aktivitas.
5. **Tampilan Data**: Menampilkan data dalam format tabel di terminal.

## Struktur Program

### Inisialisasi `WebScraper`

Konstruktor menerima dua parameter:
- `base_url`: URL dasar untuk scraping.
- `keyword`: Kata kunci pencarian untuk memfilter jurnal.

Fungsi ini juga:
- Membuat direktori output khusus untuk menyimpan file.
- Menyiapkan file log untuk mencatat aktivitas.

### Fungsi Utama

#### `fetch_page(url)`
Mengambil konten HTML dari URL yang diberikan dan mengembalikannya dalam bentuk objek `BeautifulSoup`.

#### `get_pagination(soup)`
Mengambil jumlah total halaman dari elemen pagination di halaman web.

#### `extract_journal_data(soup)`
Menarik data jurnal dari halaman web, termasuk:
- Nama jurnal
- Afiliasi
- Akreditasi
- Tautan jurnal

#### `save_to_csv(data)`
Menyimpan data yang telah di-scrape ke file CSV.

#### `visualize_data()`
Membuat visualisasi data berupa:
1. Grafik batang distribusi afiliasi.
2. Diagram pie distribusi akreditasi jurnal.

#### `run()`
Menjalankan proses scraping secara menyeluruh, termasuk:
- Mengambil jumlah halaman.
- Melakukan iterasi untuk setiap halaman.
- Menyimpan data dan membuat visualisasi.
- Menampilkan data dalam format tabel di terminal.

### Fungsi Tambahan
#### `main()`
Fungsi utama untuk memulai program dengan parameter default:
- `base_url`: "https://sinta.kemdikbud.go.id/journals/"
- `keyword`: "teknologi informasi"

## Cara Menggunakan

### 1. Instalasi
Pastikan Anda memiliki Python 3.7 atau lebih baru. Install dependensi berikut:
```bash
pip install requests beautifulsoup4 pandas matplotlib seaborn tabulate
```

### 2. Menjalankan Program
Jalankan file Python dengan perintah:
```bash
python nama_file.py
```

### 3. Hasil Output
- Data jurnal akan disimpan dalam file CSV di direktori `scraped_data/`.
- Visualisasi data akan disimpan di subdirektori `visualizations/`.
- Log aktivitas akan disimpan dalam file `.log`.
- Data jurnal juga akan ditampilkan dalam format tabel di terminal.

## Struktur Direktori Output
```
scraped_data/
|-- <keyword>_<timestamp>/
    |-- journal_data_<timestamp>.csv
    |-- scraping_log_<timestamp>.log
    |-- visualizations/
        |-- affiliation_distribution.png
        |-- accreditation_distribution.png
```

## Visualisasi Data
1. **Distribusi Afiliasi**: Grafik batang menampilkan 10 afiliasi teratas berdasarkan jumlah jurnal.
2. **Distribusi Akreditasi**: Diagram pie menunjukkan persentase akreditasi jurnal.

## Catatan Penting
- Pastikan koneksi internet stabil selama proses scraping.
- Jangan terlalu sering menjalankan scraping untuk menghindari pemblokiran IP.
- Program menghormati server dengan menambahkan jeda antara permintaan (default 2 detik per halaman).

## Log Aktivitas
Log aktivitas dapat ditemukan di file `.log` di dalam direktori output. File ini mencatat proses scraping termasuk kesalahan yang mungkin terjadi.

## Lisensi
Program ini dirilis di bawah lisensi MIT. Silakan gunakan dan modifikasi sesuai kebutuhan.

