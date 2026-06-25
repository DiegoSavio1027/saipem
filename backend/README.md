# HSE (Health, Safety & Environment) Management System - Backend

## 📋 Project Overview

Comprehensive HSE management system for offshore vessel operations. The system implements ISO 45001 compliance standards with real-time monitoring, incident reporting, permit-to-work management, HR management, and asset maintenance tracking.

### Key Features
- **JWT Authentication**: Secure token-based authentication with role-based access control
- **HR Management**: Employee management, position tracking, certification management, and payroll
- **Real-time POB Tracking**: Live headcount and personnel location monitoring
- **Permit to Work (PTW)**: Hazardous work authorization and approval workflow
- **Incident Management**: Safety incident reporting with automatic metrics updates
- **System Status Monitoring**: Global safety condition tracking (GREEN/YELLOW/RED)
- **Asset Management**: Predictive maintenance scheduling and asset tracking
- **Analytics & Compliance**: ISO 45001 compliance tracking with historical trend analysis
- **WebSocket Integration**: Real-time updates for dashboard and live feeds

---

## 🏗️ Project Structure

```
backend/
├── core_system/              # Django project settings & configuration
│   ├── settings.py          # Main Django settings
│   ├── urls.py              # Root URL routing
│   ├── asgi.py              # ASGI config for WebSocket support
│   └── wsgi.py              # WSGI config for production
│
├── auth_module/             # Authentication & Authorization Module
│   ├── models.py            # UserProfile model
│   ├── views.py             # JWT login/logout endpoints
│   ├── serializers.py       # User & token serializers
│   ├── permissions.py       # Custom permission classes
│   └── signals.py           # Auto-create user profiles
│
├── hr_module/               # Human Resources Management Module
│   ├── models.py            # Position, Certification, Asset models
│   ├── views.py             # HR API endpoints
│   ├── serializers.py       # HR data serialization
│   └── migrations/          # Database migrations
│
├── hse_module/              # HSE Core Module (contains all HSE submodules)
│   ├── hse_pob/            # Person on Board (POB) Tracking
│   │   ├── models.py       # POBLog, WorkLocation models
│   │   ├── views.py        # POB API endpoints
│   │   ├── serializers.py  # POB data serialization
│   │   └── consumers.py    # WebSocket consumers for real-time updates
│   │
│   ├── hse_ptw/            # Permit to Work (PTW) Management
│   │   ├── models.py       # PermitToWork, Employee, WorkOrder models
│   │   ├── views.py        # PTW API endpoints (CRUD, approve, reject, etc)
│   │   └── serializers.py  # PTW data serialization
│   │
│   ├── hse_safety/         # Safety Incidents & Metrics
│   │   ├── models.py       # Incident, SystemStatus, StatusOverride models
│   │   ├── views.py        # Incident & Status API endpoints
│   │   └── serializers.py  # Incident data serialization
│   │
│   ├── hse_analytics/      # Analytics & Compliance Reporting
│   │   ├── models.py       # IncidentTrend, SafetyMetrics, ComplianceReport, LocationStatistics
│   │   ├── views.py        # Analytics API endpoints
│   │   ├── serializers.py  # Analytics data serialization
│   │   └── management/commands/
│   │       └── aggregate_analytics.py  # Analytics aggregation command
│   │
│   └── urls.py             # HSE module URL routing
│
├── asset_module/            # Asset & Maintenance Management Module
│   ├── models.py            # MaintenanceTask model
│   ├── views.py             # Asset & maintenance API endpoints
│   ├── serializers.py       # Asset data serialization
│   └── migrations/          # Database migrations
│
├── offshore_module/         # Offshore Operations Module
│   ├── models.py            # Offshore-specific models
│   ├── views.py             # Offshore API endpoints
│   └── serializers.py       # Offshore data serialization
│
├── scripts/                 # Management Commands & Utilities
│   └── management/commands/
│       ├── seed_hse_data.py        # Initialize SystemStatus singleton
│       └── seed_auth_users.py      # Create test users with JWT authentication
│
├── media/                   # User-uploaded files (incident proofs, signatures, etc)
│   └── incident_proofs/     # Incident proof images
│
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in git)
└── README.md               # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 12+
- pip (Python package manager)

### Installation

**1. Clone and navigate to backend directory**
```bash
cd backend
```

**2. Create and activate virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your database credentials and settings
```

