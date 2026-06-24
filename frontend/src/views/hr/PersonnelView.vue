<template>
  <DashboardLayout>
    <!-- Toast Notifications -->
    <div class="fixed top-6 right-6 z-[200] flex flex-col gap-3 pointer-events-none">
      <transition-group name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="['pointer-events-auto bg-white dark:bg-slate-900 border rounded-xl p-4 shadow-2xl min-w-[300px] max-w-[380px] flex items-start gap-3 backdrop-blur-sm', toast.borderClass]"
        >
          <component :is="toast.icon" :class="['w-5 h-5 mt-0.5 shrink-0', toast.iconColor]" />
          <div class="flex-1 min-w-0">
            <p :class="['text-xs font-black uppercase tracking-wider', toast.titleColor]">{{ toast.title }}</p>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5 leading-relaxed">{{ toast.message }}</p>
          </div>
        </div>
      </transition-group>
    </div>

    <!-- Confirm Modal -->
    <div v-if="showConfirmModal" class="fixed inset-0 bg-black/90 backdrop-blur-md flex items-center justify-center p-4 z-[110]">
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-8 rounded-2xl w-full max-w-sm shadow-2xl text-center">
        <div class="bg-red-50 dark:bg-red-950/20 w-16 h-16 rounded-full border border-red-200 dark:border-red-500/30 flex items-center justify-center mx-auto mb-4">
          <AlertTriangle class="w-8 h-8 text-red-500 animate-pulse" />
        </div>
        <h3 class="text-xl font-black text-slate-900 dark:text-white mb-2 tracking-tight">Confirm Action</h3>
        <p class="text-xs text-slate-500 dark:text-slate-400 mb-6 leading-relaxed">{{ confirmMessage }}</p>
        <div class="flex gap-3">
          <button @click="confirmCallback = null; showConfirmModal = false" class="flex-1 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 p-3.5 rounded-xl font-bold transition text-slate-700 dark:text-white text-sm">Cancel</button>
          <button @click="executeConfirm" class="flex-1 bg-red-600 hover:bg-red-700 p-3.5 rounded-xl font-black tracking-wider uppercase transition text-white text-sm">Confirm</button>
        </div>
      </div>
    </div>

    <div class="p-8">
      <!-- Header -->
      <div class="flex justify-between items-start mb-8">
        <div>
          <h2 class="text-3xl font-black text-slate-900 dark:text-white tracking-tight">Workforce Directory</h2>
          <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">Live monitoring of offshore personnel & medical fitness status</p>
        </div>
        <button @click="openAddModal" class="bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white font-black px-5 py-2.5 rounded-xl transition flex items-center gap-2 text-sm uppercase tracking-wider shadow-sm">
          <UserPlus class="w-4 h-4" />
          Add Crew
        </button>
      </div>

      <!-- Statistics Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
        <Card class="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow overflow-hidden">
          <div class="h-1 bg-[var(--color-saipem-tertiary)] w-full" />
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2 pt-4">
            <CardTitle class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider font-mono">Crew Onboard</CardTitle>
            <div class="bg-orange-50 dark:bg-orange-950/20 p-2 rounded-lg border border-orange-200 dark:border-orange-900/30">
              <Users class="w-4 h-4 text-[var(--color-saipem-tertiary)]" />
            </div>
          </CardHeader>
          <CardContent>
            <div class="text-3xl font-black text-slate-900 dark:text-white">{{ stats.onboardCrew }}<span class="text-xl text-slate-400 dark:text-slate-600">/{{ stats.totalCrew }}</span></div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">Currently assigned to vessels</p>
          </CardContent>
        </Card>

        <Card class="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow overflow-hidden">
          <div class="h-1 bg-blue-500 w-full" />
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2 pt-4">
            <CardTitle class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider font-mono">Deployment Rate</CardTitle>
            <div class="bg-blue-50 dark:bg-blue-950/20 p-2 rounded-lg border border-blue-200 dark:border-blue-900/30">
              <Ship class="w-4 h-4 text-blue-500" />
            </div>
          </CardHeader>
          <CardContent>
            <div class="text-3xl font-black text-slate-900 dark:text-white">{{ stats.vesselRate }}<span class="text-xl text-slate-400 dark:text-slate-600">%</span></div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">Crew onboard ratio</p>
          </CardContent>
        </Card>

        <Card class="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow overflow-hidden" :class="stats.mcuAlerts > 0 ? 'border-red-200 dark:border-red-900' : ''">
          <div class="h-1 w-full" :class="stats.mcuAlerts > 0 ? 'bg-red-500' : 'bg-slate-200 dark:bg-slate-700'" />
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2 pt-4">
            <CardTitle class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider font-mono">MCU Alerts</CardTitle>
            <div class="p-2 rounded-lg border" :class="stats.mcuAlerts > 0 ? 'bg-red-50 dark:bg-red-950/20 border-red-200 dark:border-red-900/30' : 'bg-slate-50 dark:bg-slate-800 border-slate-200 dark:border-slate-700'">
              <Heart class="w-4 h-4" :class="stats.mcuAlerts > 0 ? 'text-red-500 animate-pulse' : 'text-slate-400 dark:text-slate-500'" />
            </div>
          </CardHeader>
          <CardContent>
            <div class="text-3xl font-black" :class="stats.mcuAlerts > 0 ? 'text-red-600 dark:text-red-400' : 'text-slate-900 dark:text-white'">{{ stats.mcuAlerts }}</div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">Expired or unfit certifications</p>
          </CardContent>
        </Card>

        <Card class="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow overflow-hidden">
          <div class="h-1 bg-green-500 w-full" />
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2 pt-4">
            <CardTitle class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider font-mono">Est. Payroll</CardTitle>
            <div class="bg-green-50 dark:bg-green-950/20 p-2 rounded-lg border border-green-200 dark:border-green-900/30">
              <Wallet class="w-4 h-4 text-green-500" />
            </div>
          </CardHeader>
          <CardContent>
            <div class="text-lg font-black text-slate-900 dark:text-white truncate">Rp {{ formatCurrency(stats.payroll) }}</div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">Current month estimate</p>
          </CardContent>
        </Card>
      </div>

      <!-- Personnel Table -->
      <Card class="border-slate-200 dark:border-slate-800 shadow-sm">
        <CardHeader>
          <CardTitle class="text-lg font-black text-slate-900 dark:text-white tracking-tight">Personnel Directory</CardTitle>
          <CardDescription class="text-xs text-slate-500 dark:text-slate-400">Manage offshore crew members and their medical fitness status</CardDescription>
        </CardHeader>
        <CardContent>
          <PersonnelDataTable :columns="personnelColumns" :data="employees" />
        </CardContent>
      </Card>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/90 backdrop-blur-md flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">

        <!-- Modal Header -->
        <div class="p-6 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="bg-orange-50 dark:bg-orange-950/20 p-2.5 rounded-xl border border-orange-200 dark:border-orange-900/30">
              <component :is="isEditMode ? Pencil : UserPlus" class="w-5 h-5 text-[var(--color-saipem-tertiary)]" />
            </div>
            <div>
              <h3 class="text-lg font-black text-slate-900 dark:text-white">{{ isEditMode ? 'Edit Crew Member' : 'Register New Crew' }}</h3>
              <p class="text-xs text-slate-500 dark:text-slate-400">Offshore operations personnel portal</p>
            </div>
          </div>
          <button @click="closeModal" class="text-slate-400 hover:text-slate-900 dark:hover:text-white transition p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800">
            <X class="w-5 h-5" />
          </button>
        </div>

        <!-- Tabs (edit mode only) -->
        <div v-if="isEditMode" class="flex border-b border-slate-200 dark:border-slate-800 px-6">
          <button
            @click="activeModalTab = 'profile'"
            :class="['py-3 px-4 text-xs font-black uppercase tracking-wider transition-colors border-b-2 -mb-px', activeModalTab === 'profile' ? 'text-[var(--color-saipem-tertiary)] border-[var(--color-saipem-tertiary)]' : 'text-slate-400 border-transparent hover:text-slate-700 dark:hover:text-slate-200']"
          >Profile</button>
          <button
            @click="activeModalTab = 'certifications'; fetchCertifications()"
            :class="['py-3 px-4 text-xs font-black uppercase tracking-wider transition-colors border-b-2 -mb-px', activeModalTab === 'certifications' ? 'text-[var(--color-saipem-tertiary)] border-[var(--color-saipem-tertiary)]' : 'text-slate-400 border-transparent hover:text-slate-700 dark:hover:text-slate-200']"
          >Certifications</button>
        </div>

        <!-- Profile Form -->
        <form v-show="activeModalTab === 'profile' || !isEditMode" @submit.prevent="submitForm" class="p-6 space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-1.5 block">Employee ID</label>
              <input
                v-model="formData.emp_id"
                type="text"
                placeholder="e.g., EMP001"
                :disabled="isEditMode"
                class="w-full px-4 py-3 border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-black text-slate-900 dark:text-white focus:outline-none focus:border-[var(--color-saipem-tertiary)] transition text-sm disabled:opacity-50 disabled:cursor-not-allowed"
                required
              >
            </div>
            <div>
              <label class="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-1.5 block">Full Name</label>
              <input
                v-model="formData.full_name"
                type="text"
                placeholder="e.g., John Doe"
                class="w-full px-4 py-3 border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-black text-slate-900 dark:text-white focus:outline-none focus:border-[var(--color-saipem-tertiary)] transition text-sm"
                required
              >
            </div>
            <div>
              <label class="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-1.5 block">Job Role</label>
              <select
                v-model="formData.job_role"
                class="w-full px-4 py-3 border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-black text-slate-900 dark:text-white focus:outline-none focus:border-[var(--color-saipem-tertiary)] transition text-sm"
                required
              >
                <option value="" disabled>Select Job Role</option>
                <option v-for="role in assignableRoles" :key="role" :value="role">{{ role }}</option>
              </select>
            </div>
            <div>
              <label class="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-1.5 block">Email</label>
              <input
                v-model="formData.email"
                type="email"
                placeholder="e.g., john.doe@company.com"
                class="w-full px-4 py-3 border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-black text-slate-900 dark:text-white focus:outline-none focus:border-[var(--color-saipem-tertiary)] transition text-sm"
              >
            </div>
            <div v-if="!isEditMode">
              <label class="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-1.5 block">
                Password <span class="normal-case font-normal text-slate-400">(optional)</span>
              </label>
              <input
                v-model="formData.password"
                type="password"
                placeholder="Leave empty for default"
                class="w-full px-4 py-3 border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-black text-slate-900 dark:text-white focus:outline-none focus:border-[var(--color-saipem-tertiary)] transition text-sm"
              >
              <p class="text-xs text-slate-400 dark:text-slate-500 mt-1.5">Default password: <span class="font-mono font-bold text-slate-600 dark:text-slate-300">saipem123</span></p>
            </div>
            <div>
              <label class="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-1.5 block">Roster Status</label>
              <select
                v-model="formData.roster_status"
                class="w-full px-4 py-3 border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-black text-slate-900 dark:text-white focus:outline-none focus:border-[var(--color-saipem-tertiary)] transition text-sm"
              >
                <option value="AVAILABLE">AVAILABLE</option>
                <option value="ONBOARD">ONBOARD</option>
              </select>
            </div>
            <div>
              <label class="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-1.5 block">MCU Expiry Date</label>
              <input
                v-model="formData.mcu_expiry"
                type="date"
                class="w-full px-4 py-3 border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-black text-slate-900 dark:text-white focus:outline-none focus:border-[var(--color-saipem-tertiary)] transition text-sm"
              >
            </div>
            <div>
              <label class="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-1.5 block">MCU Status</label>
              <select
                v-model="formData.mcu_status"
                class="w-full px-4 py-3 border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-black text-slate-900 dark:text-white focus:outline-none focus:border-[var(--color-saipem-tertiary)] transition text-sm"
              >
                <option value="PENDING">PENDING</option>
                <option value="FIT">FIT</option>
                <option value="UNFIT">UNFIT</option>
                <option value="EXPIRED">EXPIRED</option>
              </select>
            </div>
          </div>

          <div class="flex gap-3 pt-2">
            <button type="button" @click="closeModal" class="flex-1 px-4 py-3 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition font-bold text-sm">
              Cancel
            </button>
            <button type="submit" class="flex-1 px-4 py-3 bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white rounded-xl font-black uppercase tracking-wider transition text-sm">
              {{ isEditMode ? 'Update Crew' : 'Register Crew' }}
            </button>
          </div>
        </form>

        <!-- Certifications Tab -->
        <div v-show="activeModalTab === 'certifications' && isEditMode" class="p-6 space-y-4">
          <div class="bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
            <h4 class="text-xs font-black text-slate-600 dark:text-slate-400 uppercase tracking-wider mb-3">Add Certification</h4>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
              <input
                v-model="newCert.cert_id"
                type="text"
                placeholder="Cert ID (e.g., C-123)"
                class="w-full px-3 py-2.5 text-sm border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)] transition"
              >
              <select
                v-model="newCert.cert_type"
                class="w-full px-3 py-2.5 text-sm border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)] transition"
              >
                <option value="" disabled>Select Type</option>
                <option value="HOT_WORK">HOT_WORK</option>
                <option value="CONFINED_SPACE">CONFINED_SPACE</option>
                <option value="WORKING_AT_HEIGHT">WORKING_AT_HEIGHT</option>
                <option value="ELECTRICAL">ELECTRICAL</option>
                <option value="LIFTING">LIFTING</option>
              </select>
              <div class="flex gap-2">
                <input
                  v-model="newCert.expiry_date"
                  type="date"
                  class="flex-1 px-3 py-2.5 text-sm border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)] transition"
                >
                <button
                  @click="addCertification"
                  :disabled="isSubmittingCert"
                  class="bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white px-4 py-2 rounded-lg text-sm font-black disabled:opacity-50 transition whitespace-nowrap"
                >Add</button>
              </div>
            </div>
          </div>

          <div v-if="certifications.length === 0" class="text-center py-10 text-slate-400 dark:text-slate-600">
            <Shield class="w-10 h-10 mx-auto mb-2 opacity-30" />
            <p class="text-xs font-mono uppercase tracking-wider">No certifications found</p>
          </div>
          <div v-else class="space-y-2">
            <div
              v-for="cert in certifications"
              :key="cert.cert_id"
              class="flex items-center justify-between p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl"
            >
              <div>
                <p class="font-bold text-sm text-slate-900 dark:text-slate-100">{{ cert.cert_type }}</p>
                <p class="text-xs text-slate-500 font-mono mt-0.5">ID: {{ cert.cert_id }} • Expires: {{ cert.expiry_date }}</p>
              </div>
              <button
                @click="deleteCertification(cert.cert_id)"
                class="text-slate-400 hover:text-red-500 transition p-1.5 rounded-lg hover:bg-red-50 dark:hover:bg-red-950/20"
              >
                <Trash2 class="w-4 h-4" />
              </button>
            </div>
          </div>

          <div class="flex justify-end pt-2">
            <button type="button" @click="closeModal" class="px-6 py-2.5 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition font-bold text-sm">
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
import { getAccessToken, authState } from '@/store/auth'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { UserPlus, Users, Ship, Heart, Wallet, Pencil, X, AlertTriangle, CheckCircle, XCircle, Shield, Trash2 } from '@lucide/vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import PersonnelDataTable from './personnel-data-table.vue'
import { personnelColumns } from './personnel-columns'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1'

