<template>
  <DashboardLayout>
    <div class="p-8 space-y-8">
      <!-- Header -->
      <div class="flex justify-between items-center">
        <div>
          <h2 class="text-3xl font-heading font-black text-slate-900 dark:text-white tracking-tight uppercase">Predictive Maintenance & Telemetry</h2>
          <p class="text-sm text-slate-500 dark:text-slate-400 mt-1 font-mono">Real-time Machinery Condition Monitoring</p>
        </div>
        <div class="flex gap-2">
          <Button @click="fetchMachinery" variant="outline" class="flex items-center gap-2">
            <RefreshCw :class="['w-4 h-4', isLoading ? 'animate-spin' : '']" /> Refresh Telemetry
          </Button>
          <Button v-if="authState.userRole === 'Admin' || authState.userRole === 'Chief Engineer'" @click="openAddModal" class="bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white font-bold flex items-center gap-2">
            <Plus class="w-4 h-4" /> Add Machinery
          </Button>
        </div>
      </div>

      <!-- Stats Grid (Shadcn Cards) -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-xs font-bold text-slate-400 uppercase tracking-widest font-mono">Monitored Machinery</CardTitle>
            <Cpu class="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold text-slate-900 dark:text-white">{{ machinery.length }} Units</div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">IoT signal active</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-xs font-bold text-slate-400 uppercase tracking-widest font-mono">Healthy Machinery</CardTitle>
            <CheckCircle class="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold text-slate-900 dark:text-white">{{ healthyCount }} Units</div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">Operational & stable</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-xs font-bold text-slate-400 uppercase tracking-widest font-mono">Critical Machinery</CardTitle>
            <AlertTriangle class="h-4 w-4 text-red-500" :class="[needsMaintCount > 0 ? 'animate-pulse' : '']" />
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold text-slate-900 dark:text-white">{{ needsMaintCount }} Alerts</div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">Require immediate maintenance</p>
          </CardContent>
        </Card>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="p-12 flex justify-center items-center bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800">
        <p class="text-slate-500 animate-pulse font-mono tracking-widest text-xs uppercase">Fetching sensor telemetry...</p>
      </div>

      <!-- Machinery Grid -->
      <div v-else class="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <Card v-for="mac in machinery" :key="mac.id" :class="[mac.needs_maintenance ? 'border-red-200 dark:border-red-900/50 bg-red-50/10 dark:bg-red-950/5' : '']">
          <CardHeader class="pb-4">
            <div class="flex justify-between items-start">
              <div>
                <div class="flex items-center gap-2">
                  <h3 class="text-lg font-bold text-slate-900 dark:text-white uppercase tracking-tight">{{ mac.equipment_name }}</h3>
                  <Badge :variant="mac.needs_maintenance ? 'destructive' : 'secondary'" class="text-[10px] font-black uppercase tracking-wider font-mono">
                    {{ mac.needs_maintenance ? 'Critical' : 'Healthy' }}
                  </Badge>
                </div>
                <CardDescription class="font-mono text-xs mt-1">{{ mac.equipment_type }} • S/N: {{ mac.serial_number }}</CardDescription>
              </div>
              <div class="text-right flex flex-col items-end gap-1.5">
                <div>
                  <span class="text-[10px] text-slate-400 font-bold uppercase block font-mono">Location</span>
                  <Badge variant="outline" class="mt-1 font-bold text-xs uppercase">{{ mac.vessel_name || mac.vessel }}</Badge>
                </div>
                <div v-if="authState.userRole === 'Admin' || authState.userRole === 'Chief Engineer'" class="flex gap-1.5 mt-1">
                  <button @click="openTelemetryModal(mac)" class="text-emerald-500 hover:text-emerald-700 p-1 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded transition" title="View Telemetry">
                    <Activity class="w-3.5 h-3.5" />
                  </button>
                  <button @click="openEditModal(mac)" class="text-blue-500 hover:text-blue-700 p-1 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded transition" title="Edit Machinery">
                    <Edit class="w-3.5 h-3.5" />
                  </button>
                  <button @click="deleteMachinery(mac.id)" class="text-red-500 hover:text-red-700 p-1 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded transition" title="Delete Machinery">
                    <Trash2 class="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            </div>
          </CardHeader>
          
          <CardContent class="space-y-4">
            <!-- Equipment Snapshot -->
            <div class="grid grid-cols-2 gap-2 text-xs font-mono bg-slate-50 dark:bg-slate-900/50 p-3 rounded-lg border border-slate-100 dark:border-slate-800/60">
              <div><span class="text-slate-500">Parent Asset:</span> <span class="font-bold text-slate-700 dark:text-slate-300">{{ mac.asset_name || 'Unassigned' }}</span></div>
              <div><span class="text-slate-500">Serial No:</span> <span class="font-bold text-slate-700 dark:text-slate-300">{{ mac.serial_number }}</span></div>
              <div><span class="text-slate-500">Installed:</span> <span class="font-bold text-slate-700 dark:text-slate-300">{{ formatDateOnly(mac.installation_date) }}</span></div>
              <div><span class="text-slate-500">Rem. Life:</span> <span class="font-bold text-slate-700 dark:text-slate-300">~{{ mac.rul_hours }} hrs</span></div>
            </div>

            <!-- Health Score Progress Bar -->
            <div class="space-y-1.5">
              <div class="flex justify-between items-center text-xs font-mono">
                <span class="text-slate-400 font-bold uppercase tracking-wider">Asset Health Score</span>
                <span :class="['font-bold', mac.health_percentage > 70 ? 'text-green-500' : mac.health_percentage > 40 ? 'text-orange-500' : 'text-red-500']">{{ mac.health_percentage }}%</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-slate-800 h-2.5 rounded-full overflow-hidden border border-slate-200/50 dark:border-slate-800">
                <div :style="{ width: `${mac.health_percentage}%` }" :class="['h-full transition-all duration-500', mac.health_percentage > 70 ? 'bg-green-500' : mac.health_percentage > 40 ? 'bg-orange-500' : 'bg-red-500']"></div>
              </div>
            </div>

            <!-- Telemetry Readings Box -->
            <div class="grid grid-cols-2 gap-4 bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200/40 dark:border-slate-800/40 font-mono">
              <div class="space-y-1">
                <span class="text-[10px] text-slate-400 font-bold uppercase tracking-wider flex items-center gap-1">
                  <Gauge class="w-3.5 h-3.5 text-blue-500" /> Vibration
                </span>
                <div class="flex items-baseline gap-1 mt-0.5">
                  <span :class="['text-lg font-bold tracking-tight', mac.needs_maintenance ? 'text-red-500 font-black' : 'text-slate-800 dark:text-slate-200']">{{ mac.vibration }}</span>
                  <span class="text-[10px] text-slate-400">mm/s</span>
                </div>
              </div>

              <div class="space-y-1">
                <span class="text-[10px] text-slate-400 font-bold uppercase tracking-wider flex items-center gap-1">
                  <Thermometer class="w-3.5 h-3.5 text-red-500" /> Temperature
                </span>
                <div class="flex items-baseline gap-1 mt-0.5">
                  <span :class="['text-lg font-bold tracking-tight', mac.needs_maintenance ? 'text-red-500 font-black' : 'text-slate-800 dark:text-slate-200']">{{ mac.temperature }}</span>
                  <span class="text-[10px] text-slate-400">°C</span>
                </div>
              </div>
            </div>

            <!-- Operating Hours & Prediction Info -->
            <div class="grid grid-cols-2 gap-4 text-xs font-mono pt-2 border-t border-slate-100 dark:border-slate-800/60">
              <div>
                <span class="text-slate-400 uppercase font-bold tracking-wider text-[10px] block">Operating Hours</span>
                <span class="text-slate-700 dark:text-slate-300 font-bold mt-0.5 block">{{ mac.operating_hours }} / {{ mac.maintenance_interval_hours }} hrs</span>
              </div>
              <div>
                <span class="text-slate-400 uppercase font-bold tracking-wider text-[10px] block">Est. Maintenance Needed</span>
                <span :class="['font-bold mt-0.5 block', mac.needs_maintenance ? 'text-red-500' : 'text-slate-700 dark:text-slate-300']">
                  {{ mac.needs_maintenance ? 'IMMEDIATE' : formatDateOnly(mac.predicted_failure_date) }}
                </span>
              </div>
            </div>

            <!-- Action Button Footer -->
            <div class="flex justify-between items-center pt-4 border-t border-slate-100 dark:border-slate-800/60">
              <span class="text-[10px] text-slate-400 font-bold uppercase tracking-wider font-mono">
                {{ mac.needs_maintenance ? '[OVERDUE] Maintenance Required' : `STATUS: OPERATIONAL` }}
              </span>
              <Button @click="handleActionClick(mac)" :variant="mac.needs_maintenance ? 'destructive' : 'secondary'" size="sm" class="font-bold uppercase tracking-wider text-xs">
                {{ mac.needs_maintenance ? 'Issue Work Order' : 'Schedule Check' }}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- Add/Edit Machinery Modal -->
      <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl max-w-lg w-full p-6 max-h-[90vh] overflow-y-auto">
          <h3 class="text-xl font-heading font-black text-slate-900 dark:text-white uppercase tracking-tight mb-1">
            {{ isEditMode ? 'Edit Machinery' : 'Add Machinery' }}
          </h3>
          <p class="text-xs text-slate-500 dark:text-slate-400 font-mono mb-6">
            {{ isEditMode ? 'Update operating parameters for this equipment' : 'Register new machinery equipment to the vessel' }}
          </p>

          <form @submit.prevent="submitForm" class="space-y-4 font-mono text-xs">
            <div>
              <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Equipment Name *</label>
              <input
                v-model="formData.equipment_name"
                type="text"
                placeholder="e.g. Main Generator B"
                class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)]"
                required
              />
            </div>

            <div>
              <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Parent Asset System (Optional)</label>
              <select
                v-model="formData.asset"
                class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)]"
              >
                <option value="">-- No Parent (Independent Machinery) --</option>
                <option v-for="ast in assets" :key="ast.asset_id" :value="ast.asset_id">
                  {{ ast.name }} ({{ ast.asset_id }})
                </option>
              </select>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Equipment Type *</label>
                <select
                  v-model="formData.equipment_type"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)]"
                  required
                >
                  <option value="Generator">Generator</option>
                  <option value="Pump">Pump</option>
                  <option value="Compressor">Compressor</option>
                  <option value="Thruster">Thruster</option>
                  <option value="Hydraulic Unit">Hydraulic Unit</option>
                  <option value="Other">Other</option>
                </select>
              </div>
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Serial Number *</label>
                <input
                  v-model="formData.serial_number"
                  type="text"
                  placeholder="e.g. GEN-S7000-002"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)]"
                  :disabled="isEditMode"
                  required
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Installation Date *</label>
                <input
                  v-model="formData.installation_date"
                  type="date"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none"
                  required
                />
              </div>
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Last Maintenance Date</label>
                <input
                  v-model="formData.last_maintenance_date"
                  type="date"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none"
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Operating Hours (hrs)</label>
                <input
                  v-model.number="formData.operating_hours"
                  type="number"
                  min="0"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none"
                />
              </div>
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Interval Hours (hrs)</label>
                <input
                  v-model.number="formData.maintenance_interval_hours"
                  type="number"
                  min="1"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none"
                />
              </div>
            </div>

            <div class="flex justify-end gap-3 pt-4 border-t border-slate-100 dark:border-slate-800">
              <Button type="button" variant="outline" @click="closeModal" class="font-bold">
                Cancel
              </Button>
              <Button type="submit" class="bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white font-bold">
                {{ isEditMode ? 'Save Changes' : 'Register Machinery' }}
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <!-- Issue WO Modal -->
    <div v-if="showIssueWoModal" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl max-w-sm w-full p-6 animate-in fade-in duration-200">
        <h3 class="text-lg font-bold text-slate-900 dark:text-white uppercase mb-4">Issue Work Order</h3>
        <p class="text-xs text-slate-500 mb-4">Assign this critical maintenance task to a lead worker.</p>
        <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1 text-xs">Assign To (Lead Worker) *</label>
        <select v-model="selectedAssignee" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)] mb-6" required :disabled="isFetchingEmployees">
           <option value="" disabled>{{ isFetchingEmployees ? 'Loading...' : 'Select Assignee' }}</option>
           <option v-for="emp in assignableWorkers" :key="emp.emp_id" :value="emp.emp_id">{{ emp.full_name }} ({{ emp.job_role }})</option>
        </select>
        <div class="flex justify-end gap-3">
          <button @click="showIssueWoModal = false" class="px-4 py-2 border border-slate-200 dark:border-slate-800 rounded-lg font-bold text-xs hover:bg-slate-50 dark:hover:bg-slate-800">Cancel</button>
          <button @click="confirmCreateWorkOrder" class="px-4 py-2 bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white rounded-lg font-bold text-xs" :disabled="!selectedAssignee">Create Work Order</button>
        </div>
      </div>
    </div>

    <!-- Telemetry Chart Modal -->
    <div v-if="showTelemetryModal" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl max-w-3xl w-full p-6 animate-in fade-in duration-200">
        <div class="flex justify-between items-center mb-4">
          <div>
            <h3 class="text-lg font-bold text-slate-900 dark:text-white uppercase">Machinery Telemetry: {{ selectedTelemetryMac?.equipment_name }}</h3>
            <p class="text-xs text-slate-500 font-mono mt-1">Live streaming historical sensor data (Vibration & Temperature)</p>
          </div>
          <button @click="closeTelemetryModal" class="text-slate-400 hover:text-slate-600 transition">
            <X class="w-5 h-5" />
          </button>
        </div>
        
        <div v-if="isFetchingTelemetry" class="flex justify-center p-12">
          <p class="text-slate-500 text-sm animate-pulse font-mono">Fetching IoT stream...</p>
        </div>
        <div v-else-if="telemetryChartData" class="h-[300px] w-full">
          <Line :data="telemetryChartData" :options="chartOptions" />
        </div>
        <div v-else class="flex justify-center p-12 text-slate-500 text-sm font-mono">
          No telemetry data available for this equipment.
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Cpu, CheckCircle, AlertTriangle, RefreshCw, Gauge, Thermometer, Plus, Edit, Trash2, Activity, X } from '@lucide/vue'
import { authState, getAccessToken } from '@/store/auth'
import { toast } from 'vue-sonner'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1'
const router = useRouter()

