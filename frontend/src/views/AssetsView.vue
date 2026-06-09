<template>
  <DashboardLayout>
    <div class="p-8">
      <!-- Header -->
      <div class="flex justify-between items-start mb-8">
        <div>
          <h2 class="text-3xl font-bold text-slate-900 dark:text-white uppercase tracking-tight">Asset Registry</h2>
          <p class="text-sm text-slate-600 dark:text-slate-400 mt-1 font-mono">Fleet assets condition tracking & predictive maintenance</p>
        </div>
        <button v-if="authState.userRole === 'Admin'" @click="openAddModal" class="bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white font-bold px-4 py-2 rounded-lg transition flex items-center gap-2">
          <Plus class="w-4 h-4" /> Add Asset
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="p-12 flex justify-center bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 mb-8">
        <p class="text-slate-500 dark:text-slate-400 animate-pulse">Loading data...</p>
      </div>

      <!-- Assets Registry Section -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-if="assets.length === 0" class="col-span-full p-8 text-center text-slate-500 bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700">
          No Assets found.
        </div>
        
        <div v-for="asset in assets" :key="asset.asset_id" :class="['bg-white dark:bg-slate-800 border rounded-2xl shadow-sm p-6 relative group transition duration-300', asset.status === 'CRITICAL' ? 'border-red-200 dark:border-red-900/50 bg-red-50/5' : 'border-slate-200 dark:border-slate-700']">
          <div class="flex justify-between items-start mb-4">
            <div class="w-12 h-12 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-blue-600 dark:text-blue-400">
              <i :class="['fa-solid text-xl', asset.icon ? asset.icon.split(' ')[0] : 'fa-box']"></i>
            </div>
            <div class="flex items-center gap-2">
              <span :class="['px-2 py-1 rounded text-[10px] font-black uppercase tracking-wider', getStatusColor(asset.status)]">{{ asset.status }}</span>
              <div v-if="authState.userRole === 'Admin'" class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <button @click="openEditModal(asset)" class="text-blue-500 hover:text-blue-700 p-1 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded transition" title="Edit Asset">
                  <Edit class="w-3.5 h-3.5" />
                </button>
                <button @click="deleteAsset(asset.asset_id)" class="text-red-500 hover:text-red-700 p-1 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded transition" title="Delete Asset">
                  <Trash2 class="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          </div>
          <h3 class="text-lg font-bold text-slate-900 dark:text-white mb-0.5 uppercase tracking-tight">{{ asset.name }}</h3>
          <p class="text-xs text-slate-500 dark:text-slate-400 mb-4 font-mono">{{ asset.vessel_name || asset.vessel }} • {{ asset.capacity }}</p>

          <!-- Health Score Progress Bar -->
          <div class="space-y-1.5 mb-4">
            <div class="flex justify-between items-center text-xs font-mono">
              <span class="text-slate-400 font-bold uppercase tracking-wider">Asset Health Score</span>
              <span :class="['font-bold', asset.health_score > 70 ? 'text-green-500' : asset.health_score > 40 ? 'text-orange-500' : 'text-red-500']">{{ asset.health_score }}%</span>
            </div>
            <div class="w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full overflow-hidden border border-slate-200/50 dark:border-slate-800">
              <div :style="{ width: `${asset.health_score}%` }" :class="['h-full transition-all duration-500', asset.health_score > 70 ? 'bg-green-500' : asset.health_score > 40 ? 'bg-orange-500' : 'bg-red-500']"></div>
            </div>
          </div>

          <!-- Telemetry Readings Box (Predictive) -->
          <div class="grid grid-cols-2 gap-4 bg-slate-50 dark:bg-slate-950 p-3.5 rounded-xl border border-slate-200/40 dark:border-slate-800/40 font-mono mb-4 text-xs">
            <div class="space-y-1">
              <span class="text-[9px] text-slate-400 font-bold uppercase tracking-wider flex items-center gap-1">
                <Gauge class="w-3.5 h-3.5 text-blue-500" /> Vibration
              </span>
              <div class="flex items-baseline gap-1 mt-0.5">
                <span :class="['text-base font-bold tracking-tight', asset.status === 'CRITICAL' ? 'text-red-500 font-black' : 'text-slate-800 dark:text-slate-200']">{{ asset.vibration }}</span>
                <span class="text-[10px] text-slate-400">mm/s</span>
              </div>
            </div>

            <div class="space-y-1">
              <span class="text-[9px] text-slate-400 font-bold uppercase tracking-wider flex items-center gap-1">
                <Thermometer class="w-3.5 h-3.5 text-red-500" /> Temp
              </span>
              <div class="flex items-baseline gap-1 mt-0.5">
                <span :class="['text-base font-bold tracking-tight', asset.status === 'CRITICAL' ? 'text-red-500 font-black' : 'text-slate-800 dark:text-slate-200']">{{ asset.temperature }}</span>
                <span class="text-[10px] text-slate-400">°C</span>
              </div>
            </div>
          </div>

          <div class="flex justify-between items-center pt-3 border-t border-slate-100 dark:border-slate-750 font-mono text-[10px]">
            <span class="text-slate-400 uppercase font-bold tracking-wider">Est. Next Service</span>
            <span :class="['font-bold', asset.status === 'CRITICAL' ? 'text-red-500' : 'text-slate-700 dark:text-slate-300']">
              {{ asset.status === 'CRITICAL' ? 'IMMEDIATE' : formatDateOnly(asset.predicted_failure_date) }}
            </span>
          </div>

          <!-- Auto-create WO Button for Critical/Maintenance Assets -->
          <div v-if="asset.status === 'CRITICAL' || asset.status === 'MAINTENANCE'" class="mt-4 pt-3 border-t border-slate-100 dark:border-slate-700 flex justify-end">
            <button @click="autoCreateWorkOrder(asset)" class="w-full bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white font-mono text-[10px] uppercase font-bold py-2 rounded-lg transition">
              Issue Work Order
            </button>
          </div>
        </div>
      </div>

      <!-- Add/Edit Asset Modal -->
      <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl max-w-lg w-full p-6 max-h-[90vh] overflow-y-auto animate-in fade-in duration-200">
          <h3 class="text-xl font-heading font-black text-slate-900 dark:text-white uppercase tracking-tight mb-1">
            {{ isEditMode ? 'Edit Asset' : 'Add Asset' }}
          </h3>
          <p class="text-xs text-slate-500 dark:text-slate-400 font-mono mb-6">
            {{ isEditMode ? 'Update asset details and operational status' : 'Register a new major asset in the fleet registry' }}
          </p>

          <form @submit.prevent="submitForm" class="space-y-4 font-mono text-xs">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Asset ID *</label>
                <input
                  v-model="formData.asset_id"
                  type="text"
                  placeholder="e.g. AST-004"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)]"
                  :disabled="isEditMode"
                  required
                />
              </div>
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Asset Name *</label>
                <input
                  v-model="formData.name"
                  type="text"
                  placeholder="e.g. Auxiliary Crane B"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)]"
                  required
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Vessel *</label>
                <select
                  v-model="formData.vessel"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)]"
                  required
                >
                  <option value="" disabled>Select Vessel</option>
                  <option v-for="v in vessels" :key="v.asset_id" :value="v.vessel_id">{{ v.vessel_name }}</option>
                </select>
              </div>
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Capacity</label>
                <input
                  v-model="formData.capacity"
                  type="text"
                  placeholder="e.g. 500 Ton"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)]"
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Status *</label>
                <select
                  v-model="formData.status"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)]"
                  required
                >
                  <option value="OPERATIONAL">Operational</option>
                  <option value="MAINTENANCE">Maintenance</option>
                  <option value="CRITICAL">Critical</option>
                </select>
              </div>
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Health Score *</label>
                <input
                  v-model.number="formData.health_score"
                  type="number"
                  min="0"
                  max="100"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none"
                  required
                />
              </div>
            </div>

            <div class="flex justify-end gap-3 pt-4 border-t border-slate-100 dark:border-slate-800">
              <button type="button" @click="closeModal" class="px-4 py-2 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-white hover:bg-slate-50 dark:hover:bg-slate-800 transition font-bold">
                Cancel
              </button>
              <button type="submit" class="px-4 py-2 bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white rounded-lg font-bold transition">
                {{ isEditMode ? 'Save Changes' : 'Add Asset' }}
              </button>
            </div>
          </form>
        </div>
      </div>

    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { Plus, Edit, Trash2, Gauge, Thermometer } from '@lucide/vue'
