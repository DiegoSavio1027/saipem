<template>
  <DashboardLayout>
    <div class="p-8 space-y-8">
      <!-- Header -->
      <div class="flex justify-between items-center">
        <div>
          <h2 class="text-3xl font-heading font-black text-slate-900 dark:text-white tracking-tight uppercase">Spare Parts</h2>
          <p class="text-sm text-slate-500 dark:text-slate-400 mt-1 font-mono">Manage vessel-specific machinery spare parts</p>
        </div>
        <div class="flex gap-2">
          <Button @click="fetchSpareParts" variant="outline" class="flex items-center gap-2">
            <RefreshCw :class="['w-4 h-4', isLoading ? 'animate-spin' : '']" /> Refresh
          </Button>
          <Button v-if="authState.userRole === 'Admin' || authState.userRole === 'Chief Engineer'" @click="openAddModal" class="bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white font-bold flex items-center gap-2">
            <Plus class="w-4 h-4" /> Add Part
          </Button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="p-12 flex justify-center items-center bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800">
        <p class="text-slate-500 animate-pulse font-mono tracking-widest text-xs uppercase">Fetching spare parts data...</p>
      </div>

      <!-- Spare Parts Grid -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div v-if="spareparts.length === 0" class="col-span-full p-12 text-center text-slate-500 font-mono text-xs border border-dashed border-slate-300 dark:border-slate-700 rounded-xl">
          No spare parts found.
        </div>
        <div v-for="part in spareparts" :key="part.id" class="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 p-5 shadow-sm flex flex-col justify-between" :class="[part.quantity_on_hand <= part.reorder_level ? 'border-orange-300 dark:border-orange-900/50 bg-orange-50/10 dark:bg-orange-950/10' : '']">
          
          <div class="flex justify-between items-start mb-4">
            <div>
              <div class="flex items-center gap-2">
                <h3 class="text-lg font-bold text-slate-900 dark:text-white">{{ part.part_name }}</h3>
                <Badge :variant="part.quantity_on_hand <= part.reorder_level ? 'destructive' : 'outline'" class="text-[10px] font-black uppercase tracking-wider font-mono">
                  {{ part.quantity_on_hand <= part.reorder_level ? 'Reorder Needed' : 'Stocked' }}
                </Badge>
              </div>
              <p class="text-xs text-slate-500 font-mono mt-1">P/N: {{ part.part_number }} • Vessel: {{ part.vessel_name || part.vessel }}</p>
            </div>
            <div v-if="authState.userRole === 'Admin' || authState.userRole === 'Chief Engineer'" class="flex gap-1.5">
              <button @click="openEditModal(part)" class="text-blue-500 hover:text-blue-700 p-1.5 bg-slate-50 dark:bg-slate-950 rounded transition">
                <Edit class="w-3.5 h-3.5" />
              </button>
              <button @click="deletePart(part.id)" class="text-red-500 hover:text-red-700 p-1.5 bg-slate-50 dark:bg-slate-950 rounded transition">
                <Trash2 class="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4 text-sm font-mono mt-2 bg-slate-50 dark:bg-slate-950/50 p-4 rounded-lg">
            <div>
              <span class="text-[10px] text-slate-400 font-bold uppercase block mb-1">Quantity on Hand</span>
              <span class="text-xl font-black" :class="part.quantity_on_hand <= part.reorder_level ? 'text-red-500' : 'text-slate-800 dark:text-slate-200'">{{ part.quantity_on_hand }}</span>
              <span class="text-xs text-slate-500 ml-1">/ Min: {{ part.reorder_level }}</span>
            </div>
            <div>
              <span class="text-[10px] text-slate-400 font-bold uppercase block mb-1">Unit Cost & Supplier</span>
              <span class="font-bold text-slate-700 dark:text-slate-300">${{ part.unit_cost }}</span>
              <span class="text-xs text-slate-500 block mt-0.5 truncate">{{ part.supplier || 'Unknown Supplier' }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Add/Edit Modal -->
      <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl max-w-lg w-full p-6">
          <h3 class="text-xl font-heading font-black text-slate-900 dark:text-white uppercase tracking-tight mb-1">
            {{ isEditMode ? 'Edit Spare Part' : 'Add Spare Part' }}
          </h3>
          <p class="text-xs text-slate-500 dark:text-slate-400 font-mono mb-6">
            {{ isEditMode ? 'Update spare part details' : 'Register a new spare part to a vessel' }}
          </p>

          <form @submit.prevent="submitForm" class="space-y-4 font-mono text-xs">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Part Number *</label>
                <input
                  v-model="formData.part_number"
                  type="text"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)]"
                  :disabled="isEditMode"
                  required
                />
              </div>
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Part Name *</label>
                <input
                  v-model="formData.part_name"
                  type="text"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)]"
                  required
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Quantity *</label>
                <input
                  v-model.number="formData.quantity_on_hand"
                  type="number"
                  min="0"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none"
                  required
                />
              </div>
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Reorder Level *</label>
                <input
                  v-model.number="formData.reorder_level"
                  type="number"
                  min="0"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none"
                  required
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Supplier</label>
                <input
                  v-model="formData.supplier"
                  type="text"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none"
                />
              </div>
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Unit Cost ($)</label>
                <input
                  v-model.number="formData.unit_cost"
                  type="number"
                  step="0.01"
                  min="0"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none"
                />
              </div>
            </div>

            <div class="flex justify-end gap-3 pt-4 border-t border-slate-100 dark:border-slate-800">
              <Button type="button" variant="outline" @click="closeModal" class="font-bold">
                Cancel
              </Button>
              <Button type="submit" class="bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white font-bold">
                {{ isEditMode ? 'Save Changes' : 'Add Part' }}
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { RefreshCw, Plus, Edit, Trash2 } from '@lucide/vue'
import { authState, getAccessToken } from '@/store/auth'
import { toast } from 'vue-sonner'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1'

