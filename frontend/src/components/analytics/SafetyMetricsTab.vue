<template>
  <div class="space-y-6">
    <!-- Date Range Filter -->
    <div class="flex gap-4 items-center">
      <div class="flex gap-2">
        <button
          v-for="range in dateRanges"
          :key="range.value"
          @click="selectedRange = range.value; fetchMetrics()"
          :class="[
            'px-4 py-2 rounded-lg font-medium transition-colors',
            selectedRange === range.value
              ? 'bg-[var(--color-saipem-primary)] text-white'
              : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'
          ]"
        >
          {{ range.label }}
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[var(--color-saipem-primary)]"></div>
    </div>

    <!-- KPI Cards -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900 dark:to-blue-800 p-6 rounded-xl border border-blue-200 dark:border-blue-700">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-blue-600 dark:text-blue-400">Average POB</p>
            <p class="text-3xl font-bold text-blue-900 dark:text-blue-100 mt-2">{{ latestMetrics?.total_pob || 0 }}</p>
          </div>
          <div class="bg-blue-200 dark:bg-blue-700 p-3 rounded-lg">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-blue-600 dark:text-blue-400"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          </div>
        </div>
      </div>

      <div class="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900 dark:to-green-800 p-6 rounded-xl border border-green-200 dark:border-green-700">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-green-600 dark:text-green-400">Days Without LTI</p>
            <p class="text-3xl font-bold text-green-900 dark:text-green-100 mt-2">{{ latestMetrics?.days_without_lti || 0 }}</p>
          </div>
          <div class="bg-green-200 dark:bg-green-700 p-3 rounded-lg">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-green-600 dark:text-green-400"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
          </div>
        </div>
      </div>

      <div class="bg-gradient-to-br from-amber-50 to-amber-100 dark:from-amber-900 dark:to-amber-800 p-6 rounded-xl border border-amber-200 dark:border-amber-700">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-amber-600 dark:text-amber-400">LTIFR</p>
            <p class="text-3xl font-bold text-amber-900 dark:text-amber-100 mt-2">{{ latestMetrics?.ltifr?.toFixed(2) || '0.00' }}</p>
          </div>
          <div class="bg-amber-200 dark:bg-amber-700 p-3 rounded-lg">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-amber-600 dark:text-amber-400"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
          </div>
        </div>
      </div>

      <div class="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900 dark:to-purple-800 p-6 rounded-xl border border-purple-200 dark:border-purple-700">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-purple-600 dark:text-purple-400">TRIFR</p>
            <p class="text-3xl font-bold text-purple-900 dark:text-purple-100 mt-2">{{ latestMetrics?.trifr?.toFixed(2) || '0.00' }}</p>
          </div>
          <div class="bg-purple-200 dark:bg-purple-700 p-3 rounded-lg">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-purple-600 dark:text-purple-400"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts -->
    <div v-if="!loading" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Days Without LTI Trend -->
      <div class="bg-white dark:bg-slate-800 p-6 rounded-xl border border-slate-200 dark:border-slate-700">
        <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">Days Without LTI Trend</h3>
        <Line :data="ltiChartData" :options="chartOptions" />
      </div>

      <!-- PTW Statistics -->
      <div class="bg-white dark:bg-slate-800 p-6 rounded-xl border border-slate-200 dark:border-slate-700">
        <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">PTW Statistics</h3>
        <Line :data="ptwChartData" :options="chartOptions" />
      </div>

      <!-- Incident Count Trend -->
      <div class="bg-white dark:bg-slate-800 p-6 rounded-xl border border-slate-200 dark:border-slate-700">
        <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">Incident Count Trend</h3>
        <Line :data="incidentChartData" :options="chartOptions" />
      </div>

      <!-- Safety Rates -->
      <div class="bg-white dark:bg-slate-800 p-6 rounded-xl border border-slate-200 dark:border-slate-700">
        <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">Safety Rates (LTIFR & TRIFR)</h3>
        <Line :data="safetyRatesChartData" :options="chartOptions" />
      </div>
    </div>

    <!-- Calculation Methodology Explanation -->
    <div class="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900 dark:to-indigo-900 p-6 rounded-xl border border-blue-200 dark:border-blue-700">
      <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">📊 Safety Metrics Calculation Methodology</h3>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- LTIFR Explanation -->
        <div class="space-y-3">
          <div class="flex items-start gap-3">
            <div class="bg-amber-100 dark:bg-amber-900/30 p-2 rounded-lg mt-1">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-amber-600 dark:text-amber-400"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            </div>
            <div>
              <p class="font-semibold text-slate-900 dark:text-slate-100">LTIFR (Lost Time Injury Frequency Rate)</p>
              <p class="text-sm text-slate-600 dark:text-slate-400 mt-1">Measures the number of lost-time injuries per 1 million hours worked</p>
            </div>
          </div>

          <div class="bg-white dark:bg-slate-800 p-3 rounded-lg border border-slate-200 dark:border-slate-700 space-y-2">
            <p class="text-xs font-mono font-semibold text-slate-700 dark:text-slate-300">Formula:</p>
            <p class="text-xs font-mono text-slate-600 dark:text-slate-400">LTIFR = (LTI Count × 1,000,000) / Total Hours Worked</p>

            <p class="text-xs font-mono font-semibold text-slate-700 dark:text-slate-300 mt-2">Calculation:</p>
            <ul class="text-xs text-slate-600 dark:text-slate-400 space-y-1 list-disc list-inside">
              <li>Period: Last 30 days (rolling average)</li>
              <li>LTI Count: Number of lost-time injuries in 30 days</li>
              <li>Avg POB: Unique employees × 30 days</li>
              <li>Hours: Avg POB × 12-hour shifts × 30 days</li>
            </ul>

            <p class="text-xs font-mono font-semibold text-slate-700 dark:text-slate-300 mt-2">Interpretation:</p>
            <ul class="text-xs text-slate-600 dark:text-slate-400 space-y-1 list-disc list-inside">
              <li><span class="font-semibold">0-5:</span> Excellent safety performance</li>
              <li><span class="font-semibold">5-10:</span> Good safety performance</li>
              <li><span class="font-semibold">&gt;10:</span> Needs improvement</li>
            </ul>
          </div>
        </div>

        <!-- TRIFR Explanation -->
        <div class="space-y-3">
          <div class="flex items-start gap-3">
            <div class="bg-purple-100 dark:bg-purple-900/30 p-2 rounded-lg mt-1">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-purple-600 dark:text-purple-400"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
            </div>
            <div>
              <p class="font-semibold text-slate-900 dark:text-slate-100">TRIFR (Total Recordable Injury Frequency Rate)</p>
              <p class="text-sm text-slate-600 dark:text-slate-400 mt-1">Includes all recordable injuries (LTI + medical treatment + restricted work)</p>
            </div>
          </div>

          <div class="bg-white dark:bg-slate-800 p-3 rounded-lg border border-slate-200 dark:border-slate-700 space-y-2">
            <p class="text-xs font-mono font-semibold text-slate-700 dark:text-slate-300">Formula:</p>
            <p class="text-xs font-mono text-slate-600 dark:text-slate-400">TRIFR = LTIFR × 2.5</p>

            <p class="text-xs font-mono font-semibold text-slate-700 dark:text-slate-300 mt-2">Calculation:</p>
            <ul class="text-xs text-slate-600 dark:text-slate-400 space-y-1 list-disc list-inside">
              <li>Based on LTIFR calculation</li>
              <li>Multiplied by 2.5 (industry standard ratio)</li>
              <li>Represents broader injury categories</li>
              <li>More comprehensive safety indicator</li>
            </ul>

            <p class="text-xs font-mono font-semibold text-slate-700 dark:text-slate-300 mt-2">Interpretation:</p>
            <ul class="text-xs text-slate-600 dark:text-slate-400 space-y-1 list-disc list-inside">
              <li><span class="font-semibold">0-15:</span> Excellent safety performance</li>
              <li><span class="font-semibold">15-25:</span> Good safety performance</li>
              <li><span class="font-semibold">&gt;25:</span> Needs improvement</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Key Notes -->
      <div class="mt-4 p-3 bg-white dark:bg-slate-800 rounded-lg border border-blue-200 dark:border-blue-700">
        <p class="text-xs font-semibold text-slate-900 dark:text-slate-100 mb-2">📌 Key Notes:</p>
        <ul class="text-xs text-slate-600 dark:text-slate-400 space-y-1 list-disc list-inside">
          <li>Uses <span class="font-semibold">30-day rolling average</span> for stable and meaningful rates</li>
          <li>Counts <span class="font-semibold">unique employees</span> who worked in the period</li>
          <li>Assumes <span class="font-semibold">12-hour shifts</span> per day (offshore standard)</li>
          <li>Updated <span class="font-semibold">daily</span> with real-time incident and POB data</li>
          <li>Lower rates indicate <span class="font-semibold">better safety performance</span></li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { themeState } from '@/store/theme';
