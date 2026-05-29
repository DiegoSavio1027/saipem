<template>
  <DashboardLayout>
    <div class="space-y-6">
      <!-- Header -->
      <div class="bg-white dark:bg-slate-800 p-6 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm">
        <h1 class="text-3xl font-bold text-slate-900 dark:text-slate-100">Analytics & Reports</h1>
        <p class="text-slate-500 dark:text-slate-400 mt-2">Historical trends, safety metrics, and compliance reports</p>
      </div>

      <!-- Tabs Navigation -->
      <div class="flex gap-2 border-b border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 rounded-t-xl p-4">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="[
            'px-4 py-2 font-medium rounded-t-lg transition-colors',
            activeTab === tab.id
              ? 'bg-[var(--color-saipem-primary)] text-white'
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100'
          ]"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- Tab Content -->
      <div class="bg-white dark:bg-slate-800 rounded-b-xl border border-slate-200 dark:border-slate-700 shadow-sm p-6">
        <!-- Safety Metrics Tab -->
        <SafetyMetricsTab v-if="activeTab === 'metrics'" />

        <!-- Incident Trends Tab -->
        <IncidentTrendsTab v-if="activeTab === 'trends'" />

        <!-- Compliance Reports Tab -->
        <ComplianceReportsTab v-if="activeTab === 'compliance'" />

        <!-- Location Hotspots Tab -->
        <LocationHotspotsTab v-if="activeTab === 'hotspots'" />

        <!-- Condition Change Audit Tab -->
        <ConditionChangeAuditTab v-if="activeTab === 'audit'" />
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref } from 'vue';
import DashboardLayout from '@/layouts/DashboardLayout.vue';
import SafetyMetricsTab from '@/components/analytics/SafetyMetricsTab.vue';
import IncidentTrendsTab from '@/components/analytics/IncidentTrendsTab.vue';
import ComplianceReportsTab from '@/components/analytics/ComplianceReportsTab.vue';
import LocationHotspotsTab from '@/components/analytics/LocationHotspotsTab.vue';
import ConditionChangeAuditTab from '@/components/analytics/ConditionChangeAuditTab.vue';

const activeTab = ref('metrics');

const tabs = [
  { id: 'metrics', label: 'Safety Metrics' },
  { id: 'trends', label: 'Incident Trends' },
  { id: 'compliance', label: 'Compliance Reports' },
  { id: 'hotspots', label: 'Location Hotspots' },
  { id: 'audit', label: 'Condition Change Audit' }
];
</script>
