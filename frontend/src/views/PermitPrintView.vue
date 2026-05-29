<template>
  <div class="bg-white min-h-screen p-8">
    <!-- Print Header -->
    <div class="mb-8 flex justify-between items-start">
      <div>
        <h1 class="text-2xl font-bold text-slate-900">PERMIT TO WORK</h1>
        <p class="text-slate-600">Saipem HSE Management System</p>
      </div>
      <button
        @click="window.print()"
        class="bg-[var(--color-saipem-tertiary)] hover:bg-[var(--color-saipem-tertiary)]/90 text-white px-6 py-2 rounded-lg font-semibold text-sm transition-colors"
      >
        Print / Save as PDF
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[var(--color-saipem-tertiary)]"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
      <p class="text-red-700">{{ error }}</p>
    </div>

    <!-- Permit Card -->
    <div v-else-if="permit" class="bg-white border-2 border-slate-300 rounded-lg p-8 max-w-4xl mx-auto print:border-0 print:p-0">
      <!-- Header Section -->
      <div class="border-b-2 border-slate-300 pb-6 mb-6">
        <div class="grid grid-cols-3 gap-4 mb-4">
          <div>
            <p class="text-xs font-semibold text-slate-500 uppercase tracking-wide">Permit ID</p>
            <p class="text-xl font-bold text-slate-900">{{ permit.permit_id }}</p>
          </div>
          <div>
            <p class="text-xs font-semibold text-slate-500 uppercase tracking-wide">Permit Type</p>
            <p class="text-xl font-bold text-slate-900">{{ formatPermitType(permit.permit_type) }}</p>
          </div>
          <div class="text-right">
            <p class="text-xs font-semibold text-slate-500 uppercase tracking-wide">Status</p>
            <p :class="getStatusColor(permit.status)" class="text-xl font-bold">{{ permit.status }}</p>
          </div>
        </div>
      </div>

      <!-- Employee Information -->
      <div class="grid grid-cols-2 gap-8 mb-8">
        <div>
          <h3 class="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-4">Employee Information</h3>
          <div class="space-y-3">
            <div>
              <p class="text-xs text-slate-500">Employee Name</p>
              <p class="text-base font-semibold text-slate-900">{{ permit.employee?.full_name || permit.emp_id }}</p>
            </div>
            <div>
              <p class="text-xs text-slate-500">Employee ID</p>
              <p class="text-base font-semibold text-slate-900">{{ permit.emp_id }}</p>
            </div>
            <div>
              <p class="text-xs text-slate-500">Work Order ID</p>
              <p class="text-base font-semibold text-slate-900">{{ permit.wo_id }}</p>
            </div>
          </div>
        </div>

        <div>
          <h3 class="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-4">Work Location</h3>
          <div class="space-y-3">
            <div>
              <p class="text-xs text-slate-500">Deck Location</p>
              <p class="text-base font-semibold text-slate-900">{{ permit.deck_location || 'N/A' }}</p>
            </div>
            <div>
              <p class="text-xs text-slate-500">Created Date</p>
              <p class="text-base font-semibold text-slate-900">{{ formatDate(permit.created_at) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Approval Section -->
      <div v-if="permit.approved_by" class="border-t-2 border-slate-300 pt-6 mb-8">
        <h3 class="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-4">Approval</h3>
        <div class="grid grid-cols-2 gap-8">
          <div>
            <p class="text-xs text-slate-500">Approved By</p>
            <p class="text-base font-semibold text-slate-900">{{ permit.approved_by }}</p>
          </div>
          <div>
            <p class="text-xs text-slate-500">Approved Date</p>
            <p class="text-base font-semibold text-slate-900">{{ formatDate(permit.approved_at) }}</p>
          </div>
        </div>

        <!-- Signature -->
        <div v-if="permit.signature" class="mt-6">
          <p class="text-xs text-slate-500 mb-2">Safety Officer Signature</p>
          <div class="border border-slate-300 rounded p-4 bg-slate-50 inline-block">
            <img :src="permit.signature" alt="Signature" class="h-16 object-contain" />
          </div>
        </div>
      </div>

      <!-- Completion Section -->
      <div v-if="permit.completion_notes" class="border-t-2 border-slate-300 pt-6 mb-8">
        <h3 class="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-4">Completion Notes</h3>
        <p class="text-slate-900">{{ permit.completion_notes }}</p>
      </div>

      <!-- Closing Section -->
      <div v-if="permit.closed_by" class="border-t-2 border-slate-300 pt-6">
        <h3 class="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-4">Closed By</h3>
        <div class="grid grid-cols-2 gap-8">
          <div>
            <p class="text-xs text-slate-500">Closed By</p>
            <p class="text-base font-semibold text-slate-900">{{ permit.closed_by }}</p>
          </div>
          <div>
            <p class="text-xs text-slate-500">Closed Date</p>
            <p class="text-base font-semibold text-slate-900">{{ formatDate(permit.closed_at) }}</p>
          </div>
        </div>
        <div v-if="permit.closing_notes" class="mt-4">
          <p class="text-xs text-slate-500">Closing Notes</p>
          <p class="text-slate-900">{{ permit.closing_notes }}</p>
        </div>
      </div>

      <!-- Footer -->
      <div class="border-t-2 border-slate-300 mt-8 pt-6 text-center text-xs text-slate-500">
        <p>This is an official Permit to Work document</p>
        <p>Generated on {{ formatDate(new Date().toISOString()) }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const permit = ref(null);
const loading = ref(true);
const error = ref(null);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';

const fetchPermitDetail = async () => {
  loading.value = true;
  error.value = null;

  try {
    const response = await fetch(`${API_BASE_URL}/hse/ptw/${route.params.id}/`, {
      credentials: 'include'
    });

    if (!response.ok) {
      throw new Error('Failed to fetch permit details');
    }

    permit.value = await response.json();
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

const formatPermitType = (type) => {
  const types = {
    'HOT_WORK': 'Hot Work Permit',
    'CONFINED_SPACE': 'Confined Space Entry',
    'WORKING_AT_HEIGHT': 'Working at Height',
    'ISOLATION': 'Isolation Certificate'
  };
  return types[type] || type;
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleString();
};

const getStatusColor = (status) => {
  const colors = {
    'PENDING': 'text-yellow-600',
    'APPROVED': 'text-green-600',
    'IN_PROGRESS': 'text-blue-600',
    'WAITING_FOR_CLOSE': 'text-purple-600',
    'CLOSED': 'text-slate-600',
    'REJECTED': 'text-red-600'
  };
  return colors[status] || 'text-slate-600';
};

onMounted(() => {
  fetchPermitDetail();
});
</script>

<style scoped>
@media print {
  body {
    margin: 0;
    padding: 0;
  }

  .bg-white {
    background: white;
    padding: 0;
  }

  button {
    display: none;
  }

  .print\:border-0 {
    border: none;
  }

  .print\:p-0 {
    padding: 0;
  }
}
</style>
