<template>
  <DashboardLayout>
    <div class="space-y-8 p-8">
      <!-- Header -->
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 class="text-3xl font-black text-slate-900 dark:text-white tracking-tight">HR DASHBOARD</h1>
          <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">Crew directory overview, roster statistics, and estimated payroll budget</p>
        </div>
        <div class="flex items-center gap-2">
          <router-link to="/hr/personnel" class="bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs uppercase px-4 py-2.5 rounded-lg transition flex items-center gap-2 shadow-sm">
            <Users class="w-4 h-4" /> Manage Crew
          </router-link>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="p-12 flex justify-center bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
        <p class="text-slate-500 dark:text-slate-400 animate-pulse font-mono text-xs">Fetching HR analytics...</p>
      </div>

      <!-- Stats Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <!-- Total Crew -->
        <Card class="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow overflow-hidden">
          <div class="h-1 bg-blue-500 w-full" />
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2 pt-4">
            <CardTitle class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider font-mono">Total Crew</CardTitle>
            <div class="bg-blue-50 dark:bg-blue-950/20 p-2 rounded-lg border border-blue-200 dark:border-blue-900/30">
              <Users class="h-4 w-4 text-blue-500" />
            </div>
          </CardHeader>
          <CardContent>
            <div class="text-3xl font-black text-slate-900 dark:text-white">{{ stats.total_crew }}</div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">Registered offshore crew</p>
          </CardContent>
        </Card>

        <!-- Onboard Crew -->
        <Card class="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow overflow-hidden">
          <div class="h-1 bg-[var(--color-saipem-tertiary)] w-full" />
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2 pt-4">
            <CardTitle class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider font-mono">Onboard Crew</CardTitle>
            <div class="bg-orange-50 dark:bg-orange-950/20 p-2 rounded-lg border border-orange-200 dark:border-orange-900/30">
              <Ship class="h-4 w-4 text-[var(--color-saipem-tertiary)]" />
            </div>
          </CardHeader>
          <CardContent>
            <div class="text-3xl font-black text-slate-900 dark:text-white">{{ stats.onboard_crew }}</div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">Currently assigned to vessels</p>
          </CardContent>
        </Card>

        <!-- MCU Alerts -->
        <Card class="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow overflow-hidden" :class="stats.mcu_alerts > 0 ? 'border-red-200 dark:border-red-900' : ''">
          <div class="h-1 w-full" :class="stats.mcu_alerts > 0 ? 'bg-red-500' : 'bg-slate-200 dark:bg-slate-700'" />
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2 pt-4">
            <CardTitle class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider font-mono">MCU Alerts</CardTitle>
            <div class="p-2 rounded-lg border" :class="stats.mcu_alerts > 0 ? 'bg-red-50 dark:bg-red-950/20 border-red-200 dark:border-red-900/30' : 'bg-slate-50 dark:bg-slate-800 border-slate-200 dark:border-slate-700'">
              <AlertTriangle class="h-4 w-4 text-red-500" :class="stats.mcu_alerts > 0 ? 'animate-pulse' : 'opacity-40'" />
            </div>
          </CardHeader>
          <CardContent>
            <div class="text-3xl font-black" :class="stats.mcu_alerts > 0 ? 'text-red-600 dark:text-red-400' : 'text-slate-900 dark:text-white'">{{ stats.mcu_alerts }}</div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">Expired or unfit crew certificates</p>
          </CardContent>
        </Card>

        <!-- Est. Monthly Budget -->
        <Card class="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow overflow-hidden">
          <div class="h-1 bg-green-500 w-full" />
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2 pt-4">
            <CardTitle class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider font-mono">Est. Monthly Budget</CardTitle>
            <div class="bg-green-50 dark:bg-green-950/20 p-2 rounded-lg border border-green-200 dark:border-green-900/30">
              <DollarSign class="h-4 w-4 text-green-500" />
            </div>
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-black text-slate-900 dark:text-white truncate">{{ formatCurrency(stats.estimated_budget) }}</div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1.5">For rosters in current month</p>
          </CardContent>
        </Card>
      </div>

      <div v-if="!isLoading" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Crew Onboard Rate & Vessel Activity -->
        <Card class="col-span-1 lg:col-span-2 bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm">
          <CardHeader>
            <CardTitle class="text-lg font-black text-slate-900 dark:text-white tracking-tight">Vessel Utilization & Rosters</CardTitle>
            <CardDescription class="text-xs text-slate-500 dark:text-slate-400">Offshore vessel crew deployments and roster distribution</CardDescription>
          </CardHeader>
          <CardContent class="space-y-6">
            <div>
              <div class="flex justify-between items-center text-xs font-mono mb-2">
                <span class="text-slate-400 font-bold uppercase tracking-wider">Active Deployments (Vessels)</span>
                <span class="font-bold text-slate-800 dark:text-slate-200">{{ stats.active_vessels }} / {{ stats.total_vessels }} Vessels</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-slate-800 h-3 rounded-full overflow-hidden">
                <div :style="{ width: `${vesselDeploymentRate}%` }" class="h-full bg-gradient-to-r from-blue-500 to-[var(--color-saipem-tertiary)] transition-all duration-700 rounded-full"></div>
              </div>
            </div>

            <!-- Crew Status breakdown -->
            <div class="grid grid-cols-3 gap-4 bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-100 dark:border-slate-800/40 text-center font-mono">
              <div>
                <span class="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Onboard Rate</span>
                <div class="text-xl font-bold text-slate-800 dark:text-slate-200 mt-1">{{ onboardRate }}%</div>
              </div>
              <div>
                <span class="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Available Rate</span>
                <div class="text-xl font-bold text-slate-800 dark:text-slate-200 mt-1">{{ availableRate }}%</div>
              </div>
              <div>
                <span class="text-[10px] text-slate-400 font-bold uppercase tracking-wider">MCU Deficit</span>
                <div class="text-xl font-bold text-red-500 mt-1">{{ mcuDeficitRate }}%</div>
              </div>
            </div>

            <!-- Roster matrix overview shortcut -->
            <div class="border-t border-slate-100 dark:border-slate-800/80 pt-4 flex justify-between items-center text-xs">
              <span class="text-slate-500 dark:text-slate-400 font-mono">View the complete schedule matrix</span>
              <router-link to="/hr/roster" class="text-blue-600 hover:text-blue-500 font-bold uppercase tracking-wider flex items-center gap-1 font-mono">
                Roster Matrix <ChevronRight class="w-4 h-4" />
              </router-link>
            </div>
          </CardContent>
        </Card>

        <!-- Critical MCU Alert List -->
        <Card class="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 shadow-sm">
          <CardHeader>
            <CardTitle class="text-lg font-black text-slate-900 dark:text-white tracking-tight">Critical Crew Alerts</CardTitle>
            <CardDescription class="text-xs text-slate-500 dark:text-slate-400">Crew members with expired, unfit, or expiring MCU status</CardDescription>
          </CardHeader>
          <CardContent>
            <div v-if="criticalCrew.length === 0" class="flex flex-col items-center justify-center p-8 text-center text-slate-400 dark:text-slate-500">
              <CheckCircle class="w-10 h-10 text-green-500 mb-2 opacity-50" />
              <p class="text-xs font-mono">All crew certificates are fully fit</p>
            </div>
            <ul v-else class="space-y-3 max-h-[260px] overflow-y-auto">
              <li v-for="crew in criticalCrew" :key="crew.emp_id" class="p-3 bg-slate-50 dark:bg-slate-950 border border-slate-100 dark:border-slate-850 rounded-lg flex items-center justify-between text-xs">
                <div>
                  <h4 class="font-bold text-slate-900 dark:text-slate-100">{{ crew.full_name }}</h4>
                  <p class="text-[10px] text-slate-500 dark:text-slate-400 font-mono mt-0.5">{{ crew.job_role }} • {{ crew.emp_id }}</p>
                </div>
                <div class="text-right">
                  <span :class="[
                    'px-2 py-0.5 rounded text-[9px] font-black tracking-wide font-mono',
                    crew.mcu_status === 'FIT' ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400' : 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                  ]">
                    {{ crew.mcu_status }}
                  </span>
                  <p class="text-[9px] text-slate-400 font-mono mt-1">{{ crew.mcu_expiry ? formatDate(crew.mcu_expiry) : 'N/A' }}</p>
                </div>
              </li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import DashboardLayout from '@/layouts/DashboardLayout.vue';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Users, Ship, AlertTriangle, DollarSign, CheckCircle, ChevronRight } from '@lucide/vue';
