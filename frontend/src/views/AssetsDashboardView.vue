<template>
  <DashboardLayout>
    <div class="space-y-8 p-8">
      <!-- Header -->
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 class="text-3xl font-black text-slate-900 dark:text-white tracking-tight">ASSETS DASHBOARD</h1>
          <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">Fleet assets health monitoring, telemetry alerts, and work order tracking</p>
        </div>
        <div class="flex items-center gap-2">
          <router-link to="/assets" class="bg-orange-600 hover:bg-orange-700 text-white font-bold text-xs uppercase px-4 py-2.5 rounded-lg transition flex items-center gap-2 shadow-sm">
            <Cpu class="w-4 h-4" /> Asset Registry
          </router-link>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="p-12 flex justify-center bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
        <p class="text-slate-500 dark:text-slate-400 animate-pulse font-mono text-xs">Fetching asset telemetry...</p>
      </div>

      <!-- Stats Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        
        <!-- Fleet Health Score (OEE Equivalent) -->
        <Card class="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow">
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider font-mono">Fleet Health Score</CardTitle>
            <Settings class="h-4 w-4 text-indigo-500" />
          </CardHeader>
          <CardContent>
            <div class="flex items-end gap-2">
              <div class="text-4xl font-black text-slate-900 dark:text-white" :class="fleetHealthScore > 80 ? 'text-green-600' : 'text-amber-500'">{{ fleetHealthScore }}<span class="text-xl text-slate-400 ml-1">%</span></div>
            </div>
            <div class="w-full bg-slate-100 dark:bg-slate-800 rounded-full h-1.5 mt-4">
              <div class="bg-indigo-500 h-1.5 rounded-full transition-all duration-1000" :style="`width: ${fleetHealthScore}%`"></div>
            </div>
            <p class="text-[9px] text-slate-500 dark:text-slate-400 mt-3 font-mono uppercase tracking-widest">Overall Asset Condition</p>
          </CardContent>
        </Card>

        <!-- Monitored Machinery (IoT) -->
        <Card class="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow cursor-pointer" @click="router.push('/assets/machinery')">
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider font-mono">Monitored Machinery</CardTitle>
            <Cpu class="h-4 w-4 text-blue-500 animate-pulse" />
          </CardHeader>
          <CardContent>
            <div class="text-4xl font-black text-slate-900 dark:text-white">{{ machinery.length }}</div>
            <div class="mt-2 text-[10px] font-mono font-bold bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 px-2 py-1 rounded inline-flex items-center gap-1.5">
              <span class="w-1.5 h-1.5 rounded-full bg-blue-500 animate-ping"></span> Live Signal Active
            </div>
            <p class="text-[9px] text-slate-500 dark:text-slate-400 mt-3 font-mono uppercase tracking-widest">IoT Telemetry Units</p>
          </CardContent>
        </Card>

        <!-- Total Operating Hours -->
        <Card class="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow">
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider font-mono">Fleet Operating Hours</CardTitle>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-emerald-500"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          </CardHeader>
          <CardContent>
            <div class="text-4xl font-black text-slate-900 dark:text-white">{{ totalOperatingHours.toLocaleString() }}</div>
            <div class="mt-2 text-[10px] font-mono font-bold text-emerald-600 dark:text-emerald-400 inline-flex items-center gap-1">
               <CheckCircle class="w-3 h-3" /> All systems nominal
            </div>
            <p class="text-[9px] text-slate-500 dark:text-slate-400 mt-3 font-mono uppercase tracking-widest">Cumulative run-time</p>
          </CardContent>
        </Card>

        <!-- Alerts & Backlog -->
        <Card class="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow cursor-pointer" :class="totalAlerts > 0 ? 'border-red-200 dark:border-red-950 bg-red-50/5' : ''" @click="router.push('/assets/work-orders')">
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider font-mono">Action Required</CardTitle>
            <AlertTriangle class="h-4 w-4" :class="totalAlerts > 0 ? 'text-red-500 animate-pulse' : 'text-slate-300'" />
          </CardHeader>
          <CardContent>
            <div class="flex gap-6 items-end mt-1">
              <div>
                <span class="text-4xl font-black" :class="totalAlerts > 0 ? 'text-red-600 dark:text-red-400' : 'text-slate-900 dark:text-white'">{{ totalAlerts }}</span>
                <p class="text-[10px] text-slate-500 dark:text-slate-400 font-bold uppercase mt-1">Alerts</p>
              </div>
              <div class="h-10 w-px bg-slate-200 dark:bg-slate-700"></div>
              <div>
                <span class="text-2xl font-black text-orange-500">{{ activeWorkOrdersCount }}</span>
                <p class="text-[10px] text-slate-500 dark:text-slate-400 font-bold uppercase mt-1">Active WOs</p>
              </div>
            </div>
            <p class="text-[9px] text-slate-500 dark:text-slate-400 mt-3 font-mono uppercase tracking-widest">Pending maintenance tasks</p>
          </CardContent>
        </Card>

      </div>

      <div v-if="!isLoading" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Critical Assets List -->
        <Card class="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm">
          <CardHeader>
            <CardTitle class="text-lg font-black text-slate-900 dark:text-white tracking-tight">Critical Equipment & Systems</CardTitle>
            <CardDescription class="text-xs text-slate-500 dark:text-slate-400">Assets and machinery with warning or critical health score</CardDescription>
          </CardHeader>
          <CardContent>
            <div v-if="criticalAssets.length === 0" class="flex flex-col items-center justify-center p-8 text-center text-slate-400 dark:text-slate-500">
              <CheckCircle class="w-10 h-10 text-green-500 mb-2 opacity-50" />
              <p class="text-xs font-mono">All equipment and systems are in normal condition</p>
            </div>
            <ul v-else class="space-y-3 max-h-[300px] overflow-y-auto">
              <li v-for="asset in criticalAssets" :key="asset.asset_id" class="p-3.5 bg-slate-50 dark:bg-slate-950 border border-slate-100 dark:border-slate-850 rounded-lg text-xs font-mono">
                <div class="flex justify-between items-start mb-2">
                  <div>
                    <h4 class="font-bold text-slate-900 dark:text-slate-100 font-sans text-sm">{{ asset.name }}</h4>
                    <p class="text-[10px] text-slate-500 dark:text-slate-400 mt-0.5">{{ asset.asset_id }} • {{ asset.vessel_name || asset.vessel }}</p>
                  </div>
                  <span :class="[
                    'px-2 py-0.5 rounded text-[9px] font-black tracking-wide',
                    asset.status === 'CRITICAL' ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400' : 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400'
                  ]">
                    {{ asset.status }}
                  </span>
                </div>
                <div class="space-y-1 mt-2 pt-2 border-t border-slate-100 dark:border-slate-800/80">
                  <div class="flex justify-between">
                    <span class="text-slate-400">Health Index</span>
                    <span :class="asset.health_score > 70 ? 'text-green-500' : 'text-red-500'" class="font-bold">{{ asset.health_score }}%</span>
                  </div>
                </div>
              </li>
            </ul>
          </CardContent>
        </Card>

        <!-- Active Work Orders List -->
        <Card class="col-span-1 lg:col-span-2 bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm">
          <CardHeader class="flex flex-row justify-between items-start">
            <div>
              <CardTitle class="text-lg font-black text-slate-900 dark:text-white tracking-tight">Active Work Orders</CardTitle>
              <CardDescription class="text-xs text-slate-500 dark:text-slate-400">Pending and ongoing maintenance actions</CardDescription>
            </div>
            <router-link to="/assets/work-orders" class="text-blue-600 hover:text-blue-500 text-xs font-bold font-mono uppercase tracking-wider flex items-center gap-1">
              All Orders <ChevronRight class="w-4 h-4" />
            </router-link>
          </CardHeader>
          <CardContent>
            <div v-if="activeWorkOrders.length === 0" class="flex flex-col items-center justify-center p-12 text-center text-slate-400 dark:text-slate-500">
              <ClipboardList class="w-10 h-10 text-slate-300 mb-2 opacity-50" />
              <p class="text-xs font-mono">No active work orders</p>
            </div>
            <div v-else class="overflow-x-auto">
              <table class="w-full text-left font-mono text-xs">
                <thead>
                  <tr class="border-b border-slate-100 dark:border-slate-800 text-slate-400 font-bold uppercase tracking-wider">
                    <th class="pb-3 pr-2">ID</th>
                    <th class="pb-3 pr-2">Description</th>
                    <th class="pb-3 pr-2">Priority</th>
                    <th class="pb-3 pr-2">Status</th>
                    <th class="pb-3 pr-2">Assigned</th>
                    <th class="pb-3 text-right">Scheduled</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100 dark:divide-slate-800/80">
                  <tr v-for="wo in activeWorkOrders.slice(0, 5)" :key="wo.wo_id" class="text-slate-700 dark:text-slate-300">
                    <td class="py-3 font-bold text-slate-900 dark:text-white pr-2">{{ wo.wo_id }}</td>
                    <td class="py-3 max-w-[200px] truncate pr-2" :title="wo.description">{{ wo.description }}</td>
                    <td class="py-3 pr-2">
                      <span :class="[
                        'px-1.5 py-0.5 rounded text-[9px] font-black uppercase tracking-wider',
                        wo.priority === 'CRITICAL' ? 'bg-red-100 text-red-700 dark:bg-red-900/30' :
                        wo.priority === 'HIGH' ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/30' :
                        'bg-slate-100 text-slate-700 dark:bg-slate-800'
                      ]">
                        {{ wo.priority }}
                      </span>
                    </td>
                    <td class="py-3 pr-2">
                      <span :class="[
                        'px-1.5 py-0.5 rounded text-[9px] font-black uppercase tracking-wider',
                        wo.status === 'IN_PROGRESS' ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 text-blue-400' : 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 text-amber-400'
                      ]">
                        {{ wo.status }}
                      </span>
                    </td>
                    <td class="py-3 pr-2">
                      <div class="flex items-center text-slate-500">
                        <div class="w-5 h-5 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-[9px] font-bold mr-2 uppercase">
                          {{ wo.assigned_to_name ? wo.assigned_to_name.charAt(0) : 'U' }}
                        </div>
                        <span class="truncate max-w-[100px]" :title="wo.assigned_to_name || 'Unassigned'">
                          {{ wo.assigned_to_name || 'Unassigned' }}
                        </span>
                      </div>
                    </td>
                    <td class="py-3 text-right">{{ formatDate(wo.scheduled_date) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import DashboardLayout from '@/layouts/DashboardLayout.vue';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Cpu, CheckCircle, AlertTriangle, ClipboardList, ChevronRight, Package, Settings } from '@lucide/vue';
import { getAccessToken, authState } from '@/store/auth';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';
const router = useRouter();

const isLoading = ref(true);
const assets = ref([]);
const machinery = ref([]);
const workOrders = ref([]);
const inventory = ref([]);

const fetchDashboardData = async () => {
  isLoading.value = true;
  try {
    const headers = { 'Authorization': `Bearer ${getAccessToken()}` };
    const params = new URLSearchParams();
    if (authState.selectedVessel) {
      params.append('vessel_id', authState.selectedVessel.asset_id);
    }
    const queryString = params.toString() ? `?${params.toString()}` : '';

    // Fetch assets
    const assetsResponse = await fetch(`${API_BASE_URL}/asset/assets/${queryString}`, { headers });
    if (assetsResponse.ok) {
      assets.value = await assetsResponse.json();
    }

    // Fetch work orders
    const woResponse = await fetch(`${API_BASE_URL}/asset/workorders/${queryString}`, { headers });
    if (woResponse.ok) {
      workOrders.value = await woResponse.json();
    }

    // Fetch machinery
    const macResponse = await fetch(`${API_BASE_URL}/asset/machinery/${queryString}`, { headers });
    if (macResponse.ok) {
      machinery.value = await macResponse.json();
    }

    // Fetch inventory
    const invResponse = await fetch(`${API_BASE_URL}/asset/inventory/${queryString}`, { headers });
    if (invResponse.ok) {
      inventory.value = await invResponse.json();
    }
  } catch (error) {
    console.error('Failed to fetch Assets Dashboard data:', error);
  } finally {
    isLoading.value = false;
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '-';
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

const healthyCount = computed(() => {
  return assets.value.filter(a => a.status === 'OPERATIONAL').length;
});

const criticalCount = computed(() => {
  return assets.value.filter(a => a.status === 'CRITICAL' || a.status === 'MAINTENANCE').length;
});

const fleetHealthScore = computed(() => {
  if (assets.value.length === 0) return 100;
  const totalScore = assets.value.reduce((sum, asset) => sum + asset.health_score, 0);
  return Math.round(totalScore / assets.value.length);
});

const totalOperatingHours = computed(() => {
  return machinery.value.reduce((sum, mac) => sum + mac.operating_hours, 0);
});

const criticalMachineryCount = computed(() => {
  return machinery.value.filter(m => m.needs_maintenance).length;
});

const totalAlerts = computed(() => criticalCount.value + criticalMachineryCount.value);

const activeWorkOrders = computed(() => {
  return workOrders.value.filter(wo => wo.status === 'PENDING' || wo.status === 'IN_PROGRESS');
});

const activeWorkOrdersCount = computed(() => {
  return activeWorkOrders.value.length;
});

const lowStockInventoryCount = computed(() => {
  return inventory.value.filter(i => i.current_stock <= i.minimum_stock).length;
});

const criticalAssets = computed(() => {
  const criticalFromAssets = assets.value.filter(a => a.status === 'CRITICAL' || a.status === 'MAINTENANCE' || a.health_score < 80);
  
  const criticalFromMachinery = machinery.value.filter(m => m.needs_maintenance || m.health_percentage < 80).map(m => ({
    asset_id: m.serial_number,
    name: m.equipment_name,
    vessel_name: m.vessel_name,
    status: m.needs_maintenance ? 'MAINTENANCE' : 'WARNING',
    health_score: Math.round(m.health_percentage || 50)
  }));

  const criticalFromInventory = inventory.value.filter(i => i.status === 'CRITICAL' || i.status === 'MAINTENANCE' || i.health_score < 80).map(i => ({
    asset_id: i.item_code,
    name: i.name,
    vessel_name: i.vessel_name || i.vessel,
    status: i.status,
    health_score: Math.round(i.health_score || 50)
  }));

  return [...criticalFromAssets, ...criticalFromMachinery, ...criticalFromInventory];
});

onMounted(() => {
  fetchDashboardData();
});
</script>
