<template>
  <DashboardLayout>
    <div class="p-8">
      <!-- Header -->
      <div class="flex justify-between items-start mb-8">
        <div>
          <h2 class="text-3xl font-bold text-slate-900 dark:text-white">Vessel Registry</h2>
          <p class="text-sm text-slate-600 dark:text-slate-400 mt-1">Master data management for vessels and rigs</p>
        </div>
        <button @click="openAddModal" class="bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white font-bold px-6 py-3 rounded-lg transition shadow-lg flex items-center gap-2">
          <Plus class="w-5 h-5" />
          Add New Vessel
        </button>
      </div>

      <!-- Vessels Table -->
      <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg shadow-sm overflow-hidden">
        <table class="w-full">
          <thead class="bg-slate-50 dark:bg-slate-900 border-b border-slate-200 dark:border-slate-700">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase">Asset ID</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase">Vessel Name</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase">Capacity</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase">Type</th>
              <th class="px-6 py-3 text-center text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase">Icon</th>
              <th class="px-6 py-3 text-center text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase">Status</th>
              <th class="px-6 py-3 text-center text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase">Action</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-200 dark:divide-slate-700">
            <tr v-if="loading" class="hover:bg-slate-50 dark:hover:bg-slate-700/50">
              <td colspan="7" class="px-6 py-8 text-center">
                <Loader class="w-8 h-8 animate-spin text-[var(--color-saipem-tertiary)] mx-auto" />
                <p class="text-sm text-slate-600 dark:text-slate-400 mt-2">Loading vessels...</p>
              </td>
            </tr>
            <tr v-else-if="vessels.length === 0" class="hover:bg-slate-50 dark:hover:bg-slate-700/50">
              <td colspan="7" class="px-6 py-8 text-center text-slate-600 dark:text-slate-400">
                No vessels found
              </td>
            </tr>
            <tr v-for="vessel in vessels" :key="vessel.vessel_id" class="hover:bg-slate-50 dark:hover:bg-slate-700/50 transition">
              <td class="px-6 py-4 text-sm font-mono text-[var(--color-saipem-tertiary)]">{{ vessel.vessel_id }}</td>
              <td class="px-6 py-4 text-sm font-semibold text-slate-900 dark:text-white">{{ vessel.vessel_name }}</td>
              <td class="px-6 py-4 text-sm text-slate-600 dark:text-slate-400">-</td>
              <td class="px-6 py-4 text-sm text-slate-600 dark:text-slate-400">{{ vessel.vessel_type || 'Vessel' }}</td>
              <td class="px-6 py-4 text-center">
                <component :is="getIconComponent(vessel.icon)" class="w-5 h-5 mx-auto text-[var(--color-saipem-tertiary)]" />
              </td>
              <td class="px-6 py-4 text-center">
                <span class="px-3 py-1 rounded-full text-xs font-semibold bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400">
                  Active
                </span>
              </td>
              <td class="px-6 py-4 text-center">
                <div class="flex items-center justify-center gap-2">
                  <button @click="openModal(vessel)" class="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 text-sm font-semibold flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                    Edit
                  </button>
                  <button @click="deleteVessel(vessel.vessel_id)" class="text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 text-sm font-semibold flex items-center gap-1">
                    <Trash2 class="w-4 h-4" />Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Add/Edit Modal -->
      <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg shadow-lg max-w-2xl w-full p-6 max-h-[90vh] overflow-y-auto">
          <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-1">{{ isEditMode ? 'Edit Vessel' : 'Add New Vessel' }}</h3>
          <p class="text-sm text-slate-600 dark:text-slate-400 mb-6">Master data vessel registration</p>

          <form @submit.prevent="submitForm" class="space-y-4">
            <div>
              <label class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1 block">Vessel ID (Auto-generated)</label>
              <input
                v-model="formData.vessel_id"
                type="text"
                class="w-full px-4 py-2 border border-slate-200 dark:border-slate-700 rounded-lg bg-slate-100 dark:bg-slate-900 text-slate-600 dark:text-slate-400 cursor-not-allowed"
                disabled
                readonly
              >
            </div>
            <div>
              <label class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1 block">Vessel Name</label>
              <input
                v-model="formData.vessel_name"
                type="text"
                placeholder="e.g., Saipem Constellation"
                class="w-full px-4 py-2 border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[var(--color-saipem-tertiary)]"
                required
              >
            </div>
            <div>
              <label class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1 block">Type</label>
              <Select v-model="formData.vessel_type">
                <SelectTrigger class="w-full">
                  <SelectValue placeholder="Select vessel type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Vessel">Vessel</SelectItem>
                  <SelectItem value="Drill Ship">Drill Ship</SelectItem>
                  <SelectItem value="Crane Vessel">Crane Vessel</SelectItem>
                  <SelectItem value="Jack-up Rig">Jack-up Rig</SelectItem>
                  <SelectItem value="Platform">Platform</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <label class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1 block">Select Vessel Icon</label>
              <div class="grid grid-cols-4 gap-2 mt-2">
                <button v-for="icon in vesselIcons" :key="icon.name" type="button" @click="formData.icon = icon.name" :class="['bg-slate-50 dark:bg-slate-800 border p-3 rounded-lg transition duration-150', formData.icon === icon.name ? 'border-[var(--color-saipem-tertiary)] text-[var(--color-saipem-tertiary)] shadow-lg' : 'border-slate-200 dark:border-slate-700 text-slate-400 dark:text-slate-600 hover:border-[var(--color-saipem-tertiary)]']">
                  <component :is="icon.component" class="w-5 h-5 mx-auto" />
                </button>
              </div>
            </div>

            <!-- Assign Decks Section -->
            <div class="border-t border-slate-200 dark:border-slate-700 pt-4">
              <label class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-2 block">Assign Decks <span class="text-red-500">*</span></label>
              <p class="text-xs text-slate-500 dark:text-slate-400 mb-3">Select at least one deck to assign to this vessel. <router-link to="/offshore/locations" class="text-[var(--color-saipem-tertiary)] hover:underline">Manage decks here</router-link>.</p>
              <div v-if="availableDecks.length === 0" class="p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg mb-3">
                <p class="text-sm text-yellow-800 dark:text-yellow-400">No decks available. Please <router-link to="/offshore/locations" class="font-semibold underline">create decks first</router-link> before adding a vessel.</p>
              </div>
              <div v-else class="space-y-2 max-h-48 overflow-y-auto">
                <label v-for="deck in availableDecks" :key="deck.id" class="flex items-center gap-3 p-2 hover:bg-slate-50 dark:hover:bg-slate-700/50 rounded cursor-pointer">
                  <input
                    type="checkbox"
                    v-model="formData.assigned_decks"
                    :value="deck.id"
                    class="w-4 h-4 rounded border-slate-300 text-[var(--color-saipem-tertiary)] focus:ring-[var(--color-saipem-tertiary)]"
                  />
                  <div class="flex-1">
                    <span class="text-sm font-medium text-slate-900 dark:text-white">{{ deck.deck_name }}</span>
                    <span class="text-xs text-slate-500 dark:text-slate-400 ml-2">(Risk: {{ deck.risk_level }})</span>
                  </div>
                </label>
              </div>
            </div>

            <div class="flex gap-3 pt-4">
              <button type="button" @click="closeModal" class="flex-1 px-4 py-2 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white hover:bg-slate-50 dark:hover:bg-slate-700 transition">
                Cancel
              </button>
              <button type="submit" class="flex-1 px-4 py-2 bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white rounded-lg font-semibold transition">
                {{ isEditMode ? 'Update' : 'Add Vessel' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { getAccessToken } from '@/store/auth'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { Plus, Loader, Trash2, Ship, Anchor, Radio, Zap, Settings, Flame, Satellite, Warehouse } from '@lucide/vue'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1'

// Default Decks (no longer used - decks are managed independently)
// Kept for reference only

// State
const vessels = ref([])
const loading = ref(false)
const showModal = ref(false)
const isEditMode = ref(false)
const availableDecks = ref([])

const formData = ref({
  vessel_id: '',
  vessel_name: '',
  vessel_type: 'Vessel',
  icon: 'Ship',
  assigned_decks: []
})

// Lucide icon options for vessels
const vesselIcons = [
  { name: 'Ship', component: Ship },
  { name: 'Anchor', component: Anchor },
  { name: 'Radio', component: Radio },
  { name: 'Zap', component: Zap },
  { name: 'Settings', component: Settings },
  { name: 'Flame', component: Flame },
  { name: 'Satellite', component: Satellite },
  { name: 'Warehouse', component: Warehouse }
]

// Icon mapping for backward compatibility
const iconMap = {
  'fa-ship': Ship,
  'fa-anchor': Anchor,
  'fa-tower-broadcast': Radio,
  'fa-oil-well': Zap,
  'fa-gear': Settings,
  'fa-bolt': Zap,
  'fa-fire': Flame,
  'fa-satellite-dish': Satellite,
  'fa-warehouse': Warehouse,
  'Ship': Ship,
  'Anchor': Anchor,
  'Radio': Radio,
  'Zap': Zap,
  'Settings': Settings,
  'Flame': Flame,
  'Satellite': Satellite,
  'Warehouse': Warehouse
}

const getIconComponent = (iconName) => {
  return iconMap[iconName] || Ship
}

// Fetch vessels
const fetchVessels = async () => {
  loading.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/offshore/vessels/`, {
      headers: {
        'Authorization': `Bearer ${getAccessToken()}`
      }
    })
    if (response.ok) {
      vessels.value = await response.json()
    }
  } catch (error) {
    console.error('Error fetching vessels:', error)
  } finally {
    loading.value = false
  }
}

// Fetch available deck locations (master data)
const fetchAvailableDecks = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/offshore/locations/`, {
      headers: {
        'Authorization': `Bearer ${getAccessToken()}`
      }
    })
    if (response.ok) {
      availableDecks.value = await response.json()
    }
  } catch (error) {
    console.error('Error fetching available decks:', error)
    availableDecks.value = []
  }
}