const isLoading = ref(false)
const machinery = ref([])
const assets = ref([])

const showModal = ref(false)
const showIssueWoModal = ref(false)
const selectedAssignee = ref('')
const pendingWoMac = ref(null)
const vesselEmployees = ref([])
const isFetchingEmployees = ref(false)

const isEditMode = ref(false)
const editingMacId = ref(null)

const showTelemetryModal = ref(false)
const selectedTelemetryMac = ref(null)
const isFetchingTelemetry = ref(false)
const telemetryChartData = ref(null)

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index',
    intersect: false,
  },
  plugins: {
    legend: {
      position: 'top',
      labels: { color: '#94a3b8', font: { family: 'monospace' } }
    },
    tooltip: { mode: 'index', intersect: false }
  },
  scales: {
    y: {
      type: 'linear',
      display: true,
      position: 'left',
      title: { display: true, text: 'Vibration (mm/s)', color: '#3b82f6', font: { family: 'monospace', size: 10 } },
      grid: { color: 'rgba(148, 163, 184, 0.1)' },
      ticks: { color: '#94a3b8', font: { family: 'monospace', size: 10 } }
    },
    y1: {
      type: 'linear',
      display: true,
      position: 'right',
      title: { display: true, text: 'Temperature (°C)', color: '#ef4444', font: { family: 'monospace', size: 10 } },
      grid: { drawOnChartArea: false },
      ticks: { color: '#94a3b8', font: { family: 'monospace', size: 10 } }
    },
    x: {
      grid: { color: 'rgba(148, 163, 184, 0.1)' },
      ticks: { color: '#94a3b8', font: { family: 'monospace', size: 10 }, maxTicksLimit: 10 }
    }
  }
}