// State
const employees = ref([])
const loading = ref(false)
const showModal = ref(false)
const isEditMode = ref(false)

// Toast & Confirm
const toasts = ref([])
const showConfirmModal = ref(false)
const confirmMessage = ref('')
const confirmCallback = ref(null)

const assignableRoles = computed(() => {
  if (authState.userRole === 'Admin') {
    return ['Admin', 'HR Staff', 'Chief Engineer', 'Safety Officer', 'Worker']
  } else if (authState.userRole === 'HR Staff') {
    return ['Chief Engineer', 'Safety Officer', 'Worker']
  }
  return ['Worker']
})

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
const newCert = ref({ cert_id: '', cert_type: '', expiry_date: '' })

// Toast system
const showToast = (type, title, message) => {
  const id = Date.now()
  let borderClass = '', iconColor = '', titleColor = '', icon = null

  if (type === 'error') {
    borderClass = 'border-red-200 dark:border-red-900/60'
    iconColor = 'text-red-500'
    titleColor = 'text-red-600 dark:text-red-400'
    icon = XCircle
  } else if (type === 'warning') {
    borderClass = 'border-amber-200 dark:border-amber-900/60'
    iconColor = 'text-amber-500'
    titleColor = 'text-amber-600 dark:text-amber-400'
    icon = AlertTriangle
  } else {
    borderClass = 'border-emerald-200 dark:border-emerald-900/60'
    iconColor = 'text-emerald-500'
    titleColor = 'text-emerald-600 dark:text-emerald-400'
    icon = CheckCircle
  }

  toasts.value.push({ id, borderClass, iconColor, titleColor, icon, title, message })
  setTimeout(() => { toasts.value = toasts.value.filter(t => t.id !== id) }, 4000)
}