**Required environment variables:**
```env
# Database
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=saipem_offshore_db
DATABASE_USER=pgadmin
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Media Files
MEDIA_ROOT=media/
MEDIA_URL=/media/
```

**5. Run migrations**
```bash
python manage.py migrate
```

**6. Seed initial data**
Jalankan perintah berikut secara berurutan untuk mengisi *database* dengan data awal (dummy data) yang lengkap:

```bash
# 1. Initialize system status
python manage.py seed_hse_data

# 2. Create test users & groups
python manage.py seed_auth_users

# 3. Create HR employees, roster, & assets data
python manage.py seed_hr_asset_data

# 4. Create inventory items
python manage.py seed_inventory
```

**7. Create superuser (admin)**
```bash
python manage.py createsuperuser
```

**8. Start development server**
Buka terminal dan jalankan backend server:
```bash
python manage.py runserver 0.0.0.0:8989
```

Server runs at: `http://localhost:8989`

**9. Run IoT Telemetry Simulator (Opsional namun Penting)**
Buka terminal **baru** (biarkan server tetap berjalan), lalu jalankan simulator IoT untuk menghasilkan data sensor suhu & getaran mesin secara *real-time*:
```bash
python manage.py run_iot_simulator
```

> **💡 Catatan Integrasi Production (Koneksi ke Sistem IoT Asli)**  
> Script simulator di atas menginjeksi data langsung ke *database* menggunakan Django ORM untuk kemudahan *development*.  
> Untuk menghubungkan sistem dengan **perangkat IoT / Sensor fisik sesungguhnya** (seperti NodeMCU, PLC, atau *Edge Gateway*), Anda bisa menerapkan salah satu arsitektur berikut ke depannya:
> 1. **Via REST API (HTTP POST)**: Tambahkan endpoint *ingestion* baru (contoh: `POST /api/v1/asset/telemetry/ingest/`) di backend yang siap menerima payload JSON dari perangkat sensor Anda, lalu menyimpannya ke model `TelemetryLog`.
> 2. **Via MQTT Broker (Rekomendasi Industri)**: Setup sebuah *broker* MQTT (seperti Mosquitto/EMQX). Biarkan sensor *publish* data ke topik MQTT, lalu jalankan sebuah *worker script* di server (menggunakan *library* `paho-mqtt` atau Celery) yang *subscribe* ke topik tersebut dan mencatat datanya ke dalam sistem Saipem UOS secara asinkron.

---

## 📦 Core Modules Overview

### 1. **auth_module** - Authentication & Authorization
**Purpose**: JWT-based authentication with role-based access control

**Key Models**:
- `UserProfile`: Extended user profile with job role and roster information

**Key Features**:
- JWT token authentication (access + refresh tokens)
- Role-based permissions (Worker, Safety Officer, Admin)
- Custom token serializer with user info
- Auto-create user profiles via signals

**API Endpoints**:
- `POST /api/auth/login/` - Login and get JWT tokens
- `POST /api/auth/logout/` - Logout (blacklist refresh token)
- `POST /api/auth/token/refresh/` - Refresh access token
- `GET /api/auth/me/` - Get current user info

**Authentication Header**:
```
Authorization: Bearer <access_token>
```

---

### 2. **hr_module** - Human Resources Management
**Purpose**: Employee management, position tracking, and certification management

**Key Models**:
- `Position`: Job positions with daily rates and allowances
- `Certification`: Employee certifications with expiry tracking

**Key Features**:
- Position and salary rate management
- Employee certification tracking with expiry dates
- Integration with PTW module (Employee model)
- Certification expiry alerts

**API Endpoints**:
- `GET /api/hr/positions/` - List all positions
- `POST /api/hr/positions/` - Create new position
- `GET /api/hr/certifications/` - List certifications
- `POST /api/hr/certifications/` - Add certification
- `GET /api/hr/certifications/expiring/` - Get expiring certifications

---

### 3. **hse_module** - HSE Core Module

The HSE module contains four submodules for comprehensive safety management:

#### 3.1. **hse_pob** - Person on Board Tracking
**Purpose**: Real-time tracking of personnel location and check-in/check-out events

