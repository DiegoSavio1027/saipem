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
                <th scope="col" class="px-6 py-3">Assigned To</th>
                <th scope="col" class="px-6 py-3">Vessel</th>
                <th scope="col" class="px-6 py-3">Target Asset/Machine</th>
                <th scope="col" class="px-6 py-3">Priority</th>
                <th scope="col" class="px-6 py-3">Status</th>
                <th scope="col" class="px-6 py-3">Scheduled</th>
                <th scope="col" class="px-6 py-3">Actions</th>
              </tr>
            </thead>
            <tbody class="text-xs">
              <tr v-if="paginatedWorkOrders.length === 0" class="border-b dark:border-slate-700">
                <td colspan="8" class="px-6 py-8 text-center text-slate-500">No Work Orders found.</td>
              </tr>
              <tr v-for="wo in paginatedWorkOrders" :key="wo.wo_id" class="border-b dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-850 transition">
                <td class="px-6 py-4 font-bold text-slate-900 dark:text-white">{{ wo.wo_id }}</td>
                <td class="px-6 py-4 font-sans text-slate-700 dark:text-slate-300">{{ truncate(wo.description) }}</td>
                <td class="px-6 py-4 font-bold text-[var(--color-saipem-tertiary)]">{{ wo.assigned_to_name || 'Unassigned' }}</td>
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
                <td class="px-6 py-4 flex gap-2 items-center">
                  <!-- Complete WO: Chief Engineer finalizes work, triggers inventory deduction -->
                  <button
                    v-if="(authState.userRole === 'Admin' || authState.userRole === 'Chief Engineer') && wo.status === 'WAITING_REVIEW'"
                    @click="completeWorkOrder(wo.wo_id)"
                    class="flex items-center gap-1 px-2 py-1 bg-green-600 hover:bg-green-700 text-white text-[10px] font-black uppercase tracking-wider rounded transition"
                    title="Verify & Complete Work Order — deducts inventory"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                    Complete WO
                  </button>
                  <button v-if="authState.userRole === 'Admin' || authState.userRole === 'Chief Engineer'" @click="openEditModal(wo)" class="text-blue-500 hover:text-blue-700 p-1 border border-transparent hover:border-blue-200 hover:bg-blue-50/20 rounded transition" title="Edit Work Order">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/><path d="m15 5 4 4"/></svg>
                  </button>
                  <button v-if="authState.userRole === 'Admin' || authState.userRole === 'Chief Engineer'" @click="deleteWo(wo.wo_id)" class="text-red-500 hover:text-red-700 p-1 border border-transparent hover:border-red-200 hover:bg-red-50/20 rounded transition" title="Delete Work Order">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination Footer -->
        <div class="flex items-center justify-between space-x-2 py-4 px-6 border-t border-slate-200 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-900/30">
          <div class="flex items-center space-x-2">
            <p class="text-xs font-medium text-slate-500 dark:text-slate-400 font-mono">Rows per page</p>
            <select v-model="pageSize" class="h-8 w-[70px] rounded-md border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950 text-slate-900 dark:text-slate-100 text-xs px-2 focus:outline-none focus:border-[var(--color-saipem-tertiary)] font-mono">
              <option :value="5">5</option>
              <option :value="10">10</option>
              <option :value="20">20</option>
              <option :value="50">50</option>
            </select>
          </div>
          <div class="flex items-center space-x-6 lg:space-x-8 text-xs text-slate-500 dark:text-slate-400 font-mono">
            <div class="flex w-[100px] items-center justify-center font-medium">
              Page {{ currentPage }} of {{ totalPages }}
            </div>
            <div class="flex items-center space-x-2">
              <button
                @click="prevPage"
                :disabled="currentPage === 1"
                class="px-3 py-1.5 text-xs border border-slate-200 dark:border-slate-800 rounded bg-white dark:bg-slate-950 hover:bg-slate-50 dark:hover:bg-slate-900 transition disabled:opacity-50 disabled:cursor-not-allowed text-slate-700 dark:text-slate-300 font-bold"
              >
                Previous
              </button>
              <button
                @click="nextPage"
                :disabled="currentPage === totalPages"
                class="px-3 py-1.5 text-xs border border-slate-200 dark:border-slate-800 rounded bg-white dark:bg-slate-950 hover:bg-slate-50 dark:hover:bg-slate-900 transition disabled:opacity-50 disabled:cursor-not-allowed text-slate-700 dark:text-slate-300 font-bold"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- Create/Edit Work Order Modal -->
    <div v-if="showWoModal" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl max-w-lg w-full p-6 max-h-[95vh] overflow-y-auto font-mono text-xs animate-in fade-in duration-150">
        <h3 class="text-xl font-heading font-black text-slate-900 dark:text-white uppercase mb-1">{{ isEditMode ? 'Edit Work Order' : 'Create Work Order' }}</h3>
        <p class="text-xs text-slate-500 dark:text-slate-400 mb-6">{{ isEditMode ? 'Modify existing Work Order details' : 'Add a new Work Order to be used in PTW' }}</p>
        
        <form @submit.prevent="submitWo" class="space-y-4">
          <div>
            <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Work Order ID</label>
            <input v-model="woForm.wo_id" type="text" :placeholder="isEditMode ? '' : 'Auto-generated'" disabled
              class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)] disabled:opacity-60 disabled:cursor-not-allowed">
          </div>
          <div>
            <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Vessel *</label>
            <select v-model="woForm.vessel" required :disabled="!!authState.assignedVessel"
              class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)] disabled:opacity-60 disabled:cursor-not-allowed">
              <option value="" disabled>Select Vessel</option>
              <option v-for="v in vessels" :key="v.vessel_id" :value="v.vessel_id">{{ v.vessel_name }}</option>
            </select>
          </div>
          <div>
            <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Assign To (Lead Worker)</label>
            <select v-model="woForm.assigned_to" :disabled="!woForm.vessel || isFetchingEmployees"
              class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)] disabled:opacity-60 disabled:cursor-not-allowed">
              <option value="" disabled>{{ !woForm.vessel ? 'Select Vessel First' : (isFetchingEmployees ? 'Loading...' : 'Select Assignee') }}</option>
              <option v-for="emp in assignableWorkers" :key="emp.emp_id" :value="emp.emp_id">{{ emp.full_name }} ({{ emp.job_role }})</option>
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

          <div v-if="isEditMode">
            <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Status</label>
            <select v-model="woForm.status" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)]">
              <option value="PENDING">Pending</option>
              <option value="IN_PROGRESS">In Progress</option>
              <option value="WAITING_REVIEW">Waiting Review (CE Verification)</option>
              <option value="COMPLETED">Completed</option>
              <option value="CANCELLED">Cancelled</option>
            </select>
          </div>

          <!-- Materials Section -->
          <div class="mt-8 border-t border-slate-200 dark:border-slate-800 pt-6">
            <h4 class="text-sm font-bold text-slate-900 dark:text-white uppercase mb-4 flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-[var(--color-saipem-tertiary)]"><path d="M21.73 18l-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
              Materials Used
            </h4>
            
            <ul class="space-y-2 mb-4" v-if="woForm.materials && woForm.materials.length > 0">
              <li v-for="mat in woForm.materials" :key="mat.id" class="flex justify-between items-center p-3 bg-slate-50 dark:bg-slate-950 rounded-lg border border-slate-100 dark:border-slate-800">
                <div>
                  <p class="font-bold text-slate-800 dark:text-slate-200">{{ mat.part_name }}</p>
                  <p class="text-[10px] text-slate-500">P/N: {{ mat.part_number }} | Added: {{ new Date(mat.added_at).toLocaleDateString() }}</p>
                </div>
                <div class="px-3 py-1 bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400 rounded font-black text-xs border border-orange-200 dark:border-orange-800/50">
                  {{ mat.quantity_used }}x
                </div>
              </li>
            </ul>
            <div v-else class="text-center py-4 bg-slate-50 dark:bg-slate-950 rounded-lg mb-4 text-slate-500 border border-slate-200 dark:border-slate-800">
              No materials recorded yet.
            </div>

            <div class="grid grid-cols-12 gap-2 items-end bg-slate-50 dark:bg-slate-900 p-3 rounded-lg border border-slate-200 dark:border-slate-800">
              <div class="col-span-7">
                <label class="text-[10px] font-bold text-slate-500 uppercase block mb-1">Inventory Item</label>
                <select v-model="materialForm.spare_part_id" class="w-full px-2 py-1.5 bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded focus:outline-none focus:border-[var(--color-saipem-tertiary)]">
                  <option value="" disabled>Select Item</option>
                  <option v-for="sp in filteredInventoryItems" :key="sp.item_code" :value="sp.item_code" :disabled="sp.available_stock <= 0">
                    {{ sp.item_name }} (Avail: {{ sp.available_stock }}, Rsvd: {{ sp.quantity_reserved }})
                  </option>
                </select>
              </div>
              <div class="col-span-3">
                <label class="text-[10px] font-bold text-slate-500 uppercase block mb-1">Qty</label>
                <input v-model.number="materialForm.quantity_used" type="number" min="1" :max="filteredInventoryItems.find(i => i.item_code === materialForm.spare_part_id)?.available_stock || 1" @input="() => {
                    const maxStock = filteredInventoryItems.find(i => i.item_code === materialForm.spare_part_id)?.available_stock || 1;
                    if (materialForm.quantity_used > maxStock) materialForm.quantity_used = maxStock;
                    if (materialForm.quantity_used < 1) materialForm.quantity_used = 1;
                }" class="w-full px-2 py-1.5 bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded focus:outline-none focus:border-[var(--color-saipem-tertiary)]">
              </div>
              <div class="col-span-2">
                <button type="button" @click="addMaterialToWo" :disabled="isAddingMaterial || !materialForm.spare_part_id" class="w-full py-1.5 bg-slate-800 hover:bg-slate-700 disabled:opacity-50 text-white font-bold rounded transition text-xs flex justify-center items-center h-[34px]">
                  <span v-if="!isAddingMaterial">Add</span>
                  <svg v-else class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                </button>
              </div>
            </div>
          </div>
          
          <div class="flex gap-3 pt-4 border-t border-slate-150 dark:border-slate-850 mt-6">
            <button type="button" @click="showWoModal = false" class="flex-1 px-4 py-2 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-white hover:bg-slate-50 dark:hover:bg-slate-800 transition font-bold">
              Cancel
            </button>
            <button type="submit" class="flex-1 px-4 py-2 bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white rounded-lg font-bold transition">
              {{ isEditMode ? 'Save' : 'Create' }}
            </button>
          </div>
        </form>
      </div>
    </div>
    <!-- Confirmation Modal -->
    <div v-if="confirmState.isOpen" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl max-w-sm w-full p-6 animate-in fade-in zoom-in duration-200">
        <h3 class="text-xl font-heading font-black text-slate-900 dark:text-white uppercase mb-2">
          {{ confirmState.title }}
        </h3>
        <p class="text-sm text-slate-500 dark:text-slate-400 mb-6 font-mono leading-relaxed">
          {{ confirmState.message }}
        </p>
        <div class="flex gap-3 pt-4 border-t border-slate-150 dark:border-slate-850">
          <button type="button" @click="closeConfirmModal" class="flex-1 px-4 py-2 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-white hover:bg-slate-50 dark:hover:bg-slate-800 transition font-bold font-mono text-xs">
            Cancel
          </button>
          <button type="button" @click="executeConfirmAction" :class="[confirmState.action === 'delete' ? 'bg-red-500 hover:bg-red-600' : 'bg-green-600 hover:bg-green-700', 'flex-1 px-4 py-2 text-white rounded-lg font-bold transition font-mono text-xs']">
            Confirm
          </button>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { authState } from '@/store/auth'
