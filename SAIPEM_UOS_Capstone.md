# SAIPEM UOS Management System
**Capstone Project Presentation Details**

Sistem SAIPEM UOS (Unified Operating System) dirancang khusus untuk memenuhi standar ketat di lingkungan kerja lepas pantai (offshore) dan migas. Sistem ini mengutamakan kecepatan respon, keamanan tinggi, dan pelacakan *real-time*.

---

## 💻 Tech Stack & Arsitektur Sistem

Pemilihan stack teknologi ini sangat krusial untuk memastikan sistem berjalan *real-time*, aman, dan mudah di-scale up (diperbesar). Alasan mengapa stack ini dipilih:

### 1. Backend: Django & Django REST Framework (Python)
* **Kenapa menggunakan ini?** Python sangat tangguh untuk memproses algoritma dan data dalam jumlah besar. Django menyediakan sistem bawaan untuk keamanan tingkat tinggi (otentikasi, enkripsi password, perlindungan CSRF) dan arsitektur *Role-Based Access Control* (RBAC) yang sangat stabil untuk membedakan hak akses antar jabatan.
* **Django Channels (WebSockets)**: Digunakan untuk fitur komunikasi dua arah yang murni *real-time* secara *asynchronous* (misal: memunculkan notifikasi persetujuan secara live & tracking titik lokasi pekerja tanpa harus me-refresh halaman web).

### 2. Database: PostgreSQL
* **Kenapa menggunakan ini?** PostgreSQL adalah database relasional *enterprise-grade* yang sangat bisa diandalkan. Sangat cocok menangani integritas data yang kompleks (seperti relasi antara tabel Izin Kerja, Histori Lokasi Pegawai, Aset Mesin Kapal, dan Data HR) tanpa takut terjadinya korupsi atau inkonsistensi data.

### 3. Frontend: Vue 3 & Vite
* **Kenapa menggunakan ini?** Vue 3 dengan *Composition API* menawarkan reaktivitas yang luar biasa dan sangat ringan di browser. Vite digunakan sebagai *build tool* untuk memastikan waktu render super cepat. Kecepatan antarmuka ini sangat dibutuhkan saat *Safety Officer* memonitor status darurat di kapal.
* **Vue Router (Route Guards)**: Digunakan sebagai gerbang keamanan di sisi frontend untuk secara otomatis mendeteksi Role user dan memblokir siapa saja yang berusaha mengakses URL di luar kewenangannya.

---

## 👥 User Journey & Application Flow per Role

Sistem ini dioperasikan berdasarkan jabatan. Berikut adalah detail alur aplikasi dari kacamata masing-masing peran, diurutkan dari tingkat pengatur sistem hingga pelaksana di lapangan.

### 🖥️ 1. Role: Admin (System Administrator)
**Kapasitas:** Memegang kontrol infrastruktur sistem secara utuh.
* **Navigasi Inti**: Login dan langsung masuk ke halaman utama (`/` Admin Dashboard).
* **Manajemen Vessel & Data**:
   * Mengatur daftar kapal (*Vessel Registry*). Aplikasi ini didesain **Multi-Tenant**, artinya satu aplikasi bisa memantau beberapa kapal sekaligus (misal: "Saipem 7000" dan "Saipem 3000").
   * Mengatur *Role* pengguna ke dalam sistem grup (Django Groups), sehingga *Vue Router* bisa mengenali hak akses tiap orang dengan akurat.
   * Memiliki hak *override* (intervensi paksa) jika terjadi anomali dalam sistem.

### 👥 2. Role: HR Staff (Manajemen SDM)
**Kapasitas:** Mengatur siapa saja kru yang diizinkan beroperasi di kapal secara legal dan medis.
* **Navigasi HR**: Login dan masuk ke modul khusus HR (`/hr/roster`).
* **Rotasi Pekerja (Business Flow)**:
   * HR Staff mengubah `roster_status` pegawai dari `OFFBOARD` menjadi `ONBOARD` saat pergantian shift mingguan. Pegawai berstatus *Off-board* otomatis sistemnya terkunci dan tidak bisa membuat Izin Kerja.