**Key Models**:
- `POBLog`: Records check-in/check-out events with timestamp and location
- `WorkLocation`: Vessel deck locations (Engine Room, Heli Deck, Main Deck, Safe Zone)

**Key Features**:
- Real-time WebSocket updates for live headcount
- Location-based personnel tracking
- Check-in/check-out feed for dashboard
- Integration with PTW (auto check-in when work starts)

**API Endpoints**:
- `GET /api/v1/hse/pob/` - List all POB logs
- `POST /api/v1/hse/pob/` - Create check-in/check-out event
- `GET /api/v1/hse/locations/` - List work locations

---

#### 3.2. **hse_ptw** - Permit to Work Management
**Purpose**: Manage hazardous work authorization and approval workflow

**Key Models**:
- `PermitToWork`: PTW request with status workflow
- `Employee`: Employee information (emp_id, full_name, job_role)
- `WorkOrder`: Work order details

**PTW Workflow**:
```
PENDING → APPROVED → IN_PROGRESS → WAITING_FOR_CLOSE → CLOSED
         (Safety Officer)  (Worker)      (Worker)      (Safety Officer)
```

**Key Features**:
- Multi-step approval workflow
- Auto check-in when work starts (IN_PROGRESS)
- Auto check-out when work marked as done
- Digital signature capture for approvals
- Rejection with reason tracking

**API Endpoints**:
- `GET /api/v1/hse/ptw/` - List PTWs
- `POST /api/v1/hse/ptw/` - Create new PTW
- `POST /api/v1/hse/ptw/{id}/approve/` - Approve PTW
- `POST /api/v1/hse/ptw/{id}/reject/` - Reject PTW
- `POST /api/v1/hse/ptw/{id}/start_work/` - Start work (IN_PROGRESS)
- `POST /api/v1/hse/ptw/{id}/mark_done/` - Mark as job done
- `POST /api/v1/hse/ptw/{id}/confirm_close/` - Confirm close

---

#### 3.3. **hse_safety** - Safety Incidents & Metrics
**Purpose**: Incident reporting and system-wide safety metrics tracking

**Key Models**:
- `Incident`: Safety incident reports with severity levels
- `SystemStatus`: Singleton model tracking global safety metrics
- `StatusOverride`: Audit trail for manual status changes

**Incident Severity Levels**:
- `SAFETY_OBSERVATION`: Minor hazard observation
- `NEAR_MISS`: Close call without injury
- `FIRST_AID`: Minor injury requiring first aid
- `LTI`: Lost Time Injury (major incident)

**System Metrics Tracked**:
- `days_without_lti`: Days since last LTI incident
- `near_misses_count`: Total near miss incidents
- `global_status`: System condition (GREEN/YELLOW/RED)
- `active_permits`: Currently active PTWs

**Auto-Generated Incident IDs**:
- Format: `{SEVERITY}-{count:03d}`
- Examples: `LTI-001`, `NEAR_MISS-002`, `FIRST_AID-001`

**API Endpoints**:
- `GET /api/v1/hse/incidents/` - List incidents
- `POST /api/v1/hse/incidents/` - Report new incident
- `PATCH /api/v1/hse/incidents/{id}/` - Update incident
- `DELETE /api/v1/hse/incidents/{id}/` - Delete incident
- `GET /api/v1/hse/status/current/` - Get current system status
- `POST /api/v1/hse/status/override/` - Manual status override

---

#### 3.4. **hse_analytics** - Analytics & Compliance Reporting
**Purpose**: Historical trend analysis, safety performance reporting, and compliance tracking

**Key Models**:
- `IncidentTrend`: Aggregated incident statistics by time period (daily/weekly/monthly/quarterly/yearly)
- `SafetyMetrics`: Daily safety performance snapshots with LTIFR/TRIFR calculations
- `ComplianceReport`: ISO 45001 audit reports with compliance scoring
- `LocationStatistics`: Per-location statistics with risk scoring and hotspot analysis

**Key Features**:
- Historical incident trend analysis across multiple time periods
- Safety performance metrics with injury frequency rates (LTIFR, TRIFR)
- ISO 45001 compliance tracking with audit findings
- Location-based risk scoring and hotspot identification
- Automatic metric calculations (compliance scores, risk scores)
- Filtering and date range queries for custom reports