const isLoading = ref(false)
const spareparts = ref([])
const showModal = ref(false)
const isEditMode = ref(false)
const editingPartId = ref(null)

const formData = ref({
  part_name: '',
  part_number: '',
  quantity_on_hand: 0,
  reorder_level: 5,
  supplier: '',
  unit_cost: 0
})

const fetchSpareParts = async () => {
  isLoading.value = true
  try {
    const params = new URLSearchParams()
    if (authState.selectedVessel) {
      params.append('vessel_id', authState.selectedVessel.asset_id)
    }
    const queryString = params.toString() ? `?${params.toString()}` : ''
    const response = await fetch(`${API_BASE_URL}/asset/spareparts/${queryString}`, {
      headers: {
        'Authorization': `Bearer ${getAccessToken()}`
      }
    })
    if (response.ok) {
      spareparts.value = await response.json()
    } else {
      console.error('Failed to fetch spare parts')
      toast.error("Failed", { description: "Failed to fetch spare parts data." })
    }
  } catch (error) {
    console.error('Error fetching data:', error)
    toast.error("Error", { description: "Server connection failed." })
  } finally {
    isLoading.value = false
  }
}

const openAddModal = () => {
  isEditMode.value = false
  editingPartId.value = null
  formData.value = {
    part_name: '',
    part_number: '',
    quantity_on_hand: 0,
    reorder_level: 5,
    supplier: '',
    unit_cost: 0
  }
  showModal.value = true
}

const openEditModal = (part) => {
  isEditMode.value = true
  editingPartId.value = part.id
  formData.value = {
    part_name: part.part_name,
    part_number: part.part_number,
    quantity_on_hand: part.quantity_on_hand,
    reorder_level: part.reorder_level,
    supplier: part.supplier || '',
    unit_cost: part.unit_cost
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

    if (!payload.vessel && !isEditMode.value) {
      toast.error("Error", { description: "Please select a vessel in the Topbar first." })
      return
    }

    const url = isEditMode.value
      ? `${API_BASE_URL}/asset/spareparts/${editingPartId.value}/`
      : `${API_BASE_URL}/asset/spareparts/`

    const response = await fetch(url, {
      method: isEditMode.value ? 'PUT' : 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getAccessToken()}`
      },
      body: JSON.stringify(payload)
    })

    if (response.ok) {
      toast.success("Success", { description: `Spare part ${isEditMode.value ? 'updated' : 'added'} successfully.` })
      showModal.value = false
      fetchSpareParts()
    } else {
      const errorData = await response.json()
      console.error("Error saving spare part:", errorData)
      toast.error("Failed", { description: "Failed to save spare part." })
    }
  } catch (error) {
    console.error("Error submitting form:", error)
    toast.error("Error", { description: "Connection failed." })
  }
}

const deletePart = async (id) => {
  if (!confirm(`Are you sure you want to delete this spare part?`)) return
  try {
    const response = await fetch(`${API_BASE_URL}/asset/spareparts/${id}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${getAccessToken()}`
      }
    })

    if (response.ok) {
      toast.success("Deleted", { description: "Spare part deleted successfully." })
      fetchSpareParts()
    } else {
      toast.error("Failed", { description: "Failed to delete spare part." })
    }
  } catch (error) {
    console.error("Error deleting part:", error)
    toast.error("Error", { description: "Connection failed." })
  }
}

onMounted(() => {
  fetchSpareParts()
})
</script>
