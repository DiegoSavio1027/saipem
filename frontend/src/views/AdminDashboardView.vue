<template>
  <DashboardLayout>
    <div class="space-y-8">
      <!-- Header -->
      <div>
        <h1 class="text-3xl font-black text-slate-900 dark:text-white tracking-tight">Command Center</h1>
        <p class="text-sm text-slate-500 dark:text-slate-400 mt-2">Overview of all operational modules and systems</p>
      </div>

      <!-- Quick Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-xs text-slate-500 dark:text-slate-400 uppercase font-bold tracking-wider">Active Users</p>
              <p class="text-2xl font-black text-slate-900 dark:text-white mt-2">{{ activeUsers }}</p>
            </div>
            <div class="bg-blue-50 dark:bg-blue-950/30 p-3 rounded-lg">
              <Users class="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-xs text-slate-500 dark:text-slate-400 uppercase font-bold tracking-wider">Fleet Vessels</p>
              <p class="text-2xl font-black text-slate-900 dark:text-white mt-2">{{ totalVessels }}</p>
            </div>
            <div class="bg-orange-50 dark:bg-orange-950/30 p-3 rounded-lg">
              <Ship class="w-6 h-6 text-[var(--color-saipem-tertiary)]" />
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-xs text-slate-500 dark:text-slate-400 uppercase font-bold tracking-wider">Pending PTWs</p>
              <p class="text-2xl font-black text-slate-900 dark:text-white mt-2">{{ pendingPTWs }}</p>
            </div>
            <div class="bg-amber-50 dark:bg-amber-950/30 p-3 rounded-lg">
              <AlertCircle class="w-6 h-6 text-amber-600 dark:text-amber-400" />
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-xs text-slate-500 dark:text-slate-400 uppercase font-bold tracking-wider">System Status</p>
              <p class="text-2xl font-black text-green-600 dark:text-green-400 mt-2">{{ systemStatus }}</p>
            </div>
            <div class="bg-green-50 dark:bg-green-950/30 p-3 rounded-lg">
              <CheckCircle class="w-6 h-6 text-green-600 dark:text-green-400" />
            </div>
          </div>
        </div>
      </div>

      <!-- Module Cards -->
      <div>
        <h2 class="text-lg font-black text-slate-900 dark:text-white mb-4 tracking-tight">Operational Modules</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <!-- HSE Module -->
          <router-link to="/hse" class="group bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm hover:shadow-md hover:border-[var(--color-saipem-tertiary)] transition-all duration-200">
            <div class="flex items-start justify-between mb-4">
              <div class="bg-orange-50 dark:bg-orange-950/30 p-3 rounded-lg group-hover:bg-orange-100 dark:group-hover:bg-orange-900/50 transition-colors">
                <AlertTriangle class="w-6 h-6 text-[var(--color-saipem-tertiary)]" />
              </div>
              <ChevronRight class="w-5 h-5 text-slate-400 group-hover:text-[var(--color-saipem-tertiary)] transition-colors" />
            </div>
            <h3 class="text-lg font-black text-slate-900 dark:text-white mb-1">HSE Command Center</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">PTW management, incidents, safety monitoring</p>
          </router-link>

          <!-- HR Module -->
          <router-link to="/hr/personnel" class="group bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm hover:shadow-md hover:border-blue-500 transition-all duration-200">
            <div class="flex items-start justify-between mb-4">
              <div class="bg-blue-50 dark:bg-blue-950/30 p-3 rounded-lg group-hover:bg-blue-100 dark:group-hover:bg-blue-900/50 transition-colors">
                <Users class="w-6 h-6 text-blue-600 dark:text-blue-400" />
              </div>
              <ChevronRight class="w-5 h-5 text-slate-400 group-hover:text-blue-600 transition-colors" />
            </div>
            <h3 class="text-lg font-black text-slate-900 dark:text-white mb-1">HR Management</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">Personnel, roster, payroll management</p>
          </router-link>

          <!-- Analytics Module -->
          <router-link to="/hse/analytics" class="group bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm hover:shadow-md hover:border-purple-500 transition-all duration-200">
            <div class="flex items-start justify-between mb-4">
              <div class="bg-purple-50 dark:bg-purple-950/30 p-3 rounded-lg group-hover:bg-purple-100 dark:group-hover:bg-purple-900/50 transition-colors">
                <BarChart3 class="w-6 h-6 text-purple-600 dark:text-purple-400" />
              </div>
              <ChevronRight class="w-5 h-5 text-slate-400 group-hover:text-purple-600 transition-colors" />
            </div>
            <h3 class="text-lg font-black text-slate-900 dark:text-white mb-1">Analytics & Reports</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">Performance metrics and data insights</p>
          </router-link>

          <!-- Live POB Module -->
          <router-link to="/hse/live-pob" class="group bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm hover:shadow-md hover:border-green-500 transition-all duration-200">
            <div class="flex items-start justify-between mb-4">
              <div class="bg-green-50 dark:bg-green-950/30 p-3 rounded-lg group-hover:bg-green-100 dark:group-hover:bg-green-900/50 transition-colors">
                <Radio class="w-6 h-6 text-green-600 dark:text-green-400" />
              </div>
              <ChevronRight class="w-5 h-5 text-slate-400 group-hover:text-green-600 transition-colors" />
            </div>
            <h3 class="text-lg font-black text-slate-900 dark:text-white mb-1">Live POB Tracking</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">Real-time personnel on board monitoring</p>
          </router-link>

          <!-- Work Locations Module -->
          <router-link to="/offshore/locations" class="group bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm hover:shadow-md hover:border-red-500 transition-all duration-200">
            <div class="flex items-start justify-between mb-4">
              <div class="bg-red-50 dark:bg-red-950/30 p-3 rounded-lg group-hover:bg-red-100 dark:group-hover:bg-red-900/50 transition-colors">
                <MapPin class="w-6 h-6 text-red-600 dark:text-red-400" />
              </div>
              <ChevronRight class="w-5 h-5 text-slate-400 group-hover:text-red-600 transition-colors" />
            </div>
            <h3 class="text-lg font-black text-slate-900 dark:text-white mb-1">Work Locations</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">Hazard zones and work area management</p>
          </router-link>

          <!-- Incidents Module -->
          <router-link to="/hse/incidents" class="group bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm hover:shadow-md hover:border-red-600 transition-all duration-200">
            <div class="flex items-start justify-between mb-4">
              <div class="bg-red-50 dark:bg-red-950/30 p-3 rounded-lg group-hover:bg-red-100 dark:group-hover:bg-red-900/50 transition-colors">
                <AlertTriangle class="w-6 h-6 text-red-600 dark:text-red-400" />
              </div>
              <ChevronRight class="w-5 h-5 text-slate-400 group-hover:text-red-600 transition-colors" />
            </div>
            <h3 class="text-lg font-black text-slate-900 dark:text-white mb-1">Incident Reports</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">Safety incidents and near misses</p>
          </router-link>

          <!-- Vessel Registry Module -->
          <router-link to="/offshore/vessels" class="group bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm hover:shadow-md hover:border-cyan-500 transition-all duration-200">
            <div class="flex items-start justify-between mb-4">
              <div class="bg-cyan-50 dark:bg-cyan-950/30 p-3 rounded-lg group-hover:bg-cyan-100 dark:group-hover:bg-cyan-900/50 transition-colors">
                <Ship class="w-6 h-6 text-cyan-600 dark:text-cyan-400" />
              </div>
              <ChevronRight class="w-5 h-5 text-slate-400 group-hover:text-cyan-600 transition-colors" />
            </div>
            <h3 class="text-lg font-black text-slate-900 dark:text-white mb-1">Vessel Registry</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">Fleet management and vessel configuration</p>
          </router-link>

          <!-- Deck Management Module -->
          <router-link to="/offshore/locations" class="group bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm hover:shadow-md hover:border-indigo-500 transition-all duration-200">
            <div class="flex items-start justify-between mb-4">
              <div class="bg-indigo-50 dark:bg-indigo-950/30 p-3 rounded-lg group-hover:bg-indigo-100 dark:group-hover:bg-indigo-900/50 transition-colors">
                <MapPin class="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
              </div>
              <ChevronRight class="w-5 h-5 text-slate-400 group-hover:text-indigo-600 transition-colors" />
            </div>
            <h3 class="text-lg font-black text-slate-900 dark:text-white mb-1">Deck Management</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">Create and manage deck locations</p>
          </router-link>
        </div>
      </div>

      <!-- System Info -->
      <div class="bg-slate-50 dark:bg-slate-950/50 border border-slate-200 dark:border-slate-800 rounded-xl p-6">
        <h3 class="text-sm font-black text-slate-900 dark:text-white mb-4 uppercase tracking-wider">System Information</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
          <div>
            <p class="text-slate-500 dark:text-slate-400 font-bold">Current User</p>
            <p class="text-slate-900 dark:text-white font-mono mt-1">{{ authState.username }}</p>
          </div>
          <div>
            <p class="text-slate-500 dark:text-slate-400 font-bold">User Role</p>
            <p class="text-slate-900 dark:text-white font-mono mt-1">{{ authState.userRole }}</p>
          </div>
          <div>
            <p class="text-slate-500 dark:text-slate-400 font-bold">Selected Vessel</p>
            <p class="text-slate-900 dark:text-white font-mono mt-1">{{ authState.selectedVessel?.name || 'N/A' }}</p>
          </div>
          <div>
            <p class="text-slate-500 dark:text-slate-400 font-bold">Connection Status</p>
            <p class="text-green-600 dark:text-green-400 font-mono mt-1">{{ websocketState.isConnected ? 'CONNECTED' : 'OFFLINE' }}</p>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { authState } from '@/store/auth'
import { websocketState } from '@/store/websocket'
import { Users, Ship, AlertCircle, CheckCircle, AlertTriangle, ChevronRight, BarChart3, Radio, MapPin } from '@lucide/vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1'

const activeUsers = ref(0)
const totalVessels = ref(0)
const pendingPTWs = ref(0)
const systemStatus = ref('ONLINE')

const fetchDashboardData = async () => {
  try {
    // Fetch vessels count from Offshore Module (single source of truth)
    const vesselRes = await fetch(`${API_BASE_URL}/offshore/vessels/`, {
      credentials: 'include'
    })
    if (vesselRes.ok) {
      const vessels = await vesselRes.json()
      totalVessels.value = vessels.length
    }

    // Fetch pending PTWs count
    const ptwRes = await fetch(`${API_BASE_URL}/hse/ptw/`, { credentials: 'include' })
    if (ptwRes.ok) {
      const ptws = await ptwRes.json()
      pendingPTWs.value = ptws.filter(p => p.status === 'PENDING').length
    }

    activeUsers.value = websocketState.liveFeeds?.length || 0
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  }
}

onMounted(() => {
  fetchDashboardData()
})
</script>