**API Endpoints**:
- `GET /api/v1/hse/analytics/trends/` - List incident trends
- `GET /api/v1/hse/analytics/trends/latest/` - Get latest trend by period type
- `GET /api/v1/hse/analytics/trends/summary/` - Get trend summary (last 12 periods)
- `GET /api/v1/hse/analytics/metrics/` - List safety metrics
- `GET /api/v1/hse/analytics/metrics/latest/` - Get latest safety metrics
- `GET /api/v1/hse/analytics/metrics/weekly_summary/` - Get last 7 days metrics
- `GET /api/v1/hse/analytics/metrics/monthly_summary/` - Get last 30 days metrics
- `GET /api/v1/hse/analytics/compliance/` - List compliance reports
- `GET /api/v1/hse/analytics/compliance/latest/` - Get latest compliance report
- `GET /api/v1/hse/analytics/compliance/compliance_summary/` - Get compliance statistics
- `GET /api/v1/hse/analytics/locations/` - List location statistics
- `GET /api/v1/hse/analytics/locations/hotspots/` - Get high-risk locations
- `GET /api/v1/hse/analytics/locations/location_trend/` - Get trend for specific location
- `GET /api/v1/hse/analytics/locations/summary/` - Get summary for all locations

**Query Parameters**:
- `period_type`: Filter by DAILY/WEEKLY/MONTHLY/QUARTERLY/YEARLY
- `start_date`: Filter by start date (YYYY-MM-DD)
- `end_date`: Filter by end date (YYYY-MM-DD)
- `status`: Filter by status (GREEN/YELLOW/RED or COMPLIANT/PARTIAL/NON_COMPLIANT)
- `location`: Filter by location name
- `threshold`: Risk score threshold for hotspots (default: 50.0)
- `limit`: Limit number of results
- `days`: Number of days for trend analysis (default: 30)

**Automatic Data Aggregation**:
Analytics data is automatically aggregated from operational data using a background scheduler (APScheduler):

- **Schedule**: Runs every 6 hours + daily at 1:00 AM
- **Data Sources**:
  - `IncidentTrend`: Aggregated from `hse_safety.Incident` (grouped by period)
  - `SafetyMetrics`: Calculated from `SystemStatus`, `PermitToWork`, `POBLog` (daily snapshots)
  - `ComplianceReport`: Auto-generated with 7-point compliance checks
  - `LocationStatistics`: Aggregated from `hse_pob.POBLog` (per-location occupancy & incidents)

- **Manual Trigger**:
```bash
# Aggregate all analytics data
python manage.py aggregate_analytics

# Aggregate specific type
python manage.py aggregate_analytics --type metrics      # Safety metrics only
python manage.py aggregate_analytics --type locations    # Location statistics only
python manage.py aggregate_analytics --type trends       # Incident trends only
python manage.py aggregate_analytics --type compliance   # Compliance reports only

# Aggregate for specific date
python manage.py aggregate_analytics --date 2026-05-27

# Aggregate last N days
python manage.py aggregate_analytics --days-back 60

# Force re-aggregate (delete and recreate)
python manage.py aggregate_analytics --force
```

**Compliance Checks** (7-point scoring):
1. PTW Signature Compliance (90% threshold)
2. PTW Approval Compliance (80% threshold)
3. No LTI Incidents
4. Incident Closure Rate (70% threshold)
5. POB Check-in Compliance (95% threshold)
6. System Status (GREEN status required)
7. PTW Same-Day Closure (50% threshold)

---

### 4. **asset_module** - Asset & Maintenance Management
**Purpose**: Predictive maintenance scheduling, machinery tracking, and spare parts management

**Key Models**:
- `Vessel`: Vessel information and operational status
- `MachineryEquipment`: Equipment tracking with operating hours for predictive maintenance
- `SparePart`: Spare parts inventory management with reorder levels
- `WorkOrder`: Work orders created by Chief Engineer
- `MaintenanceTask`: Scheduled maintenance tasks linked to equipment and work orders

