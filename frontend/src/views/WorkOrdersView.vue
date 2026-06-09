<template>
  <DashboardLayout>
    <div class="p-8">
      <!-- Header -->
      <div class="flex justify-between items-start mb-8">
        <div>
          <h2 class="text-3xl font-bold text-slate-900 dark:text-white uppercase tracking-tight">Work Orders</h2>
          <p class="text-sm text-slate-600 dark:text-slate-400 mt-1 font-mono">Manage maintenance tasks and operations</p>
        </div>
        <button v-if="authState.userRole === 'Admin' || authState.userRole === 'Chief Engineer'" @click="openWoModal" class="bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white font-bold px-4 py-2 rounded-lg transition flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M12 5v14"/></svg>
          Create Work Order
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="p-12 flex justify-center bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 mb-8">
        <p class="text-slate-500 dark:text-slate-400 animate-pulse">Loading data...</p>
      </div>

      <!-- Work Orders List -->
      <div v-else class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-sm text-left text-slate-500 dark:text-slate-400 font-mono">
            <thead class="text-xs text-slate-700 uppercase bg-slate-50 dark:bg-slate-900/50 dark:text-slate-400 border-b border-slate-200 dark:border-slate-700 font-bold">
              <tr>
                <th scope="col" class="px-6 py-3">WO ID</th>
                <th scope="col" class="px-6 py-3">Description</th>
                <th scope="col" class="px-6 py-3">Vessel</th>
                <th scope="col" class="px-6 py-3">Target Asset/Machine</th>
                <th scope="col" class="px-6 py-3">Priority</th>
                <th scope="col" class="px-6 py-3">Status</th>
                <th scope="col" class="px-6 py-3">Scheduled</th>
                <th scope="col" class="px-6 py-3">Actions</th>
              </tr>
            </thead>
            <tbody class="text-xs">
              <tr v-if="workOrders.length === 0" class="border-b dark:border-slate-700">
                <td colspan="8" class="px-6 py-8 text-center text-slate-500">No Work Orders found.</td>
              </tr>
              <tr v-for="wo in workOrders" :key="wo.wo_id" class="border-b dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-850 transition">
                <td class="px-6 py-4 font-bold text-slate-900 dark:text-white">{{ wo.wo_id }}</td>
                <td class="px-6 py-4 font-sans text-slate-700 dark:text-slate-300">{{ truncate(wo.description) }}</td>
                <td class="px-6 py-4">{{ wo.vessel_name || wo.vessel }}</td>
                <td class="px-6 py-4">
                  <span v-if="wo.machinery_name" class="px-2 py-0.5 rounded bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-[10px] font-bold">
                    🤖 {{ wo.machinery_name }}
                  </span>
                  <span v-else-if="wo.asset_name" class="px-2 py-0.5 rounded bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300 text-[10px] font-bold">
                    🏗️ {{ wo.asset_name }}
                  </span>
                  <span v-else class="text-slate-400">-</span>
                </td>
                <td class="px-6 py-4">
                  <span :class="['px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-wider', getPriorityColor(wo.priority)]">{{ wo.priority }}</span>
                </td>
                <td class="px-6 py-4">
                  <span :class="['px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-wider', getStatusColor(wo.status)]">{{ wo.status }}</span>
                </td>
                <td class="px-6 py-4">{{ wo.scheduled_date }}</td>
                <td class="px-6 py-4 flex gap-2">
                  <button v-if="authState.userRole === 'Admin' || authState.userRole === 'Chief Engineer'" @click="deleteWo(wo.wo_id)" class="text-red-500 hover:text-red-700 p-1 border border-transparent hover:border-red-200 hover:bg-red-50/20 rounded transition"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg></button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- Create Work Order Modal -->
    <div v-if="showWoModal" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl max-w-lg w-full p-6 max-h-[95vh] overflow-y-auto font-mono text-xs">
        <h3 class="text-xl font-heading font-black text-slate-900 dark:text-white uppercase mb-1">Create Work Order</h3>
        <p class="text-xs text-slate-500 dark:text-slate-400 mb-6">Add a new Work Order to be used in PTW</p>
        
        <form @submit.prevent="submitWo" class="space-y-4">
          <div>
            <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Work Order ID *</label>
            <input v-model="woForm.wo_id" type="text" placeholder="e.g. WO-2026-001" required
              class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)]">
          </div>
          <div>
            <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Vessel *</label>
            <select v-model="woForm.vessel" required
              class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)]">
              <option value="" disabled>Select Vessel</option>
              <option v-for="v in vessels" :key="v.vessel_id" :value="v.vessel_id">{{ v.vessel_name }}</option>
            </select>
          </div>

          <!-- Optional targets -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Link to Asset (Optional)</label>
              <select v-model="woForm.asset" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none">
                <option value="">None</option>
                <option v-for="a in filteredAssets" :key="a.asset_id" :value="a.asset_id">{{ a.name }}</option>
              </select>
            </div>
            <div>
              <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Link to Machine (Optional)</label>
              <select v-model="woForm.machinery" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none">
                <option value="">None</option>
                <option v-for="m in filteredMachinery" :key="m.id" :value="m.id">{{ m.equipment_name }}</option>
              </select>
            </div>
          </div>

          <div>
            <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Description *</label>
            <textarea v-model="woForm.description" rows="3" required placeholder="Describe the maintenance requirements..."
              class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none font-sans text-xs"></textarea>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Priority</label>
              <select v-model="woForm.priority" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none">
                <option value="LOW">Low</option>
                <option value="MEDIUM">Medium</option>
                <option value="HIGH">High</option>
                <option value="CRITICAL">Critical</option>
              </select>
            </div>
            <div>
              <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Scheduled Date *</label>
              <input v-model="woForm.scheduled_date" type="date" required
                class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none">
            </div>
          </div>
          
          <div class="flex gap-3 pt-4 border-t border-slate-150 dark:border-slate-850 mt-6">
            <button type="button" @click="showWoModal = false" class="flex-1 px-4 py-2 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-white hover:bg-slate-50 dark:hover:bg-slate-800 transition font-bold">
              Cancel
            </button>
            <button type="submit" class="flex-1 px-4 py-2 bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white rounded-lg font-bold transition">
              Create
            </button>
          </div>
        </form>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { authState } from '@/store/auth'
