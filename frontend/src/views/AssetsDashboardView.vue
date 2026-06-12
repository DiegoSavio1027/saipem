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
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Monitored Assets -->
        <Card class="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow">
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider font-mono">Monitored Assets</CardTitle>
            <Cpu class="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div class="text-3xl font-black text-slate-900 dark:text-white">{{ assets.length }}</div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">IoT signal active</p>
          </CardContent>
        </Card>

        <!-- Healthy Status -->
        <Card class="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow">
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider font-mono">Healthy Assets</CardTitle>
            <CheckCircle class="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div class="text-3xl font-black text-slate-900 dark:text-white">{{ healthyCount }}</div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">Operational & stable</p>
          </CardContent>
        </Card>

        <!-- Critical Warnings -->
        <Card class="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow" :class="criticalCount > 0 ? 'border-red-200 dark:border-red-950 bg-red-50/5' : ''">
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider font-mono">Critical Warnings</CardTitle>
            <AlertTriangle class="h-4 w-4 text-red-500" :class="criticalCount > 0 ? 'animate-pulse' : ''" />
          </CardHeader>
          <CardContent>
            <div class="text-3xl font-black text-slate-900 dark:text-white" :class="criticalCount > 0 ? 'text-red-600 dark:text-red-400' : ''">{{ criticalCount }}</div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">Require immediate maintenance</p>
          </CardContent>
        </Card>

        <!-- Active Work Orders -->
        <Card class="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow cursor-pointer" @click="router.push('/assets/work-orders')">
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider font-mono">Active WOs</CardTitle>
            <ClipboardList class="h-4 w-4 text-orange-500" />
          </CardHeader>
          <CardContent>
            <div class="text-3xl font-black text-slate-900 dark:text-white">{{ activeWorkOrdersCount }}</div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">Pending or in-progress jobs</p>
          </CardContent>
        </Card>

        <!-- Low Stock Inventory -->
        <Card class="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow cursor-pointer" :class="lowStockInventoryCount > 0 ? 'border-orange-200 dark:border-orange-900 bg-orange-50/5' : ''" @click="router.push('/assets/inventory')">
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider font-mono">Inv. Alerts</CardTitle>
            <Package class="h-4 w-4 text-orange-500" />
          </CardHeader>
          <CardContent>
            <div class="text-3xl font-black text-slate-900 dark:text-white" :class="lowStockInventoryCount > 0 ? 'text-orange-600 dark:text-orange-400' : ''">{{ lowStockInventoryCount }}</div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">General items below min stock</p>
          </CardContent>
        </Card>

        <!-- Low Stock Spare Parts -->
        <Card class="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow cursor-pointer" :class="lowStockSparepartsCount > 0 ? 'border-red-200 dark:border-red-900 bg-red-50/5' : ''" @click="router.push('/assets/spareparts')">
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider font-mono">Part Alerts</CardTitle>
            <Settings class="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div class="text-3xl font-black text-slate-900 dark:text-white" :class="lowStockSparepartsCount > 0 ? 'text-red-600 dark:text-red-400' : ''">{{ lowStockSparepartsCount }}</div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">Machine parts need reorder</p>
          </CardContent>
        </Card>
      </div>

      <div v-if="!isLoading" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Critical Assets List -->
        <Card class="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm">
          <CardHeader>
            <CardTitle class="text-lg font-black text-slate-900 dark:text-white tracking-tight">Critical Assets</CardTitle>
            <CardDescription class="text-xs text-slate-500 dark:text-slate-400">Vessel machinery with warning or critical health score</CardDescription>
          </CardHeader>
          <CardContent>
            <div v-if="criticalAssets.length === 0" class="flex flex-col items-center justify-center p-8 text-center text-slate-400 dark:text-slate-500">
              <CheckCircle class="w-10 h-10 text-green-500 mb-2 opacity-50" />
              <p class="text-xs font-mono">All machinery is operating within normal telemetry ranges</p>
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
                  <div class="flex justify-between">
                    <span class="text-slate-400">Temp / Vibration</span>
                    <span class="text-slate-700 dark:text-slate-300 font-bold">{{ asset.temperature }}°C / {{ asset.vibration }}mm/s</span>
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
const workOrders = ref([]);
const inventory = ref([]);
const spareparts = ref([]);

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
    const woResponse = await fetch(`${API_BASE_URL}/asset/workorders/`, { headers });
    if (woResponse.ok) {
      workOrders.value = await woResponse.json();
    }

    // Fetch inventory
    const invResponse = await fetch(`${API_BASE_URL}/asset/inventory/`, { headers });
    if (invResponse.ok) {
      inventory.value = await invResponse.json();
    }

    // Fetch spareparts
    const spResponse = await fetch(`${API_BASE_URL}/asset/spareparts/${queryString}`, { headers });
    if (spResponse.ok) {
      spareparts.value = await spResponse.json();
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

const activeWorkOrders = computed(() => {
  return workOrders.value.filter(wo => wo.status === 'PENDING' || wo.status === 'IN_PROGRESS');
});

const activeWorkOrdersCount = computed(() => {
  return activeWorkOrders.value.length;
});

const lowStockInventoryCount = computed(() => {
  return inventory.value.filter(i => i.current_stock <= i.minimum_stock).length;
});

const lowStockSparepartsCount = computed(() => {
  return spareparts.value.filter(s => s.quantity_on_hand <= s.reorder_level).length;
});

const criticalAssets = computed(() => {
  return assets.value.filter(a => a.status === 'CRITICAL' || a.status === 'MAINTENANCE' || a.health_score < 80);
});

onMounted(() => {
  fetchDashboardData();
});
</script>