**Key Features**:
- Predictive maintenance based on operating hours
- Equipment lifecycle tracking with operating hours
- Spare parts inventory management with reorder alerts
- Work order management (created by Chief Engineer)
- Priority-based task management (LOW, MEDIUM, HIGH, CRITICAL)
- Integration with HR module for crew assignment
- Maintenance history and reporting
- Multi-vessel support with vessel filtering

**API Endpoints**:
- `GET /api/asset/vessels/` - List vessels
- `GET /api/asset/equipment/` - List machinery equipment
- `GET /api/asset/equipment/{id}/hours/` - Get operating hours
- `GET /api/asset/spareparts/` - List spare parts
- `GET /api/asset/spareparts/low-stock/` - Get low stock alerts
- `GET /api/asset/workorders/` - List work orders
- `POST /api/asset/workorders/` - Create work order (Chief Engineer)
- `GET /api/asset/maintenance/` - List maintenance tasks
- `POST /api/asset/maintenance/` - Create maintenance task
- `GET /api/asset/maintenance/overdue/` - Get overdue tasks

---

### 5. **offshore_module** - Offshore Operations
**Purpose**: Offshore-specific operations and vessel management

**Key Features**:
- Offshore vessel operations management
- Integration with HSE and HR modules
- Offshore-specific workflows and reporting

**API Endpoints**:
- `GET /api/offshore/` - List offshore operations
- (Additional endpoints based on specific offshore requirements)

---

## 🗄️ Database Models

### Auth Module
```
UserProfile
├── id (PK)
├── user (OneToOne to Django User)
├── job_role
└── roster_status (ONBOARD/OFFBOARD)
```

### HR Module
```
Position
├── id (PK)
├── title (unique)
├── discipline
├── daily_rate
└── allowance_rate

Certification
├── cert_id (PK)
├── cert_type
├── employee (FK to Employee)
└── expiry_date
```

### HSE POB Module
```
WorkLocation
├── id (PK)
├── vessel (FK to Vessel)
├── name (Engine Room, Heli Deck, etc)
└── description

POBLog
├── id (PK)
├── emp_id (FK to Employee)
├── deck_location (FK to WorkLocation)
├── action (IN/OUT)
├── timestamp
└── ptw (FK to PermitToWork, nullable)
```

### HSE PTW Module
```
Employee
├── emp_id (PK)
├── full_name
├── job_role
└── department

PermitToWork
├── id (PK)
├── permit_id (unique)
├── vessel (FK to Vessel)
├── emp_id (FK to Employee)
├── wo_id (FK to WorkOrder - from Asset Module)
├── permit_type (HOT_WORK, CONFINED_SPACE, etc)
├── deck_location (FK to WorkLocation)
├── status (PENDING, APPROVED, IN_PROGRESS, etc)
├── approved_by
├── approved_at
└── signature
```

### HSE Safety Module
```
Incident
├── id (PK)
├── incident_id (auto-generated, unique)
├── vessel (FK to Vessel)
├── severity (SAFETY_OBSERVATION, NEAR_MISS, FIRST_AID, LTI)
├── location (FK to WorkLocation)
├── description
├── proof_image
├── employee_name
├── reported_by (emp_id)
├── incident_date
├── reported_date
├── status (OPEN, INVESTIGATING, CLOSED)
├── investigation_notes
├── closed_by
└── closed_date

SystemStatus (Singleton)
├── id = 1 (always)
├── global_status (GREEN, YELLOW, RED)
├── days_without_lti
├── last_lti_date
├── near_misses_count
├── active_permits
└── last_incident_date

StatusOverride
├── id (PK)
├── previous_status
├── new_status
├── override_reason
├── changed_by (emp_id)
└── created_at
```

