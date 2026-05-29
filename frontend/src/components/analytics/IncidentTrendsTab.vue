<template>
  <div class="space-y-6">
    <!-- Period Type Filter -->
    <div class="flex gap-2 flex-wrap">
      <button
        v-for="period in periodTypes"
        :key="period.value"
        @click="selectedPeriod = period.value; fetchTrends()"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-colors',
          selectedPeriod === period.value
            ? 'bg-[var(--color-saipem-primary)] text-white'
            : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'
        ]"
      >
        {{ period.label }}
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[var(--color-saipem-primary)]"></div>
    </div>

    <!-- Summary Cards -->
    <div v-else class="grid grid-cols-2 md:grid-cols-5 gap-4">
      <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-200 dark:border-blue-700">
        <p class="text-xs font-medium text-blue-600 dark:text-blue-400">Safety Observations</p>
        <p class="text-2xl font-bold text-blue-900 dark:text-blue-100 mt-1">{{ totalStats.safety_observation_count }}</p>
      </div>
      <div class="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg border border-yellow-200 dark:border-yellow-700">
        <p class="text-xs font-medium text-yellow-600 dark:text-yellow-400">Near Misses</p>
        <p class="text-2xl font-bold text-yellow-900 dark:text-yellow-100 mt-1">{{ totalStats.near_miss_count }}</p>
      </div>
      <div class="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg border border-orange-200 dark:border-orange-700">
        <p class="text-xs font-medium text-orange-600 dark:text-orange-400">First Aid</p>
        <p class="text-2xl font-bold text-orange-900 dark:text-orange-100 mt-1">{{ totalStats.first_aid_count }}</p>
      </div>
      <div class="bg-red-50 dark:bg-red-900/20 p-4 rounded-lg border border-red-200 dark:border-red-700">
        <p class="text-xs font-medium text-red-600 dark:text-red-400">LTI</p>
        <p class="text-2xl font-bold text-red-900 dark:text-red-100 mt-1">{{ totalStats.lti_count }}</p>
      </div>
      <div class="bg-slate-50 dark:bg-slate-800 p-4 rounded-lg border border-slate-200 dark:border-slate-700">
        <p class="text-xs font-medium text-slate-600 dark:text-slate-400">Total</p>
        <p class="text-2xl font-bold text-slate-900 dark:text-slate-100 mt-1">{{ totalStats.total_incidents }}</p>
      </div>
    </div>

    <!-- Charts -->
    <div v-if="!loading" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Incidents by Severity -->
      <div class="bg-white dark:bg-slate-800 p-6 rounded-xl border border-slate-200 dark:border-slate-700">
        <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">Incidents by Severity</h3>
        <Bar :data="severityChartData" :options="chartOptions" />
      </div>

      <!-- Total Incidents Trend -->
      <div class="bg-white dark:bg-slate-800 p-6 rounded-xl border border-slate-200 dark:border-slate-700">
        <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">Total Incidents Trend</h3>
        <Line :data="trendChartData" :options="chartOptions" />
      </div>

      <!-- Average Response Time -->
      <div class="bg-white dark:bg-slate-800 p-6 rounded-xl border border-slate-200 dark:border-slate-700">
        <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">Average Response Time</h3>
        <Line :data="responseTimeChartData" :options="chartOptions" />
      </div>

      <!-- Days Without LTI -->
      <div class="bg-white dark:bg-slate-800 p-6 rounded-xl border border-slate-200 dark:border-slate-700">
        <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">Days Without LTI</h3>
        <Line :data="daysWithoutLTIChartData" :options="chartOptions" />
      </div>
    </div>

    <!-- Trends Table -->
    <div v-if="!loading && trendsData.length > 0" class="bg-white dark:bg-slate-800 p-6 rounded-xl border border-slate-200 dark:border-slate-700">
      <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">Detailed Trends</h3>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="border-b border-slate-200 dark:border-slate-700">
            <tr>
              <th class="text-left py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Period</th>
              <th class="text-center py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Safety Obs</th>
              <th class="text-center py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Near Miss</th>
              <th class="text-center py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">First Aid</th>
              <th class="text-center py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">LTI</th>
              <th class="text-center py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Total</th>
              <th class="text-center py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Avg Response (hrs)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="trend in trendsData" :key="trend.id" class="border-b border-slate-100 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700">
              <td class="py-3 px-4 text-slate-900 dark:text-slate-100">{{ formatPeriod(trend) }}</td>
              <td class="text-center py-3 px-4 text-blue-600 dark:text-blue-400 font-medium">{{ trend.safety_observation_count }}</td>
              <td class="text-center py-3 px-4 text-yellow-600 dark:text-yellow-400 font-medium">{{ trend.near_miss_count }}</td>
              <td class="text-center py-3 px-4 text-orange-600 dark:text-orange-400 font-medium">{{ trend.first_aid_count }}</td>
              <td class="text-center py-3 px-4 text-red-600 dark:text-red-400 font-medium">{{ trend.lti_count }}</td>
              <td class="text-center py-3 px-4 text-slate-900 dark:text-slate-100 font-semibold">{{ trend.total_incidents }}</td>
              <td class="text-center py-3 px-4 text-slate-600 dark:text-slate-400">{{ trend.average_response_time?.toFixed(1) || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Incident Classification Explanation -->
    <div class="bg-gradient-to-r from-red-50 to-orange-50 dark:from-red-900/20 dark:to-orange-900/20 p-6 rounded-xl border border-red-200 dark:border-red-700">
      <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">📊 Incident Classification & Severity Levels</h3>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <!-- Safety Observation -->
        <div class="bg-white dark:bg-slate-800 p-4 rounded-lg border border-blue-200 dark:border-blue-700">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-3 h-3 rounded-full bg-blue-500"></div>
            <p class="font-semibold text-slate-900 dark:text-slate-100">Safety Observation</p>
          </div>
          <p class="text-xs text-slate-600 dark:text-slate-400 mb-2">Potential hazard identified before injury occurs</p>
          <p class="text-xs font-mono text-slate-500 dark:text-slate-500">Severity: LOW</p>
        </div>

        <!-- Near Miss -->
        <div class="bg-white dark:bg-slate-800 p-4 rounded-lg border border-yellow-200 dark:border-yellow-700">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
            <p class="font-semibold text-slate-900 dark:text-slate-100">Near Miss</p>
          </div>
          <p class="text-xs text-slate-600 dark:text-slate-400 mb-2">Incident that could have caused injury but didn't</p>
          <p class="text-xs font-mono text-slate-500 dark:text-slate-500">Severity: LOW-MEDIUM</p>
        </div>

        <!-- First Aid -->
        <div class="bg-white dark:bg-slate-800 p-4 rounded-lg border border-orange-200 dark:border-orange-700">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-3 h-3 rounded-full bg-orange-500"></div>
            <p class="font-semibold text-slate-900 dark:text-slate-100">First Aid</p>
          </div>
          <p class="text-xs text-slate-600 dark:text-slate-400 mb-2">Minor injury requiring basic medical treatment</p>
          <p class="text-xs font-mono text-slate-500 dark:text-slate-500">Severity: MEDIUM</p>
        </div>

        <!-- LTI -->
        <div class="bg-white dark:bg-slate-800 p-4 rounded-lg border border-red-200 dark:border-red-700">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-3 h-3 rounded-full bg-red-500"></div>
            <p class="font-semibold text-slate-900 dark:text-slate-100">LTI (Lost Time Injury)</p>
          </div>
          <p class="text-xs text-slate-600 dark:text-slate-400 mb-2">Serious injury causing lost work time</p>
          <p class="text-xs font-mono text-slate-500 dark:text-slate-500">Severity: CRITICAL</p>
        </div>
      </div>

      <!-- Key Metrics Explanation -->
      <div class="bg-white dark:bg-slate-800 p-4 rounded-lg border border-slate-200 dark:border-slate-700 space-y-3">
        <p class="text-sm font-semibold text-slate-900 dark:text-slate-100">📌 Key Metrics:</p>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p class="text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Total Incidents</p>
            <p class="text-xs text-slate-600 dark:text-slate-400">Sum of all incident types in the period. Higher numbers indicate more safety events.</p>
          </div>

          <div>
            <p class="text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Average Response Time</p>
            <p class="text-xs text-slate-600 dark:text-slate-400">Time from incident report to closure (in hours). Lower is better - indicates faster resolution.</p>
          </div>

          <div>
            <p class="text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Days Without LTI</p>
            <p class="text-xs text-slate-600 dark:text-slate-400">Consecutive days with no lost-time injuries. Key safety performance indicator.</p>
          </div>

          <div>
            <p class="text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Trend Analysis</p>
            <p class="text-xs text-slate-600 dark:text-slate-400">Upward trend = increasing incidents (concern). Downward trend = improving safety (positive).</p>
          </div>
        </div>
      </div>

      <!-- Interpretation Guide -->
      <div class="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-700">
        <p class="text-xs font-semibold text-slate-900 dark:text-slate-100 mb-2">💡 How to Interpret:</p>
        <ul class="text-xs text-slate-600 dark:text-slate-400 space-y-1 list-disc list-inside">
          <li><span class="font-semibold">Increasing total incidents:</span> May indicate better reporting culture OR actual safety issues</li>
          <li><span class="font-semibold">High LTI count:</span> Immediate action required - investigate root causes</li>
          <li><span class="font-semibold">Long response times:</span> Improve incident handling procedures</li>
          <li><span class="font-semibold">More safety observations:</span> Good - proactive hazard identification</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { Bar, Line } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { themeState } from '@/store/theme';
import { authState } from '@/store/auth';

ChartJS.register(CategoryScale, LinearScale, BarElement, PointElement, LineElement, Title, Tooltip, Legend);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';

const loading = ref(true);
const selectedPeriod = ref('MONTHLY');
const trendsData = ref([]);

const periodTypes = [
  { label: 'Daily', value: 'DAILY' },
  { label: 'Weekly', value: 'WEEKLY' },
  { label: 'Monthly', value: 'MONTHLY' },
  { label: 'Quarterly', value: 'QUARTERLY' },
  { label: 'Yearly', value: 'YEARLY' }
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

const totalStats = computed(() => {
  if (trendsData.value.length === 0) {
    return { safety_observation_count: 0, near_miss_count: 0, first_aid_count: 0, lti_count: 0, total_incidents: 0 };
  }
  return trendsData.value.reduce((acc, trend) => ({
    safety_observation_count: acc.safety_observation_count + trend.safety_observation_count,
    near_miss_count: acc.near_miss_count + trend.near_miss_count,
    first_aid_count: acc.first_aid_count + trend.first_aid_count,
    lti_count: acc.lti_count + trend.lti_count,
    total_incidents: acc.total_incidents + trend.total_incidents
  }), { safety_observation_count: 0, near_miss_count: 0, first_aid_count: 0, lti_count: 0, total_incidents: 0 });
});

const severityChartData = computed(() => ({
  labels: trendsData.value.map(t => formatPeriod(t)),
  datasets: [
    {
      label: 'Safety Observations',
      data: trendsData.value.map(t => t.safety_observation_count),
      backgroundColor: themeState.isDark ? 'rgba(96, 165, 250, 0.8)' : 'rgba(59, 130, 246, 0.8)'
    },
    {
      label: 'Near Misses',
      data: trendsData.value.map(t => t.near_miss_count),
      backgroundColor: themeState.isDark ? 'rgba(253, 186, 116, 0.8)' : 'rgba(251, 146, 60, 0.8)'
    },
    {
      label: 'First Aid',
      data: trendsData.value.map(t => t.first_aid_count),
      backgroundColor: themeState.isDark ? 'rgba(251, 146, 60, 0.8)' : 'rgba(249, 115, 22, 0.8)'
    },
    {
      label: 'LTI',
      data: trendsData.value.map(t => t.lti_count),
      backgroundColor: themeState.isDark ? 'rgba(248, 113, 113, 0.8)' : 'rgba(239, 68, 68, 0.8)'
    }
  ]
}));

const trendChartData = computed(() => ({
  labels: trendsData.value.map(t => formatPeriod(t)),
  datasets: [{
    label: 'Total Incidents',
    data: trendsData.value.map(t => t.total_incidents),
    borderColor: themeState.isDark ? 'rgb(167, 139, 250)' : 'rgb(139, 92, 246)',
    backgroundColor: themeState.isDark ? 'rgba(167, 139, 250, 0.1)' : 'rgba(139, 92, 246, 0.1)',
    tension: 0.4
  }]
}));

const responseTimeChartData = computed(() => ({
  labels: trendsData.value.map(t => formatPeriod(t)),
  datasets: [{
    label: 'Avg Response Time (hours)',
    data: trendsData.value.map(t => t.average_response_time || 0),
    borderColor: themeState.isDark ? 'rgb(74, 222, 128)' : 'rgb(34, 197, 94)',
    backgroundColor: themeState.isDark ? 'rgba(74, 222, 128, 0.1)' : 'rgba(34, 197, 94, 0.1)',
    tension: 0.4
  }]
}));

const daysWithoutLTIChartData = computed(() => ({
  labels: trendsData.value.map(t => formatPeriod(t)),
  datasets: [{
    label: 'Days Without LTI',
    data: trendsData.value.map(t => t.days_without_lti),
    borderColor: themeState.isDark ? 'rgb(74, 222, 128)' : 'rgb(34, 197, 94)',
    backgroundColor: themeState.isDark ? 'rgba(74, 222, 128, 0.1)' : 'rgba(34, 197, 94, 0.1)',
    tension: 0.4
  }]
}));

const formatPeriod = (trend) => {
  const start = new Date(trend.period_start).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  const end = new Date(trend.period_end).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  return `${start} - ${end}`;
};

const fetchTrends = async () => {
  loading.value = true;
  try {
    const vesselParam = authState.selectedVessel ? `&vessel=${authState.selectedVessel.asset_id}` : '';
    const response = await fetch(
      `${API_BASE_URL}/hse/analytics/trends/?period_type=${selectedPeriod.value}&limit=12${vesselParam}`,
      { credentials: 'include' }
    );

    if (response.ok) {
      const data = await response.json();
      trendsData.value = data.reverse();
    }
  } catch (error) {
    console.error('Failed to fetch incident trends:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchTrends();
});
</script>