const assignableWorkers = computed(() => {
  return vesselEmployees.value.filter(emp => !['Chief Engineer', 'Safety Officer'].includes(emp.job_role))
})

const formData = ref({
  asset: '',
  equipment_name: '',
  equipment_type: 'Generator',
  serial_number: '',
  installation_date: '',
  operating_hours: 0,
  maintenance_interval_hours: 1000,
  last_maintenance_date: ''
})

const healthyCount = computed(() => machinery.value.filter(m => !m.needs_maintenance).length)
const needsMaintCount = computed(() => machinery.value.filter(m => m.needs_maintenance).length)

const fetchMachinery = async () => {
  isLoading.value = true
  try {
    const params = new URLSearchParams()
    if (authState.selectedVessel) {
      params.append('vessel_id', authState.selectedVessel.asset_id)
    }
    const queryString = params.toString() ? `?${params.toString()}` : ''
    const response = await fetch(`${API_BASE_URL}/asset/machinery/${queryString}`, {
      headers: {
        'Authorization': `Bearer ${getAccessToken()}`
      }
    })
    if (response.ok) {
      machinery.value = await response.json()
    } else {
      console.error('Failed to fetch machinery:', response.status)
      toast.error("Failed", { description: "Failed to fetch telemetry data." })
    }
  } catch (error) {
    console.error('Error fetching data:', error)
    toast.error("Error", { description: "Server connection failed." })
  } finally {
    isLoading.value = false
  }
}

