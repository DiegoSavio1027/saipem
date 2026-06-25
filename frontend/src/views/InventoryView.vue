<template>
  <DashboardLayout>
    <div class="p-8 space-y-8">
      <!-- Header -->
      <div class="flex justify-between items-center">
        <div>
          <h2 class="text-3xl font-heading font-black text-slate-900 dark:text-white tracking-tight uppercase">Inventory Management</h2>
          <p class="text-sm text-slate-500 dark:text-slate-400 mt-1 font-mono">Monitor stock levels and manage asset inventory</p>
        </div>
        <div class="flex gap-2">
          <Button @click="fetchInventory" variant="outline" class="flex items-center gap-2">
            <RefreshCw :class="['w-4 h-4', isLoading ? 'animate-spin' : '']" /> Refresh
          </Button>
          <Button v-if="authState.userRole === 'Admin' || authState.userRole === 'Chief Engineer'" @click="openAddModal" class="bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white font-bold flex items-center gap-2">
            <Plus class="w-4 h-4" /> Add Item
          </Button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="p-12 flex justify-center items-center bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800">
        <p class="text-slate-500 animate-pulse font-mono tracking-widest text-xs uppercase">Fetching inventory data...</p>
      </div>

      <!-- Inventory Table -->
      <div v-else class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 overflow-hidden shadow-sm">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-sm whitespace-nowrap">
            <thead class="bg-slate-50 dark:bg-slate-800/50 text-slate-500 dark:text-slate-400 font-mono text-xs uppercase tracking-wider">
              <tr>
                <th class="px-6 py-4 font-bold border-b border-slate-200 dark:border-slate-700">Item Code</th>
                <th class="px-6 py-4 font-bold border-b border-slate-200 dark:border-slate-700">Item Name</th>
                <th class="px-6 py-4 font-bold border-b border-slate-200 dark:border-slate-700">Category</th>
                <th class="px-6 py-4 font-bold border-b border-slate-200 dark:border-slate-700">Vessel</th>
                <th class="px-6 py-4 font-bold border-b border-slate-200 dark:border-slate-700 text-center">Current Stock</th>
                <th class="px-6 py-4 font-bold border-b border-slate-200 dark:border-slate-700 text-center">Reserved</th>
                <th class="px-6 py-4 font-bold border-b border-slate-200 dark:border-slate-700 text-center">Unit Cost ($)</th>
                <th class="px-6 py-4 font-bold border-b border-slate-200 dark:border-slate-700 text-center">Status</th>
                <th v-if="authState.userRole === 'Admin' || authState.userRole === 'Chief Engineer'" class="px-6 py-4 font-bold border-b border-slate-200 dark:border-slate-700 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
              <tr v-if="inventory.length === 0">
                <td colspan="6" class="px-6 py-8 text-center text-slate-500 font-mono text-xs">No inventory items found.</td>
              </tr>
              <tr v-for="item in inventory" :key="item.item_code" class="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
                <td class="px-6 py-4 font-mono text-slate-900 dark:text-slate-100 font-bold">{{ item.item_code }}</td>
                <td class="px-6 py-4 text-slate-700 dark:text-slate-300">{{ item.item_name }}</td>
                <td class="px-6 py-4 text-slate-500">{{ item.category }}</td>
                <td class="px-6 py-4 text-slate-700 dark:text-slate-300">{{ item.vessel_name || '-' }}</td>
                <td class="px-6 py-4 text-center">
                  <span class="font-mono text-lg font-bold" :class="item.current_stock <= item.minimum_stock ? 'text-red-500' : 'text-slate-700 dark:text-slate-300'">
                    {{ item.current_stock }}
                  </span>
                  <span class="text-[10px] text-slate-400 block font-mono">Min: {{ item.minimum_stock }}</span>
                </td>
                <td class="px-6 py-4 text-center">
                  <span class="font-mono text-lg text-slate-700 dark:text-slate-300 font-bold">
                    {{ item.quantity_reserved }}
                  </span>
                </td>
                <td class="px-6 py-4 text-center text-slate-700 dark:text-slate-300">
                  {{ item.unit_cost }}
                </td>
                <td class="px-6 py-4 text-center">
                  <Badge :variant="item.current_stock <= item.minimum_stock ? 'destructive' : 'secondary'" class="text-[10px] font-black uppercase tracking-wider font-mono">
                    {{ item.current_stock <= item.minimum_stock ? 'Low Stock' : 'Optimal' }}
                  </Badge>
                </td>
                <td v-if="authState.userRole === 'Admin' || authState.userRole === 'Chief Engineer'" class="px-6 py-4 text-right">
                  <div class="flex justify-end gap-2">
                    <button @click="openEditModal(item)" class="text-blue-500 hover:text-blue-700 p-1.5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded transition shadow-sm" title="Edit Item">
                      <Edit class="w-4 h-4" />
                    </button>
                    <button @click="deleteItem(item.item_code)" class="text-red-500 hover:text-red-700 p-1.5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded transition shadow-sm" title="Delete Item">
                      <Trash2 class="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Add/Edit Modal -->
      <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl max-w-lg w-full p-6">
          <h3 class="text-xl font-heading font-black text-slate-900 dark:text-white uppercase tracking-tight mb-1">
            {{ isEditMode ? 'Edit Inventory Item' : 'Add Inventory Item' }}
          </h3>
          <p class="text-xs text-slate-500 dark:text-slate-400 font-mono mb-6">
            {{ isEditMode ? 'Update details and stock levels for this item' : 'Register a new item to the general inventory' }}
          </p>

          <form @submit.prevent="submitForm" class="space-y-4 font-mono text-xs">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Item Code *</label>
                <input
                  v-model="formData.item_code"
                  type="text"
                  placeholder="e.g. INV-001"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)]"
                  :disabled="isEditMode"
                  required
                />
              </div>
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Category *</label>
                <select v-model="selectedCategory" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)]" required>
                  <option value="Spare Part">Spare Part</option>
                  <option value="Consumable">Consumable</option>
                  <option value="Equipment">Equipment</option>
                  <option value="PPE">PPE</option>
                  <option value="Others">Others (Manual Entry)</option>
                </select>
                <input
                  v-if="selectedCategory === 'Others'"
                  v-model="customCategory"
                  type="text"
                  placeholder="Enter custom category"
                  class="w-full px-3 py-2 mt-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)]"
                  required
                />
              </div>
            </div>

            <div>
              <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Item Name *</label>
              <input
                v-model="formData.item_name"
                type="text"
                placeholder="e.g. Safety Gloves XL"
                class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)]"
                required
              />
            </div>

            <div>
              <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Vessel Assignment *</label>
              <select v-model="formData.vessel" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)]" required :disabled="!!authState.assignedVessel">
                <option value="" disabled>Select Vessel</option>
                <option v-for="v in vessels" :key="v.asset_id || v.vessel_id" :value="v.asset_id || v.vessel_id">{{ v.name || v.vessel_name }}</option>
              </select>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Current Stock *</label>
                <input
                  v-model.number="formData.current_stock"
                  type="number"
                  min="0"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none"
                  required
                />
              </div>
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Minimum Stock *</label>
                <input
                  v-model.number="formData.minimum_stock"
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
                  placeholder="e.g. Acme Corp"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)]"
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
                {{ isEditMode ? 'Save Changes' : 'Add Item' }}
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
const inventory = ref([])
const vessels = ref([])
const showModal = ref(false)
const isEditMode = ref(false)

