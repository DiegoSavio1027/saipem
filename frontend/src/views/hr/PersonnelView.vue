<template>
  <DashboardLayout>
    <div class="p-8">
      <!-- Header -->
      <div class="flex justify-between items-start mb-8">
        <div>
          <h2 class="text-3xl font-bold text-slate-900 dark:text-white">Workforce Dashboard</h2>
          <p class="text-sm text-slate-600 dark:text-slate-400 mt-1">Live monitoring of offshore personnel & medical fitness logs</p>
        </div>
        <button @click="openAddModal" class="bg-red-600 hover:bg-red-700 text-white font-bold px-4 py-2 rounded-lg transition flex items-center gap-2">
          <UserPlus class="w-4 h-4" />
          Deploy New Crew
        </button>
      </div>

      <!-- Statistics Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 p-6 rounded-lg shadow-sm">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-slate-600 dark:text-slate-400 font-semibold">Crew Onboard</p>
              <p class="text-2xl font-bold text-slate-900 dark:text-white mt-1">{{ stats.onboardCrew }}/{{ stats.totalCrew }}</p>
            </div>
            <Users class="text-red-500 w-8 h-8 opacity-20" />
          </div>
        </div>

        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 p-6 rounded-lg shadow-sm">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-slate-600 dark:text-slate-400 font-semibold">Vessel Rate</p>
              <p class="text-2xl font-bold text-slate-900 dark:text-white mt-1">{{ stats.vesselRate }}%</p>
            </div>
            <Ship class="text-red-500 w-8 h-8 opacity-20" />
          </div>
        </div>

        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 p-6 rounded-lg shadow-sm">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-slate-600 dark:text-slate-400 font-semibold">Medical Warnings</p>
              <p class="text-2xl font-bold text-slate-900 dark:text-white mt-1">{{ stats.mcuAlerts }}</p>
            </div>
            <Heart class="text-red-500 w-8 h-8 opacity-20" />
          </div>
        </div>

        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 p-6 rounded-lg shadow-sm">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-slate-600 dark:text-slate-400 font-semibold">Est. Payroll</p>
              <p class="text-2xl font-bold text-slate-900 dark:text-white mt-1">Rp {{ formatCurrency(stats.payroll) }}</p>
            </div>
            <Wallet class="text-red-500 w-8 h-8 opacity-20" />
          </div>
        </div>
      </div>

      <!-- Personnel Table -->
      <Card>
        <CardHeader>
          <CardTitle>Personnel Directory</CardTitle>
          <CardDescription>Manage offshore crew members and their medical fitness status</CardDescription>
        </CardHeader>
        <CardContent>
          <PersonnelDataTable :columns="personnelColumns" :data="employees" />
        </CardContent>
      </Card>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg shadow-lg max-w-md w-full p-6">
        <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-1">{{ isEditMode ? 'Edit Crew Member' : 'Deploy New Crew' }}</h3>
        <p class="text-sm text-slate-600 dark:text-slate-400 mb-6">Offshore operations registration portal</p>

        <form @submit.prevent="submitForm" class="space-y-4">
          <div>
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1 block">Employee ID</label>
            <input
              v-model="formData.emp_id"
              type="text"
              placeholder="e.g., EMP001"
              :disabled="isEditMode"
              class="w-full px-4 py-2 border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-red-500 disabled:opacity-50 disabled:bg-slate-100 dark:disabled:bg-slate-900"
              required
            >
          </div>

          <div>
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1 block">Full Name</label>
            <input
              v-model="formData.full_name"
              type="text"
              placeholder="e.g., John Doe"
              class="w-full px-4 py-2 border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-red-500"
              required
            >
          </div>

          <div>
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1 block">Job Role</label>
            <input
              v-model="formData.job_role"
              type="text"
              placeholder="e.g., Safety Officer"
              class="w-full px-4 py-2 border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-red-500"
              required
            >
          </div>

          <div>
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1 block">Email</label>
            <input
              v-model="formData.email"
              type="email"
              placeholder="e.g., john.doe@company.com"
              class="w-full px-4 py-2 border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-red-500"
            >
          </div>

          <div v-if="!isEditMode">
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1 block">Password (Optional)</label>
            <input
              v-model="formData.password"
              type="password"
              placeholder="Leave empty for auto-generated password"
              class="w-full px-4 py-2 border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-red-500"
            >
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">If empty, a default password will be generated</p>
          </div>

          <div>
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1 block">Roster Status</label>
            <select
              v-model="formData.roster_status"
              class="w-full px-4 py-2 border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-red-500"
            >
              <option value="AVAILABLE">AVAILABLE</option>
              <option value="ONBOARD">ONBOARD</option>
            </select>
          </div>

          <div>
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1 block">MCU Expiry Date</label>
            <input
              v-model="formData.mcu_expiry"
              type="date"
              class="w-full px-4 py-2 border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-red-500"
            >
          </div>

          <div>
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1 block">MCU Status</label>
            <select
              v-model="formData.mcu_status"
              class="w-full px-4 py-2 border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-red-500"
            >
              <option value="PENDING">PENDING</option>
              <option value="FIT">FIT</option>
              <option value="UNFIT">UNFIT</option>
              <option value="EXPIRED">EXPIRED</option>
            </select>
          </div>

          <div class="flex gap-3 pt-4">
            <button type="button" @click="closeModal" class="flex-1 px-4 py-2 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white hover:bg-slate-50 dark:hover:bg-slate-700 transition">
              Cancel
            </button>
            <button type="submit" class="flex-1 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-semibold transition">
              {{ isEditMode ? 'Update' : 'Deploy' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getAccessToken, authState } from '@/store/auth'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { UserPlus, Users, Ship, Heart, Wallet } from '@lucide/vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import PersonnelDataTable from './personnel-data-table.vue'
import { personnelColumns } from './personnel-columns'

const router = useRouter()
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1'

// State
const employees = ref([])
const loading = ref(false)
const showModal = ref(false)
const isEditMode = ref(false)
const currentUser = ref('User')

const stats = ref({
  onboardCrew: 0,
  totalCrew: 0,
  vesselRate: 0,
  mcuAlerts: 0,
  payroll: 0
})

const formData = ref({
  emp_id: '',
  full_name: '',
  job_role: '',
  email: '',
  roster_status: 'ONBOARD',
  mcu_expiry: '',
  mcu_status: 'PENDING',
  password: ''
})

// Methods
const fetchEmployees = async () => {
  loading.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/hse/employees/`, {
      headers: { 'Authorization': `Bearer ${getAccessToken()}` }
    })
    if (response.ok) {
      employees.value = await response.json()
      updateStats()
    } else {
      console.error('Failed to fetch employees:', response.status)
    }
  } catch (error) {
    console.error('Error fetching employees:', error)
  } finally {
    loading.value = false
  }
}

const updateStats = () => {
  stats.value.totalCrew = employees.value.length
  stats.value.onboardCrew = employees.value.filter(e => e.roster_status === 'ONBOARD').length
  stats.value.vesselRate = stats.value.totalCrew > 0 ? Math.round((stats.value.onboardCrew / stats.value.totalCrew) * 100) : 0
  stats.value.mcuAlerts = employees.value.filter(e => e.mcu_status === 'EXPIRED' || e.mcu_status === 'UNFIT').length
}

const openAddModal = () => {
  isEditMode.value = false
  formData.value = {
    emp_id: '',
    full_name: '',
    job_role: '',
    email: '',
    roster_status: 'ONBOARD',
    mcu_expiry: '',
    mcu_status: 'PENDING',
    password: ''
  }
  showModal.value = true
}

const editEmployee = (emp) => {
  isEditMode.value = true
  formData.value = { ...emp }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const submitForm = async () => {
  try {
    const method = isEditMode.value ? 'PUT' : 'POST'
    const url = isEditMode.value
      ? `${API_BASE_URL}/hr/employees/update/${formData.value.emp_id}/`
      : `${API_BASE_URL}/hr/employees/add/`

    const payload = { ...formData.value }
    // Remove password if empty on create
    if (!isEditMode.value && !payload.password) {
      delete payload.password
    }
    // Never send password on update
    if (isEditMode.value) {
      delete payload.password
    }

    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getAccessToken()}`
      },
      body: JSON.stringify(payload)
    })

    if (response.ok) {
      closeModal()
      fetchEmployees()
      alert(isEditMode.value ? 'Employee updated successfully!' : 'Employee added successfully!')
    } else {
      const error = await response.json()
      alert('Failed to save employee: ' + JSON.stringify(error))
    }
  } catch (error) {
    console.error('Error submitting form:', error)
    alert('Network error occurred. Please try again.')
  }
}

const deleteEmployee = async (empId) => {
  if (!confirm(`Are you sure you want to delete employee ${empId}?`)) return

  try {
    const response = await fetch(`${API_BASE_URL}/hr/employees/delete/${empId}/`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${getAccessToken()}` }
    })

    if (response.ok) {
      fetchEmployees()
      alert('Employee deleted successfully!')
    } else {
      alert('Failed to delete employee')
    }
  } catch (error) {
    console.error('Error deleting employee:', error)
    alert('Network error occurred. Please try again.')
  }
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('id-ID').format(value)
}

// Lifecycle
onMounted(() => {
  currentUser.value = authState.username || 'User'
  fetchEmployees()

  // Listen for edit-personnel event from data-table
  window.addEventListener('edit-personnel', (event) => {
    editEmployee(event.detail)
  })

  // Listen for delete-personnel event from data-table
  window.addEventListener('delete-personnel', (event) => {
    deleteEmployee(event.detail)
  })
})
</script>
