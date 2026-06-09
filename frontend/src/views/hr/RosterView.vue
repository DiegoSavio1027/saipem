<template>
  <DashboardLayout>
    <div class="p-8">
      <!-- Toolbar -->
      <div class="space-y-4 mb-8">
        <button @click="openNewAddModal" class="w-full bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white font-black py-4 px-6 rounded-xl transition tracking-wider uppercase flex items-center justify-center gap-3">
          <Ship class="w-5 h-5" /> Deploy Crew to Vessel
        </button>

        <div class="pt-2">
          <h2 class="text-xs font-bold text-slate-500 dark:text-slate-600 uppercase tracking-widest mb-2">Deployed Crew</h2>
          <div class="relative mb-3">
            <Search class="absolute left-3.5 top-3.5 text-slate-400 dark:text-slate-600 w-4 h-4" />
            <input v-model="crewSearch" type="text" placeholder="Filter crew by name..." class="w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-slate-800 pl-9 pr-4 py-2.5 rounded-xl text-xs text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-600 focus:border-[var(--color-saipem-tertiary)] outline-none transition">
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="flex flex-col xl:flex-row justify-between items-center gap-4 mb-8 min-w-[800px]">
          <!-- Time Navigation -->
          <div class="flex items-center gap-3">
            <button @click="navigateTime(-1)" class="bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-white p-3 rounded-xl transition">
              <ChevronLeft class="w-5 h-5" />
            </button>
            <h2 class="text-xl font-black text-slate-900 dark:text-white tracking-tight w-64 text-center">{{ timeRangeLabel }}</h2>
            <button @click="navigateTime(1)" class="bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-white p-3 rounded-xl transition">
              <ChevronRight class="w-5 h-5" />
            </button>
          </div>

          <!-- Filters and View Modes -->
          <div class="flex items-center gap-4">
            <div class="bg-white dark:bg-slate-900 p-1.5 rounded-xl border border-slate-200 dark:border-slate-800 flex items-center">
              <span class="text-xs text-slate-500 dark:text-slate-600 font-bold uppercase tracking-wider px-3">Vessel Filter:</span>
              <select v-model="vesselFilter" @change="renderGrid" class="bg-slate-50 dark:bg-black border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-white text-xs py-2 px-4 rounded-lg font-bold uppercase focus:border-[var(--color-saipem-tertiary)] outline-none transition cursor-pointer">
                <option value="ALL">ALL VESSELS</option>
                <option v-for="asset in assets" :key="asset.asset_id" :value="asset.asset_id">{{ asset.name.toUpperCase() }}</option>
              </select>
            </div>

            <div class="bg-white dark:bg-slate-900 p-1.5 rounded-xl border border-slate-200 dark:border-slate-800 flex gap-1">
              <button @click="switchView('week')" :class="['px-5 py-2 rounded-lg text-sm font-bold uppercase tracking-wider transition', viewMode === 'week' ? 'bg-[var(--color-saipem-tertiary)] text-white' : 'text-slate-400 dark:text-slate-500 hover:text-slate-900 dark:hover:text-white']">Week</button>
              <button @click="switchView('month')" :class="['px-5 py-2 rounded-lg text-sm font-bold uppercase tracking-wider transition', viewMode === 'month' ? 'bg-[var(--color-saipem-tertiary)] text-white' : 'text-slate-400 dark:text-slate-500 hover:text-slate-900 dark:hover:text-white']">Month</button>
              <button @click="switchView('year')" :class="['px-5 py-2 rounded-lg text-sm font-bold uppercase tracking-wider transition', viewMode === 'year' ? 'bg-[var(--color-saipem-tertiary)] text-white' : 'text-slate-400 dark:text-slate-500 hover:text-slate-900 dark:hover:text-white']">Year</button>
            </div>
          </div>
        </div>

        <!-- Roster Grid -->
        <div :style="{ minWidth: tableMinWidth }" class="bg-white dark:bg-slate-900 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-800 overflow-hidden flex-1 transition-all duration-300">
          <table class="w-full border-collapse text-left table-fixed">
            <thead>
              <tr class="bg-slate-50 dark:bg-slate-950 border-b border-slate-200 dark:border-slate-800 text-slate-500 dark:text-slate-400 font-bold text-xs uppercase tracking-wider">
                <th class="p-4 w-64 border-r border-slate-200 dark:border-slate-800 text-slate-900 dark:text-white font-black">Asset Assignment</th>
                <th v-for="(unit, index) in timeUnits" :key="index" :class="['p-3 text-center border-r border-slate-200 dark:border-slate-800', viewMode === 'week' ? 'w-32' : '', 'font-mono']">
                  <div v-if="viewMode === 'week'" class="text-slate-900 dark:text-white font-bold">{{ formatDate(unit, 'short') }}</div>
                  <div v-if="viewMode === 'week'" class="text-xs text-slate-500 dark:text-slate-600 mt-0.5">{{ formatDate(unit, 'weekday') }}</div>
                  <div v-if="viewMode === 'month'" class="text-slate-900 dark:text-white font-bold">{{ unit.getDate() }}</div>
                  <div v-if="viewMode === 'month'" class="text-slate-600 dark:text-slate-700 text-xs font-normal">{{ formatDate(unit, 'narrow') }}</div>
                  <div v-if="viewMode === 'year'" class="text-slate-900 dark:text-white font-black">{{ formatMonth(unit.month) }}</div>
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-200 dark:divide-slate-800/60">
              <!-- Activity Row (only when vessel filter is active) -->
              <template v-if="vesselFilter !== 'ALL'">
                <tr class="bg-slate-50 dark:bg-slate-950/70 border-b-2 border-slate-200 dark:border-slate-800">
                  <td class="p-4 border-r border-slate-200 dark:border-slate-800 bg-slate-100 dark:bg-slate-950/90">
                    <div class="flex items-center gap-3">
                      <div class="bg-orange-50 dark:bg-orange-950/20 p-2.5 rounded-xl border border-orange-200 dark:border-orange-900/30">
                        <ListChecks class="text-[var(--color-saipem-tertiary)] w-4 h-4" />
                      </div>
                      <div>
                        <h4 class="font-black text-[var(--color-saipem-tertiary)] text-xs uppercase tracking-widest leading-tight">Vessel Activity</h4>
                        <p class="text-xs text-slate-500 dark:text-slate-600 font-mono mt-1">Operational Status</p>
                      </div>
                    </div>
                  </td>
                  <template v-for="(cell, index) in activityRow" :key="'activity-' + index">
                    <td v-if="cell.visible" :colspan="cell.colSpan" :class="['p-2 border-r border-slate-200 dark:border-slate-800 align-middle', cell.activity ? 'bg-slate-50 dark:bg-slate-950/20' : 'bg-slate-50 dark:bg-slate-950/20 hover:bg-slate-100 dark:hover:bg-slate-900/30 transition-all duration-150 cursor-pointer group']" @click="cell.activity ? null : openActivityModalWithDate(cell.date)">
                      <div v-if="cell.activity" @dblclick="deleteActivity(cell.activity.id)" :title="cell.activity.activity_name + ' (Double-click to delete)'" class="bg-slate-100 dark:bg-slate-900 border border-orange-300 dark:border-orange-500/30 hover:border-orange-400 dark:hover:border-orange-500 text-[var(--color-saipem-tertiary)] text-xs py-2.5 px-3 rounded-lg font-black flex items-center justify-center transition duration-200 my-1 mx-0.5 cursor-pointer select-none">
                        <AlertTriangle class="mr-1.5 animate-pulse text-orange-500 w-3 h-3" />
                        <span class="truncate uppercase tracking-wider">{{ cell.activity.activity_name }}</span>
                      </div>
                      <div v-else class="text-center text-slate-300 dark:text-slate-800" title="Click to log activity">
                        <Plus class="w-4 h-4 opacity-0 group-hover:opacity-100 group-hover:text-[var(--color-saipem-tertiary)] transition-all mx-auto" />
                      </div>
                    </td>
                  </template>
                </tr>
              </template>

              <!-- Asset Rows -->
              <tr v-for="asset in activeAssets" :key="asset.asset_id" class="hover:bg-slate-50 dark:hover:bg-slate-900/40 transition duration-200">
                <td class="p-4 border-r border-slate-200 dark:border-slate-800">
                  <div class="flex items-center gap-3">
                    <div class="bg-slate-50 dark:bg-black p-2.5 rounded-xl border border-slate-200 dark:border-slate-800">
                      <component :is="getIconComponent(asset.icon)" class="w-5 h-5 text-slate-700 dark:text-slate-300" />
                    </div>
                    <div>
                      <h4 class="font-bold text-slate-900 dark:text-white text-sm leading-tight">{{ asset.name }}</h4>
                      <p class="text-xs text-slate-500 dark:text-slate-600 font-mono mt-1">{{ asset.capacity }}</p>
                    </div>
                  </div>
                </td>
                <template v-for="(cell, index) in assetRows[asset.asset_id]" :key="'roster-' + asset.asset_id + '-' + index">
                  <td v-if="cell.visible" :colspan="cell.colSpan" :class="['p-2 border-r border-slate-200 dark:border-slate-800/60 align-middle', cell.assignment ? '' : 'text-center text-slate-300 dark:text-slate-800 hover:bg-slate-50 dark:hover:bg-slate-900/20 transition-all duration-150']">
                    <div v-if="cell.assignment" @dblclick="deleteAssignment(cell.assignment.id)" :title="cell.assignment.title + ' (Double-click to terminate)'" class="bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white text-xs py-2 px-3 rounded-lg font-black flex items-center justify-center transition duration-150 my-1 mx-0.5 cursor-pointer">
                      <Clock class="mr-1.5 w-3 h-3" />
                      <span @click.stop="showEmployeeDetailsByName(cell.assignment.title)" class="truncate uppercase tracking-wider hover:underline cursor-pointer">{{ cell.assignment.title }}</span>
                    </div>
                    <MoreHorizontal v-else class="w-4 h-4 opacity-20 mx-auto" />
                  </td>
                </template>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    <!-- Assign Modal -->
    <div v-if="showAssignModal" class="fixed inset-0 bg-black/90 backdrop-blur-md flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-8 rounded-2xl w-full max-w-md shadow-sm text-slate-900 dark:text-white">
        <h3 class="text-2xl font-black text-slate-900 dark:text-white mb-2 tracking-tight">Deploy Personnel</h3>
        <p class="text-xs text-slate-500 dark:text-slate-600 uppercase tracking-widest mb-6">Configure manual deployment duration</p>

        <form @submit.prevent="submitAssignment" class="space-y-5">
          <div>
            <label class="text-xs text-slate-600 dark:text-slate-400 uppercase font-bold tracking-wider">Select Crew Member</label>
            <select v-model="assignForm.employee" class="w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-slate-800 p-3.5 rounded-xl mt-1 text-slate-900 dark:text-white focus:border-[var(--color-saipem-tertiary)] outline-none transition" required>
              <option value="">-- Choose Crew --</option>
              <option v-for="emp in employees" :key="emp.emp_id" :value="emp.emp_id">{{ emp.full_name }}</option>
            </select>
          </div>

          <div>
            <label class="text-xs text-slate-600 dark:text-slate-400 uppercase font-bold tracking-wider">Select Vessel</label>
            <select v-model="assignForm.vessel" class="w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-slate-800 p-3.5 rounded-xl mt-1 text-slate-900 dark:text-white focus:border-[var(--color-saipem-tertiary)] outline-none transition" required>
              <option value="">-- Choose Vessel --</option>
              <option v-for="asset in assets" :key="asset.asset_id" :value="asset.asset_id">{{ asset.name }}</option>
            </select>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="text-xs text-slate-600 dark:text-slate-400 uppercase font-bold tracking-wider">Start Date</label>
              <input v-model="assignForm.start" type="date" class="w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-slate-800 p-3 rounded-xl mt-1 text-slate-900 dark:text-white focus:border-[var(--color-saipem-tertiary)] outline-none transition" required>
            </div>
            <div>
              <label class="text-xs text-slate-600 dark:text-slate-400 uppercase font-bold tracking-wider">End Date</label>
              <input v-model="assignForm.end" type="date" class="w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-slate-800 p-3 rounded-xl mt-1 text-slate-900 dark:text-white focus:border-[var(--color-saipem-tertiary)] outline-none transition" required>
            </div>
          </div>

          <div class="flex gap-3 pt-4">
            <button type="button" @click="showAssignModal = false" class="flex-1 bg-slate-200 dark:bg-slate-800 hover:bg-slate-300 dark:hover:bg-slate-700 p-3.5 rounded-xl font-bold transition text-slate-900 dark:text-white">Cancel</button>
            <button type="submit" class="flex-1 bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 p-3.5 rounded-xl font-black tracking-wider uppercase transition text-white">Confirm</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Activity Modal -->
    <div v-if="showActivityModal" class="fixed inset-0 bg-black/90 backdrop-blur-md flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-8 rounded-2xl w-full max-w-md shadow-sm text-slate-900 dark:text-white">
        <h3 class="text-2xl font-black text-slate-900 dark:text-white mb-2 tracking-tight">Log Vessel Activity</h3>
        <p class="text-xs text-slate-500 dark:text-slate-600 uppercase tracking-widest mb-6">Record scheduled logs</p>

        <form @submit.prevent="submitActivity" class="space-y-5">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="text-xs text-slate-600 dark:text-slate-400 uppercase font-bold tracking-wider">Start Date</label>
              <input v-model="activityForm.start" type="date" class="w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-slate-800 p-3 rounded-xl mt-1 text-slate-900 dark:text-white focus:border-[var(--color-saipem-tertiary)] outline-none transition" required>
            </div>
            <div>
              <label class="text-xs text-slate-600 dark:text-slate-400 uppercase font-bold tracking-wider">End Date</label>
              <input v-model="activityForm.end" type="date" class="w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-slate-800 p-3 rounded-xl mt-1 text-slate-900 dark:text-white focus:border-[var(--color-saipem-tertiary)] outline-none transition" required>
            </div>
          </div>
          <div>
            <label class="text-xs text-slate-600 dark:text-slate-400 uppercase font-bold tracking-wider">Activity Description</label>
            <input v-model="activityForm.activity_name" type="text" placeholder="ex: Safety Induction Training" class="w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-slate-800 p-3.5 rounded-xl mt-1 text-slate-900 dark:text-white focus:border-[var(--color-saipem-tertiary)] outline-none transition" required>
          </div>
          <div class="flex gap-3 pt-4">
            <button type="button" @click="showActivityModal = false" class="flex-1 bg-slate-200 dark:bg-slate-800 hover:bg-slate-300 dark:hover:bg-slate-700 p-3.5 rounded-xl font-bold transition text-slate-900 dark:text-white">Cancel</button>
            <button type="submit" class="flex-1 bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 p-3.5 rounded-xl font-black tracking-wider uppercase transition text-white">Add Log</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Detail Modal -->
    <div v-if="showDetailModal && selectedEmployee" class="fixed inset-0 bg-black/90 backdrop-blur-md flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-8 rounded-2xl w-full max-w-md shadow-sm text-slate-900 dark:text-white relative">
        <button @click="showDetailModal = false" class="absolute top-6 right-6 text-slate-500 dark:text-slate-600 hover:text-slate-900 dark:hover:text-white transition">
          <X class="w-5 h-5" />
        </button>

        <div class="flex items-center gap-4 mb-6">
          <div class="bg-orange-50 dark:bg-orange-950/30 p-4 rounded-2xl border border-orange-200 dark:border-orange-500/20 text-[var(--color-saipem-tertiary)]">
            <Shield class="w-8 h-8" />
          </div>
          <div>
            <h3 class="text-2xl font-black text-slate-900 dark:text-white leading-tight uppercase">{{ selectedEmployee.full_name }}</h3>
            <p class="text-xs text-[var(--color-saipem-tertiary)] font-mono tracking-widest mt-1">{{ selectedEmployee.emp_id }}</p>
          </div>
        </div>

        <div class="space-y-4 border-t border-slate-200 dark:border-slate-800 pt-5">
          <div class="grid grid-cols-2">
            <span class="text-xs text-slate-500 dark:text-slate-600 uppercase font-bold tracking-wider">Job Role</span>
            <span class="text-sm text-slate-900 dark:text-slate-200 font-semibold truncate">{{ selectedEmployee.job_role }}</span>
          </div>
          <div class="grid grid-cols-2">
            <span class="text-xs text-slate-500 dark:text-slate-600 uppercase font-bold tracking-wider">Email</span>
            <span class="text-sm text-slate-900 dark:text-slate-200 font-semibold truncate">{{ selectedEmployee.email }}</span>
          </div>
          <div class="grid grid-cols-2">
            <span class="text-xs text-slate-500 dark:text-slate-600 uppercase font-bold tracking-wider">MCU Status</span>
            <div>
              <span :class="['px-2.5 py-1 rounded-full text-xs font-black tracking-widest uppercase', getMCUBadgeClass(selectedEmployee.mcu_status)]">{{ selectedEmployee.mcu_status }}</span>
            </div>
          </div>
          <div class="grid grid-cols-2">
            <span class="text-xs text-slate-500 dark:text-slate-600 uppercase font-bold tracking-wider">MCU Expiry</span>
            <span class="text-sm text-orange-600 dark:text-orange-400 font-mono font-bold">{{ formatMCUExpiry(selectedEmployee.mcu_expiry) }}</span>
          </div>
        </div>

        <button @click="showDetailModal = false" class="w-full bg-slate-200 dark:bg-slate-800 hover:bg-slate-300 dark:hover:bg-slate-700 p-3.5 rounded-xl font-bold transition mt-8 text-slate-900 dark:text-white">Dismiss Profile</button>
      </div>
    </div>

    <!-- Confirm Modal -->
    <div v-if="showConfirmModal" class="fixed inset-0 bg-black/95 backdrop-blur-md flex items-center justify-center p-4 z-[110]">
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-8 rounded-2xl w-full max-w-sm shadow-sm text-slate-900 dark:text-white text-center">
        <div class="bg-orange-50 dark:bg-orange-950/20 w-16 h-16 rounded-full border border-orange-200 dark:border-orange-500/30 flex items-center justify-center mx-auto mb-4 text-[var(--color-saipem-tertiary)]">
          <AlertTriangle class="w-8 h-8 animate-pulse" />
        </div>
        <h3 class="text-xl font-black text-slate-900 dark:text-white mb-2 tracking-tight uppercase">System Confirmation</h3>
        <p class="text-xs text-slate-500 dark:text-slate-600 uppercase tracking-widest mb-6 leading-relaxed">{{ confirmMessage }}</p>
        <div class="flex gap-3">
          <button @click="confirmCallback = null; showConfirmModal = false" class="flex-1 bg-slate-200 dark:bg-slate-800 hover:bg-slate-300 dark:hover:bg-slate-700 p-3.5 rounded-xl font-bold transition text-slate-900 dark:text-white">Cancel</button>
          <button @click="executeConfirm" class="flex-1 bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 p-3.5 rounded-xl font-black tracking-wider uppercase transition text-white">Confirm</button>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { authState, getAccessToken } from '@/store/auth'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { Ship, Plus, Search, ChevronLeft, ChevronRight, ListChecks, AlertTriangle, Trash2, Clock, MoreHorizontal, X, Shield, Anchor, Radio, Zap, Flame, Satellite, Settings, Warehouse } from '@lucide/vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1'

