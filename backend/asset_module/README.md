bisa# Asset Module - Maintenance & Inventory Management

## 📋 Module Overview

The Asset Module manages maintenance scheduling and inventory tracking for offshore vessel operations. It ensures equipment reliability through preventive maintenance tracking and maintains accurate inventory records for spare parts and consumables. The module integrates with the HSE system to prevent PTW approvals when critical maintenance is overdue.

### Key Features
- **Maintenance Task Management**: Schedule and track preventive and corrective maintenance
- **Inventory Management**: Track spare parts, consumables, and equipment stock levels
- **Maintenance Status Tracking**: Monitor overdue, pending, and completed maintenance tasks
- **Inventory Alerts**: Low stock warnings and reorder notifications
- **Integration with PTW**: Maintenance status affects work permit approvals
- **Audit Trail**: Complete history of maintenance activities and inventory movements

---

## 🏗️ Module Structure

```
asset_module/
├── models.py              # Database models for maintenance and inventory
├── views.py               # API endpoints for asset operations
├── serializers.py         # Data serialization for API responses
├── urls.py                # URL routing for asset endpoints
├── admin.py               # Django admin configuration
├── migrations/            # Database migrations
└── README.md             # This file
```

---

## 📊 Database Models

### 1. **MaintenanceTask**
Represents scheduled maintenance activities for equipment and vessels.

**Fields**:
- `task_id` (CharField, unique): Maintenance task identifier (e.g., "MAINT-001")
- `equipment_name` (CharField): Name of equipment requiring maintenance
- `task_description` (TextField): Detailed description of maintenance work
- `scheduled_date` (DateField): Planned maintenance date
- `completed_date` (DateField, nullable): Actual completion date
- `status` (CharField): Task status
  - `PENDING`: Scheduled but not started
  - `IN_PROGRESS`: Currently being worked on
  - `COMPLETED`: Finished successfully
  - `OVERDUE`: Past scheduled date and not completed
- `assigned_to` (CharField): Personnel assigned to perform maintenance
- `priority` (CharField): Task priority level
  - `LOW`: Routine maintenance
  - `MEDIUM`: Important but not urgent
  - `HIGH`: Critical maintenance
  - `CRITICAL`: Safety-critical, blocks operations
- `notes` (TextField, nullable): Additional notes and observations
- `created_at` (DateTimeField): Record creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

**Business Rules**:
- Tasks automatically marked OVERDUE if scheduled_date < today and status != COMPLETED
- CRITICAL priority tasks block PTW approvals until completed
- Completion requires both completed_date and status = COMPLETED

**Integration**: Critical maintenance tasks affect PTW approval workflow in HSE system.

---

### 2. **InventoryItem**
Represents spare parts, consumables, and equipment in stock.

**Fields**:
- `item_code` (CharField, unique): Inventory item identifier (e.g., "SPARE-001")
- `item_name` (CharField): Item name/description
- `category` (CharField): Item category
  - `SPARE_PARTS`: Replacement parts for equipment
  - `CONSUMABLES`: Consumable materials (oil, filters, etc.)
  - `TOOLS`: Tools and equipment
  - `SAFETY_EQUIPMENT`: PPE and safety gear
  - `CHEMICALS`: Chemicals and hazardous materials
- `quantity` (IntegerField): Current stock quantity
- `unit` (CharField): Unit of measurement (pcs, liters, kg, etc.)
- `minimum_stock` (IntegerField): Reorder threshold
- `location` (CharField): Storage location (e.g., "Warehouse A", "Deck Storage")
- `supplier` (CharField, nullable): Supplier name
- `unit_price` (DecimalField): Price per unit
- `last_restock_date` (DateField, nullable): Last restocking date
- `notes` (TextField, nullable): Additional notes
- `created_at` (DateTimeField): Record creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

**Business Rules**:
- Low stock alert when quantity <= minimum_stock
- Negative quantities not allowed
- Safety equipment items require special handling

**Integration**: Inventory validation ensures required materials are available before PTW approval.

---

## 🔌 API Endpoints

All endpoints use the `/api/v1/asset/` prefix and require authentication.

### Maintenance Management