import { authState } from '@/store/auth';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';

const loading = ref(true);
const selectedRange = ref('weekly');
const metricsData = ref([]);
const latestMetrics = ref(null);

const dateRanges = [
  { label: 'Last 7 Days', value: 'weekly' },
  { label: 'Last 30 Days', value: 'monthly' }
];

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: {
      display: true,
      position: 'top',
      labels: {
        color: themeState.isDark ? '#E8EAED' : '#33363A',
        font: { size: 12 }
      }
    },
    tooltip: {
      backgroundColor: themeState.isDark ? '#1A1F26' : '#FFFFFF',
      titleColor: themeState.isDark ? '#E8EAED' : '#33363A',
      bodyColor: themeState.isDark ? '#E8EAED' : '#33363A',
      borderColor: themeState.isDark ? '#2D3139' : '#E5E7EB',
      borderWidth: 1
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        color: themeState.isDark ? '#9CA3AF' : '#6B7280'
      },
      grid: {
        color: themeState.isDark ? '#2D3139' : '#E5E7EB'
      }
    },
    x: {
      ticks: {
        color: themeState.isDark ? '#9CA3AF' : '#6B7280'
      },
      grid: {
        color: themeState.isDark ? '#2D3139' : '#E5E7EB'
      }
    }
  }
}));