// Font Awesome to Lucide icon mapping
const iconMap = {
  'fa-ship': Ship,
  'fa-anchor': Anchor,
  'fa-tower-broadcast': Radio,
  'fa-oil-well': Zap,
  'fa-helicopter': Ship,
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

// Data
const employees = ref([])
const rosters = ref([])
const assets = ref([])
const activities = ref([])
const toasts = ref([])
const timeUnits = ref([])
const activityRow = ref([])
const assetRows = ref({})

// UI State
const crewSearch = ref('')
const viewMode = ref('week')
const vesselFilter = ref('ALL')
const currentStartDate = ref(new Date())
const selectedEmployee = ref(null)
const confirmCallback = ref(null)
const confirmMessage = ref('')

// Modal States
const showAssignModal = ref(false)
const showAssetModal = ref(false)
const showActivityModal = ref(false)
const showDetailModal = ref(false)
const showConfirmModal = ref(false)

// Form Data
const assignForm = ref({ employee: '', vessel: '', start: '', end: '' })
const activityForm = ref({ start: '', end: '', activity_name: '' })

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

// Computed
const filteredEmployees = computed(() => {
  const query = crewSearch.value.toLowerCase()
  return employees.value.filter(emp => emp.full_name.toLowerCase().includes(query))
})

const activeAssets = computed(() => {
  return vesselFilter.value === 'ALL' ? assets.value : assets.value.filter(a => a.asset_id === vesselFilter.value)
})

const timeRangeLabel = computed(() => {
  if (timeUnits.value.length === 0) return 'Loading...'
  if (viewMode.value === 'week') {
    const start = timeUnits.value[0]
    const end = timeUnits.value[6]
    return `${start.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} - ${end.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`
  } else if (viewMode.value === 'month') {
    return currentStartDate.value.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
  } else {
    return `YEAR ${currentStartDate.value.getFullYear()}`
  }
})

const tableMinWidth = computed(() => {
  if (viewMode.value === 'week') return '1000px'
  if (viewMode.value === 'month') return '1800px'
  return '1200px'
})

// Methods
const formatDate = (date, format) => {
  if (format === 'short') return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  if (format === 'weekday') return date.toLocaleDateString('en-US', { weekday: 'short' })
  if (format === 'narrow') return date.toLocaleDateString('en-US', { weekday: 'narrow' })
  return date.toLocaleDateString()
}

const formatMonth = (monthIndex) => {
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  return months[monthIndex]
}

const formatMCUExpiry = (date) => {
  if (!date) return 'NO RECORD / N/A'
  return new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

const getMCUBadgeClass = (status) => {
  if (status === 'FIT') return 'bg-green-100 dark:bg-green-950/20 text-green-700 dark:text-green-400 border border-green-200 dark:border-green-500/20'
  if (status === 'UNFIT') return 'bg-red-100 dark:bg-red-950/20 text-red-700 dark:text-red-400 border border-red-200 dark:border-red-500/20'
  if (status === 'EXPIRED') return 'bg-amber-100 dark:bg-amber-950/20 text-amber-700 dark:text-amber-400 border border-amber-200 dark:border-amber-500/20'
  return 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-400 border border-slate-200 dark:border-slate-700'
}

const showToast = (type, title, message) => {
  const id = Date.now()
  let borderClass = '', iconClass = '', titleColor = ''

  if (type === 'error') {
    borderClass = 'border-red-600/50 shadow-[0_0_20px_rgba(239,68,68,0.1)]'
    iconClass = 'fa-solid fa-circle-xmark text-red-500 text-lg animate-bounce'
    titleColor = 'text-red-500'
  } else if (type === 'warning') {
    borderClass = 'border-amber-600/50 shadow-[0_0_20px_rgba(217,119,6,0.1)]'
    iconClass = 'fa-solid fa-triangle-exclamation text-amber-500 text-lg animate-pulse'
    titleColor = 'text-amber-500'
  } else {
    borderClass = 'border-emerald-600/50 shadow-[0_0_20px_rgba(16,185,129,0.1)]'
    iconClass = 'fa-solid fa-circle-check text-emerald-500 text-lg'
    titleColor = 'text-emerald-500'
  }

  toasts.value.push({ id, borderClass, iconClass, titleColor, title, message })
  setTimeout(() => removeToast(id), 5000)
}

const removeToast = (id) => {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

const showConfirm = (message, callback) => {
  confirmMessage.value = message.toUpperCase()
  confirmCallback.value = callback
  showConfirmModal.value = true
}

const executeConfirm = () => {
  if (confirmCallback.value) confirmCallback.value()
  showConfirmModal.value = false
  confirmCallback.value = null
}

// API Calls
const fetchEmployees = async () => {
  try {
    const res = await fetch(`${API_BASE_URL}/hr/employees/`, {
      headers: { 'Authorization': `Bearer ${getAccessToken()}` }
    })
    employees.value = await res.json()
  } catch (err) {
    console.error('Error loading employees:', err)
  }
}

const fetchAssets = async () => {
  try {
    const res = await fetch(`${API_BASE_URL}/offshore/vessels/`, {
      headers: { 'Authorization': `Bearer ${getAccessToken()}` }
    })
    assets.value = await res.json()
  } catch (err) {
    console.error('Error loading assets:', err)
  }
}

const fetchRosters = async () => {
  try {
    const res = await fetch(`${API_BASE_URL}/hr/rosters/`, {
      headers: { 'Authorization': `Bearer ${getAccessToken()}` }
    })
    rosters.value = await res.json()
  } catch (err) {
    console.error('Error loading rosters:', err)
  }
}

const fetchActivities = async () => {
  try {
    const res = await fetch(`${API_BASE_URL}/hr/activities/`, {
      headers: { 'Authorization': `Bearer ${getAccessToken()}` }
    })
    activities.value = await res.json()
  } catch (err) {
    console.error('Error loading activities:', err)
  }
}

// Navigation
const navigateTime = (direction) => {
  if (viewMode.value === 'week') {
    currentStartDate.value.setDate(currentStartDate.value.getDate() + (direction * 7))
  } else if (viewMode.value === 'month') {
    currentStartDate.value.setMonth(currentStartDate.value.getMonth() + direction)
  } else if (viewMode.value === 'year') {
    currentStartDate.value.setFullYear(currentStartDate.value.getFullYear() + direction)
  }
  renderGrid()
}

const switchView = (mode) => {
  viewMode.value = mode
  if (mode === 'month') {
    currentStartDate.value = new Date(currentStartDate.value.getFullYear(), currentStartDate.value.getMonth(), 1)
  } else if (mode === 'year') {
    currentStartDate.value = new Date(currentStartDate.value.getFullYear(), 0, 1)
  }
  renderGrid()
}

// Grid Rendering
const renderGrid = () => {
  timeUnits.value = []

  if (viewMode.value === 'week') {
    for (let i = 0; i < 7; i++) {
      const day = new Date(currentStartDate.value)
      day.setDate(currentStartDate.value.getDate() + i)
      timeUnits.value.push(day)
    }
  } else if (viewMode.value === 'month') {
    const year = currentStartDate.value.getFullYear()
    const month = currentStartDate.value.getMonth()
    const numDays = new Date(year, month + 1, 0).getDate()
    for (let d = 1; d <= numDays; d++) {
      timeUnits.value.push(new Date(year, month, d))
    }
  } else if (viewMode.value === 'year') {
    const year = currentStartDate.value.getFullYear()
    for (let m = 0; m < 12; m++) {
      timeUnits.value.push({ year, month: m })
    }
  }

  renderActivityRow()
  renderAssetRows()
}

const renderActivityRow = () => {
  if (vesselFilter.value === 'ALL') {
    activityRow.value = []
    return
  }

  const filteredActivities = activities.value.filter(act => act.asset === vesselFilter.value)
  const cells = []
  let colIndex = 0

  while (colIndex < timeUnits.value.length) {
    let activity = null
    let formattedDate = ''

    if (viewMode.value === 'week' || viewMode.value === 'month') {
      formattedDate = timeUnits.value[colIndex].toISOString().split('T')[0]
      activity = filteredActivities.find(act => formattedDate >= act.start && formattedDate <= act.end)
    } else if (viewMode.value === 'year') {
      const targetMonth = timeUnits.value[colIndex]
      const monthStart = `${targetMonth.year}-${String(targetMonth.month + 1).padStart(2, '0')}-01`
      const monthEnd = `${targetMonth.year}-${String(targetMonth.month + 1).padStart(2, '0')}-${new Date(targetMonth.year, targetMonth.month + 1, 0).getDate()}`
      activity = filteredActivities.find(act => act.start <= monthEnd && act.end >= monthStart)
    }

    if (activity) {
      let colSpan = 1
      let nextIndex = colIndex + 1
      while (nextIndex < timeUnits.value.length) {
        let nextActivity = null
        if (viewMode.value === 'week' || viewMode.value === 'month') {
          const nextDate = timeUnits.value[nextIndex].toISOString().split('T')[0]
          nextActivity = filteredActivities.find(act => nextDate >= act.start && nextDate <= act.end && act.id === activity.id)
        } else if (viewMode.value === 'year') {
          const nextMonth = timeUnits.value[nextIndex]
          const nStart = `${nextMonth.year}-${String(nextMonth.month + 1).padStart(2, '0')}-01`
          const nEnd = `${nextMonth.year}-${String(nextMonth.month + 1).padStart(2, '0')}-${new Date(nextMonth.year, nextMonth.month + 1, 0).getDate()}`
          nextActivity = filteredActivities.find(act => act.start <= nEnd && act.end >= nStart && act.id === activity.id)
        }
        if (nextActivity) {
          colSpan++
          nextIndex++
        } else {
          break
        }
      }
      cells.push({ visible: true, colSpan, activity, date: formattedDate })
      for (let i = 1; i < colSpan; i++) {
        cells.push({ visible: false })
      }
      colIndex += colSpan
    } else {
      cells.push({ visible: true, colSpan: 1, activity: null, date: formattedDate })
      colIndex++
    }
  }

  activityRow.value = cells
}

const renderAssetRows = () => {
  const rows = {}
  const query = crewSearch.value.toLowerCase()

  activeAssets.value.forEach(asset => {
    const cells = []
    let colIndex = 0

    while (colIndex < timeUnits.value.length) {
      let assignment = null
      let formattedDate = ''

      if (viewMode.value === 'week' || viewMode.value === 'month') {
        formattedDate = timeUnits.value[colIndex].toISOString().split('T')[0]
        assignment = rosters.value.find(r => {
          const matchesSearch = query === '' || r.title.toLowerCase().includes(query)
          return r.vessel === asset.asset_id && formattedDate >= r.start && formattedDate <= r.end && matchesSearch
        })
      } else if (viewMode.value === 'year') {
        const targetMonth = timeUnits.value[colIndex]
        const monthStart = `${targetMonth.year}-${String(targetMonth.month + 1).padStart(2, '0')}-01`
        const monthEnd = `${targetMonth.year}-${String(targetMonth.month + 1).padStart(2, '0')}-${new Date(targetMonth.year, targetMonth.month + 1, 0).getDate()}`
        assignment = rosters.value.find(r => {
          const matchesSearch = query === '' || r.title.toLowerCase().includes(query)
          return r.vessel === asset.asset_id && r.start <= monthEnd && r.end >= monthStart && matchesSearch
        })
      }

      if (assignment) {
        let colSpan = 1
        let nextIndex = colIndex + 1
        while (nextIndex < timeUnits.value.length) {
          let nextAssignment = null
          if (viewMode.value === 'week' || viewMode.value === 'month') {
            const nextDate = timeUnits.value[nextIndex].toISOString().split('T')[0]
            nextAssignment = rosters.value.find(r => {
              const matchesSearch = query === '' || r.title.toLowerCase().includes(query)
              return r.vessel === asset.asset_id && nextDate >= r.start && nextDate <= r.end && r.id === assignment.id && matchesSearch
            })
          } else if (viewMode.value === 'year') {
            const nextMonth = timeUnits.value[nextIndex]
            const nStart = `${nextMonth.year}-${String(nextMonth.month + 1).padStart(2, '0')}-01`
            const nEnd = `${nextMonth.year}-${String(nextMonth.month + 1).padStart(2, '0')}-${new Date(nextMonth.year, nextMonth.month + 1, 0).getDate()}`
            nextAssignment = rosters.value.find(r => {
              const matchesSearch = query === '' || r.title.toLowerCase().includes(query)
              return r.vessel === asset.asset_id && r.start <= nEnd && r.end >= nStart && r.id === assignment.id && matchesSearch
            })
          }
          if (nextAssignment) {
            colSpan++
            nextIndex++
          } else {
            break
          }
        }
        cells.push({ visible: true, colSpan, assignment })
        for (let i = 1; i < colSpan; i++) {
          cells.push({ visible: false })
        }
        colIndex += colSpan
      } else {
        cells.push({ visible: true, colSpan: 1, assignment: null })
        colIndex++
      }
    }

    rows[asset.asset_id] = cells
  })

  assetRows.value = rows
}

// Modal Handlers
const openNewAddModal = () => {
  const today = new Date().toISOString().split('T')[0]
  assignForm.value = { employee: '', vessel: '', start: today, end: today }
  showAssignModal.value = true
}

const openAssetModal = () => {
  assetForm.value = { asset_id: '', name: '', capacity: '', icon: 'Ship' }
  showAssetModal.value = true
}

const openActivityModal = () => {
  if (vesselFilter.value === 'ALL') {
    showToast('warning', 'VESSEL FILTER REQUIRED', 'Please select a specific fleet vessel from the filter first to assign activities.')
    return
  }
  const today = new Date().toISOString().split('T')[0]
  activityForm.value = { start: today, end: today, activity_name: '' }
  showActivityModal.value = true
}

const openActivityModalWithDate = (date) => {
  if (vesselFilter.value === 'ALL') {
    showToast('warning', 'VESSEL FILTER REQUIRED', 'Please select a specific fleet vessel from the filter first.')
    return
  }
  activityForm.value = { start: date, end: date, activity_name: '' }
  showActivityModal.value = true
}

const showEmployeeDetails = (empId) => {
  selectedEmployee.value = employees.value.find(e => e.emp_id === empId)
  if (selectedEmployee.value) showDetailModal.value = true
}

const showEmployeeDetailsByName = (name) => {
  selectedEmployee.value = employees.value.find(e => e.full_name === name)
  if (selectedEmployee.value) showDetailModal.value = true
}

// CRUD Operations
const submitAssignment = async () => {
  const selectedCrew = employees.value.find(emp => emp.emp_id === assignForm.value.employee)

  if (selectedCrew) {
    const today = new Date().toISOString().split('T')[0]
    const isMcuExpired = selectedCrew.mcu_expiry && selectedCrew.mcu_expiry < today

    if (selectedCrew.mcu_status === 'UNFIT') {
      showToast('error', 'DEPLOYMENT BLOCKED', `PERSONNEL ${selectedCrew.full_name.toUpperCase()} IS MEDICALLY UNFIT FOR OFFSHORE OPERATIONS.`)
      return
    }

    if (selectedCrew.mcu_status === 'EXPIRED' || isMcuExpired) {
      const expiryFormatted = formatMCUExpiry(selectedCrew.mcu_expiry)
      showToast('error', 'DEPLOYMENT DENIED', `PERSONNEL ${selectedCrew.full_name.toUpperCase()} MCU EXPIRED ON ${expiryFormatted.toUpperCase()}.`)
      return
    }
  }

  if (new Date(assignForm.value.end) < new Date(assignForm.value.start)) {
    showToast('error', 'INVALID DATE RANGE', 'The offboard date cannot be earlier than the onboard date.')
    return
  }

  try {
    const response = await fetch(`${API_BASE_URL}/hr/rosters/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getAccessToken()}`
      },
      body: JSON.stringify(assignForm.value)
    })

    if (response.ok) {
      showAssignModal.value = false
      await fetchRosters()
      renderGrid()
      showToast('success', 'CREW DEPLOYED', 'Personnel has been successfully allocated to the asset.')
    } else {
      const errorData = await response.json()
      if (errorData.non_field_errors) {
        showToast('error', 'CRITICAL BLOCK', errorData.non_field_errors[0])
      } else {
        showToast('error', 'DEPLOYMENT FAILURE', 'System failed to write crew allocation data.')
      }
    }
  } catch (err) {
    showToast('error', 'DEPLOYMENT FAILURE', 'Network error occurred.')
  }
}

const deleteAssignment = (id) => {
  showConfirm('Terminate crew deployment duration?', async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/hr/rosters/delete/${id}/`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${getAccessToken()}` }
      })
      if (response.ok) {
        await fetchRosters()
        renderGrid()
        showToast('success', 'DEPLOYMENT TERMINATED', 'The crew roster allocation has been successfully removed.')
      } else {
        showToast('error', 'TERMINATION FAILURE', 'Failed to update roster deletion on the server.')
      }
    } catch (err) {
      showToast('error', 'TERMINATION FAILURE', 'Network error occurred.')
    }
  })
}