const fetchAssets = async () => {
  try {
    const params = new URLSearchParams()
    if (authState.selectedVessel) {
      params.append('vessel_id', authState.selectedVessel.asset_id)
    }
    const response = await fetch(`${API_BASE_URL}/asset/assets/?${params.toString()}`, {
      headers: {
        'Authorization': `Bearer ${getAccessToken()}`
      }
    })
    if (response.ok) {
      assets.value = await response.json()
    }
  } catch (error) {
    console.error('Error fetching assets:', error)
  }
}

// Unused fetchEmployees removed in favor of dynamic fetch

const formatDateOnly = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const autoCreateWorkOrder = async (mac) => {
  pendingWoMac.value = mac
  selectedAssignee.value = ''
  showIssueWoModal.value = true
  isFetchingEmployees.value = true
  vesselEmployees.value = []
  
  try {
    const vesselId = mac.vessel_id || mac.vessel
    const headers = { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
    const response = await fetch(`${API_BASE_URL}/hse/employees/?vessel_id=${vesselId}`, { headers })
    if (response.ok) {
      vesselEmployees.value = await response.json()
    }
  } catch (error) {
    console.error('Error fetching vessel employees:', error)
  } finally {
    isFetchingEmployees.value = false
  }
}

const confirmCreateWorkOrder = async () => {
  if (!pendingWoMac.value || !selectedAssignee.value) return
  const mac = pendingWoMac.value

  try {
    const timestamp = Date.now().toString().slice(-4)
    const wo_id = `WO-MAC-${mac.id}-${timestamp}`
    const payload = {
      wo_id: wo_id,
      vessel: mac.vessel,
      machinery: mac.id,
      asset: mac.asset || null,  // Inherit parent asset so deck locations are available for PTW
      description: `AUTO-GENERATED: Urgent predictive maintenance required for machinery "${mac.equipment_name}" S/N: ${mac.serial_number} due to abnormal sensor readings (Vibration: ${mac.vibration} mm/s, Temp: ${mac.temperature}°C).`,
      priority: 'CRITICAL',
      scheduled_date: new Date().toISOString().split('T')[0],
      status: 'PENDING',
      assigned_to: selectedAssignee.value,
      created_by: authState.username || 'Chief Engineer'
    }

    const response = await fetch(`${API_BASE_URL}/asset/workorders/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getAccessToken()}`
      },
      body: JSON.stringify(payload)
    })

    if (response.ok) {
      toast.success("Work Order Created", { description: `Automatically created ${wo_id} for ${mac.equipment_name} and assigned.` })
      showIssueWoModal.value = false
      router.push('/assets/work-orders')
    } else {
      const errorData = await response.json()
      console.error("Auto WO creation failed:", errorData)
      toast.error("Failed", { description: "Failed to automatically create Work Order." })
    }
  } catch (error) {
    console.error("Error creating WO:", error)
    toast.error("Error", { description: "Connection error." })
  }
}