### HSE Analytics Module
```
IncidentTrend
├── id (PK)
├── period_type (DAILY, WEEKLY, MONTHLY, QUARTERLY, YEARLY)
├── period_start
├── period_end
├── safety_observation_count
├── near_miss_count
├── first_aid_count
├── lti_count
├── total_incidents
├── days_without_lti
├── average_response_time
├── created_at
└── updated_at

SafetyMetrics
├── id (PK)
├── date (unique)
├── total_pob
├── total_ptw_issued
├── total_ptw_completed
├── total_ptw_rejected
├── average_ptw_duration
├── days_without_lti
├── near_misses_count
├── total_incidents
├── ltifr (Lost Time Injury Frequency Rate)
├── trifr (Total Recordable Injury Frequency Rate)
├── global_status (GREEN, YELLOW, RED)
└── created_at

ComplianceReport
├── id (PK)
├── report_type (DAILY, WEEKLY, MONTHLY, QUARTERLY, ANNUAL)
├── report_date
├── period_start
├── period_end
├── overall_status (COMPLIANT, PARTIAL, NON_COMPLIANT)
├── compliance_score (0-100)
├── total_checks
├── passed_checks
├── failed_checks
├── findings
├── recommendations
├── auditor_name
├── auditor_emp_id
├── created_at
└── updated_at

LocationStatistics
├── id (PK)
├── location_name
├── date
├── total_check_ins
├── total_check_outs
├── average_occupancy
├── peak_occupancy
├── total_incidents
├── total_ptw_issued
├── risk_score (0-100, calculated)
└── created_at
```

### Asset Module
```
Vessel
├── id (PK)
├── vessel_name (unique)
├── vessel_type
├── imo_number
└── operational_status

MachineryEquipment
├── id (PK)
├── vessel (FK to Vessel)
├── equipment_name
├── equipment_type
├── serial_number
├── installation_date
├── operating_hours
├── last_maintenance_date
└── maintenance_interval_hours

SparePart
├── id (PK)
├── vessel (FK to Vessel)
├── part_name
├── part_number
├── quantity_on_hand
├── reorder_level
├── supplier
└── unit_cost

WorkOrder
├── wo_id (PK)
├── vessel (FK to Vessel)
├── created_by (Chief Engineer)
├── description
├── priority (LOW, MEDIUM, HIGH, CRITICAL)
├── scheduled_date
├── status (PENDING, IN_PROGRESS, COMPLETED, CANCELLED)
└── created_at

MaintenanceTask
├── task_id (PK)
├── vessel (FK to Vessel)
├── equipment (FK to MachineryEquipment)
├── wo_id (FK to WorkOrder)
├── description
├── priority (LOW, MEDIUM, HIGH, CRITICAL)
├── scheduled_date
├── status (PENDING, IN_PROGRESS, COMPLETED)
├── assigned_crew (FK to Employee)
└── completion_date
```

---

## 🔌 WebSocket Integration

Real-time updates via WebSocket for live dashboard updates.

**Consumer**: `hse_module.hse_pob.consumers.POBConsumer`

**WebSocket URL**: `ws://localhost:8989/ws/pob/`

**Events**:
- `pob_dashboard`: POB location updates
- `ptw_updates`: PTW status changes
- `incident_alerts`: New incident reports

**Usage Example**:
```javascript
// Frontend WebSocket connection
const ws = new WebSocket('ws://localhost:8989/ws/pob/');

ws.onopen = () => {
  console.log('WebSocket connected');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Real-time update:', data);
  // Handle real-time updates (POB, PTW, incidents)
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('WebSocket disconnected');
};
```

**Note**: WebSocket requires Daphne ASGI server (not Django development server for production)

---

## 🔐 Authentication & Permissions

**Authentication Method**: JWT (JSON Web Token) via `djangorestframework-simplejwt`

**Token Types**:
- **Access Token**: Short-lived token for API requests (expires in 60 minutes)
- **Refresh Token**: Long-lived token to obtain new access tokens (expires in 7 days)

**User Roles & Permissions**:

### Worker Role
- ✅ Submit Permit to Work (PTW)
- ✅ Check-in/Check-out (POB tracking)
- ✅ Report incidents (Safety Observation, Near Miss, First Aid)
- ✅ View own PTW history
- ✅ View own incidents
- ✅ Start work on approved PTW
- ✅ Mark PTW as done
- ❌ Cannot approve/reject PTW
- ❌ Cannot override system status
- ❌ Cannot view other workers' data

### Safety Officer Role
- ✅ View all PTWs
- ✅ Approve/Reject PTWs with digital signature
- ✅ Close completed PTWs
- ✅ View all incidents
- ✅ Investigate incidents
- ✅ Manual status override (emergency)
- ✅ View analytics and compliance reports
- ✅ View POB tracking and location hotspots
- ❌ Cannot delete PTWs/incidents (audit trail)
- ❌ Cannot manage employees or work locations