const submitActivity = async () => {
  if (new Date(activityForm.value.end) < new Date(activityForm.value.start)) {
    showToast('error', 'INVALID LOG RANGE', 'The activity end date cannot occur before the start date.')
    return
  }

  const activityData = {
    asset: vesselFilter.value,
    start: activityForm.value.start,
    end: activityForm.value.end,
    activity_name: activityForm.value.activity_name.trim()
  }

  try {
    const response = await fetch(`${API_BASE_URL}/hr/activities/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getAccessToken()}`
      },
      body: JSON.stringify(activityData)
    })

    if (response.ok) {
      showActivityModal.value = false
      await fetchActivities()
      renderGrid()
      showToast('success', 'LOG REGISTERED', 'Vessel operational activity successfully logged.')
    } else {
      showToast('error', 'LOG ALLOCATION FAILURE', 'Vessel activity log could not be saved.')
    }
  } catch (err) {
    showToast('error', 'LOG ALLOCATION FAILURE', 'Network error occurred.')
  }
}

const deleteActivity = (id) => {
  showConfirm('Permanently delete this vessel activity log?', async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/hr/activities/delete/${id}/`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${getAccessToken()}` }
      })
      if (response.ok) {
        await fetchActivities()
        renderGrid()
        showToast('success', 'LOG DELETED', 'The activity entry was successfully flushed from database logs.')
      } else {
        showToast('error', 'LOG DELETION FAILURE', 'Server refused log entry termination requests.')
      }
    } catch (err) {
      showToast('error', 'LOG DELETION FAILURE', 'Network error occurred.')
    }
  })
}

onMounted(async () => {
  await fetchEmployees()
  await fetchAssets()
  await fetchRosters()
  await fetchActivities()
  renderGrid()
})
</script>
