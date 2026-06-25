# HR Module
**Manajemen Sumber Daya Manusia & Rotasi Offshore**

HR Module berfokus pada pelacakan kualifikasi pekerja, penjadwalan ke lapangan (Roster), dan perhitungan jam terbang pekerja untuk kompensasi. Modul ini merupakan garis pertahanan pertama (Safety Interlock) yang mencegah pekerja tidak berkualifikasi masuk ke area operasional kapal.

## 1. Tanggung Jawab Utama
*   **Personnel Registry**: Mencatat data kru, posisi pekerjaan, dan status Medical Check-Up (MCU).
*   **Smart MCU Blocker**: Otomatis menolak penjadwalan pekerja jika status MCU mereka `UNFIT` atau masa berlaku MCU sudah habis (`EXPIRED`).
*   **Certification Management**: Mencatat sertifikasi teknis dan keselamatan (contoh: Hot Work, Confined Space, BOSIET).
*   **Roster Matrix**: Menjadwalkan pekerja ke dalam Vessel untuk periode rotasi tertentu.
*   **Offshore Payroll System**: Kalkulasi kompensasi otomatis berdasarkan durasi *On Board* dikali dengan tarif harian (*Daily Rate*) jabatan tersebut, eksklusif hanya untuk peran lapangan.

## 2. Aktor Utama
*   **HR Staff**: Memasukkan data medis kru, mengunggah sertifikat, dan mengelola jadwal ploting kru pada Roster Matrix.

## 3. Fitur & Endpoint API (`/api/v1/hr/`)
*   `GET/POST /employees/` - Manajemen daftar pekerja.
*   `PUT /employees/update/<emp_id>/` - Update profil dan verifikasi *Fit to Work* (MCU).
*   `GET/POST /certifications/<emp_id>/` - Manajemen sertifikat K3 dan teknis per pekerja.
*   `GET/POST /rosters/` - Alokasi jadwal pekerja (Roster) ke Kapal (Vessel).
*   `GET /payroll/` - Kalkulasi gaji/payroll operasional offshore secara otomatis.
*   `GET /analytics/` - Dashboard HR (Statistik jabatan, status MCU, Roster aktif).

## 4. Alur Kerja (Flow)
1. **Registrasi Pekerja**: HR Staff mendaftarkan kru baru beserta Job Position-nya.
2. **Validasi Medis & Skill**: HR memastikan status kesehatan (MCU) di-update dan mengunggah histori sertifikat kompetensi.
3. **Ploting Roster**: HR Staff menugaskan pekerja ke Vessel. Jika MCU `UNFIT`, sistem membatalkan proses (Error Failsafe).
4. **Perubahan Status Onboard**: Saat kru masuk jadwal Roster, status mereka dapat dikonversi menjadi `ONBOARD`.
5. **Kalkulasi Payroll**: Saat akhir bulan, sistem merangkum jumlah hari aktif di Roster untuk kalkulasi gaji kru offshore.

## 5. Keterkaitan dengan Modul Lain
*   **CORE Module**: Mengaitkan profil Employee HR dengan Akun Login/User Django.
*   **HSE Module**: Sistem Permit to Work (PTW) di HSE Module selalu memverifikasi apakah pemohon izin sedang berstatus *Onboard* (berdasarkan Roster HR) dan apakah MCU-nya *Fit* sebelum izin disetujui.
