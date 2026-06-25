# ENGINEERING Module (Asset & Maintenance)
**Manajemen Aset, Pemeliharaan Mesin, dan Inventaris**

Engineering Module (Asset Module) berfungsi untuk memastikan keandalan mesin di atas kapal, merencanakan pemeliharaan preventif, serta mengelola ketersediaan suku cadang (Inventory).

## 1. Tanggung Jawab Utama
*   **Asset & Machinery Hierarchy**: Mendata seluruh mesin (seperti Main Generator, Crane) yang terpasang di atas aset utama kapal.
*   **IoT Telemetry & Health Monitoring**: Memantau kesehatan mesin secara real-time berdasarkan data sensor (Suhu & Getaran), serta menghitung persentase keandalan operasional (*Overall Equipment Effectiveness / OEE*).
*   **Predictive Maintenance**: Secara otomatis memperingatkan teknisi ketika mesin menunjukkan indikasi anomali atau ketika sudah mencapai batas jam operasional servis (Maintenance Interval).
*   **Work Orders (Surat Perintah Kerja)**: Sistem untuk menugaskan kru agar melakukan perbaikan pada mesin tertentu.
*   **Smart Inventory & Auto-Booking**: Manajemen stok suku cadang cerdas. Material langsung di-*reserve* saat ditambahkan ke Work Order, dan hanya dipotong dari fisik gudang (*Auto-Deduct*) ketika Work Order di-verifikasi selesai secara teknis.

## 2. Aktor Utama
*   **Chief Engineer**: Mengawasi indikator kesehatan mesin, merilis Work Order (WO), mengalokasikan stok material ke WO, serta melakukan Verifikasi Akhir penyelesaian WO.
*   **Worker**: Kru teknis yang menerima penugasan WO dan melakukan perbaikan fisik.

## 3. Fitur & Endpoint API (`/api/v1/asset/`)
*   `GET/POST /machinery/` - Daftar peralatan operasional kapal.
*   `GET/POST /workorders/` - Pembuatan perintah kerja.
*   `POST /workorders/<id>/add_material/` - Menambahkan material ke WO (otomatis masuk ke status `Reserved`).
*   `POST /workorders/<id>/complete/` - Verifikasi akhir WO oleh Chief Engineer (merubah WO jadi `COMPLETED` dan mengeksekusi `Auto-Deduct` inventory).
*   `GET/POST /inventory/` - Manajemen master stok suku cadang.
*   `GET /maintenance/` - Pengelolaan jadwal perawatan berkala.

## 4. Alur Kerja (Flow) - The 2-Step Closure
1. **Identifikasi Kerusakan**: Sistem IoT mendeteksi kelainan getaran mesin (Atau, tercapai batas jam servis rutin).
2. **Terbit WO**: Chief Engineer menerbitkan Work Order untuk mesin tersebut.
3. **Pemesanan Material**: Chief Engineer memasukkan spare part yang dibutuhkan ke dalam WO (stok inventory masuk fase *Booking/Reserved*).
4. **Eksekusi Lapangan**: Pekerja mengeksekusi WO. Pekerja berkoordinasi dengan modul HSE untuk Izin Kerja.
5. **Verifikasi Keselamatan (Step 1)**: Pekerjaan di lapangan selesai. Safety Officer melakukan *Confirm Close* izin kerja. **WO berubah status menjadi `WAITING_REVIEW`**. (Inventory belum dipotong).
6. **Verifikasi Teknis & Finalisasi (Step 2)**: Chief Engineer melihat WO yang *Waiting Review*, memastikan kesesuaian suku cadang terpakai, lalu menekan **Complete WO**. Sistem memotong stok permanen dan menutup WO secara tuntas.

## 5. Keterkaitan dengan Modul Lain
*   **CORE Module**: Machinery dan Work Orders selalu terikat dengan identitas *Vessel* dari modul CORE.
*   **HSE Module**: Setiap Work Order yang melibatkan area berisiko **wajib** dibuatkan *Permit to Work* di modul HSE. Pekerja tidak dapat melakukan `Start Work` tanpa melalui *approval* dari HSE Officer.