// Confirm system
const showConfirm = (message, callback) => {
  confirmMessage.value = message
  confirmCallback.value = callback
  showConfirmModal.value = true
}

const executeConfirm = () => {
  if (confirmCallback.value) confirmCallback.value()
  showConfirmModal.value = false
  confirmCallback.value = null
}

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
  formData.value = { emp_id: '', full_name: '', job_role: '', email: '', roster_status: 'ONBOARD', mcu_expiry: '', mcu_status: 'PENDING', password: '' }
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
    if (!isEditMode.value && !payload.password) delete payload.password
    if (isEditMode.value) delete payload.password

    const response = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${getAccessToken()}` },
      body: JSON.stringify(payload)
    })

    if (response.ok) {
      closeModal()
      fetchEmployees()
      showToast('success', isEditMode.value ? 'CREW UPDATED' : 'CREW REGISTERED', isEditMode.value ? 'Personnel record has been updated successfully.' : 'New crew member has been registered.')
    } else {
      const error = await response.json()
      const msg = Object.values(error).flat().join(' ') || 'Failed to save personnel record.'
      showToast('error', 'SAVE FAILED', msg)
    }
  } catch (error) {
    showToast('error', 'NETWORK ERROR', 'Connection failed. Please try again.')
  }
}

const deleteEmployee = async (empId) => {
  showConfirm(`Delete employee ${empId}? This action cannot be undone.`, async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/hr/employees/delete/${empId}/`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${getAccessToken()}` }
      })
      if (response.ok) {
        fetchEmployees()
        showToast('success', 'CREW REMOVED', `Personnel ${empId} has been removed from the system.`)
      } else {
        showToast('error', 'DELETE FAILED', 'Server refused to delete this personnel record.')
      }
    } catch (error) {
      showToast('error', 'NETWORK ERROR', 'Connection failed. Please try again.')
    }
  })
}

const fetchCertifications = async () => {
  if (!formData.value.emp_id) return
  try {
    const response = await fetch(`${API_BASE_URL}/hr/certifications/${formData.value.emp_id}/`, {
      headers: { 'Authorization': `Bearer ${getAccessToken()}` }
    })
    if (response.ok) certifications.value = await response.json()
  } catch (error) {
    console.error('Error fetching certifications:', error)
  }
}

const addCertification = async () => {
  if (!newCert.value.cert_id || !newCert.value.cert_type || !newCert.value.expiry_date) {
    showToast('warning', 'MISSING FIELDS', 'Please fill in all certification fields before adding.')
    return
  }
  isSubmittingCert.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/hr/certifications/add/${formData.value.emp_id}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${getAccessToken()}` },
      body: JSON.stringify(newCert.value)
    })
    if (response.ok) {
      newCert.value = { cert_id: '', cert_type: '', expiry_date: '' }
      fetchCertifications()
      showToast('success', 'CERT ADDED', 'Certification has been recorded successfully.')
    } else {
      showToast('error', 'CERT ERROR', 'Failed to add certification. Please try again.')
    }
  } catch (error) {
    showToast('error', 'NETWORK ERROR', 'Connection failed. Please try again.')
  } finally {
    isSubmittingCert.value = false
  }
}

const deleteCertification = async (certId) => {
  showConfirm(`Delete certification ${certId}?`, async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/hr/certifications/delete/${certId}/`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${getAccessToken()}` }
      })
      if (response.ok) {
        fetchCertifications()
        showToast('success', 'CERT REMOVED', 'Certification has been deleted.')
      }
    } catch (error) {
      showToast('error', 'NETWORK ERROR', 'Connection failed. Please try again.')
    }
  })
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('id-ID').format(value)
}

onMounted(() => {
  fetchEmployees()

  window.addEventListener('edit-personnel', (event) => {
    editEmployee(event.detail)
  })

  window.addEventListener('delete-personnel', (event) => {
    deleteEmployee(event.detail)
  })
})
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}
.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>
