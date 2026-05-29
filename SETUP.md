# 🚀 Saipem HSE - Team Setup Guide

Panduan lengkap untuk setup project HSE Management System untuk tim development.

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
- PostgreSQL 12+
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
VITE_WS_URL=ws://localhost:8989/ws/pob/
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

## 📁 Project Structure

```
saipemuos/
├── backend/                 # Django REST API
│   ├── core_system/        # Django settings
│   ├── auth_module/        # Authentication
│   ├── hr_module/          # HR Management
│   ├── hse_module/         # HSE Core (POB, PTW, Safety, Analytics)
│   ├── asset_module/       # Asset Management
│   ├── offshore_module/    # Offshore Operations
│   ├── scripts/            # Management commands
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/               # Vue 3 + Vite
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── views/         # Page components
│   │   ├── store/         # State management
│   │   ├── utils/         # Utility functions
│   │   ├── router/        # Vue Router
│   │   └── App.vue
│   ├── package.json
│   ├── vite.config.js
│   ├── .env
│   └── README.md
│
├── .gitignore
├── README.md
└── SETUP.md               # This file
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