const ltiChartData = computed(() => ({
  labels: metricsData.value.map(m => new Date(m.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })),
  datasets: [{
    label: 'Days Without LTI',
    data: metricsData.value.map(m => m.days_without_lti),
    borderColor: themeState.isDark ? 'rgb(74, 222, 128)' : 'rgb(34, 197, 94)',
    backgroundColor: themeState.isDark ? 'rgba(74, 222, 128, 0.1)' : 'rgba(34, 197, 94, 0.1)',
    tension: 0.4
  }]
}));

const ptwChartData = computed(() => ({
  labels: metricsData.value.map(m => new Date(m.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })),
  datasets: [
    {
      label: 'PTW Issued',
      data: metricsData.value.map(m => m.total_ptw_issued),
      borderColor: themeState.isDark ? 'rgb(96, 165, 250)' : 'rgb(59, 130, 246)',
      backgroundColor: themeState.isDark ? 'rgba(96, 165, 250, 0.1)' : 'rgba(59, 130, 246, 0.1)',
      tension: 0.4
    },
    {
      label: 'PTW Completed',
      data: metricsData.value.map(m => m.total_ptw_completed),
      borderColor: themeState.isDark ? 'rgb(74, 222, 128)' : 'rgb(34, 197, 94)',
      backgroundColor: themeState.isDark ? 'rgba(74, 222, 128, 0.1)' : 'rgba(34, 197, 94, 0.1)',
      tension: 0.4
    }
  ]
}));

const incidentChartData = computed(() => ({
  labels: metricsData.value.map(m => new Date(m.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })),
  datasets: [
    {
      label: 'Total Incidents',
      data: metricsData.value.map(m => m.total_incidents),
      borderColor: themeState.isDark ? 'rgb(248, 113, 113)' : 'rgb(239, 68, 68)',
      backgroundColor: themeState.isDark ? 'rgba(248, 113, 113, 0.1)' : 'rgba(239, 68, 68, 0.1)',
      tension: 0.4
    },
    {
      label: 'Near Misses',
      data: metricsData.value.map(m => m.near_misses_count),
      borderColor: themeState.isDark ? 'rgb(253, 186, 116)' : 'rgb(251, 146, 60)',
      backgroundColor: themeState.isDark ? 'rgba(253, 186, 116, 0.1)' : 'rgba(251, 146, 60, 0.1)',
      tension: 0.4
    }
  ]
}));

const safetyRatesChartData = computed(() => ({
  labels: metricsData.value.map(m => new Date(m.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })),
  datasets: [
    {
      label: 'LTIFR',
      data: metricsData.value.map(m => m.ltifr || 0),
      borderColor: themeState.isDark ? 'rgb(253, 224, 71)' : 'rgb(245, 158, 11)',
      backgroundColor: themeState.isDark ? 'rgba(253, 224, 71, 0.1)' : 'rgba(245, 158, 11, 0.1)',
      tension: 0.4
    },
    {
      label: 'TRIFR',
      data: metricsData.value.map(m => m.trifr || 0),
      borderColor: themeState.isDark ? 'rgb(196, 181, 253)' : 'rgb(168, 85, 247)',
      backgroundColor: themeState.isDark ? 'rgba(196, 181, 253, 0.1)' : 'rgba(168, 85, 247, 0.1)',
      tension: 0.4
    }
  ]
}));

const fetchMetrics = async () => {
  loading.value = true;
  try {
    const endpoint = selectedRange.value === 'weekly' ? 'weekly_summary' : 'monthly_summary';
    const vesselParam = authState.selectedVessel ? `?vessel=${authState.selectedVessel.asset_id}` : '';
    const response = await fetch(`${API_BASE_URL}/hse/analytics/metrics/${endpoint}/${vesselParam}`, {
      credentials: 'include'
    });

    if (response.ok) {
      const data = await response.json();
      metricsData.value = data.reverse();
      latestMetrics.value = data[data.length - 1];
    }
  } catch (error) {
    console.error('Failed to fetch safety metrics:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchMetrics();
});
</script>