### Admin Role
- ✅ Full system access
- ✅ Manage employees and work orders
- ✅ Create/Edit/Delete work locations
- ✅ View all data and audit trails
- ✅ Access Django admin panel
- ✅ Manage system settings
- ✅ Manage user roles and permissions

**Permission Implementation**:
- ViewSet-level permissions using Django REST Framework
- Object-level permissions for PTW and Incident access
- Group-based permissions (Worker, Safety Officer, Admin groups)
- Custom permission classes in `auth_module/permissions.py`

**Authentication Flow**:
1. User logs in with username/password → receives access + refresh tokens
2. Client stores tokens (localStorage/sessionStorage)
3. Client includes access token in Authorization header for API requests
4. When access token expires, use refresh token to get new access token
5. When refresh token expires, user must log in again

---

## 📊 Dashboard Metrics

The dashboard displays real-time metrics from multiple modules:

| Metric | Source | Calculation |
|--------|--------|-------------|
| **Live Headcount** | hse_pob | Count of personnel with action=IN |
| **Active Permits** | hse_ptw | Count of PTWs with status=IN_PROGRESS |
| **Days Without LTI** | hse_safety | Days since last LTI incident |
| **Near Misses Logged** | hse_safety | Total count of NEAR_MISS incidents |
| **Global Status** | hse_safety | GREEN/YELLOW/RED based on metrics |
| **Pending PTWs** | hse_ptw | Count of PTWs with status=PENDING |
| **Open Incidents** | hse_safety | Count of incidents with status=OPEN |
| **Compliance Score** | hse_analytics | Latest compliance report score (0-100) |

**Real-time vs Analytics**:
- **Real-time Metrics** (Dashboard): Come from operational modules (hse_safety, hse_ptw, hse_pob)
- **Historical Analytics**: Aggregated daily by hse_analytics module for trend analysis and compliance reporting
- **Compliance Reports**: Auto-generated daily with 7-point compliance checks

**Status Color Coding**:
- 🟢 **GREEN**: All systems normal, no critical issues
- 🟡 **YELLOW**: Warning state, attention required
- 🔴 **RED**: Critical state, immediate action required

---

## 🛠️ Development

### Running Tests
```bash
python manage.py test
```

### Running Specific Module Tests
```bash
python manage.py test hse_module.hse_ptw
python manage.py test auth_module
python manage.py test hr_module
```

### Creating Migrations
```bash
# Create migrations for all apps
python manage.py makemigrations

# Create migrations for specific app
python manage.py makemigrations hse_module

# Apply migrations
python manage.py migrate
```

### Django Admin Panel
Access at: `http://localhost:8989/admin`

Login with superuser credentials created during setup.

### API Documentation
- **Swagger UI**: `http://localhost:8989/api/schema/swagger/`
- **ReDoc**: `http://localhost:8989/api/schema/redoc/`
- **OpenAPI Schema**: `http://localhost:8989/api/schema/`

### Code Quality Tools
```bash
# Format code with Black
black .

# Lint with flake8
flake8 .

# Type checking with mypy
mypy .
```

### Database Shell
```bash
# Django shell
python manage.py shell

# PostgreSQL shell
psql -U pgadmin -d saipem_offshore_db
```

---

## 🚢 Deployment

### Production Checklist
- [ ] Set `DEBUG=False` in .env
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` with production domain
- [ ] Set up PostgreSQL production database
- [ ] Configure static files serving (`collectstatic`)
- [ ] Set up SSL/HTTPS certificates
- [ ] Configure CORS for production domain
- [ ] Set up media files storage (S3/local)
- [ ] Use production ASGI server (Daphne/Uvicorn)
- [ ] Set up process manager (systemd/supervisor)
- [ ] Configure logging and monitoring
- [ ] Set up database backups
- [ ] Configure firewall rules

### Using Daphne (WebSocket support)
```bash
# Install Daphne (already in requirements.txt)
pip install daphne

# Run Daphne server
daphne -b 0.0.0.0 -p 8989 core_system.asgi:application

# Run with multiple workers
daphne -b 0.0.0.0 -p 8989 --workers 4 core_system.asgi:application
```

### Using Gunicorn (HTTP only, no WebSocket)
```bash
# Install Gunicorn
pip install gunicorn