import { toast } from 'vue-sonner'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1'

const isLoading = ref(false)
const workOrders = ref([])
const vessels = ref([])
const allAssets = ref([])
const allMachinery = ref([])
const allInventoryItems = ref([])
const vesselEmployees = ref([])
const isFetchingEmployees = ref(false)
const showWoModal = ref(false)
const isEditMode = ref(false)

const woForm = ref({
  wo_id: '',
  vessel: '',
  asset: '',
  machinery: '',
  description: '',
  priority: 'MEDIUM',
  scheduled_date: new Date().toISOString().split('T')[0],
  status: 'PENDING',
  assigned_to: '',
  created_by: authState.username || 'Admin',
  materials: []
})

const materialForm = ref({
  spare_part_id: '',
  quantity_used: 1
})
const isAddingMaterial = ref(false)

const filteredAssets = computed(() => {
  if (!woForm.value.vessel) return []
  return allAssets.value.filter(a => a.vessel === woForm.value.vessel || a.vessel_id === woForm.value.vessel)
})

const filteredMachinery = computed(() => {
  if (!woForm.value.vessel) return []
  let machinery = allMachinery.value.filter(m => m.vessel === woForm.value.vessel || m.vessel_id === woForm.value.vessel)
  
  // If an asset is selected, filter machinery to only those belonging to the selected asset
  if (woForm.value.asset) {
    machinery = machinery.filter(m => m.asset === woForm.value.asset || m.asset_id === woForm.value.asset)
  }
  
  return machinery
})