import { authState } from '@/store/auth'
import { vessels, fetchVessels } from '@/store/vessel'
import { toast } from 'vue-sonner'

const router = useRouter()
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1'

const isLoading = ref(false)
const assets = ref([])
const showModal = ref(false)
const isEditMode = ref(false)

const formData = ref({
  asset_id: '',
  name: '',
  vessel: '',
  capacity: '50 Pax',
  icon: 'fa-ship text-red-500',
  status: 'OPERATIONAL',
  health_score: 100
})

const fetchAssets = async () => {
  isLoading.value = true
  try {
    const headers = { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
    const params = new URLSearchParams()
    if (authState.selectedVessel) {
      params.append('vessel_id', authState.selectedVessel.asset_id)
    }
    const queryString = params.toString() ? `?${params.toString()}` : ''
    const assetResponse = await fetch(`${API_BASE_URL}/asset/assets/${queryString}`, { headers })
    if (assetResponse.ok) {
      assets.value = await assetResponse.json()
    }
  } catch (error) {
    console.error('Error fetching data:', error)
  } finally {
    isLoading.value = false
  }
}

const openAddModal = () => {
  isEditMode.value = false
  formData.value = {
    asset_id: '',
    name: '',
    vessel: vessels.value[0]?.vessel_id || '',
    capacity: '50 Pax',
    icon: 'fa-ship text-red-500',
    status: 'OPERATIONAL',
    health_score: 100
  }
  showModal.value = true
}

const openEditModal = (asset) => {
  isEditMode.value = true
  formData.value = {
    asset_id: asset.asset_id,
    name: asset.name,
    vessel: asset.vessel,
    capacity: asset.capacity,
    icon: asset.icon || 'fa-ship text-red-500',
    status: asset.status,
    health_score: asset.health_score
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const submitForm = async () => {
  try {
    const url = isEditMode.value
      ? `${API_BASE_URL}/asset/assets/${formData.value.asset_id}/`
      : `${API_BASE_URL}/asset/assets/`

    const response = await fetch(url, {
      method: isEditMode.value ? 'PUT' : 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify(formData.value)
    })

    if (response.ok) {
      toast.success("Success", { description: `Asset ${isEditMode.value ? 'updated' : 'added'} successfully.` })
      showModal.value = false
      fetchAssets()
    } else {
      const errorData = await response.json()
      console.error("Error saving asset:", errorData)
      const msg = Object.values(errorData).flat()[0] || "Failed to save asset."
      toast.error("Failed", { description: msg })
    }
  } catch (error) {
    console.error("Error submitting asset:", error)
    toast.error("Error", { description: "Connection failed." })
  }
}

const deleteAsset = async (assetId) => {
  if (!confirm("Are you sure you want to delete this asset?")) return
  try {
    const response = await fetch(`${API_BASE_URL}/asset/assets/${assetId}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })

    if (response.ok) {
      toast.success("Deleted", { description: "Asset deleted successfully." })
      fetchAssets()
    } else {
      toast.error("Failed", { description: "Failed to delete asset." })
    }
  } catch (error) {
    console.error("Error deleting asset:", error)
    toast.error("Error", { description: "Connection failed." })
  }
}

const getStatusColor = (status) => {
  const map = {
    'OPERATIONAL': 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400',
    'MAINTENANCE': 'bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400',
    'CRITICAL': 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
  }
  return map[status] || 'bg-slate-100 text-slate-700'
}

const formatDateOnly = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const autoCreateWorkOrder = async (asset) => {
  try {
    const timestamp = Date.now().toString().slice(-4)
    const wo_id = `WO-AST-${asset.asset_id}-${timestamp}`
    const payload = {
      wo_id: wo_id,
      vessel: asset.vessel,
      machinery: null,
      asset: asset.asset_id,
      description: `AUTO-GENERATED: Urgent predictive maintenance required for fleet asset "${asset.name}" S/N: ${asset.asset_id} due to abnormal sensor readings (Vibration: ${asset.vibration} mm/s, Temp: ${asset.temperature}°C).`,
      priority: asset.status === 'CRITICAL' ? 'CRITICAL' : 'HIGH',
      scheduled_date: new Date().toISOString().split('T')[0],
      status: 'PENDING',
      created_by: authState.username || 'Chief Engineer'
    }

    const response = await fetch(`${API_BASE_URL}/asset/workorders/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify(payload)
    })

    if (response.ok) {
      toast.success("Work Order Created", { description: `Automatically created ${wo_id} for ${asset.name}.` })
      router.push('/assets/work-orders')
    } else {
      const errorData = await response.json()
      console.error("Auto WO creation failed:", errorData)
      toast.error("Failed", { description: "Failed to automatically create Work Order." })
    }
  } catch (error) {
    console.error("Error creating WO:", error)
    toast.error("Error", { description: "Server connection failed." })
  }
}

onMounted(() => {
  fetchAssets()
  fetchVessels()
})
</script>
