# CORE Module
**Pusat Pengaturan Sistem & Autentikasi**

CORE Module adalah tulang punggung dari aplikasi Saipem UOS. Modul ini menangani keamanan, manajemen pengguna, serta pendataan lokasi dasar yang akan digunakan oleh semua modul lainnya (HR, Engineering, HSE).

## 1. Tanggung Jawab Utama
*   **Autentikasi & Otorisasi**: Mengamankan endpoint API dengan JSON Web Token (JWT) dan membedakan hak akses berdasarkan *Role* (Admin, HR, Engineer, HSE, Worker).
*   **User Management**: Mendaftarkan akun pengguna baru, mengatur password, dan menetapkan jabatan operasional.
*   **Vessel Registry**: Mendaftarkan kapal-kapal (Vessel) tempat operasional berlangsung (seperti Saipem 7000, Castorone).
*   **Deck & Work Locations**: Memetakan struktur fisik kapal (contoh: Engine Room, Main Deck) lengkap dengan tingkat bahaya (Risk Level).

## 2. Aktor Utama
*   **Admin / System Administrator**: Satu-satunya peran yang memiliki akses penuh ke fitur manajemen akun dan konfigurasi master data Vessel/Deck.

## 3. Fitur & Endpoint API
Modul ini secara teknis mencakup aplikasi Django `auth_module`, `core_system`, dan `offshore_module`.

### Authentication & Users (`/api/v1/auth/`)
*   `POST /login/` - Autentikasi dan penerbitan Access & Refresh Token.
*   `GET /me/` - Mendapatkan profil *user* yang sedang login.
*   `POST /logout/` - Mengakhiri sesi (Blacklist Token).
*   `GET/POST /users/` - Menampilkan & membuat akun baru (Admin Only).
*   `PUT/DELETE /users/<id>/` - Mengupdate atau menghapus akun.

### Master Data Kapal & Lokasi (`/api/v1/offshore/`)
*   `GET/POST /vessels/` - Manajemen identitas Kapal Utama.
*   `GET/POST /locations/` - Manajemen area kerja (Deck).
*   `POST /vessels/<id>/assign-decks/` - Menugaskan (mapping) suatu area Deck ke dalam Kapal tertentu.

## 4. Alur Kerja (Flow)
1. **Inisiasi Sistem**: Admin mendaftarkan profil Kapal (Vessel) dan menentukan nama-nama Deck Location.
2. **Setup Karyawan**: Admin mendaftarkan akun login untuk personel yang akan digunakan untuk mengakses sistem (terhubung ke Employee ID).
3. **Role Assignment**: Saat registrasi, Admin memilih grup otorisasi yang akan menentukan menu apa saja yang bisa dilihat pengguna di Frontend Vue.

## 5. Keterkaitan dengan Modul Lain
*   **HR Module**: Menggunakan daftar *Vessel* dari CORE untuk menjadwalkan penempatan kru (Roster).
*   **Engineering Module**: Aset mesin dan Inventory selalu terkait pada *Vessel* tertentu.
*   **HSE Module**: PTW dan Live POB sangat bergantung pada data *Deck Location* untuk memetakan titik koordinat evakuasi.
