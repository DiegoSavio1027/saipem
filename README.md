# Saipem UOS (Unified Offshore System)

![Vue.js](https://img.shields.io/badge/Vue.js-3.0-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Build](https://img.shields.io/badge/build-passing-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)

## 📌 Deskripsi Singkat Proyek

**Saipem UOS** adalah sistem manajemen terintegrasi tingkat lanjut yang dirancang khusus untuk mengelola operasional *Human Resources* (HR), *Asset/Vessel*, dan *Health, Safety, and Environment* (HSE) secara tersentralisasi. Sistem ini digunakan oleh admin, staf HSE, dan manajemen eksekutif untuk memantau status pekerja (termasuk kelayakan medis/MCU), melacak aktivitas kapal, memanajemen asstet, dan menerbitkan Surat Izin Kerja Aman (Permit to Work). Dengan Saipem UOS, koordinasi operasional lepas pantai (offshore) menjadi lebih transparan, aman, dan efisien dari ujung ke ujung.


---

## 🚀 Fitur Utama (Key Features)

- **Sistem Autentikasi Terpusat:** Role-Based Access Control (RBAC) dengan JWT (JSON Web Token) untuk Admin, HR, HSE Officer, dan Management.
- **HR Module (Manajemen Personalia & Jadwal):**
  - Manajemen data karyawan lengkap beserta histori sertifikasinya.
  - Penjadwalan Roster pekerja ke kapal (vessel) secara real-time.
  - **Smart Blocker MCU:** Sistem otomatis mencegah pekerja yang berstatus medis *UNFIT* atau sertifikasi kesehatannya telah *EXPIRED* untuk dijadwalkan ke lapangan kerja.
- **Asset Module (Manajemen Kapal & Peralatan):**
  - Manajemen detail kapal (Vessel) beserta lokasinya (deck/area).
  - Pelacakan Machinery, Spare Parts, Inventory, dan Maintenance Tasks.
  - Work Order (Surat Perintah Kerja) untuk setiap aset.
- **HSE Module (K3 & Personnel On Board):**
  - Pembuatan dan persetujuan elektronik untuk *Permit to Work* (PTW).
  - Sistem pencatatan POB (Personnel On Board) *real-time* berbasis WebSocket dan Redis.
  - Manajemen Laporan Insiden (Incident Management).
- **Dashboard Interaktif & Analitik:** Visualisasi data komprehensif bagi pimpinan untuk memantau keselamatan dan operasional harian.

---

## 📂 Struktur Direktori Proyek (Folder Tree)

Struktur repositori ini dibagi menjadi dua bagian utama: `backend` (Django) dan `frontend` (Vue.js).

```text
saipem-hse/
├── backend/                  # Django REST API Backend
│   ├── asset_module/         # Asset, Machinery, Inventory, & Work Order
│   ├── auth_module/          # Authentication & Manajemen Role Akses
│   ├── core_system/          # URL Utama & Konfigurasi Settings Django
│   ├── hr_module/            # Modul Karyawan, Roster Matrix, & Validasi MCU
│   ├── hse_module/           # Permit to Work, Incident Report, & POB
│   ├── offshore_module/      # Pemetaan Lokasi (Vessel & Area Deck)
│   ├── manage.py             # Entry point utama untuk Django CLI
│   └── requirements.txt      # Daftar dependensi Python
│
├── frontend/                 # Vue.js 3 Frontend Web App
│   ├── public/               # File Statis publik
│   ├── src/                  # *Source code* utama aplikasi Vue
│   │   ├── assets/           # File gambar, CSS/Tailwind
│   │   ├── components/       # Komponen UI Vue yang dapat digunakan ulang
│   │   ├── router/           # Konfigurasi Vue Router (Navigasi URL)
│   │   ├── stores/           # Manajemen State (Pinia)
│   │   ├── views/            # Halaman utama aplikasi (Dashboard, HR, HSE)
│   │   └── App.vue           # Root Component Vue
│   ├── package.json          # Daftar dependensi NPM / Node.js
│   └── vite.config.js        # Konfigurasi *build tool* Vite
│
└── README.md                 # Dokumentasi Proyek yang sedang Anda baca
```

---

## ⚖️ Perbandingan Proses Bisnis (Sebelum vs Sesudah Automasi)

| Proses Manual (Lama) 🔴 | Automasi Sistem (Baru) 🟢 | Dampak Positif 🚀 |
| --- | --- | --- |
| Pengecekan MCU/Sertifikat pekerja dilakukan manual via dokumen kertas/Excel sebelum ditugaskan ke kapal lepas pantai. | **Smart Blocker:** Sistem secara otomatis menolak pembuatan Roster jika status MCU pekerja *UNFIT* atau sudah lewat tanggal kedaluwarsa. | Menghilangkan risiko kelalaian (human error) 100%, memangkas waktu verifikasi medis dari jam menjadi instan. |
| Pengajuan *Permit to Work* (PTW) memakan waktu lama karena pencarian tanda tangan fisik *Safety Officer*. | Persetujuan PTW dilakukan secara digital. Form langsung terhubung ke status aset dan pekerja. | Memangkas waktu tunggu dokumen hingga 80%, pekerjaan lebih cepat dimulai. |
| Manajemen Maintenance dan Work Order aset dicatat dalam dokumen terpisah dengan risiko hilang. | *Work Order* dan *Maintenance Task* terhubung ke *Inventory*. Penggunaan *Spare Part* tercatat otomatis. | Perencanaan pemeliharaan lebih presisi dan riwayat servis terpusat (*traceable*). |
| Sulit melacak total *Personnel On Board* (POB) di atas kapal. | Sistem POB terhubung dengan jadwal *Roster* HR. | Total manifest penumpang (POB) terpantau transparan dan *real-time*. |

---

## 🔄 Diagram Alur Proses Bisnis Terintegrasi (Workflows)

### 1. Alur HR - Roster Scheduling & Smart MCU Blocker
```mermaid
sequenceDiagram
    participant HR as HR Admin
    participant System as Saipem UOS Backend
    participant DB as Database
    
    HR->>System: Buat Jadwal Roster (Pekerja, Kapal, Tanggal)
    activate System
    System->>DB: Query Data Employee (MCU Status, Expiry)
    DB-->>System: Return Data Karyawan
    
    alt MCU = UNFIT atau Expired < Hari Ini
        System--xHR: ❌ Error 400: Deployment Denied (Medically UNFIT/Expired)
    else MCU = FIT dan Belum Kedaluwarsa
        System->>DB: Simpan Data Roster
        DB-->>System: Data Tersimpan
        System-->>HR: ✅ Success: Roster Tersimpan
        System->>System: Update POB (Personnel on Board)
    end
    deactivate System
```

### 2. Alur HSE - Permit to Work (PTW)
```mermaid
sequenceDiagram
    participant Worker as HSE Officer / Requester
    participant System as Saipem UOS
    participant Manager as Management / Approver
    
    Worker->>System: Buat Permit to Work (Aset, Pekerja, Lokasi)
    activate System
    System-->>System: Validasi Pekerja (Harus ada di Roster Kapal ybs)
    System->>System: Status PTW = DRAFT
    System-->>Worker: Form PTW Disimpan
    deactivate System
    
    Worker->>System: Submit for Approval
    System-->>Manager: Notifikasi (Dashboard/UI)
    
    Manager->>System: Approve PTW
    activate System
    System->>System: Update Status = APPROVED, Form Terkunci
    System-->>Worker: PTW Diterbitkan (Active)
    deactivate System
```

### 3. Alur ASSET - Work Order & Maintenance
```mermaid
sequenceDiagram
    participant Eng as Engineer
    participant System as Saipem UOS
    participant DB as Inventory & Asset DB
    
    Eng->>System: Buat Work Order (WO) untuk Machinery X
    System-->>Eng: WO Terbuat (Pending)
    
    Eng->>System: Tambahkan Sparepart yang digunakan ke WO
    activate System
    System->>DB: Cek Stok Sparepart (Inventory)
    alt Stok Cukup
        System->>DB: Kurangi Stok (Deduct Inventory)
        System-->>Eng: Sparepart Ditambahkan
    else Stok Kurang
        System--xEng: ❌ Error: Insufficient Stock
    end
    deactivate System
    
    Eng->>System: Selesaikan WO (Complete)
    System->>DB: Update Status Machinery (Operational)
```

---

## 🌐 Dokumentasi API Endpoints Lengkap (Django REST)

Seluruh API berada pada path dasar: `http://localhost:8989/api/v1/`

### 🛡️ 1. Auth Module (`/api/v1/auth/`)
Sistem autentikasi menggunakan JWT (JSON Web Token).
- `POST /login/` - Login dan dapatkan akses token
- `POST /token/` - Dapatkan Access & Refresh token (Token Pair)
- `POST /token/refresh/` - Refresh Access token
- `GET /me/` - Mendapatkan profile user yang sedang login
- `POST /logout/` - Logout sistem
- `GET/POST /users/` - Manajemen Akun (List/Create) - *Admin Only*
- `GET/PUT/DELETE /users/<id>/` - Detail, Update, Hapus Akun
- `GET /dev/quick-login-accounts/` - Mendapatkan list akun demo (Dev only)

### 👥 2. HR Module (`/api/v1/hr/`)
- `GET /employees/` - List seluruh karyawan
- `POST /employees/add/` - Menambah karyawan baru
- `DELETE /employees/delete/<emp_id>/` - Menghapus karyawan
- `POST /employees/toggle/<emp_id>/` - Mengganti status ketersediaan (*Available/On Board*)
- `PUT /employees/update/<emp_id>/` - Update profil dan status MCU karyawan
- `GET /rosters/` - List jadwal *Roster*
- `DELETE /rosters/delete/<id>/` - Menghapus *Roster*
- `GET /activities/` - List Vessel Activity (Aktivitas Kapal)
- `DELETE /activities/delete/<id>/` - Menghapus Aktivitas
- `GET /payroll/` - Mengambil kalkulasi otomatis payroll/gaji pekerja
- `GET /analytics/` - Dashboard analitik HR (statistik MCU, roster, dll)
- `GET /positions/` - Master data *Job Position*
- `DELETE /positions/delete/<id>/` - Menghapus posisi
- `GET /certifications/<emp_id>/` - Detail sertifikasi per pekerja
- `POST /certifications/add/<emp_id>/` - Tambah sertifikat baru
- `DELETE /certifications/delete/<cert_id>/` - Hapus sertifikat

### 🦺 3. HSE Module (`/api/v1/hse/`)
- `GET/POST /ptw/` - Buat/List *Permit to Work* (PTW)
- `GET/PUT/DELETE /ptw/<id>/` - Kelola detail PTW (Approve/Reject)
- `GET/POST /employees/` - (Router PTW) List/Tambah pekerja dalam konteks HSE
- `GET /pob/` - Data Personnel On Board (POB) *real-time*
- `GET/POST /incidents/` - List/Buat Laporan Insiden Kecelakaan Kerja
- `GET/PUT/DELETE /incidents/<id>/` - Update Laporan Insiden
- `GET/POST /status/` - System Status Operasional HSE
- `GET /analytics/` - Grafik analitik HSE (Safe man hours, Incident Rate)

### 🚢 4. Offshore Module (`/api/v1/offshore/`)
Manajemen Lokasi (Deck/Area) dan penghubungan ke Kapal Utama.
- `GET /vessels/` - List Kapal (Khusus tampilan relasional area)
- `GET /vessels/<id>/` - Detail Kapal
- `POST /vessels/<id>/assign-decks/` - Menugaskan *Deck/Area* ke dalam suatu Kapal
- `DELETE /vessels/<id>/assign-decks/<deck_id>/` - Melepas penugasan *Deck* dari Kapal
- `GET /locations/` - List Lokasi Offshore (Deck)
- `GET /locations/<id>/` - Detail Lokasi

### 🔧 5. Asset Module (`/api/v1/asset/`)
- `GET /assets/` - List Seluruh Kapal Utama (*Vessel Assets*)
- `GET /assets/<asset_id>/` - Detail *Asset*
- `GET /machinery/` - Peralatan mesin yang terpasang pada *Asset*
- `GET /machinery/<id>/` - Detail *Machinery*
- `GET /spareparts/` - Master data Suku Cadang (*Spare Part*)
- `GET /spareparts/<id>/` - Detail *Spare Part*
- `GET /workorders/` - List Surat Perintah Kerja (WO)
- `GET /workorders/<id>/` - Detail WO
- `GET /maintenance/` - List Jadwal Tugas Pemeliharaan Rutin
- `GET /maintenance/<id>/` - Detail *Maintenance Task*
- `GET /inventory/` - Stok *Inventory* Barang
- `GET /inventory/<id>/` - Detail Stok

*(Catatan: Sebagian besar endpoint Asset Module mendukung operasi lengkap POST/PUT/DELETE tergantung hak akses role Anda)*

---

## 👥 Pemetaan Tugas Aktor (Actor Role Mapping)

| Aktor / Role | Hak Akses & Aksi Spesifik di Aplikasi | Automasi & Proses Sistem di Latar Belakang |
| --- | --- | --- |
| **Super Admin / System Administrator** | • *Full Access* ke semua modul sistem.<br>• Manajemen CRUD Akun Pengguna & Role (Assign Role, reset password).<br>• Manajemen Master Data Absolut: *Vessel, Machinery, Job Positions, Location/Deck, Inventory*. | • Log audit sistem terekam untuk setiap perubahan data kritikal.<br>• Menerapkan perlindungan integritas relasi *database* (misal: memblokir penghapusan *Vessel* jika masih ada pekerja *On Board* atau PTW aktif di dalamnya). |
| **HR Manager / HR Admin** | • Menambahkan profil *Employee*, *Job Position*, dan histori *Certification* pekerja.<br>• Menyusun jadwal alokasi pekerja (*Roster Matrix*) ke lokasi/kapal tertentu.<br>• Melakukan pembaruan status kelayakan *Medical Check-Up* (MCU).<br>• Memproses kalkulasi *Payroll/Timesheet* otomatis.<br>• Memantau *Analytics Dashboard* departemen HR. | • **Smart MCU Blocker:** Sistem secara *real-time* menolak form penjadwalan *Roster* jika pekerja berstatus medis *UNFIT* atau sertifikasinya *EXPIRED*.<br>• Kalkulasi penggajian otomatis di- *generate* berdasarkan *Daily Rate* posisi dikali dengan durasi hari pada *Roster*.<br>• *Auto-trigger* penambahan kuota manifest *Personnel On Board* (POB) kapal saat jadwal pekerja dimulai. |
| **HSE Officer / Safety Inspector** | • Membuat form *Permit to Work* (PTW) untuk pekerjaan berisiko (Panas, Dingin, Ruang Terbatas).<br>• Menginput *Incident Report* (Laporan Kecelakaan Kerja) lengkap dengan kronologi.<br>• Memantau daftar riil *Personnel On Board* (POB) harian.<br>• Mengupdate *System Status* keamanan operasional. | • **PTW Location Conflict Check:** Sistem memastikan lokasi/deck *Permit to Work* tidak tumpang tindih dengan pekerjaan berbahaya lainnya di area yang sama.<br>• Sistem otomatis memverifikasi pekerja yang dimasukkan ke form PTW benar-benar sedang berada di kapal tersebut (*POB Validation*).<br>• Sistem secara otomatis mengakumulasi log *Safe Man Hours* harian dari total POB. |
| **Asset Engineer / Maintenance Manager** | • Menerbitkan dan menjalankan *Work Order* (WO) untuk peralatan mesin.<br>• Mengelola stok masuk/keluar *Spare Part* & *Inventory*.<br>• Menjadwalkan *Maintenance Tasks* berkala untuk tiap *Machinery* di atas kapal. | • **Auto-Deduct Inventory:** Sistem otomatis mengurangi (deduct) stok barang di *Inventory* secara *real-time* ketika suku cadang digunakan di dalam suatu WO aktif.<br>• Sistem otomatis mengubah status operasional mesin menjadi *Under Maintenance* selama WO berjalan, mencegah mesin digunakan dalam operasional (terhubung ke modul HSE). |
| **Executive Management / OIM (Offshore Installation Manager)** | • Memiliki kewenangan akhir untuk melakukan *Approval* atau *Rejection* terhadap *Permit to Work* (PTW).<br>• Melakukan *Approval* terhadap *Work Order* yang membutuhkan material/biaya tingkat tinggi.<br>• Mengakses *High-Level Analytics Dashboard* (Statistik Insiden, Total POB Lintas Kapal, Utilisasi Pekerja). | • Saat izin PTW di-*approve*, form tersebut otomatis terkunci oleh sistem (*hukum read-only / immutable*) untuk tujuan audit.<br>• Status *Permit to Work* otomatis berubah menjadi *Active*.<br>• Mengkompilasi agregasi Big Data dari 3 modul (HR, HSE, Asset) menjadi visualisasi grafik tanpa membebani *query* performa harian aplikasi. |
| **Offshore Crew / General Worker** | • *Read-only access* ke portal pekerja.<br>• Melihat detail jadwal *Roster* keberangkatan dan penugasan lokasi pribadi miliknya.<br>• Mengecek masa berlaku *Certification* dan *MCU* pribadinya sendiri. | • Sistem *cron job* dapat men-*trigger* notifikasi peringatan (misal H-30) kepada pekerja secara sistemik jika sertifikat atau pemeriksaan medisnya akan segera kedaluwarsa. |

---

## 📸 Tangkapan Layar / Demo Visual

*(Tambahkan Screenshot Aplikasi Di Sini)*
> `Contoh format: ![HSE Dashboard](/docs/images/hse-dashboard.png)`
> `Contoh format: ![Smart Blocker MCU Error](/docs/images/mcu-error.png)`
> `Contoh format: ![Work Order Flow](/docs/images/work-order.png)`

---

## ⚙️ Prasyarat Sistem (Prerequisites)

Pastikan sistem operasi Anda (Windows/macOS/Linux) telah terpasang perangkat lunak berikut:
- **Python** (>= 3.10)
- **Node.js** (>= 18.x) & **NPM** (>= 9.x)
- **PostgreSQL** atau **SQLite** (Default untuk *development*)
- **Redis Server** (Wajib untuk fitur *real-time WebSocket* & POB)
- **Git**

---

## 🚀 Saipem HSE - Team Setup Guide

Panduan lengkap untuk *setup project* HSE Management System untuk tim *development*.

---

## 📋 Quick Start (Clone Repository)

### Untuk Teman yang Ingin Clone Repository

**Repository**: `https://github.com/DiegoSavio1027/saipemuos.git` (Private)

#### Opsi 1: Clone dengan PAT (Personal Access Token)

```bash
# Clone dengan PAT embedded
git clone https://DiegoSavio1027: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@github.com/DiegoSavio1027/saipemuos.git

cd saipemuos
```

#### Opsi 2: Clone Normal + Input PAT saat Diminta

```bash
# Clone repository
git clone https://github.com/DiegoSavio1027/saipemuos.git

cd saipemuos

# Saat diminta credentials:
# Username: DiegoSavio1027
# Password: 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
```

#### Opsi 3: Setup SSH (Recommended untuk jangka panjang)

Jika ingin menghindari input PAT setiap kali, setup SSH key:

```bash
# Generate SSH key (jika belum punya)
ssh-keygen -t ed25519 -C "your-email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Paste ke GitHub: Settings → SSH and GPG keys → New SSH key

# Clone dengan SSH
git clone git@github.com:DiegoSavio1027/saipemuos.git

cd saipemuos
```

---

## 🔧 Backend Setup

### Prerequisites
- Python 3.10+
- PostgreSQL 12+ (atau SQLite bawaan Django)
- Redis Server (Wajib untuk fitur real-time WebSocket)
- pip (Python package manager)

### Installation Steps

**1. Navigate to backend directory**
```bash
cd backend
```

**2. Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Setup environment variables**
```bash
# Copy example env file
cp .env.example .env

# Edit .env dengan database credentials kamu
nano .env  # atau gunakan editor favorit
```

**Required environment variables:**
```env
# Database Configuration
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=saipem_offshore_db
DATABASE_USER=pgadmin
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Media Files
MEDIA_ROOT=media/
MEDIA_URL=/media/
```

**5. Run database migrations**
```bash
python manage.py migrate
```

**6. Seed initial data**
```bash
# Initialize system status
python manage.py seed_hse_data

# Create test users
python manage.py seed_auth_users
```

**7. Create superuser (admin)**
```bash
python manage.py createsuperuser
```

**8. Start development server**
```bash
# Pastikan server Redis sudah berjalan sebelum mengeksekusi ini
python manage.py runserver 0.0.0.0:8989
```

Backend runs at: `http://localhost:8989`

### Test Users (After Seeding)

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Safety Officer | safety_officer | safety123 |
| Worker | worker | worker123 |

---

## 🎨 Frontend Setup

### Prerequisites
- Node.js 18.0+
- npm or yarn

### Installation Steps

**1. Navigate to frontend directory**
```bash
cd frontend
```

**2. Install dependencies**
```bash
npm install
```

**3. Create environment file**
```bash
cat > .env << EOF
VITE_API_BASE_URL=http://localhost:8989/api/v1
VITE_WS_URL=ws://localhost:8989/ws/pob_updates/
EOF
```

**4. Start development server**
```bash
npm run dev
```

Frontend runs at: `http://localhost:5173`

### Available Scripts

```bash
# Development server with HMR
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🔐 Authentication & PAT Management

### Personal Access Token (PAT) Info

**Token**: `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`

**Permissions**: Full access to private repositories

**Expiry**: Check GitHub settings for expiration date

### Storing PAT Securely

#### macOS (Keychain)
```bash
# Store in Keychain
git config --global credential.helper osxkeychain

# First push will prompt for credentials, then stores in Keychain
git push
```

#### Linux (Pass)
```bash
# Install pass
sudo apt-get install pass

# Configure git
git config --global credential.helper pass

# Initialize pass
pass init your-gpg-key-id
```

#### Windows (Credential Manager)
```bash
# Configure git
git config --global credential.helper manager-core

# First push will prompt for credentials, then stores in Credential Manager
git push
```

---

## 🚀 Development Workflow

### 1. Pull Latest Changes
```bash
git pull origin main
```

### 2. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes
- Backend: Edit files in `backend/`
- Frontend: Edit files in `frontend/`

### 4. Test Changes
```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests (if configured)
cd frontend
npm run test
```

### 5. Commit Changes
```bash
git add .
git commit -m "feat: description of your changes"
```

### 6. Push to GitHub
```bash
git push origin feature/your-feature-name
```

### 7. Create Pull Request
- Go to GitHub repository
- Create PR from your branch to `main`
- Add description and request review

### 8. Merge to Main
- After review and approval
- Merge PR to main branch
- Delete feature branch

---

## 🐛 Troubleshooting

### Backend Issues

**Database Connection Error**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -U pgadmin -d saipem_offshore_db

# If connection fails, check .env DATABASE_* variables
```

**Migration Errors**
```bash
# Show migration status
python manage.py showmigrations

# Reset migrations (CAUTION: deletes data)
python manage.py migrate hse_module zero
python manage.py migrate
```

**Port Already in Use**
```bash
# Run on different port
python manage.py runserver 0.0.0.0:8990
```

### Frontend Issues

**Dependencies Installation Failed**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**API Connection Failed**
```bash
# Check .env file
cat .env

# Verify backend is running on http://localhost:8989
# Verify VITE_API_BASE_URL is correct
```

**Port 5173 Already in Use**
```bash
# Run on different port
npm run dev -- --port 5174
```

### Git Issues

**Authentication Failed**
```bash
# Update remote URL with PAT
git remote set-url origin https://DiegoSavio1027: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@github.com/DiegoSavio1027/saipemuos.git

# Try push again
git push origin main
```

**Merge Conflicts**
```bash
# Pull latest changes
git pull origin main

# Resolve conflicts in your editor
# Then commit
git add .
git commit -m "Resolve merge conflicts"
git push origin feature/your-branch
```

---

## 📚 Documentation

- **Backend README**: `backend/README.md` - Detailed API documentation
- **Frontend README**: `frontend/README.md` - UI components and features
- **API Docs**: `http://localhost:8989/api/schema/swagger/` (when backend running)

---

## 🤝 Team Collaboration Tips

1. **Always pull before starting work**
   ```bash
   git pull origin main
   ```

2. **Use descriptive commit messages**
   ```bash
   git commit -m "feat: add PTW approval workflow"
   git commit -m "fix: resolve POB tracking bug"
   git commit -m "docs: update API documentation"
   ```

3. **Keep branches updated**
   ```bash
   git fetch origin
   git rebase origin/main
   ```

4. **Review before pushing**
   ```bash
   git diff origin/main
   ```

5. **Communicate with team**
   - Inform team before major changes
   - Discuss architecture decisions
   - Review each other's code

---

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Review backend/frontend README files
3. Check API documentation at `/api/schema/swagger/`
4. Contact team lead

---

**Last Updated**: May 29, 2026  
**Version**: 1.0.0  
**Status**: Ready for Team Collaboration ✅