**List All Maintenance Tasks**
```
GET /api/v1/asset/maintenance/
Response: [{
  task_id: "MAINT-001",
  equipment_name: "Main Engine",
  task_description: "Oil change and filter replacement",
  scheduled_date: "2026-06-01",
  completed_date: null,
  status: "PENDING",
  assigned_to: "John Doe",
  priority: "HIGH",
  notes: "",
  created_at: "2026-05-20T10:00:00Z",
  updated_at: "2026-05-20T10:00:00Z"
}]

Query Parameters:
- status: Filter by status (PENDING, IN_PROGRESS, COMPLETED, OVERDUE)
- priority: Filter by priority (LOW, MEDIUM, HIGH, CRITICAL)
- equipment_name: Filter by equipment name
```

**Get Maintenance Task Details**
```
GET /api/v1/asset/maintenance/<task_id>/
Response: {
  task_id: "MAINT-001",
  equipment_name: "Main Engine",
  task_description: "Oil change and filter replacement",
  scheduled_date: "2026-06-01",
  completed_date: null,
  status: "PENDING",
  assigned_to: "John Doe",
  priority: "HIGH",
  notes: "",
  created_at: "2026-05-20T10:00:00Z",
  updated_at: "2026-05-20T10:00:00Z"
}
```

**Create Maintenance Task**
```
POST /api/v1/asset/maintenance/
Body: {
  task_id: "MAINT-002",
  equipment_name: "Crane Unit 1",
  task_description: "Annual inspection and certification",
  scheduled_date: "2026-06-15",
  assigned_to: "Jane Smith",
  priority: "CRITICAL",
  notes: "Required for crane operation permit"
}
Response: { task_id, equipment_name, ... }
```

**Update Maintenance Task**
```
PUT /api/v1/asset/maintenance/<task_id>/
Body: {
  status: "COMPLETED",
  completed_date: "2026-06-01",
  notes: "Completed successfully. All systems operational."
}
Response: { task_id, status, completed_date, ... }
```

**Delete Maintenance Task**
```
DELETE /api/v1/asset/maintenance/<task_id>/
Response: { status: "deleted" }
```

---

### Inventory Management

**List All Inventory Items**
```
GET /api/v1/asset/inventory/
Response: [{
  item_code: "SPARE-001",
  item_name: "Engine Oil Filter",
  category: "SPARE_PARTS",
  quantity: 15,
  unit: "pcs",
  minimum_stock: 10,
  location: "Warehouse A",
  supplier: "Marine Parts Co.",
  unit_price: "25.50",
  last_restock_date: "2026-05-15",
  notes: "",
  created_at: "2026-01-10T08:00:00Z",
  updated_at: "2026-05-15T14:30:00Z"
}]

Query Parameters:
- category: Filter by category
- location: Filter by storage location
- low_stock: true/false (items at or below minimum_stock)
```

**Get Inventory Item Details**
```
GET /api/v1/asset/inventory/<item_code>/
Response: {
  item_code: "SPARE-001",
  item_name: "Engine Oil Filter",
  category: "SPARE_PARTS",
  quantity: 15,
  unit: "pcs",
  minimum_stock: 10,
  location: "Warehouse A",
  supplier: "Marine Parts Co.",
  unit_price: "25.50",
  last_restock_date: "2026-05-15",
  notes: "",
  created_at: "2026-01-10T08:00:00Z",
  updated_at: "2026-05-15T14:30:00Z"
}
```

**Create Inventory Item**
```
POST /api/v1/asset/inventory/
Body: {
  item_code: "SPARE-002",
  item_name: "Hydraulic Fluid",
  category: "CONSUMABLES",
  quantity: 50,
  unit: "liters",
  minimum_stock: 20,
  location: "Deck Storage",
  supplier: "Marine Supplies Ltd.",
  unit_price: "15.00",
  notes: "Store in cool, dry place"
}
Response: { item_code, item_name, ... }
```

**Update Inventory Item**
```
PUT /api/v1/asset/inventory/<item_code>/
Body: {
  quantity: 60,
  last_restock_date: "2026-05-28",
  notes: "Restocked 10 liters"
}
Response: { item_code, quantity, last_restock_date, ... }
```