const handleActionClick = (mac) => {
  if (mac.needs_maintenance) {
    autoCreateWorkOrder(mac)
  } else {
    toast.info("Equipment Schedule", { description: `${mac.equipment_name} is working within normal operating parameters.` })
  }
}

const openAddModal = () => {
  isEditMode.value = false
  editingMacId.value = null
  formData.value = {
    equipment_name: '',
    equipment_type: 'Generator',
    serial_number: '',
    installation_date: new Date().toISOString().split('T')[0],
    operating_hours: 0,
    maintenance_interval_hours: 1000,
    last_maintenance_date: ''
  }
  showModal.value = true
}

const openEditModal = (mac) => {
  isEditMode.value = true
  editingMacId.value = mac.id
  formData.value = {
    asset: mac.asset || '',
    equipment_name: mac.equipment_name,
    equipment_type: mac.equipment_type,
    serial_number: mac.serial_number,
    installation_date: mac.installation_date,
    operating_hours: mac.operating_hours,
    maintenance_interval_hours: mac.maintenance_interval_hours,
    last_maintenance_date: mac.last_maintenance_date || ''
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const submitForm = async () => {
  try {
    const payload = {
      ...formData.value,
      vessel: authState.selectedVessel ? authState.selectedVessel.asset_id : null
    }

    if (!payload.vessel) {
      toast.error("Error", { description: "Please select a vessel in the Topbar first." })
      return
    }

    const url = isEditMode.value
      ? `${API_BASE_URL}/asset/machinery/${editingMacId.value}/`
      : `${API_BASE_URL}/asset/machinery/`

    const response = await fetch(url, {
      method: isEditMode.value ? 'PUT' : 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getAccessToken()}`
      },
      body: JSON.stringify(payload)
    })

    if (response.ok) {
      toast.success("Success", { description: `Machinery ${isEditMode.value ? 'updated' : 'registered'} successfully.` })
      showModal.value = false
      fetchMachinery()
    } else {
      const errorData = await response.json()
      console.error("Error saving machinery:", errorData)
      const msg = Object.values(errorData).flat()[0] || "Failed to save machinery."
      toast.error("Failed", { description: msg })
    }
  } catch (error) {
    console.error("Error submitting form:", error)
    toast.error("Error", { description: "Connection failed." })
  }
}

const deleteMachinery = async (id) => {
  if (!confirm("Are you sure you want to delete this machinery?")) return
  try {
    const response = await fetch(`${API_BASE_URL}/asset/machinery/${id}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${getAccessToken()}`
      }
    })

    if (response.ok) {
      toast.success("Deleted", { description: "Machinery deleted successfully." })
      fetchMachinery()
    } else {
      toast.error("Failed", { description: "Failed to delete machinery." })
    }
  } catch (error) {
    console.error("Error deleting machinery:", error)
    toast.error("Error", { description: "Connection failed." })
  }
}

let telemetryInterval = null;

const fetchTelemetryData = async () => {
  if (!selectedTelemetryMac.value) return;
  try {
    const headers = { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
    const response = await fetch(`${API_BASE_URL}/asset/telemetry/history/?machinery_id=${selectedTelemetryMac.value.id}&limit=50&_t=${Date.now()}`, { headers })
    if (response.ok) {
      const data = await response.json()
      if (data.length > 0) {
        telemetryChartData.value = {
          labels: data.map(d => new Date(d.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })),
          datasets: [
            {
              label: 'Vibration (mm/s)',
              data: data.map(d => d.vibration),
              borderColor: '#3b82f6',
              backgroundColor: 'rgba(59, 130, 246, 0.1)',
              yAxisID: 'y',
              tension: 0.3,
              fill: true
            },
            {
              label: 'Temperature (°C)',
              data: data.map(d => d.temperature),
              borderColor: '#ef4444',
              backgroundColor: 'transparent',
              yAxisID: 'y1',
              tension: 0.3
            }
          ]
        }
      }
    }
  } catch (error) {
    console.error("Error fetching telemetry:", error)
  }
}

const openTelemetryModal = async (mac) => {
  selectedTelemetryMac.value = mac
  showTelemetryModal.value = true
  isFetchingTelemetry.value = true
  telemetryChartData.value = null
  
  await fetchTelemetryData()
  isFetchingTelemetry.value = false
  
  if (telemetryInterval) clearInterval(telemetryInterval)
  telemetryInterval = setInterval(fetchTelemetryData, 5000)
}

const closeTelemetryModal = () => {
  showTelemetryModal.value = false
  selectedTelemetryMac.value = null
  if (telemetryInterval) clearInterval(telemetryInterval)
}

onMounted(() => {
  fetchMachinery()
  fetchAssets()
})
</script>
