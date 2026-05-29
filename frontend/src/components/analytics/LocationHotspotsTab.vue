<template>
  <div class="space-y-6">
    <!-- Risk Threshold Filter -->
    <div class="flex gap-4 items-center">
      <label class="text-sm font-medium text-slate-700 dark:text-slate-300">Risk Threshold:</label>
      <input
        v-model.number="riskThreshold"
        type="range"
        min="0"
        max="100"
        step="5"
        @change="fetchHotspots()"
        class="w-48"
      />
      <span class="text-sm font-semibold text-slate-900 dark:text-slate-100">{{ riskThreshold }}</span>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[var(--color-saipem-primary)]"></div>
    </div>

    <!-- Hotspots Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="location in hotspotsData"
        :key="location.id"
        class="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-hidden hover:shadow-lg transition-shadow"
      >
        <!-- Risk Score Header -->
        <div
          :class="[
            'p-4 text-white font-semibold flex items-center justify-between',
            location.risk_score >= 75
              ? 'bg-red-500'
              : location.risk_score >= 50
              ? 'bg-orange-500'
              : 'bg-yellow-500'
          ]"
        >
          <span>{{ location.location_name }}</span>
          <span class="text-2xl font-bold">{{ location.risk_score.toFixed(1) }}</span>
        </div>

        <!-- Location Details -->
        <div class="p-4 space-y-3">
          <div class="flex justify-between items-center">
            <span class="text-sm text-slate-600 dark:text-slate-400">Date</span>
            <span class="text-sm font-medium text-slate-900 dark:text-slate-100">{{ formatDate(location.date) }}</span>
          </div>

          <div class="flex justify-between items-center">
            <span class="text-sm text-slate-600 dark:text-slate-400">Avg Occupancy</span>
            <span class="text-sm font-medium text-slate-900 dark:text-slate-100">{{ location.average_occupancy.toFixed(1) }} ppl</span>
          </div>

          <div class="flex justify-between items-center">
            <span class="text-sm text-slate-600 dark:text-slate-400">Peak Occupancy</span>
            <span class="text-sm font-medium text-slate-900 dark:text-slate-100">{{ location.peak_occupancy }} ppl</span>
          </div>

          <div class="flex justify-between items-center">
            <span class="text-sm text-slate-600 dark:text-slate-400">Incidents</span>
            <span class="text-sm font-medium text-red-600 dark:text-red-400 font-semibold">{{ location.total_incidents }}</span>
          </div>

          <div class="flex justify-between items-center">
            <span class="text-sm text-slate-600 dark:text-slate-400">PTW Issued</span>
            <span class="text-sm font-medium text-slate-900 dark:text-slate-100">{{ location.total_ptw_issued }}</span>
          </div>

          <div class="flex justify-between items-center">
            <span class="text-sm text-slate-600 dark:text-slate-400">Check-ins</span>
            <span class="text-sm font-medium text-slate-900 dark:text-slate-100">{{ location.total_check_ins }}</span>
          </div>

          <!-- Risk Indicator -->
          <div class="pt-2 border-t border-slate-200 dark:border-slate-700">
            <div class="flex items-center gap-2">
              <div class="flex-1 bg-slate-200 dark:bg-slate-700 rounded-full h-2 overflow-hidden">
                <div
                  :class="[
                    'h-full transition-all',
                    location.risk_score >= 75
                      ? 'bg-red-500'
                      : location.risk_score >= 50
                      ? 'bg-orange-500'
                      : 'bg-yellow-500'
                  ]"
                  :style="{ width: `${location.risk_score}%` }"
                ></div>
              </div>
              <span class="text-xs font-medium text-slate-600 dark:text-slate-400">
                {{ location.risk_score >= 75 ? 'HIGH' : location.risk_score >= 50 ? 'MEDIUM' : 'LOW' }}
              </span>
            </div>
          </div>

          <!-- View Trend Button -->
          <button
            @click="viewLocationTrend(location.location_name)"
            class="w-full mt-3 px-3 py-2 bg-[var(--color-saipem-primary)] text-white rounded-lg text-sm font-medium hover:bg-[var(--color-saipem-primary)]/90 transition-colors"
          >
            View Trend
          </button>
        </div>
      </div>

      <div v-if="hotspotsData.length === 0" class="col-span-full py-12 text-center">
        <p class="text-slate-500">No locations found with risk score above {{ riskThreshold }}</p>
      </div>
    </div>

    <!-- All Locations Summary -->
    <div v-if="!loading && allLocationsData.length > 0" class="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-6">
      <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">All Locations Summary</h3>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="border-b border-slate-200 dark:border-slate-700">
            <tr>
              <th class="text-left py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Location</th>
              <th class="text-center py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Risk Score</th>
              <th class="text-center py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Avg Occupancy</th>
              <th class="text-center py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Incidents</th>
              <th class="text-center py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">PTW Issued</th>
              <th class="text-center py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="location in allLocationsData" :key="location.id" class="border-b border-slate-100 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700">
              <td class="py-3 px-4 text-slate-900 dark:text-slate-100 font-medium">{{ location.location_name }}</td>
              <td class="text-center py-3 px-4">
                <span class="font-semibold text-slate-900 dark:text-slate-100">{{ location.risk_score.toFixed(1) }}</span>
              </td>
              <td class="text-center py-3 px-4 text-slate-600 dark:text-slate-400">{{ location.average_occupancy.toFixed(1) }}</td>
              <td class="text-center py-3 px-4">
                <span class="text-red-600 dark:text-red-400 font-semibold">{{ location.total_incidents }}</span>
              </td>
              <td class="text-center py-3 px-4 text-slate-600 dark:text-slate-400">{{ location.total_ptw_issued }}</td>
              <td class="text-center py-3 px-4">
                <span
                  :class="[
                    'px-2 py-1 rounded text-xs font-medium',
                    location.risk_score >= 75
                      ? 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
                      : location.risk_score >= 50
                      ? 'bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400'
                      : 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400'
                  ]"
                >
                  {{ location.risk_score >= 75 ? 'HIGH' : location.risk_score >= 50 ? 'MEDIUM' : 'LOW' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Location Trend Modal -->
    <div
      v-if="showTrendModal"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
      @click="showTrendModal = false"
    >
      <div class="bg-white dark:bg-slate-800 rounded-xl max-w-4xl w-full max-h-[80vh] overflow-y-auto p-6" @click.stop>
        <div class="flex justify-between items-start mb-4">
          <div>
            <h2 class="text-xl font-bold text-slate-900 dark:text-slate-100">{{ selectedLocationName }} - 30 Day Trend</h2>
            <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">Historical risk and activity data</p>
          </div>
          <button @click="showTrendModal = false" class="text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        </div>

        <!-- Loading State -->
        <div v-if="loadingTrend" class="flex justify-center items-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[var(--color-saipem-primary)]"></div>
        </div>

        <!-- Trend Data -->
        <div v-else-if="trendData.length > 0" class="space-y-6">
          <!-- Summary Cards -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-200 dark:border-blue-700">
              <p class="text-xs font-medium text-blue-600 dark:text-blue-400">Avg Risk Score</p>
              <p class="text-2xl font-bold text-blue-900 dark:text-blue-100 mt-1">{{ calculateAvgRisk().toFixed(1) }}</p>
            </div>
            <div class="bg-red-50 dark:bg-red-900/20 p-4 rounded-lg border border-red-200 dark:border-red-700">
              <p class="text-xs font-medium text-red-600 dark:text-red-400">Total Incidents</p>
              <p class="text-2xl font-bold text-red-900 dark:text-red-100 mt-1">{{ calculateTotalIncidents() }}</p>
            </div>
            <div class="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg border border-green-200 dark:border-green-700">
              <p class="text-xs font-medium text-green-600 dark:text-green-400">Total PTWs</p>
              <p class="text-2xl font-bold text-green-900 dark:text-green-100 mt-1">{{ calculateTotalPTWs() }}</p>
            </div>
            <div class="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg border border-purple-200 dark:border-purple-700">
              <p class="text-xs font-medium text-purple-600 dark:text-purple-400">Avg Occupancy</p>
              <p class="text-2xl font-bold text-purple-900 dark:text-purple-100 mt-1">{{ calculateAvgOccupancy().toFixed(1) }}</p>
            </div>
          </div>

          <!-- Trend Table -->
          <div class="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-hidden">
            <div class="overflow-x-auto">
              <table class="w-full text-sm">
                <thead class="bg-slate-50 dark:bg-slate-700 border-b border-slate-200 dark:border-slate-600">
                  <tr>
                    <th class="text-left py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Date</th>
                    <th class="text-center py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Risk Score</th>
                    <th class="text-center py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Occupancy</th>
                    <th class="text-center py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Incidents</th>
                    <th class="text-center py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">PTWs</th>
                    <th class="text-center py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Check-ins</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="trend in trendData" :key="trend.id" class="border-b border-slate-100 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700">
                    <td class="py-3 px-4 text-slate-900 dark:text-slate-100">{{ formatDate(trend.date) }}</td>
                    <td class="text-center py-3 px-4">
                      <span
                        :class="[
                          'px-2 py-1 rounded text-xs font-semibold',
                          trend.risk_score >= 75
                            ? 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
                            : trend.risk_score >= 50
                            ? 'bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400'
                            : 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400'
                        ]"
                      >
                        {{ trend.risk_score.toFixed(1) }}
                      </span>
                    </td>
                    <td class="text-center py-3 px-4 text-slate-600 dark:text-slate-400">{{ trend.average_occupancy.toFixed(1) }}</td>
                    <td class="text-center py-3 px-4">
                      <span class="text-red-600 dark:text-red-400 font-semibold">{{ trend.total_incidents }}</span>
                    </td>
                    <td class="text-center py-3 px-4 text-slate-600 dark:text-slate-400">{{ trend.total_ptw_issued }}</td>
                    <td class="text-center py-3 px-4 text-slate-600 dark:text-slate-400">{{ trend.total_check_ins }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- No Data -->
        <div v-else class="py-12 text-center">
          <p class="text-slate-500 dark:text-slate-400">No trend data available for this location</p>
        </div>
      </div>
    </div>

    <!-- Risk Assessment Explanation -->
    <div class="bg-gradient-to-r from-orange-50 to-red-50 dark:from-orange-900/20 dark:to-red-900/20 p-6 rounded-xl border border-orange-200 dark:border-orange-700">
      <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">🎯 Location Risk Assessment & Hotspot Analysis</h3>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <!-- Low Risk -->
        <div class="bg-white dark:bg-slate-800 p-4 rounded-lg border border-yellow-200 dark:border-yellow-700">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
            <p class="font-semibold text-slate-900 dark:text-slate-100">LOW RISK</p>
          </div>
          <p class="text-xs text-slate-600 dark:text-slate-400 mb-2">Safe location with minimal hazards</p>
          <p class="text-xs font-mono text-slate-500 dark:text-slate-500">Score: 0-50</p>
        </div>

        <!-- Medium Risk -->
        <div class="bg-white dark:bg-slate-800 p-4 rounded-lg border border-orange-200 dark:border-orange-700">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-3 h-3 rounded-full bg-orange-500"></div>
            <p class="font-semibold text-slate-900 dark:text-slate-100">MEDIUM RISK</p>
          </div>
          <p class="text-xs text-slate-600 dark:text-slate-400 mb-2">Moderate hazards requiring attention</p>
          <p class="text-xs font-mono text-slate-500 dark:text-slate-500">Score: 50-75</p>
        </div>

        <!-- High Risk -->
        <div class="bg-white dark:bg-slate-800 p-4 rounded-lg border border-red-200 dark:border-red-700">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-3 h-3 rounded-full bg-red-500"></div>
            <p class="font-semibold text-slate-900 dark:text-slate-100">HIGH RISK</p>
          </div>
          <p class="text-xs text-slate-600 dark:text-slate-400 mb-2">Significant hazards - immediate action needed</p>
          <p class="text-xs font-mono text-slate-500 dark:text-slate-500">Score: 75-100</p>
        </div>
      </div>

      <!-- Risk Calculation -->
      <div class="bg-white dark:bg-slate-800 p-4 rounded-lg border border-slate-200 dark:border-slate-700 space-y-3 mb-4">
        <p class="text-sm font-semibold text-slate-900 dark:text-slate-100">📊 Risk Score Calculation:</p>

        <div class="space-y-2">
          <div class="text-xs text-slate-600 dark:text-slate-400">
            <p class="font-mono font-semibold text-slate-700 dark:text-slate-300">Risk Score = (Incident Weight × 40%) + (Occupancy Weight × 30%) + (PTW Weight × 30%)</p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mt-3">
            <div class="bg-red-50 dark:bg-red-900/20 p-3 rounded border border-red-200 dark:border-red-700">
              <p class="text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Incident Weight (40%)</p>
              <p class="text-xs text-slate-600 dark:text-slate-400">More incidents = higher risk</p>
              <p class="text-xs font-mono text-slate-500 dark:text-slate-500 mt-1">Max: 10 incidents</p>
            </div>

            <div class="bg-blue-50 dark:bg-blue-900/20 p-3 rounded border border-blue-200 dark:border-blue-700">
              <p class="text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Occupancy Weight (30%)</p>
              <p class="text-xs text-slate-600 dark:text-slate-400">More people = higher risk</p>
              <p class="text-xs font-mono text-slate-500 dark:text-slate-500 mt-1">Max: 50 people</p>
            </div>

            <div class="bg-green-50 dark:bg-green-900/20 p-3 rounded border border-green-200 dark:border-green-700">
              <p class="text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">PTW Weight (30%)</p>
              <p class="text-xs text-slate-600 dark:text-slate-400">More permits = higher risk</p>
              <p class="text-xs font-mono text-slate-500 dark:text-slate-500 mt-1">Max: 20 PTWs</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Key Metrics -->
      <div class="bg-white dark:bg-slate-800 p-4 rounded-lg border border-slate-200 dark:border-slate-700 space-y-3">
        <p class="text-sm font-semibold text-slate-900 dark:text-slate-100">📌 Key Metrics Explained:</p>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div>
            <p class="text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Average Occupancy</p>
            <p class="text-xs text-slate-600 dark:text-slate-400">Average number of people at location per day. Higher occupancy = more exposure to hazards.</p>
          </div>

          <div>
            <p class="text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Peak Occupancy</p>
            <p class="text-xs text-slate-600 dark:text-slate-400">Maximum number of people at location at any time. Indicates capacity stress.</p>
          </div>

          <div>
            <p class="text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Total Incidents</p>
            <p class="text-xs text-slate-600 dark:text-slate-400">Number of safety incidents reported at this location. Higher = more hazardous area.</p>
          </div>

          <div>
            <p class="text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">PTW Issued</p>
            <p class="text-xs text-slate-600 dark:text-slate-400">Number of work permits issued. Indicates work activity level and complexity.</p>
          </div>

          <div>
            <p class="text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Check-ins</p>
            <p class="text-xs text-slate-600 dark:text-slate-400">Number of personnel check-ins. Tracks who is present at location.</p>
          </div>

          <div>
            <p class="text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">30-Day Trend</p>
            <p class="text-xs text-slate-600 dark:text-slate-400">Historical data showing how risk has changed over time. Click "View Trend" to see details.</p>
          </div>
        </div>
      </div>

      <!-- Action Items -->
      <div class="mt-4 p-3 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-700">
        <p class="text-xs font-semibold text-slate-900 dark:text-slate-100 mb-2">⚠️ Action Items by Risk Level:</p>
        <ul class="text-xs text-slate-600 dark:text-slate-400 space-y-1 list-disc list-inside">
          <li><span class="font-semibold">HIGH RISK (75+):</span> Immediate investigation required. Increase supervision and safety measures.</li>
          <li><span class="font-semibold">MEDIUM RISK (50-75):</span> Monitor closely. Implement preventive measures. Review incident patterns.</li>
          <li><span class="font-semibold">LOW RISK (&lt;50):</span> Maintain current safety standards. Continue regular monitoring.</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { authState } from '@/store/auth';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';

const loading = ref(true);
const riskThreshold = ref(50);
const hotspotsData = ref([]);
const allLocationsData = ref([]);

// Trend modal states
const showTrendModal = ref(false);
const selectedLocationName = ref('');
const trendData = ref([]);
const loadingTrend = ref(false);

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

const fetchHotspots = async () => {
  loading.value = true;
  try {
    const vesselParam = authState.selectedVessel ? `&vessel=${authState.selectedVessel.asset_id}` : '';
    const response = await fetch(
      `${API_BASE_URL}/hse/analytics/locations/hotspots/?threshold=${riskThreshold.value}&limit=20${vesselParam}`,
      { credentials: 'include' }
    );

    if (response.ok) {
      hotspotsData.value = await response.json();
    }
  } catch (error) {
    console.error('Failed to fetch hotspots:', error);
  } finally {
    loading.value = false;
  }
};

const fetchAllLocations = async () => {
  try {
    const vesselParam = authState.selectedVessel ? `?vessel=${authState.selectedVessel.asset_id}` : '';
    const response = await fetch(`${API_BASE_URL}/hse/analytics/locations/summary/${vesselParam}`, {
      credentials: 'include'
    });

    if (response.ok) {
      allLocationsData.value = await response.json();
    }
  } catch (error) {
    console.error('Failed to fetch location summary:', error);
  }
};

const viewLocationTrend = async (locationName) => {
  selectedLocationName.value = locationName;
  showTrendModal.value = true;
  loadingTrend.value = true;
  trendData.value = [];

  try {
    const vesselParam = authState.selectedVessel ? `&vessel=${authState.selectedVessel.asset_id}` : '';
    const response = await fetch(
      `${API_BASE_URL}/hse/analytics/locations/location_trend/?location=${encodeURIComponent(locationName)}&days=30${vesselParam}`,
      { credentials: 'include' }
    );

    if (response.ok) {
      trendData.value = await response.json();
    } else {
      console.error('Failed to fetch trend data:', response.status);
    }
  } catch (error) {
    console.error('Failed to fetch location trend:', error);
  } finally {
    loadingTrend.value = false;
  }
};

const calculateAvgRisk = () => {
  if (trendData.value.length === 0) return 0;
  const sum = trendData.value.reduce((acc, item) => acc + item.risk_score, 0);
  return sum / trendData.value.length;
};

const calculateTotalIncidents = () => {
  return trendData.value.reduce((acc, item) => acc + item.total_incidents, 0);
};

const calculateTotalPTWs = () => {
  return trendData.value.reduce((acc, item) => acc + item.total_ptw_issued, 0);
};

const calculateAvgOccupancy = () => {
  if (trendData.value.length === 0) return 0;
  const sum = trendData.value.reduce((acc, item) => acc + item.average_occupancy, 0);
  return sum / trendData.value.length;
};

onMounted(() => {
  fetchHotspots();
  fetchAllLocations();
});
</script>