import { getAccessToken } from '@/store/auth';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';

const stats = ref({
  total_crew: 0,
  onboard_crew: 0,
  mcu_alerts: 0,
  total_vessels: 0,
  active_vessels: 0,
  estimated_budget: 0
});
const crewList = ref([]);
const isLoading = ref(true);

const fetchDashboardData = async () => {
  isLoading.value = true;
  try {
    const headers = { 'Authorization': `Bearer ${getAccessToken()}` };
    
    // Fetch stats
    const statsResponse = await fetch(`${API_BASE_URL}/hr/analytics/`, { headers });
    if (statsResponse.ok) {
      stats.value = await statsResponse.json();
    }

    // Fetch employees for critical list
    const employeesResponse = await fetch(`${API_BASE_URL}/hr/employees/`, { headers });
    if (employeesResponse.ok) {
      crewList.value = await employeesResponse.json();
    }
  } catch (error) {
    console.error('Failed to fetch HR dashboard data:', error);
  } finally {
    isLoading.value = false;
  }
};

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0
  }).format(amount);
};

const formatDate = (dateString) => {
  if (!dateString) return '-';
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

const vesselDeploymentRate = computed(() => {
  if (stats.value.total_vessels === 0) return 0;
  return Math.round((stats.value.active_vessels / stats.value.total_vessels) * 100);
});

const onboardRate = computed(() => {
  if (stats.value.total_crew === 0) return 0;
  return Math.round((stats.value.onboard_crew / stats.value.total_crew) * 100);
});

const availableRate = computed(() => {
  return Math.max(0, 100 - onboardRate.value);
});

const mcuDeficitRate = computed(() => {
  if (stats.value.total_crew === 0) return 0;
  return Math.round((stats.value.mcu_alerts / stats.value.total_crew) * 100);
});

const criticalCrew = computed(() => {
  const today = new Date();
  const thirtyDaysLater = new Date();
  thirtyDaysLater.setDate(today.getDate() + 30);

  return crewList.value.filter(crew => {
    if (crew.mcu_status === 'UNFIT' || crew.mcu_status === 'EXPIRED') {
      return true;
    }
    if (crew.mcu_expiry) {
      const expiryDate = new Date(crew.mcu_expiry);
      return expiryDate < thirtyDaysLater;
    }
    return false;
  });
});

onMounted(() => {
  fetchDashboardData();
});
</script>
