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

### ⚙️ 3. Role: Chief Engineer (Kepala Teknisi Mesin)
**Kapasitas:** Bertanggung jawab penuh atas pengelolaan aset kapal (mesin/peralatan) dan jadwal *Maintenance*.
* **Predictive Monitoring (Business Flow)**:
   * Login ke modul Aset (`/assets`). Chief Engineer memantau daftar mesin.
   * Sistem secara cerdas menghitung sisa waktu berdasarkan *Operating Hours*. Jika batas waktu perawatan hampir habis, sistem akan menyorot alat tersebut dengan peringatan merah (*Needs Maintenance*).
* **Pembuatan Work Order (Form Data)**:
   * Chief Engineer menekan tombol **Create Work Order**. Ia mengatur jadwal (`scheduled_date`), prioritas (`HIGH`/`CRITICAL`), dan deskripsi pekerjaan.
   * *Work Order* ini di-*publish* ke sistem operasional untuk diambil oleh tim Worker.

### 🦺 4. Role: Safety Officer (Pengendali Keselamatan / HSE)
**Kapasitas:** Bertugas memastikan bahwa semua *Work Order* dieksekusi dengan aman tanpa mengancam nyawa.
* **Monitoring Real-time (UI Flow)**: 
   * Login dan membuka Dashboard HSE. Terus memantau **Live POB** (`/hse/live-pob`) dan **Daftar Izin Kerja/PTW** (`/hse/ptw`).
* **Review & Approval (Form & Business Flow)**:
   * Melalui WebSockets, saat Worker mengirim Izin Kerja (PTW), layar berkedip/bunyi (status PTW: `PENDING`).
   * Officer me-review lokasi kerja (`deck_location`). Jika aman, memasukkan *Digital Signature* dan menekan **Approve**.
* **Pengecekan Akhir Lapangan (Form Data)**:
   * Ketika Worker melaporkan selesai, Officer turun ke lapangan untuk memastikan lokasi kerja steril. Ia kemudian menginput `closing_notes` dan menekan **Confirm Close**.
* **Protokol Darurat "Emergency Lockdown"**:
   * Jika ada kebakaran, Officer mengaktifkan status "CONDITION RED". **Aplikasi seketika membekukan seluruh fitur pengajuan Izin Kerja**. Layar beralih mode merah dan memaksa kru memantau *Live POB* guna mengatur prioritas area evakuasi.

### 👷‍♂️ 5. Role: Worker (Pekerja Lapangan / Teknisi)
**Kapasitas:** Mengeksekusi pekerjaan fisik di lapangan berdasarkan *Work Order*.
* **Cek Tugas (UI Flow)**: Login (diarahkan ke `/hse`). Worker mengecek daftar *Work Order* yang di-assign untuknya hari itu.
* **Pembuatan Izin Kerja / PTW**:
   * Worker masuk ke menu **Permit to Work (PTW)** dan menekan *Create*. Ia memilih `deck_location` dan `permit_type`, lalu mengirimnya (Status: `PENDING`). Worker dilarang bekerja sebelum disetujui.
* **Eksekusi & Auto Check-In (Business Flow) 🔥**:
   * Begitu disetujui, Worker menekan tombol **Start Work** di aplikasinya.
   * *Otomatisasi Sistem*: Di belakang layar, **aplikasi melacak titik awal pekerja (Check-In) dan memunculkannya di Peta Live POB kapal**.
* **Penyelesaian & Auto Check-Out (Business Flow) 🔥**:
   * Pekerjaan selesai, Worker menekan **Mark as Done** beserta `completion_notes`.
   * *Otomatisasi Sistem*: Aplikasi secara otomatis mencabut titik lokasi pekerja dari peta *Live POB* (Auto Check-Out), mendandakan ia sudah keluar dari bahaya.

---

### 🌟 Kesimpulan: "Siklus Kehidupan" (The Life Cycle) Sistem

Sistem SAIPEM UOS ini adalah sebuah rantai operasi yang kuat dan anti-bocor:
1. **Admin** membuat fondasi data kapal dan profil penggunanya.
2. **HR Staff** memfilter pekerja, memastikan hanya pekerja "Sehat" dan sedang bertugas (*On-board*) yang memiliki akses ke dalam sistem kerja.
3. **Chief Engineer** mengidentifikasi aset kapal yang butuh perawatan dan merilis instruksi kerja (*Work Order*).
4. **Worker** melihat *Work Order* tersebut, lalu merilis Permohonan Izin Kerja (*PTW*) ke sistem.
5. **Safety Officer** memantau radar keamanan, memberikan Izin (*Approve*), dan melacak setiap jengkal pergerakan Worker yang sedang bekerja (*Live POB Check-In*).
6. Pekerjaan selesai, **Worker** *Check-Out* secara otomatis, **Safety Officer** menutup dokumen permanen, dan seluruh data diarsip selamanya untuk keperluan analitik serta audit perusahaan.