// Open add/edit modal
const openModal = (vessel = null) => {
  if (vessel) {
    isEditMode.value = true
    formData.value = {
      vessel_id: vessel.vessel_id,
      vessel_name: vessel.vessel_name,
      vessel_type: vessel.vessel_type,
      icon: vessel.icon || 'Ship',
      assigned_decks: vessel.assigned_decks?.map(d => d.id) || []
    }
  } else {
    isEditMode.value = false
    formData.value = {
      vessel_id: 'Auto-generated',
      vessel_name: '',
      vessel_type: 'Vessel',
      icon: 'Ship',
      assigned_decks: []
    }
  }
  showModal.value = true
}

// Alias for backward compatibility
const openAddModal = () => openModal(null)

// Close modal
const closeModal = () => {
  showModal.value = false
}

// Submit form
const submitForm = async () => {
  // Validate that at least one deck is assigned
  if (formData.value.assigned_decks.length === 0) {
    alert('Please assign at least one deck to this vessel. You can create decks in the Deck Management page.')
    return
  }

  try {
    // Create or update vessel
    const url = isEditMode.value
      ? `${API_BASE_URL}/offshore/vessels/${formData.value.vessel_id}/`
      : `${API_BASE_URL}/offshore/vessels/`

    const vesselPayload = {
      name: formData.value.vessel_name,
      type: formData.value.vessel_type,
      icon: formData.value.icon
    }

    const response = await fetch(url, {
      method: isEditMode.value ? 'PUT' : 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getAccessToken()}`
      },
      body: JSON.stringify(vesselPayload)
    })

    if (response.ok) {
      const vessel = await response.json()

      // Assign decks to vessel
      await fetch(`${API_BASE_URL}/offshore/vessels/${vessel.vessel_id}/assign-decks/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${getAccessToken()}`
        },
        body: JSON.stringify({ deck_ids: formData.value.assigned_decks })
      })

      closeModal()
      fetchVessels()
      alert(`Vessel "${vessel.vessel_name}" ${isEditMode.value ? 'updated' : 'created'} successfully with ${formData.value.assigned_decks.length} deck(s)!`)
    } else {
      const error = await response.text()
      console.error('Error submitting form:', error)
      alert('Failed to save vessel. Check console for details.')
    }
  } catch (error) {
    console.error('Error submitting form:', error)
    alert('Network error occurred.')
  }
}

// Delete vessel
const deleteVessel = async (vesselId) => {
  if (!confirm('Are you sure you want to delete this vessel?')) return

  try {
    const response = await fetch(`${API_BASE_URL}/offshore/vessels/${vesselId}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${getAccessToken()}`
      }
    })

    if (response.ok) {
      fetchVessels()
    }
  } catch (error) {
    console.error('Error deleting vessel:', error)
  }
}

// Lifecycle
onMounted(() => {
  fetchVessels()
  fetchAvailableDecks()
})
</script>