**Delete Inventory Item**
```
DELETE /api/v1/asset/inventory/<item_code>/
Response: { status: "deleted" }
```

---

## 🔐 Access Control

### Role-Based Permissions

**Admin**:
- Full access to all maintenance and inventory operations
- Can create, update, delete maintenance tasks and inventory items
- Can mark tasks as completed
- Can adjust inventory quantities

**Safety Officer**:
- View all maintenance tasks and inventory
- Can update maintenance task status
- Can add notes to maintenance tasks
- Cannot delete tasks or inventory items

**Worker**:
- View maintenance tasks assigned to them
- View inventory items
- Cannot modify maintenance or inventory data

---

## 🔗 Integration Points

### With HSE PTW Module
- **Maintenance Blocking**: CRITICAL priority maintenance tasks block PTW approvals
- **Equipment Validation**: PTW approval checks if equipment has overdue maintenance
- **Inventory Validation**: PTW approval verifies required materials are in stock

### With HR Module
- **Asset References**: Maintenance tasks can reference assets from HR module
- **Personnel Assignment**: Maintenance tasks assigned to employees from HR database

---

## 🚀 Usage Examples

### Creating a Critical Maintenance Task

```python
POST /api/v1/asset/maintenance/
{
  "task_id": "MAINT-CRIT-001",
  "equipment_name": "Fire Suppression System",
  "task_description": "Annual inspection and pressure test",
  "scheduled_date": "2026-06-01",
  "assigned_to": "Safety Team",
  "priority": "CRITICAL",
  "notes": "Required by maritime safety regulations"
}

# This task will block PTW approvals until completed
```

### Completing a Maintenance Task

```python
PUT /api/v1/asset/maintenance/MAINT-CRIT-001/
{
  "status": "COMPLETED",
  "completed_date": "2026-06-01",
  "notes": "Inspection passed. System operational. Certificate valid until 2027-06-01."
}

# PTW approvals now unblocked for this equipment
```

### Checking Low Stock Items

```python
GET /api/v1/asset/inventory/?low_stock=true

# Returns all items where quantity <= minimum_stock
# Example response:
[
  {
    "item_code": "SPARE-003",
    "item_name": "Safety Harness",
    "quantity": 5,
    "minimum_stock": 10,
    "location": "Safety Equipment Room"
  }
]
```

### Restocking Inventory

```python
PUT /api/v1/asset/inventory/SPARE-003/
{
  "quantity": 20,
  "last_restock_date": "2026-05-28",
  "notes": "Restocked 15 units. New supplier: SafetyGear Pro"
}
```

---

## 📝 Serializers

### MaintenanceTaskSerializer
Serializes MaintenanceTask model data:
- All fields included
- Auto-calculates overdue status based on scheduled_date
- Validates priority levels
- Ensures completed_date is set when status = COMPLETED

### InventoryItemSerializer
Serializes InventoryItem model data:
- All fields included
- Validates quantity >= 0
- Calculates low_stock flag (quantity <= minimum_stock)
- Validates category choices

---

## 🔧 Configuration

### Environment Variables
No specific environment variables required for Asset module. Uses Django settings from core_system.

### Database Requirements
- PostgreSQL 12+ recommended
- Proper unique constraints on task_id and item_code
- Indexes on status, priority, category for performance

---

## 📋 Management Commands

### Seed Asset Data
```bash
python manage.py seed_asset_data
```
Populates initial asset data including:
- Sample maintenance tasks
- Sample inventory items
- Sample equipment records

### Check Overdue Maintenance
```bash
python manage.py check_overdue_maintenance
```
Scans all maintenance tasks and updates status to OVERDUE if:
- scheduled_date < today
- status != COMPLETED

---

## 🧪 Testing

### Test Maintenance Task Creation
```bash
curl -X POST http://localhost:8989/api/v1/asset/maintenance/ \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "MAINT-TEST-001",
    "equipment_name": "Test Equipment",
    "task_description": "Test maintenance task",
    "scheduled_date": "2026-06-15",
    "assigned_to": "Test User",
    "priority": "MEDIUM"
  }'
```

