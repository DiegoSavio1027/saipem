<template>
  <DashboardLayout>
    <div class="p-8">
      <!-- Header -->
      <div class="flex justify-between items-start mb-8">
        <div>
          <h2 class="text-3xl font-bold text-slate-900 dark:text-white">Deck Management</h2>
          <p class="text-sm text-slate-600 dark:text-slate-400 mt-1">Create and manage deck locations independently</p>
        </div>
        <button @click="openAddModal" class="bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white font-bold px-6 py-3 rounded-lg transition shadow-lg flex items-center gap-2">
          <Plus class="w-5 h-5" />
          Add New Deck
        </button>
      </div>

      <!-- Decks Table -->
      <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg shadow-sm overflow-hidden">
        <table class="w-full">
          <thead class="bg-slate-50 dark:bg-slate-900 border-b border-slate-200 dark:border-slate-700">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase">Deck Name</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase">Risk Level</th>
              <th class="px-6 py-3 text-center text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase">Action</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-200 dark:divide-slate-700">
            <tr v-if="loading" class="hover:bg-slate-50 dark:hover:bg-slate-700/50">
              <td colspan="3" class="px-6 py-8 text-center">
                <Loader class="w-8 h-8 animate-spin text-[var(--color-saipem-tertiary)] mx-auto" />
                <p class="text-sm text-slate-600 dark:text-slate-400 mt-2">Loading decks...</p>
              </td>
            </tr>
            <tr v-else-if="decks.length === 0" class="hover:bg-slate-50 dark:hover:bg-slate-700/50">
              <td colspan="3" class="px-6 py-8 text-center text-slate-600 dark:text-slate-400">
                No decks found. Create your first deck!
              </td>
            </tr>
            <tr v-for="deck in decks" :key="deck.id" class="hover:bg-slate-50 dark:hover:bg-slate-700/50 transition">
              <td class="px-6 py-4 text-sm font-semibold text-slate-900 dark:text-white">{{ deck.deck_name }}</td>
              <td class="px-6 py-4 text-sm">
                <span :class="['px-3 py-1 rounded-full text-xs font-semibold', getRiskLevelClass(deck.risk_level)]">
                  {{ deck.risk_level }}
                </span>
              </td>
              <td class="px-6 py-4 text-center">
                <button @click="deleteDeck(deck.id)" class="text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 text-sm font-semibold flex items-center gap-1 mx-auto">
                  <Trash2 class="w-4 h-4" />Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Add/Edit Modal -->
      <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg shadow-lg max-w-md w-full p-6">
          <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-1">{{ isEditMode ? 'Edit Deck' : 'Add New Deck' }}</h3>
          <p class="text-sm text-slate-600 dark:text-slate-400 mb-6">Create a new deck location</p>

          <form @submit.prevent="submitForm" class="space-y-4">
            <div>
              <label class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1 block">Deck Name</label>
              <input
                v-model="formData.deck_name"
                type="text"
                placeholder="e.g., Main Deck"
                class="w-full px-4 py-2 border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[var(--color-saipem-tertiary)]"
                required
              >
            </div>

            <div>
              <label class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1 block">Risk Level</label>
              <Select v-model="formData.risk_level">
                <SelectTrigger class="w-full">
                  <SelectValue placeholder="Select risk level" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="LOW">Low</SelectItem>
                  <SelectItem value="MEDIUM">Medium</SelectItem>
                  <SelectItem value="HIGH">High</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div class="flex gap-3 pt-4">
              <button type="button" @click="closeModal" class="flex-1 px-4 py-2 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white hover:bg-slate-50 dark:hover:bg-slate-700 transition">
                Cancel
              </button>
              <button type="submit" class="flex-1 px-4 py-2 bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white rounded-lg font-semibold transition">
                {{ isEditMode ? 'Update' : 'Add Deck' }}
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
import { authState, getAccessToken } from '@/store/auth'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { Plus, Loader, Trash2 } from '@lucide/vue'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1'

// State
const decks = ref([])
const loading = ref(false)
const showModal = ref(false)
const isEditMode = ref(false)

const formData = ref({
  deck_name: '',
  risk_level: 'MEDIUM'
})

const getRiskLevelClass = (riskLevel) => {
  const classes = {
    'LOW': 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400',
    'MEDIUM': 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-400',
    'HIGH': 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-400'
  }
  return classes[riskLevel] || classes['MEDIUM']
}

// Fetch decks
const fetchDecks = async () => {
  loading.value = true
  try {
    let url = `${API_BASE_URL}/offshore/locations/`
    if (authState.selectedVessel) {
        url += `?vessel_id=${authState.selectedVessel.id}`
    }
    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${getAccessToken()}`
      }
    })
    if (response.ok) {
      decks.value = await response.json()
    }
  } catch (error) {
    console.error('Error fetching decks:', error)
  } finally {
    loading.value = false
  }
}

// Open add modal
const openAddModal = () => {
  isEditMode.value = false
  formData.value = {
    deck_name: '',
    risk_level: 'MEDIUM'
  }
  showModal.value = true
}

// Close modal
const closeModal = () => {
  showModal.value = false
}

// Submit form
const submitForm = async () => {
  if (!formData.value.deck_name.trim()) {
    alert('Deck name is required')
    return
  }

  try {
    const response = await fetch(`${API_BASE_URL}/offshore/locations/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getAccessToken()}`
      },
      body: JSON.stringify({
        deck_name: formData.value.deck_name.trim(),
        risk_level: formData.value.risk_level
      })
    })

    if (response.ok) {
      const result = await response.json()
      alert(`Deck "${result.deck_name}" created successfully!`)
      formData.value = {
        deck_name: '',
        risk_level: 'MEDIUM'
      }
      closeModal()
      fetchDecks()
    } else {
      const error = await response.json()
      console.error('Error submitting form:', error)
      alert(`Failed to save deck: ${JSON.stringify(error)}`)
    }
  } catch (error) {
    console.error('Error submitting form:', error)
    alert('Network error occurred.')
  }
}

// Delete deck
const deleteDeck = async (deckId) => {
  if (!confirm('Are you sure you want to delete this deck?')) return

  try {
    const response = await fetch(`${API_BASE_URL}/offshore/locations/${deckId}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${getAccessToken()}`
      }
    })

    if (response.ok) {
      fetchDecks()
    }
  } catch (error) {
    console.error('Error deleting deck:', error)
  }
}

// Lifecycle
onMounted(() => {
  fetchDecks()
})
</script>