import { toast } from 'vue-sonner'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1'

const isLoading = ref(false)
const workOrders = ref([])
const vessels = ref([])
const allAssets = ref([])
const allMachinery = ref([])
const showWoModal = ref(false)

const woForm = ref({
  wo_id: '',
  vessel: '',
  asset: '',
  machinery: '',
  description: '',
  priority: 'MEDIUM',
  scheduled_date: new Date().toISOString().split('T')[0],
  status: 'PENDING',
  created_by: authState.username || 'Admin'
})

const filteredAssets = computed(() => {
  if (!woForm.value.vessel) return []
  return allAssets.value.filter(a => a.vessel === woForm.value.vessel || a.vessel_id === woForm.value.vessel)
})

const filteredMachinery = computed(() => {
  if (!woForm.value.vessel) return []
  return allMachinery.value.filter(m => m.vessel === woForm.value.vessel || m.vessel_id === woForm.value.vessel)
})

const fetchWorkOrders = async () => {
  isLoading.value = true
  try {
    const headers = { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
    const woResponse = await fetch(`${API_BASE_URL}/asset/workorders/`, { headers })
    if (woResponse.ok) {
      workOrders.value = await woResponse.json()
    }
  } catch (error) {
    console.error('Error fetching data:', error)
  } finally {
    isLoading.value = false
  }
}

const fetchVessels = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/offshore/vessels/`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
    })
    if (response.ok) {
      vessels.value = await response.json()
    }
  } catch (error) {
    console.error('Error fetching vessels:', error)
  }
}

const fetchAssetsAndMachinery = async () => {
  try {
    const headers = { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
    const [assetRes, macRes] = await Promise.all([
      fetch(`${API_BASE_URL}/asset/assets/`, { headers }),
      fetch(`${API_BASE_URL}/asset/machinery/`, { headers })
    ])
    if (assetRes.ok) allAssets.value = await assetRes.json()
    if (macRes.ok) allMachinery.value = await macRes.json()
  } catch (error) {
    console.error("Error fetching assets/machinery:", error)
  }
}

const openWoModal = () => {
  woForm.value = {
    wo_id: '',
    vessel: vessels.value[0]?.vessel_id || '',
    asset: '',
    machinery: '',
    description: '',
    priority: 'MEDIUM',
    scheduled_date: new Date().toISOString().split('T')[0],
    status: 'PENDING',
    created_by: authState.username || 'Admin'
  }
  showWoModal.value = true
}

const submitWo = async () => {
  try {
    const payload = {
      ...woForm.value,
      asset: woForm.value.asset || null,
      machinery: woForm.value.machinery || null
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
      toast.success('Work Order Created Successfully')
      showWoModal.value = false
      fetchWorkOrders()
    } else {
      const err = await response.json()
      const msg = Object.values(err).flat()[0] || "Failed to create Work Order."
      toast.error('Failed to create Work Order', { description: msg })
    }
  } catch (error) {
    toast.error('Network error')
  }
}

const deleteWo = async (id) => {
  if (!confirm(`Delete Work Order ${id}?`)) return
  try {
    const response = await fetch(`${API_BASE_URL}/asset/workorders/${id}/`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
    })
    if (response.ok || response.status === 204) {
      toast.success('Work Order deleted')
      fetchWorkOrders()
    }
  } catch (error) {
    toast.error('Error deleting')
  }
}

const truncate = (text) => text && text.length > 50 ? text.substring(0, 50) + '...' : text

const getPriorityColor = (priority) => {
  const map = {
    'LOW': 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300',
    'MEDIUM': 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400',
    'HIGH': 'bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400',
    'CRITICAL': 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
  }
  return map[priority] || 'bg-slate-100 text-slate-700'
}

const getStatusColor = (status) => {
  const map = {
    'PENDING': 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400',
    'IN_PROGRESS': 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400',
    'COMPLETED': 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400',
    'CANCELLED': 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300',
  }
  return map[status] || 'bg-slate-100 text-slate-700'
}

onMounted(() => {
  fetchWorkOrders()
  fetchVessels()
  fetchAssetsAndMachinery()
})
</script>