* **Validasi Keselamatan Medis (Form Data)**:
   * Memantau status kesehatan (Medical Check Up) setiap pekerja. Jika status pekerja adalah `EXPIRED` atau `UNFIT`, HR Staff menahan mereka di darat (*Off-Board*) untuk mencegah pekerja sakit beroperasi di lapangan.
* **Kalkulasi Payroll Terotomasi (Business Flow)**:
   * Mengambil data *Timesheet* berdasarkan *Roster* untuk kru operasional lapangan (Offshore). Sistem memiliki logika eksklusif yang secara otomatis **mengecualikan peran Admin dan HR Staff** dari slip gaji lapangan.

### ⚙️ 3. Role: Chief Engineer (Kepala Teknisi Mesin)
**Kapasitas:** Bertanggung jawab penuh atas pengelolaan aset kapal, inventaris, dan jadwal *Maintenance*.
* **IoT Predictive Monitoring (Business Flow)**:
   * Login ke modul Aset (`/assets`). Chief Engineer memantau daftar mesin terhubung **IoT Telemetry Streaming**.
   * Grafik *real-time* menampilkan suhu dan getaran mesin. Jika melampaui batas kritis, sistem akan menyorot alat tersebut dengan peringatan merah (*Needs Maintenance*).
* **Pembuatan Work Order & Auto-Booking Inventory (Form Data)**:
   * Chief Engineer menekan tombol **Create Work Order** dan menambahkan kebutuhan material dari **Inventory Terpadu**.
   * *Otomatisasi Sistem*: Sistem melakukan **Smart Inventory Reservation**, yaitu mencadangkan (*booking*) jumlah stok secara logis, memastikan material aman dari WO lain tanpa memotong fisik sebelum eksekusi selesai.
   * *Work Order* di-*publish* ke sistem operasional untuk dieksekusi.
* **Verifikasi & Finalisasi WO (Business Flow) 🔑**:
   * Setelah Safety Officer menutup PTW, WO otomatis berubah ke status `WAITING_REVIEW`.
   * Chief Engineer melihat badge ungu **Waiting Review** di tabel Work Order, lalu klik **Complete WO** untuk memverifikasi bahwa material benar-benar terpakai.
   * *Otomatisasi Sistem*: WO berubah menjadi `COMPLETED` dan sistem **Auto-Deduct** stok inventory secara permanen.

### 🦺 4. Role: Safety Officer (Pengendali Keselamatan / HSE)
**Kapasitas:** Bertugas memastikan bahwa semua *Work Order* dieksekusi dengan aman tanpa mengancam nyawa.
* **Monitoring Real-time (UI Flow)**: 
   * Login dan membuka Dashboard HSE. Terus memantau **Live POB** (`/hse/live-pob`) dan **Daftar Izin Kerja/PTW** (`/hse/ptw`).
* **Review & Approval (Form & Business Flow)**:
   * Melalui WebSockets, saat Worker mengirim Izin Kerja (PTW), layar berkedip/bunyi (status PTW: `PENDING`).
   * Officer me-review lokasi kerja (`deck_location`). Jika aman, memasukkan *Digital Signature* dan menekan **Approve**.
* **Pengecekan Akhir Lapangan (Form Data)**:
   * Ketika Worker melaporkan selesai, Officer turun ke lapangan untuk memastikan lokasi kerja steril. Ia kemudian menginput `closing_notes` dan menekan **Confirm Close**.
   * *Otomatisasi Sistem*: PTW = `CLOSED` dan WO otomatis berubah ke `WAITING_REVIEW`. **Inventory belum terpotong** — ini adalah ranah verifikasi teknis Chief Engineer.