const assignableWorkers = computed(() => {
  return vesselEmployees.value.filter(emp => !['Chief Engineer', 'Safety Officer'].includes(emp.job_role))
})

const filteredInventoryItems = computed(() => {
  if (!woForm.value.vessel) return []
  return allInventoryItems.value.filter(i => {
    if (i.vessel === woForm.value.vessel || i.vessel_id === woForm.value.vessel) return true;
    
    // Also check if the item is linked to an asset that belongs to the selected vessel
    if (i.asset_location) {
      const asset = allAssets.value.find(a => a.asset_id === i.asset_location || a.id === i.asset_location);
      if (asset && (asset.vessel === woForm.value.vessel || asset.vessel_id === woForm.value.vessel)) {
        return true;
      }
    }
    return false;
  })
})

const fetchWorkOrders = async () => {
  isLoading.value = true
  try {
    const headers = { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
    let url = `${API_BASE_URL}/asset/workorders/`
    const params = new URLSearchParams()
    
    if (authState.userRole === 'Worker') {
      params.append('assigned_to', authState.empId)
    }
    
    if (authState.selectedVessel) {
      params.append('vessel_id', authState.selectedVessel.asset_id)
    }

    if (params.toString()) {
      url += `?${params.toString()}`
    }

    const woResponse = await fetch(url, { headers })
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
    const [assetRes, macRes, spareRes] = await Promise.all([
      fetch(`${API_BASE_URL}/asset/assets/`, { headers }),
      fetch(`${API_BASE_URL}/asset/machinery/`, { headers }),
      fetch(`${API_BASE_URL}/asset/inventory/`, { headers })
    ])
    if (assetRes.ok) allAssets.value = await assetRes.json()
    if (macRes.ok) allMachinery.value = await macRes.json()
    if (spareRes.ok) {
      const allItems = await spareRes.json()
      // Only show items that are 'Spare Part' or relevant for work orders
      allInventoryItems.value = allItems.filter(item => item.category !== 'General')
    }
  } catch (error) {
    console.error("Error fetching dependencies:", error)
  }
}

const fetchVesselEmployees = async (vesselId) => {
  if (!vesselId) {
    vesselEmployees.value = []
    return
  }
  isFetchingEmployees.value = true
  try {
    const headers = { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
    const response = await fetch(`${API_BASE_URL}/hse/employees/?vessel_id=${vesselId}`, { headers })
    if (response.ok) {
      vesselEmployees.value = await response.json()
      // Optional: Check if current assigned_to is still valid
      if (woForm.value.assigned_to && !vesselEmployees.value.some(e => e.emp_id === woForm.value.assigned_to)) {
          woForm.value.assigned_to = ''
      }
    }
  } catch (error) {
    console.error('Error fetching employees for vessel:', error)
  } finally {
    isFetchingEmployees.value = false
  }
}

watch(() => woForm.value.vessel, (newVessel) => {
  if (showWoModal.value) {
      fetchVesselEmployees(newVessel)
  }
  // Clear asset and machinery when vessel changes
  if (isEditMode.value === false) {
    woForm.value.asset = ''
    woForm.value.machinery = ''
  }
})

watch(() => woForm.value.asset, () => {
  // Clear selected machinery if it doesn't belong to the newly selected asset
  if (woForm.value.machinery) {
    const isValid = filteredMachinery.value.some(m => m.id === woForm.value.machinery)
    if (!isValid) {
      woForm.value.machinery = ''
    }
  }
})

const openWoModal = () => {
  isEditMode.value = false
  
  const initialVessel = authState.assignedVessel?.asset_id 
    || authState.selectedVessel?.asset_id 
    || authState.assignedVessel?.vessel_id 
    || authState.selectedVessel?.vessel_id 
    || vessels.value[0]?.vessel_id 
    || ''

  woForm.value = {
    wo_id: '',
    vessel: initialVessel,
    asset: '',
    machinery: '',
    description: '',
    priority: 'MEDIUM',
    scheduled_date: new Date().toISOString().split('T')[0],
    status: 'PENDING',
    assigned_to: '',
    created_by: authState.username || 'Admin',
    materials: []
  }
  showWoModal.value = true
  if (woForm.value.vessel) fetchVesselEmployees(woForm.value.vessel)
}

const openEditModal = (wo) => {
  isEditMode.value = true
  woForm.value = {
    wo_id: wo.wo_id,
    vessel: wo.vessel_id || wo.vessel || '',
    asset: wo.asset || '',
    machinery: wo.machinery || '',
    description: wo.description,
    priority: wo.priority,
    scheduled_date: wo.scheduled_date,
    status: wo.status,
    assigned_to: wo.assigned_to || '',
    created_by: wo.created_by || authState.username || 'Admin',
    materials: wo.materials || []
  }
  showWoModal.value = true
  if (woForm.value.vessel) fetchVesselEmployees(woForm.value.vessel)
}

const addMaterialToWo = async () => {
  if (!materialForm.value.spare_part_id) return
  
  if (!isEditMode.value) {
    // Local addition for new WO
    const sp = allInventoryItems.value.find(i => i.item_code === materialForm.value.spare_part_id);
    if (!sp) return;
    
    const qty = materialForm.value.quantity_used;
    if (qty > sp.available_stock) {
        toast.error(`Insufficient stock. Only ${sp.available_stock} available.`);
        return;
    }
    
    // Deduct locally for UI purposes (so they can't add more than available)
    sp.available_stock -= qty;
    
    woForm.value.materials.push({
      id: 'local-' + Date.now(),
      inventory_item: sp.item_code,
      part_name: sp.item_name,
      part_number: sp.item_code,
      quantity_used: qty,
      added_at: new Date().toISOString()
    });
    
    toast.success('Material added locally. Will be saved with Work Order.');
    materialForm.value = { spare_part_id: '', quantity_used: 1 }
    return;
  }

  isAddingMaterial.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/asset/workorders/${woForm.value.wo_id}/add_material/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify(materialForm.value)
    })
    
    if (response.ok) {
      const updatedWo = await response.json()
      woForm.value.materials = updatedWo.materials
      toast.success('Material added and stock deducted automatically!')
      materialForm.value = { spare_part_id: '', quantity_used: 1 }
      fetchWorkOrders() // update list in background
      // Refresh inventory items to show updated stock
      const spareRes = await fetch(`${API_BASE_URL}/asset/inventory/`, { headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` } })
      if (spareRes.ok) {
        const allItems = await spareRes.json()
        allInventoryItems.value = allItems.filter(item => item.category !== 'General')
      }
    } else {
      const err = await response.json()
      toast.error(err.error || 'Failed to add material')
    }
  } catch (error) {
    toast.error('Network error')
  } finally {
    isAddingMaterial.value = false
  }
}

const submitWo = async () => {
  try {
    const payload = {
      ...woForm.value,
      asset: woForm.value.asset || null,
      machinery: woForm.value.machinery || null
    }

    const url = isEditMode.value
      ? `${API_BASE_URL}/asset/workorders/${woForm.value.wo_id}/`
      : `${API_BASE_URL}/asset/workorders/`

    const method = isEditMode.value ? 'PUT' : 'POST'

    const response = await fetch(url, {
      method: method,
      headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify(payload)
    })
    
    if (response.ok) {
      const savedWo = await response.json()
      
      if (!isEditMode.value && woForm.value.materials.length > 0) {
          // Add local materials to the newly created WO
          for (const mat of woForm.value.materials) {
              await fetch(`${API_BASE_URL}/asset/workorders/${savedWo.wo_id}/add_material/`, {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                  },
                  body: JSON.stringify({
                      spare_part_id: mat.inventory_item,
                      quantity_used: mat.quantity_used
                  })
              });
          }
      }

      toast.success(isEditMode.value ? 'Work Order Updated Successfully' : 'Work Order Created Successfully')
      showWoModal.value = false
      fetchWorkOrders()
      // Refresh inventory
      fetchAssetsAndMachinery()
    } else {
      const err = await response.json()
      const msg = Object.values(err).flat()[0] || `Failed to ${isEditMode.value ? 'update' : 'create'} Work Order.`
      toast.error(`Failed to ${isEditMode.value ? 'update' : 'create'} Work Order`, { description: msg })
    }
  } catch (error) {
    toast.error('Network error')
  }
}

const confirmState = ref({
  isOpen: false,
  title: '',
  message: '',
  action: null,
  payload: null
})

const openConfirmModal = (title, message, action, payload) => {
  confirmState.value = {
    isOpen: true,
    title,
    message,
    action,
    payload
  }
}

const closeConfirmModal = () => {
  confirmState.value.isOpen = false
}

const executeConfirmAction = async () => {
  const { action, payload } = confirmState.value
  closeConfirmModal()
  if (action === 'delete') {
    await performDeleteWo(payload)
  } else if (action === 'complete') {
    await performCompleteWorkOrder(payload)
  }
}

const deleteWo = (id) => {
  openConfirmModal(
    'Delete Work Order',
    `Are you sure you want to delete Work Order ${id}?`,
    'delete',
    id
  )
}

const performDeleteWo = async (id) => {
  try {
    const response = await fetch(`${API_BASE_URL}/asset/workorders/${id}/`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
    })
    if (response.ok || response.status === 204) {
      toast.success('Work Order deleted')
      fetchWorkOrders()
    } else {
      const err = await response.json()
      toast.error('Failed to delete Work Order', { description: err.error || 'Unknown error' })
    }
  } catch (error) {
    toast.error('Network error deleting Work Order')
  }
}

const completeWorkOrder = (woId) => {
  openConfirmModal(
    'Complete Work Order',
    `Complete Work Order ${woId}? This will permanently deduct all reserved inventory materials (Current physical stock will be reduced).`,
    'complete',
    woId
  )
}

const performCompleteWorkOrder = async (woId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/asset/workorders/${woId}/complete/`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
    })
    if (response.ok) {
      const data = await response.json()
      const deducted = data.deducted_items?.map(i => `${i.item}: -${i.qty_deducted} (remaining: ${i.remaining_stock})`).join(', ') || 'No materials'
      toast.success(`WO ${woId} Completed!`, { description: `Inventory deducted: ${deducted}` })
      fetchWorkOrders()
      fetchAssetsAndMachinery()
    } else {
      const err = await response.json()
      toast.error('Failed to complete WO', { description: err.error || 'Unknown error' })
    }
  } catch (error) {
    toast.error('Network error completing WO')
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
    'WAITING_REVIEW': 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400',
    'COMPLETED': 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400',
    'CANCELLED': 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300',
  }
  return map[status] || 'bg-slate-100 text-slate-700'
}

// Pagination logic
const currentPage = ref(1)
const pageSize = ref(10)
const totalPages = computed(() => Math.ceil(workOrders.value.length / pageSize.value) || 1)

const paginatedWorkOrders = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return workOrders.value.slice(start, end)
})

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

watch([pageSize, workOrders], () => {
  if (currentPage.value > totalPages.value) {
    currentPage.value = totalPages.value
  }
  if (currentPage.value < 1) {
    currentPage.value = 1
  }
})

onMounted(() => {
  fetchWorkOrders()
  fetchVessels()
  fetchAssetsAndMachinery()
})
</script>