const predefinedCategories = ['Spare Part', 'Consumable', 'Equipment', 'PPE']
const selectedCategory = ref('Spare Part')
const customCategory = ref('')

const formData = ref({
  item_code: '',
  item_name: '',
  category: 'Spare Part',
  vessel: '',
  current_stock: 0,
  minimum_stock: 10,
  supplier: '',
  unit_cost: 0.00
})

const fetchVessels = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/offshore/vessels/`, {
      headers: { 'Authorization': `Bearer ${getAccessToken()}` }
    })
    if (response.ok) {
      vessels.value = await response.json()
    }
  } catch (error) {
    console.error('Error fetching vessels:', error)
  }
}

const fetchInventory = async () => {
  isLoading.value = true
  try {
    let url = `${API_BASE_URL}/asset/inventory/`
    if (authState.selectedVessel) {
      url += `?vessel_id=${authState.selectedVessel.asset_id}`
    }
    
    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${getAccessToken()}`
      }
    })
    if (response.ok) {
      inventory.value = await response.json()
    } else {
      console.error('Failed to fetch inventory')
      toast.error("Failed", { description: "Failed to fetch inventory data." })
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
  selectedCategory.value = 'Consumable'
  customCategory.value = ''
  formData.value = {
    item_code: '',
    item_name: '',
    category: 'Consumable',
    vessel: authState.assignedVessel ? authState.assignedVessel.asset_id : (authState.selectedVessel ? authState.selectedVessel.asset_id : ''),
    current_stock: 0,
    minimum_stock: 10,
    supplier: '',
    unit_cost: 0.00
  }
  showModal.value = true
}

const openEditModal = (item) => {
  isEditMode.value = true
  if (predefinedCategories.includes(item.category)) {
    selectedCategory.value = item.category
    customCategory.value = ''
  } else {
    selectedCategory.value = 'Others'
    customCategory.value = item.category || ''
  }
  
  formData.value = {
    item_code: item.item_code,
    item_name: item.item_name,
    category: item.category,
    vessel: item.vessel || '',
    current_stock: item.current_stock,
    minimum_stock: item.minimum_stock,
    supplier: item.supplier || '',
    unit_cost: item.unit_cost || 0.00
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const submitForm = async () => {
  try {
    formData.value.category = selectedCategory.value === 'Others' ? customCategory.value : selectedCategory.value
    
    const url = isEditMode.value
      ? `${API_BASE_URL}/asset/inventory/${formData.value.item_code}/`
      : `${API_BASE_URL}/asset/inventory/`

    const response = await fetch(url, {
      method: isEditMode.value ? 'PUT' : 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getAccessToken()}`
      },
      body: JSON.stringify(formData.value)
    })

    if (response.ok) {
      toast.success("Success", { description: `Item ${isEditMode.value ? 'updated' : 'added'} successfully.` })
      showModal.value = false
      fetchInventory()
    } else {
      toast.error("Failed", { description: "Failed to save item." })
    }
  } catch (error) {
    console.error("Error submitting form:", error)
    toast.error("Error", { description: "Connection failed." })
  }
}

const deleteItem = async (itemCode) => {
  if (!confirm(`Are you sure you want to delete item ${itemCode}?`)) return
  try {
    const response = await fetch(`${API_BASE_URL}/asset/inventory/${itemCode}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${getAccessToken()}`
      }
    })

    if (response.ok) {
      toast.success("Deleted", { description: "Item deleted successfully." })
      fetchInventory()
    } else {
      toast.error("Failed", { description: "Failed to delete item." })
    }
  } catch (error) {
    console.error("Error deleting item:", error)
    toast.error("Error", { description: "Connection failed." })
  }
}

onMounted(() => {
  fetchVessels()
  fetchInventory()
})
</script>
