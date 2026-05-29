<template>
  <div class="space-y-6">
    <!-- Filters -->
    <div class="flex gap-4 flex-wrap items-center">
      <div>
        <label class="text-sm font-medium text-slate-700 dark:text-slate-300">Report Type:</label>
        <select
          v-model="selectedReportType"
          @change="fetchReports()"
          class="mt-1 px-3 py-2 border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[var(--color-saipem-primary)]"
        >
          <option value="">All Types</option>
          <option value="DAILY">Daily</option>
          <option value="WEEKLY">Weekly</option>
          <option value="MONTHLY">Monthly</option>
          <option value="QUARTERLY">Quarterly</option>
          <option value="ANNUAL">Annual</option>
        </select>
      </div>

      <div>
        <label class="text-sm font-medium text-slate-700 dark:text-slate-300">Status:</label>
        <select
          v-model="selectedStatus"
          @change="fetchReports()"
          class="mt-1 px-3 py-2 border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[var(--color-saipem-primary)]"
        >
          <option value="">All Status</option>
          <option value="COMPLIANT">Compliant</option>
          <option value="PARTIAL">Partially Compliant</option>
          <option value="NON_COMPLIANT">Non-Compliant</option>
        </select>
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg border border-green-200 dark:border-green-700">
        <p class="text-xs font-medium text-green-600 dark:text-green-400">Compliant</p>
        <p class="text-2xl font-bold text-green-900 dark:text-green-100 mt-1">{{ summary.compliant }}</p>
      </div>
      <div class="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg border border-yellow-200 dark:border-yellow-700">
        <p class="text-xs font-medium text-yellow-600 dark:text-yellow-400">Partially Compliant</p>
        <p class="text-2xl font-bold text-yellow-900 dark:text-yellow-100 mt-1">{{ summary.partial_compliant }}</p>
      </div>
      <div class="bg-red-50 dark:bg-red-900/20 p-4 rounded-lg border border-red-200 dark:border-red-700">
        <p class="text-xs font-medium text-red-600 dark:text-red-400">Non-Compliant</p>
        <p class="text-2xl font-bold text-red-900 dark:text-red-100 mt-1">{{ summary.non_compliant }}</p>
      </div>
      <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-200 dark:border-blue-700">
        <p class="text-xs font-medium text-blue-600 dark:text-blue-400">Avg Score</p>
        <p class="text-2xl font-bold text-blue-900 dark:text-blue-100 mt-1">{{ summary.average_compliance_score }}%</p>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[var(--color-saipem-primary)]"></div>
    </div>

    <!-- Reports Table -->
    <div v-else class="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-slate-50 dark:bg-slate-700 border-b border-slate-200 dark:border-slate-600">
            <tr>
              <th class="text-left py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Report Date</th>
              <th class="text-left py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Type</th>
              <th class="text-left py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Period</th>
              <th class="text-center py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Score</th>
              <th class="text-center py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Status</th>
              <th class="text-center py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Checks</th>
              <th class="text-left py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Auditor</th>
              <th class="text-center py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="report in reportsData" :key="report.id" class="border-b border-slate-100 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700">
              <td class="py-3 px-4 text-slate-900 dark:text-slate-100">{{ formatDate(report.report_date) }}</td>
              <td class="py-3 px-4">
                <span class="px-2 py-1 rounded text-xs font-medium bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300">
                  {{ report.report_type }}
                </span>
              </td>
              <td class="py-3 px-4 text-slate-600 dark:text-slate-400 text-xs">
                {{ formatDate(report.period_start) }} to {{ formatDate(report.period_end) }}
              </td>
              <td class="text-center py-3 px-4">
                <span class="font-semibold text-slate-900 dark:text-slate-100">{{ report.compliance_score.toFixed(1) }}%</span>
              </td>
              <td class="text-center py-3 px-4">
                <span
                  :class="[
                    'px-2 py-1 rounded text-xs font-medium',
                    report.overall_status === 'COMPLIANT'
                      ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400'
                      : report.overall_status === 'PARTIAL'
                      ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400'
                      : 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
                  ]"
                >
                  {{ report.overall_status }}
                </span>
              </td>
              <td class="text-center py-3 px-4 text-slate-600 dark:text-slate-400">
                <span class="text-xs">{{ report.passed_checks }}/{{ report.total_checks }}</span>
              </td>
              <td class="py-3 px-4 text-slate-600 dark:text-slate-400 text-sm">{{ report.auditor_name }}</td>
              <td class="text-center py-3 px-4">
                <button
                  @click="viewReport(report)"
                  class="text-[var(--color-saipem-primary)] hover:text-[var(--color-saipem-primary)]/80 font-medium text-sm"
                >
                  View
                </button>
              </td>
            </tr>
            <tr v-if="reportsData.length === 0">
              <td colspan="8" class="py-8 px-4 text-center text-slate-500 dark:text-slate-400">
                No compliance reports found
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Report Details Modal -->
    <div
      v-if="selectedReport"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
      @click="selectedReport = null"
    >
      <div class="bg-white dark:bg-slate-800 rounded-xl max-w-2xl w-full max-h-96 overflow-y-auto p-6" @click.stop>
        <div class="flex justify-between items-start mb-4">
          <h2 class="text-xl font-bold text-slate-900 dark:text-slate-100">{{ selectedReport.report_type }} Report</h2>
          <button @click="selectedReport = null" class="text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        </div>

        <div class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-slate-600 dark:text-slate-400">Report Date</p>
              <p class="font-semibold text-slate-900 dark:text-slate-100">{{ formatDate(selectedReport.report_date) }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-600 dark:text-slate-400">Compliance Score</p>
              <p class="font-semibold text-slate-900 dark:text-slate-100">{{ selectedReport.compliance_score.toFixed(1) }}%</p>
            </div>
            <div>
              <p class="text-sm text-slate-600 dark:text-slate-400">Status</p>
              <p class="font-semibold text-slate-900 dark:text-slate-100">{{ selectedReport.overall_status }}</p>
            </div>
            <div>
              <p class="text-sm text-slate-600 dark:text-slate-400">Checks Passed</p>
              <p class="font-semibold text-slate-900 dark:text-slate-100">{{ selectedReport.passed_checks }}/{{ selectedReport.total_checks }}</p>
            </div>
          </div>

          <div>
            <p class="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-2">Findings</p>
            <p class="text-slate-700 dark:text-slate-300 text-sm">{{ selectedReport.findings }}</p>
          </div>

          <div>
            <p class="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-2">Recommendations</p>
            <p class="text-slate-700 dark:text-slate-300 text-sm">{{ selectedReport.recommendations }}</p>
          </div>

          <div class="border-t border-slate-200 dark:border-slate-700 pt-4">
            <p class="text-xs text-slate-600 dark:text-slate-400">Auditor: {{ selectedReport.auditor_name }} ({{ selectedReport.auditor_emp_id }})</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Compliance Methodology Explanation -->
    <div class="bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 p-6 rounded-xl border border-green-200 dark:border-green-700">
      <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">📋 ISO 45001 Compliance Assessment</h3>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <!-- Compliant -->
        <div class="bg-white dark:bg-slate-800 p-4 rounded-lg border border-green-200 dark:border-green-700">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-3 h-3 rounded-full bg-green-500"></div>
            <p class="font-semibold text-slate-900 dark:text-slate-100">COMPLIANT</p>
          </div>
          <p class="text-xs text-slate-600 dark:text-slate-400 mb-2">All safety standards met</p>
          <p class="text-xs font-mono text-slate-500 dark:text-slate-500">Score: ≥90%</p>
        </div>

        <!-- Partially Compliant -->
        <div class="bg-white dark:bg-slate-800 p-4 rounded-lg border border-yellow-200 dark:border-yellow-700">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
            <p class="font-semibold text-slate-900 dark:text-slate-100">PARTIALLY COMPLIANT</p>
          </div>
          <p class="text-xs text-slate-600 dark:text-slate-400 mb-2">Some gaps in compliance</p>
          <p class="text-xs font-mono text-slate-500 dark:text-slate-500">Score: 70-89%</p>
        </div>

        <!-- Non-Compliant -->
        <div class="bg-white dark:bg-slate-800 p-4 rounded-lg border border-red-200 dark:border-red-700">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-3 h-3 rounded-full bg-red-500"></div>
            <p class="font-semibold text-slate-900 dark:text-slate-100">NON-COMPLIANT</p>
          </div>
          <p class="text-xs text-slate-600 dark:text-slate-400 mb-2">Significant compliance issues</p>
          <p class="text-xs font-mono text-slate-500 dark:text-slate-500">Score: &lt;70%</p>
        </div>
      </div>

      <!-- Compliance Checks -->
      <div class="bg-white dark:bg-slate-800 p-4 rounded-lg border border-slate-200 dark:border-slate-700 space-y-3">
        <p class="text-sm font-semibold text-slate-900 dark:text-slate-100">✓ Compliance Checks Evaluated:</p>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div class="text-xs text-slate-600 dark:text-slate-400">
            <p class="font-semibold text-slate-700 dark:text-slate-300 mb-1">1. PTW Signature Compliance</p>
            <p>All permits have proper signatures (90% threshold)</p>
          </div>

          <div class="text-xs text-slate-600 dark:text-slate-400">
            <p class="font-semibold text-slate-700 dark:text-slate-300 mb-1">2. PTW Approval Compliance</p>
            <p>All permits properly approved (80% threshold)</p>
          </div>

          <div class="text-xs text-slate-600 dark:text-slate-400">
            <p class="font-semibold text-slate-700 dark:text-slate-300 mb-1">3. No LTI Incidents</p>
            <p>Zero lost-time injuries in the period</p>
          </div>

          <div class="text-xs text-slate-600 dark:text-slate-400">
            <p class="font-semibold text-slate-700 dark:text-slate-300 mb-1">4. Incident Closure Rate</p>
            <p>Incidents closed timely (70% threshold)</p>
          </div>

          <div class="text-xs text-slate-600 dark:text-slate-400">
            <p class="font-semibold text-slate-700 dark:text-slate-300 mb-1">5. POB Check-in Compliance</p>
            <p>All workers properly checked in/out (95% threshold)</p>
          </div>

          <div class="text-xs text-slate-600 dark:text-slate-400">
            <p class="font-semibold text-slate-700 dark:text-slate-300 mb-1">6. System Status</p>
            <p>System in GREEN status (no emergencies)</p>
          </div>

          <div class="text-xs text-slate-600 dark:text-slate-400">
            <p class="font-semibold text-slate-700 dark:text-slate-300 mb-1">7. PTW Same-Day Closure</p>
            <p>Permits closed same day (50% threshold)</p>
          </div>
        </div>
      </div>

      <!-- Key Notes -->
      <div class="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-700">
        <p class="text-xs font-semibold text-slate-900 dark:text-slate-100 mb-2">💡 Key Information:</p>
        <ul class="text-xs text-slate-600 dark:text-slate-400 space-y-1 list-disc list-inside">
          <li>Reports are <span class="font-semibold">auto-generated daily</span> based on system data</li>
          <li>Compliance Score = (Passed Checks / Total Checks) × 100</li>
          <li>Findings show which checks failed and why</li>
          <li>Recommendations provide actionable improvement steps</li>
          <li>Auditor: System Auto-Audit (automated evaluation)</li>
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
const selectedReportType = ref('');
const selectedStatus = ref('');
const reportsData = ref([]);
const selectedReport = ref(null);
const summary = ref({
  total_reports: 0,
  compliant: 0,
  partial_compliant: 0,
  non_compliant: 0,
  average_compliance_score: 0
});

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

const viewReport = (report) => {
  selectedReport.value = report;
};

const fetchReports = async () => {
  loading.value = true;
  try {
    let url = `${API_BASE_URL}/hse/analytics/compliance/?`;
    if (authState.selectedVessel) url += `vessel=${authState.selectedVessel.asset_id}&`;
    if (selectedReportType.value) url += `report_type=${selectedReportType.value}&`;
    if (selectedStatus.value) url += `status=${selectedStatus.value}&`;

    const response = await fetch(url, { credentials: 'include' });

    if (response.ok) {
      const data = await response.json();
      reportsData.value = data;
    }
  } catch (error) {
    console.error('Failed to fetch compliance reports:', error);
  } finally {
    loading.value = false;
  }
};

const fetchSummary = async () => {
  try {
    const vesselParam = authState.selectedVessel ? `?vessel=${authState.selectedVessel.asset_id}` : '';
    const response = await fetch(`${API_BASE_URL}/hse/analytics/compliance/compliance_summary/${vesselParam}`, {
      credentials: 'include'
    });

    if (response.ok) {
      summary.value = await response.json();
    }
  } catch (error) {
    console.error('Failed to fetch compliance summary:', error);
  }
};

onMounted(() => {
  fetchReports();
  fetchSummary();
});
</script>