# Run Gunicorn
gunicorn core_system.wsgi:application --bind 0.0.0.0:8989 --workers 4
```

### Systemd Service Example
```ini
[Unit]
Description=HSE Backend Service
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/daphne -b 0.0.0.0 -p 8989 core_system.asgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

### Nginx Reverse Proxy Configuration
```nginx
upstream hse_backend {
    server 127.0.0.1:8989;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://hse_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws/ {
        proxy_pass http://hse_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    location /media/ {
        alias /path/to/backend/media/;
    }

    location /static/ {
        alias /path/to/backend/staticfiles/;
    }
}
```

---

## 📚 API Response Format

All API responses follow a consistent format for better client-side handling:

**Success Response**:
```json
{
  "data": {
    "id": 1,
    "name": "Example"
  },
  "message": "Operation successful",
  "status": 200
}
```

**List Response**:
```json
{
  "data": [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"}
  ],
  "count": 2,
  "message": "Retrieved successfully",
  "status": 200
}
```

**Error Response**:
```json
{
  "error": "Error message",
  "detail": "Detailed error information",
  "status": 400
}
```

**Validation Error Response**:
```json
{
  "error": "Validation failed",
  "detail": {
    "field_name": ["Error message for this field"]
  },
  "status": 400
}
```

---

## 🐛 Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -U pgadmin -d saipem_offshore_db

# Reset migrations (CAUTION: deletes data)
python manage.py migrate hse_module zero
python manage.py migrate
```

### WebSocket Connection Failed
- Ensure Daphne is running (not Django development server)
- Check CORS settings in `core_system/settings.py`
- Verify WebSocket URL in frontend (ws:// or wss://)
- Check firewall rules for WebSocket port

### Permission Denied Errors
- Check user role and group assignments in Django admin
- Verify `get_queryset()` filters in ViewSets
- Check `permission_classes` in views
- Ensure JWT token is valid and not expired

### Migration Conflicts
```bash
# Show migration status
python manage.py showmigrations

# Fake a migration (if already applied manually)
python manage.py migrate --fake hse_module 0001

# Squash migrations (combine multiple migrations)
python manage.py squashmigrations hse_module 0001 0010
```

### Media Files Not Serving
- Check `MEDIA_ROOT` and `MEDIA_URL` in settings
- Ensure media directory has correct permissions
- In production, serve media files via Nginx/Apache

### JWT Token Issues
```bash
# Token expired → use refresh token to get new access token
# Token invalid → user must log in again
# Token not provided → check Authorization header format
```

---

## 📞 Support & Documentation

### Official Documentation
- **Django**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **Channels (WebSocket)**: https://channels.readthedocs.io/
- **PostgreSQL**: https://www.postgresql.org/docs/
- **JWT Authentication**: https://django-rest-framework-simplejwt.readthedocs.io/

### Project Resources
- **Backend Repository**: Internal Git repository
- **API Documentation**: Available at `/api/schema/swagger/` when server is running
- **Issue Tracker**: Internal project management system

---

## 📄 License

**Internal Project** - Saipem Offshore Operations

This software is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

---

## 📝 Changelog

### Version 2.1.0 (May 29, 2026)
- ✅ Updated README with accurate project structure
- ✅ Added auth_module documentation (JWT authentication)
- ✅ Added hr_module documentation (HR management)
- ✅ Added asset_module documentation (maintenance management)
- ✅ Clarified hse_module as parent module containing submodules
- ✅ Updated deployment instructions with Daphne and Nginx examples
- ✅ Added troubleshooting section
- ✅ Improved API documentation

### Version 2.0.0 (May 28, 2026)
- ✅ PTW Management with multi-step workflow
- ✅ POB Tracking with real-time WebSocket updates
- ✅ Incident Reporting with automatic metrics
- ✅ Analytics & Compliance module
- ✅ WebSocket real-time updates

---

**Last Updated**: May 29, 2026  
**Version**: 2.1.0  
**Status**: Production Ready ✅  
**Python**: 3.10+  
**Django**: 5.2.4  
**Database**: PostgreSQL 12+

---

**Maintained by**: Saipem HSE Development Team
