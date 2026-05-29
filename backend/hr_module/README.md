# HR Module - Human Resources Management

## 📋 Module Overview

The HR Module manages all human resources operations including employee management, roster scheduling, vessel asset assignments, crew activities, and payroll calculations. It integrates seamlessly with the HSE system to ensure only medically fit personnel are deployed to hazardous work.

### Key Features
- **Employee Management**: Centralized crew database with medical certification tracking
- **Roster Scheduling**: Assign personnel to vessels with MCU (Medical Check-Up) validation
- **Asset Management**: Track vessel and equipment assignments
- **Vessel Activity Tracking**: Monitor crew activities and work assignments
- **Payroll Calculation**: Automated payroll processing based on roster and activities
- **Dashboard Analytics**: HR metrics and tactical insights
- **Position Master Rates**: Manage job positions and salary rates

---

## 🏗️ Module Structure

```
hr_module/
├── models.py              # Database models for HR data
├── views.py               # API endpoints for HR operations
├── serializers.py         # Data serialization for API responses
├── urls.py                # URL routing for HR endpoints
├── admin.py               # Django admin configuration
├── migrations/            # Database migrations
└── README.md             # This file
```

---

## 📊 Database Models

### 1. **Employee** (Shared from hse_ptw)
Represents crew members with medical and certification information.

**Fields**:
- `emp_id` (CharField, unique): Employee identifier
- `full_name` (CharField): Employee full name
- `job_role` (CharField): Job position/role
- `mcu_status` (CharField): Medical Check-Up status (FIT, UNFIT, EXPIRED)
- `mcu_expiry` (DateField): MCU expiration date
- `created_at` (DateTimeField): Record creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

**Integration Note**: Employee model is shared with hse_ptw module to maintain single source of truth for crew data.

---

### 2. **Asset**
Represents vessels and equipment used in operations.

**Fields**:
- `asset_id` (CharField, unique): Asset identifier
- `name` (CharField): Asset name (e.g., "Vessel Alpha", "Crane Unit 1")
- `capacity` (IntegerField): Personnel capacity or equipment capacity
- `status` (CharField): Asset operational status (ACTIVE, MAINTENANCE, INACTIVE)
- `created_at` (DateTimeField): Record creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

**Usage**: Assets are assigned to rosters and activities to track personnel deployment.

---

### 3. **Roster**
Represents crew scheduling and asset assignments.

**Fields**:
- `employee` (ForeignKey): Reference to Employee
- `asset` (ForeignKey): Reference to Asset (vessel assignment)
- `start_date` (DateField): Roster start date
- `end_date` (DateField): Roster end date
- `created_at` (DateTimeField): Record creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

**Validation Rules**:
- Employee MCU status must be FIT (not UNFIT or EXPIRED)
- Employee MCU expiry date must not be in the past
- Prevents deployment of medically unfit personnel

**Integration**: Roster validation prevents unfit personnel from being assigned to PTW work.

---

### 4. **VesselActivity**
Tracks crew activities and work assignments on vessels.

**Fields**:
- `asset` (ForeignKey): Reference to Asset (vessel)
- `start_date` (DateField): Activity start date
- `end_date` (DateField): Activity end date
- `activity_name` (CharField): Description of activity
- `created_at` (DateTimeField): Record creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

**Usage**: Records what activities are happening on each vessel during specific periods.

---

### 5. **Certification**
Represents crew certifications and qualifications.

**Fields**:
- `employee` (ForeignKey): Reference to Employee
- `certification_name` (CharField): Certification type
- `issue_date` (DateField): Certification issue date
- `expiry_date` (DateField): Certification expiration date
- `issuing_authority` (CharField): Authority that issued certification
- `created_at` (DateTimeField): Record creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

**Usage**: Track professional certifications required for specific job roles.

---

### 6. **Position**
Master data for job positions and salary rates.

**Fields**:
- `position_name` (CharField): Job position title
- `base_salary` (DecimalField): Base monthly salary
- `allowance` (DecimalField): Position-specific allowance
- `description` (TextField): Position description
- `created_at` (DateTimeField): Record creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

**Usage**: Reference data for payroll calculations and position management.

---

## 🔌 API Endpoints

All endpoints use the `/api/v1/hr/` prefix and require authentication.

### Employee Management

**List All Employees**
```
GET /api/v1/hr/employees/
Response: [{ emp_id, full_name, job_role, mcu_status, mcu_expiry, ... }]
```

**Add New Employee**
```
POST /api/v1/hr/employees/add/
Body: { emp_id, full_name, job_role, mcu_status, mcu_expiry }
Response: { id, emp_id, full_name, ... }
```

**Update Employee**
```
PUT /api/v1/hr/employees/update/<emp_id>/
Body: { full_name, job_role, mcu_status, mcu_expiry }
Response: { id, emp_id, full_name, ... }
```

**Delete Employee**
```
DELETE /api/v1/hr/employees/delete/<emp_id>/
Response: { status: "deleted" }
```

**Toggle Roster Status**
```
POST /api/v1/hr/employees/toggle/<emp_id>/
Response: { emp_id, roster_status }
```

---

### Roster Management

**List All Rosters**
```
GET /api/v1/hr/rosters/
Response: [{ id, employee, title, start, end, location, ... }]
```

**Create Roster**
```
POST /api/v1/hr/rosters/
Body: { employee, asset_id, start_date, end_date }
Response: { id, employee, title, start, end, location }
Validation: Employee MCU must be FIT and not expired
```

**Delete Roster**
```
DELETE /api/v1/hr/rosters/delete/<pk>/
Response: { status: "deleted" }
```

