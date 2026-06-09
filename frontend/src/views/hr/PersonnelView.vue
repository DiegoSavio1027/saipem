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
      <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg shadow-lg max-w-2xl w-full p-6 max-h-[90vh] overflow-y-auto">
        <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-1">{{ isEditMode ? 'Edit Crew Member' : 'Deploy New Crew' }}</h3>
        <p class="text-sm text-slate-600 dark:text-slate-400 mb-4">Offshore operations registration portal</p>

        <!-- Tabs -->
        <div v-if="isEditMode" class="flex gap-4 border-b border-slate-200 dark:border-slate-700 mb-4">
          <button @click="activeModalTab = 'profile'" :class="['py-2 px-1 font-medium transition-colors', activeModalTab === 'profile' ? 'text-red-600 border-b-2 border-red-600' : 'text-slate-500 hover:text-slate-700']">Profile</button>
          <button @click="activeModalTab = 'certifications'; fetchCertifications()" :class="['py-2 px-1 font-medium transition-colors', activeModalTab === 'certifications' ? 'text-red-600 border-b-2 border-red-600' : 'text-slate-500 hover:text-slate-700']">Certifications</button>
        </div>

        <form v-show="activeModalTab === 'profile' || !isEditMode" @submit.prevent="submitForm" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
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
          </div>

          <div class="flex gap-3 pt-4 border-t border-slate-200 dark:border-slate-700 mt-6">
            <button type="button" @click="closeModal" class="flex-1 px-4 py-2 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white hover:bg-slate-50 dark:hover:bg-slate-700 transition">
              Cancel
            </button>
            <button type="submit" class="flex-1 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-semibold transition">
              {{ isEditMode ? 'Update' : 'Deploy' }}
            </button>
          </div>
        </form>

        <!-- Certifications Tab Content -->
        <div v-show="activeModalTab === 'certifications' && isEditMode" class="space-y-4">
          <div class="bg-slate-50 dark:bg-slate-900 p-4 rounded-lg border border-slate-200 dark:border-slate-700">
            <h4 class="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-3">Add Certification</h4>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
              <div>
                <input v-model="newCert.cert_id" type="text" placeholder="Cert ID (e.g., C-123)" class="w-full px-3 py-2 text-sm border rounded bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100">
              </div>
              <div>
                <select v-model="newCert.cert_type" class="w-full px-3 py-2 text-sm border rounded bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100">
                  <option value="" disabled>Select Type</option>
                  <option value="HOT_WORK">HOT_WORK</option>
                  <option value="CONFINED_SPACE">CONFINED_SPACE</option>
                  <option value="WORKING_AT_HEIGHT">WORKING_AT_HEIGHT</option>
                  <option value="ELECTRICAL">ELECTRICAL</option>
                  <option value="LIFTING">LIFTING</option>
                </select>
              </div>
              <div class="flex gap-2">
                <input v-model="newCert.expiry_date" type="date" class="w-full px-3 py-2 text-sm border rounded bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100">
                <button @click="addCertification" :disabled="isSubmittingCert" class="bg-red-600 text-white px-3 py-2 rounded text-sm hover:bg-red-700 disabled:opacity-50">
                  Add
                </button>
              </div>
            </div>
          </div>

          <div v-if="certifications.length === 0" class="text-center py-6 text-slate-500">
            No certifications found for this employee.
          </div>
          <div v-else class="space-y-2 mt-4">
            <div v-for="cert in certifications" :key="cert.cert_id" class="flex items-center justify-between p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg">
              <div>
                <p class="font-semibold text-sm text-slate-900 dark:text-slate-100">{{ cert.cert_type }}</p>
                <p class="text-xs text-slate-500">ID: {{ cert.cert_id }} • Expires: {{ cert.expiry_date }}</p>
              </div>
              <button @click="deleteCertification(cert.cert_id)" class="text-red-500 hover:text-red-700 p-1">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>
              </button>
            </div>
          </div>

          <div class="flex justify-end pt-4 border-t border-slate-200 dark:border-slate-700 mt-4">
            <button type="button" @click="closeModal" class="px-6 py-2 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white hover:bg-slate-50 dark:hover:bg-slate-700 transition">
              Close
            </button>
          </div>
        </div>
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

const activeModalTab = ref('profile')
const certifications = ref([])
const isSubmittingCert = ref(false)
const newCert = ref({
  cert_id: '',
  cert_type: '',
  expiry_date: ''
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
  activeModalTab.value = 'profile'
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
  activeModalTab.value = 'profile'
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

// Certifications Management
const fetchCertifications = async () => {
  if (!formData.value.emp_id) return
  try {
    const response = await fetch(`${API_BASE_URL}/hr/certifications/${formData.value.emp_id}/`, {
      headers: { 'Authorization': `Bearer ${getAccessToken()}` }
    })
    if (response.ok) {
      certifications.value = await response.json()
    }
  } catch (error) {
    console.error('Error fetching certifications:', error)
  }
}

const addCertification = async () => {
  if (!newCert.value.cert_id || !newCert.value.cert_type || !newCert.value.expiry_date) {
    alert('Please fill all certification fields')
    return
  }
  isSubmittingCert.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/hr/certifications/add/${formData.value.emp_id}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getAccessToken()}`
      },
      body: JSON.stringify(newCert.value)
    })
    
    if (response.ok) {
      newCert.value = { cert_id: '', cert_type: '', expiry_date: '' }
      fetchCertifications()
    } else {
      const err = await response.json()
      alert('Failed to add certification: ' + JSON.stringify(err))
    }
  } catch (error) {
    console.error('Error adding certification:', error)
  } finally {
    isSubmittingCert.value = false
  }
}

const deleteCertification = async (certId) => {
  if (!confirm(`Delete certification ${certId}?`)) return
  try {
    const response = await fetch(`${API_BASE_URL}/hr/certifications/delete/${certId}/`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${getAccessToken()}` }
    })
    if (response.ok) {
      fetchCertifications()
    }
  } catch (error) {
    console.error('Error deleting certification:', error)
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
