# HSE Module (Health, Safety, & Environment)
**Keselamatan Kerja, Manajemen Izin, & Respons Darurat**

HSE Module dirancang untuk memastikan setiap pekerjaan fisik di lapangan mematuhi standar keselamatan migas tertinggi. Modul ini menjadi pusat pengendalian operasional harian yang menghubungkan perizinan administratif dengan status pergerakan fisik pekerja di kapal secara real-time.

## 1. Tanggung Jawab Utama
*   **Permit to Work (PTW)**: Sistem perizinan kerja terpusat berbasis digital. Pekerja tidak dapat memulai *Work Order* sebelum HSE menerbitkan persetujuan.
*   **Pre-Job Safety Verification**: Mewajibkan kru untuk mengisi Job Safety Analysis (JSA) dan Toolbox Talk (TBT) *sebelum* tombol "Start Work" aktif.
*   **Personnel On Board (POB) Live Tracking**: Pemantauan titik lokasi kru secara *real-time* dengan WebSockets. Status masuk/keluar area (Check-in/Check-out) berjalan secara *otomatis* berdasarkan status PTW (tanpa input manual).
*   **Incident Management**: Pelaporan dan pelacakan riwayat insiden kerja (Kecelakaan).
*   **Emergency Muster Drill**: Pemicu status darurat (Lockdown) yang dapat membekukan seluruh operasional izin kerja dengan satu klik, disertai fitur sirine visual.

## 2. Aktor Utama
*   **Safety Officer (HSE)**: Melakukan pengecekan konflik keamanan area, menyetujui izin PTW, memantau *Live POB*, menginvestigasi kecelakaan, dan mengeksekusi kendali darurat.
*   **Worker**: Kru yang mengajukan Izin Kerja (PTW), melakukan validasi TBT, dan mengeksekusi status pekerjaan `Start Work` & `Mark as Done`.

## 3. Fitur & Endpoint API (`/api/v1/hse/`)
*   `GET/POST /ptw/` - Daftar pengajuan Izin Kerja.
*   `POST /ptw/<id>/approve/` - Persetujuan izin kerja oleh Safety Officer.
*   `POST /ptw/<id>/start_work/` - Eksekusi kerja: Mengubah PTW menjadi `IN_PROGRESS` dan melakukan `Auto-Check-in` lokasi kru di POB.
*   `POST /ptw/<id>/mark_done/` - Pekerjaan selesai: Melakukan `Auto-Check-out` lokasi kru dari POB, mengubah PTW menjadi `WAITING_FOR_CLOSE`.
*   `POST /ptw/<id>/confirm_close/` - Verifikasi akhir Safety Officer terhadap area lokasi. PTW menjadi `CLOSED`, dan WO menjadi `WAITING_REVIEW`.
*   `GET /pob/` - Data histori dan lokasi saat ini untuk semua pekerja di manifes kapal.
*   `POST /test-trigger/` - Memancarkan sinyal darurat (Red/Yellow) secara global via WebSocket.

## 4. Alur Kerja (Flow) - Keselamatan Operasional
1. **Request Izin**: Worker memilih *Work Order* dari Engineering, mengumpulkan kru pendukung, lalu mengajukan PTW.
2. **Safety Review**: Safety Officer melihat notifikasi, memverifikasi kualifikasi keselamatan kru pendukung, meneliti deskripsi risiko, lalu menekan **Approve**.
3. **Execution & Check-in (Lock)**: Worker menekan `Start Work`. Sistem langsung melemparkan lokasi pekerja ke Dashboard **Live POB**, sehingga lokasi keberadaannya diawasi di peta.
4. **Completion & Check-out**: Worker menyelesaikan pekerjaan fisik, menekan `Mark as Done`. Pekerja otomatis ditarik keluar dari manifes POB area bahaya.
5. **Konfirmasi Final**: Safety Officer menyusuri lapangan fisik. Setelah dirasa aman, ia menekan **Confirm Close** untuk mengunci PTW. Operasional selanjutnya (verifikasi barang) diserahkan ke sistem Engineering.

## 5. Keterkaitan dengan Modul Lain
*   **CORE Module**: Peta *Deck Location* di modul CORE digunakan sebagai referensi titik koordinat POB dalam pengajuan izin.
*   **HR Module**: MCU *Fit-to-Work* adalah syarat mutlak yang harus dibaca oleh modul HSE sebelum menerima pembuatan form PTW oleh Worker.
*   **Engineering Module**: Setiap Work Order di Engineering membutuhkan penerbitan PTW di HSE. Setelah PTW dinyatakan *Closed*, WO diteruskan kembali ke modul Engineering untuk ditinjau Chief Engineer (`WAITING_REVIEW`).