### Test Inventory Item Creation
```bash
curl -X POST http://localhost:8989/api/v1/asset/inventory/ \
  -H "Content-Type: application/json" \
  -d '{
    "item_code": "TEST-001",
    "item_name": "Test Item",
    "category": "SPARE_PARTS",
    "quantity": 100,
    "unit": "pcs",
    "minimum_stock": 20,
    "location": "Test Warehouse",
    "unit_price": "10.00"
  }'
```

### Test Low Stock Query
```bash
curl -X GET "http://localhost:8989/api/v1/asset/inventory/?low_stock=true"
```

### Test Overdue Maintenance Query
```bash
curl -X GET "http://localhost:8989/api/v1/asset/maintenance/?status=OVERDUE"
```

---

## 📊 Business Logic

### Maintenance Status Workflow

```
PENDING → IN_PROGRESS → COMPLETED
   ↓
OVERDUE (if scheduled_date < today and not COMPLETED)
```

**Status Transitions**:
1. Task created with status = PENDING
2. Worker starts work → status = IN_PROGRESS
3. Worker completes work → status = COMPLETED (requires completed_date)
4. System auto-updates to OVERDUE if past scheduled_date

### Inventory Stock Management

**Low Stock Alert Logic**:
```python
if item.quantity <= item.minimum_stock:
    trigger_low_stock_alert(item)
```

**Stock Movement Tracking**:
- Every quantity update should include notes explaining the change
- last_restock_date updated when quantity increases
- Audit trail maintained through updated_at timestamp

---

## 🔔 Alerts and Notifications

### Maintenance Alerts
- **Overdue Tasks**: Daily check for tasks past scheduled_date
- **Critical Tasks**: Immediate notification when CRITICAL task created
- **Completion Reminders**: Notification 3 days before scheduled_date

### Inventory Alerts
- **Low Stock**: Alert when quantity <= minimum_stock
- **Out of Stock**: Critical alert when quantity = 0
- **Restock Confirmation**: Notification when item restocked

---

## 📈 Reporting

### Maintenance Reports
- **Overdue Maintenance Report**: List of all overdue tasks
- **Completion Rate**: Percentage of tasks completed on time
- **Equipment Downtime**: Time equipment unavailable due to maintenance

### Inventory Reports
- **Stock Level Report**: Current quantities of all items
- **Low Stock Report**: Items requiring reorder
- **Consumption Report**: Usage patterns over time
- **Valuation Report**: Total inventory value (quantity × unit_price)

---

## 🔍 Common Queries

### Find All Critical Overdue Maintenance
```python
GET /api/v1/asset/maintenance/?status=OVERDUE&priority=CRITICAL
```

### Find All Low Stock Safety Equipment
```python
GET /api/v1/asset/inventory/?category=SAFETY_EQUIPMENT&low_stock=true
```

### Find Maintenance Tasks for Specific Equipment
```python
GET /api/v1/asset/maintenance/?equipment_name=Main%20Engine
```

### Find Inventory Items by Location
```python
GET /api/v1/asset/inventory/?location=Warehouse%20A
```

---

## 📚 Related Documentation

- [Backend README](../README.md) - Main backend documentation
- [HR Module README](../hr_module/README.md) - Human resources management
- [HSE PTW Module](../hse_ptw/) - Permit to Work system
- [HSE Safety Module](../hse_safety/) - Safety incidents and metrics

---

## 🛠️ Troubleshooting

### Issue: Maintenance task not blocking PTW approval
**Solution**: Verify task priority is set to CRITICAL and status is not COMPLETED

### Issue: Inventory quantity showing negative
**Solution**: Check serializer validation - negative quantities should be rejected

### Issue: Overdue status not updating automatically
**Solution**: Run `python manage.py check_overdue_maintenance` command or set up cron job

### Issue: Low stock alerts not triggering
**Solution**: Verify minimum_stock threshold is set correctly for each item

---

## 📝 Version History

- **v2.0.0** (2026-05-28): Initial integration with HSE system
  - Maintenance task management
  - Inventory tracking
  - Integration with PTW workflow
  - Role-based access control