---

### Asset Management

**List All Assets**
```
GET /api/v1/hr/assets/
Response: [{ asset_id, name, capacity, status, ... }]
```

**Create Asset**
```
POST /api/v1/hr/assets/
Body: { asset_id, name, capacity, status }
Response: { id, asset_id, name, capacity, status }
```

**Delete Asset**
```
DELETE /api/v1/hr/assets/delete/<asset_id>/
Response: { status: "deleted" }
```

---

### Vessel Activity

**List All Activities**
```
GET /api/v1/hr/activities/
Response: [{ id, asset, asset_name, start, end, activity_name, ... }]
```

**Create Activity**
```
POST /api/v1/hr/activities/
Body: { asset, start_date, end_date, activity_name }
Response: { id, asset, asset_name, start, end, activity_name }
```

**Delete Activity**
```
DELETE /api/v1/hr/activities/delete/<pk>/
Response: { status: "deleted" }
```

---

### Payroll & Analytics

**Calculate Payroll**
```
GET /api/v1/hr/payroll/
Response: [{ employee, period, gross_salary, allowance, deductions, net_salary }]
```

**Dashboard Analytics**
```
GET /api/v1/hr/analytics/
Response: {
  total_employees: number,
  active_rosters: number,
  upcoming_deployments: number,
  payroll_summary: { ... }
}
```

---

### Position Management

**List All Positions**
```
GET /api/v1/hr/positions/
Response: [{ id, position_name, base_salary, allowance, description, ... }]
```

**Create Position**
```
POST /api/v1/hr/positions/
Body: { position_name, base_salary, allowance, description }
Response: { id, position_name, base_salary, allowance, description }
```

**Delete Position**
```
DELETE /api/v1/hr/positions/delete/<pk>/
Response: { status: "deleted" }
```

---

## 🔐 Access Control

### Role-Based Permissions

**Admin**:
- Full access to all HR operations
- Can create, update, delete employees, rosters, assets, positions
- Can view all analytics and payroll data

**Safety Officer**:
- View-only access to employee and roster data
- Can view analytics and payroll summaries
- Cannot modify HR data

**Worker**:
- View own employee information
- View own roster assignments
- Cannot modify any HR data

---

## 🔗 Integration Points

### With HSE PTW Module
- **Employee Sharing**: Employee model is shared from hse_ptw to maintain single source of truth
- **Roster Validation**: Roster creation validates employee MCU status before assignment
- **Deployment Prevention**: Unfit or expired MCU personnel cannot be assigned to PTW work

### With Asset Module
- **Asset References**: Assets can be referenced in rosters and activities
- **Maintenance Tracking**: Asset maintenance status affects deployment availability

---

## 🚀 Usage Examples

### Creating a Roster with MCU Validation

```python
# This will succeed - employee is FIT
POST /api/v1/hr/rosters/
{
  "employee": 1,
  "asset_id": 5,
  "start_date": "2026-06-01",
  "end_date": "2026-06-15"
}

# This will fail - employee MCU is EXPIRED
POST /api/v1/hr/rosters/
{
  "employee": 2,
  "asset_id": 5,
  "start_date": "2026-06-01",
  "end_date": "2026-06-15"
}
# Response: "DEPLOYMENT DENIED: Personnel John Doe MCU has EXPIRED."
```

### Payroll Calculation

```python
GET /api/v1/hr/payroll/
# Returns payroll data for all employees based on:
# - Position base salary
# - Roster duration
# - Position allowances
# - Deductions (if any)
```

---

## 📝 Serializers

### EmployeeSerializer
Serializes Employee model data with all fields.

### AssetSerializer
Serializes Asset model data with all fields.

### RosterSerializer
Transforms roster data for API responses:
- Converts `employee` ID to `title` (employee full_name)
- Converts `start_date` to `start` field
- Converts `end_date` to `end` field
- Converts `asset` ID to `location` (asset name)
- Includes MCU validation on create

### VesselActivitySerializer
Transforms activity data:
- Includes `asset_name` for readability
- Converts date fields to `start` and `end`

### PositionSerializer
Serializes Position model data with all fields.

---

## 🔧 Configuration

### Environment Variables
No specific environment variables required for HR module. Uses Django settings from core_system.

### Database Requirements
- PostgreSQL 12+ recommended
- Proper foreign key constraints enabled
- Indexes on emp_id, asset_id for performance

---

## 📋 Management Commands

### Seed HR Data
```bash
python manage.py seed_hr_data
```
Populates initial HR data including:
- Sample employees
- Sample assets/vessels
- Sample positions
- Sample rosters

---

## 🧪 Testing

### Test Employee Creation
```bash
curl -X POST http://localhost:8989/api/v1/hr/employees/add/ \
  -H "Content-Type: application/json" \
  -d '{
    "emp_id": "EMP001",
    "full_name": "John Doe",
    "job_role": "Technician",
    "mcu_status": "FIT",
    "mcu_expiry": "2027-12-31"
  }'
```

### Test Roster Creation with Validation
```bash
curl -X POST http://localhost:8989/api/v1/hr/rosters/ \
  -H "Content-Type: application/json" \
  -d '{
    "employee": 1,
    "asset_id": 5,
    "start_date": "2026-06-01",
    "end_date": "2026-06-15"
  }'
```

---

## 📚 Related Documentation

- [Backend README](../README.md) - Main backend documentation
- [Asset Module README](../asset_module/README.md) - Asset and maintenance management
- [HSE PTW Module](../hse_ptw/) - Permit to Work system
- [HSE Safety Module](../hse_safety/) - Safety incidents and metrics