* **Protokol Darurat "Emergency Lockdown"**:
   * Jika ada kebakaran, Officer mengaktifkan status "CONDITION RED". **Aplikasi seketika membekukan seluruh fitur pengajuan Izin Kerja**. Layar beralih mode merah dan memaksa kru memantau *Live POB* guna mengatur prioritas area evakuasi.

### 👷‍♂️ 5. Role: Worker (Offshore Crew / Pekerja Lapangan)
**Kapasitas:** Mengeksekusi pekerjaan fisik di lapangan berdasarkan *Work Order*.
* **Cek Tugas (UI Flow)**: Login (diarahkan ke `/hse`). Worker mengecek daftar *Work Order* (WO) yang di-assign untuknya hari itu dengan status `PENDING`.
* **Pembuatan Izin Kerja / PTW**:
   * Worker diwajibkan untuk menekan **Request PTW** langsung dari Work Order tersebut. Izin kerja ini akan terkait secara hierarkis (Status PTW: `PENDING`).
* **Eksekusi & Auto Check-In (Business Flow) 🔥**:
   * Begitu PTW disetujui oleh Safety Officer, Worker diwajibkan mengisi lembar *Pre-Job Safety Verification* (JSA/TBT), mengumpulkan tanda tangan, dan mengunggah foto lapangan.
   * Setelah diverifikasi, Worker menekan tombol **Start Work**.
   * *Otomatisasi Sistem*: Di belakang layar, status PTW dan WO berubah menjadi `IN_PROGRESS`, lalu **sistem melacak titik awal pekerja (Check-In) dan memunculkannya di Peta Live POB kapal secara real-time**.
* **Penyelesaian & Auto Check-Out (Business Flow) 🔥**:
   * Pekerjaan selesai, Worker menekan **Mark as Job Done** beserta `completion_notes`.
   * *Otomatisasi Sistem*: Aplikasi secara otomatis mencabut titik lokasi pekerja dari peta *Live POB* (Auto Check-Out), PTW berubah menjadi `WAITING_FOR_CLOSE`, menandakan ia sudah keluar dari zona bahaya.

---

### 🌟 Kesimpulan: "Siklus Kehidupan" (The Life Cycle) Sistem

Sistem SAIPEM UOS ini adalah sebuah rantai operasi yang kuat dan anti-bocor:
1. **Admin** membuat fondasi data kapal, struktur *Deck Location*, dan otorisasi *Role* akun pengguna.
2. **HR Staff** memfilter pekerja, memastikan hanya kru "Sehat" (MCU *Fit*) dan sedang bertugas (*On-board*) yang dapat mengakses modul HSE.
3. **Chief Engineer** memantau *IoT Telemetry*, merilis *Work Order*, dan memesan (*Reserve*) stok inventaris secara otomatis.
4. **Worker** melihat *Work Order* miliknya, lalu wajib merilis Permohonan Izin Kerja (*Request PTW*) ke sistem untuk divalidasi.
5. **Safety Officer** memastikan lokasi aman, tidak ada konflik LOTO, lalu memberikan Izin (*Approve* PTW).
6. **Worker** mengisi *Pre-Job Safety* (JSA/TBT) dan mengeklik *Start Work*, memicu **Auto Check-In Live POB**. *Safety Officer* melacak pergerakan kru selama pekerjaan *In Progress*.
7. Pekerjaan selesai, **Worker** mengeklik *Mark as Job Done* untuk *Auto Check-Out* dari area bahaya. PTW = `WAITING_FOR_CLOSE`.
8. **Safety Officer** melakukan verifikasi lapangan dan menutup (Close) izin kerja → PTW = `CLOSED` dan WO berubah ke **`WAITING_REVIEW`**. Inventory belum dipotong.
9. **Chief Engineer** memverifikasi pekerjaan secara teknis dan mengeklik **Complete WO** → WO = `COMPLETED` + **Auto-Deduct Inventory** secara permanen. Seluruh data transaksi diarsip abadi secara transparan.
