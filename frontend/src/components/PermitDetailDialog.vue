<template>
  <Dialog :open="open" @update:open="$emit('update:open', $event)">
    <DialogContent class="max-w-4xl max-h-[90vh] overflow-y-auto">
      <DialogHeader>
        <DialogTitle>Permit to Work Detail</DialogTitle>
        <DialogDescription>{{ permit?.permit_id }}</DialogDescription>
      </DialogHeader>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[var(--color-saipem-tertiary)]"></div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700 rounded-lg p-6 text-center">
        <p class="text-red-700 dark:text-red-400">{{ error }}</p>
      </div>

      <!-- Permit Details -->
      <div v-else-if="permit" class="space-y-6">
        <!-- Status Badge -->
        <div class="flex items-center justify-between p-4 bg-slate-50 dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700">
          <div>
            <p class="text-sm text-slate-500 dark:text-slate-400 mb-1">Current Status</p>
            <span :class="getStatusClass(permit.status)" class="px-4 py-2 rounded-full text-sm font-semibold inline-block">
              {{ permit.status }}
            </span>
          </div>
          <div class="text-right">
            <p class="text-sm text-slate-500 dark:text-slate-400">Created</p>
            <p class="font-semibold text-slate-900 dark:text-slate-100">{{ formatDate(permit.created_at) }}</p>
          </div>
        </div>

        <!-- Basic Information -->
        <div>
          <h3 class="font-semibold text-slate-900 dark:text-slate-100 mb-3">Basic Information</h3>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="text-sm font-medium text-slate-500 dark:text-slate-400">Permit ID</label>
              <p class="text-base font-semibold text-slate-900 dark:text-slate-100">{{ permit.permit_id }}</p>
            </div>
            <div>
              <label class="text-sm font-medium text-slate-500 dark:text-slate-400">Permit Type</label>
              <p class="text-base font-semibold text-slate-900 dark:text-slate-100">{{ permit.permit_type }}</p>
            </div>
            <div>
              <label class="text-sm font-medium text-slate-500 dark:text-slate-400">Employee ID</label>
              <p class="text-base font-semibold text-slate-900 dark:text-slate-100">{{ permit.emp_id }}</p>
            </div>
            <div>
              <label class="text-sm font-medium text-slate-500 dark:text-slate-400">Work Order ID</label>
              <p class="text-base font-semibold text-slate-900 dark:text-slate-100">{{ permit.wo_id }}</p>
            </div>
            <div>
              <label class="text-sm font-medium text-slate-500 dark:text-slate-400">Location</label>
              <p class="text-base font-semibold text-slate-900 dark:text-slate-100">{{ permit.deck_location || 'N/A' }}</p>
            </div>
          </div>
        </div>

        <!-- Approval Information -->
        <div v-if="permit.approved_by">
          <h3 class="font-semibold text-slate-900 dark:text-slate-100 mb-3">Approval Information</h3>
          <div class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm font-medium text-slate-500 dark:text-slate-400">Approved By</label>
                <p class="text-base font-semibold text-slate-900 dark:text-slate-100">{{ permit.approved_by_name || permit.approved_by }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-slate-500 dark:text-slate-400">Approved At</label>
                <p class="text-base font-semibold text-slate-900 dark:text-slate-100">{{ formatDate(permit.approved_at) }}</p>
              </div>
            </div>

            <!-- Signature -->
            <div v-if="permit.signature">
              <label class="text-sm font-medium text-slate-500 dark:text-slate-400 block mb-2">Digital Signature</label>
              <div class="border-2 border-slate-200 dark:border-slate-700 rounded-lg p-4 bg-slate-50 dark:bg-slate-800 inline-block">
                <img :src="permit.signature" alt="Signature" class="max-w-xs h-20 object-contain" />
              </div>
            </div>
          </div>
        </div>

        <!-- Rejection Information -->
        <div v-if="permit.rejected_by">
          <h3 class="font-semibold text-slate-900 dark:text-slate-100 mb-3">Rejection Information</h3>
          <div class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm font-medium text-slate-500 dark:text-slate-400">Rejected By</label>
                <p class="text-base font-semibold text-slate-900 dark:text-slate-100">{{ permit.rejected_by_name || permit.rejected_by }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-slate-500 dark:text-slate-400">Rejected At</label>
                <p class="text-base font-semibold text-slate-900 dark:text-slate-100">{{ formatDate(permit.rejected_at) }}</p>
              </div>
            </div>
            <div>
              <label class="text-sm font-medium text-slate-500 dark:text-slate-400">Rejection Reason</label>
              <p class="text-slate-900 dark:text-slate-100">{{ permit.rejection_reason }}</p>
            </div>
          </div>
        </div>

        <!-- Completion Information -->
        <div v-if="permit.completion_notes">
          <h3 class="font-semibold text-slate-900 dark:text-slate-100 mb-3">Completion Information</h3>
          <div>
            <label class="text-sm font-medium text-slate-500 dark:text-slate-400">Completion Notes</label>
            <p class="text-slate-900 dark:text-slate-100 mt-2">{{ permit.completion_notes }}</p>
          </div>
        </div>

        <!-- Closing Information -->
        <div v-if="permit.closed_by">
          <h3 class="font-semibold text-slate-900 dark:text-slate-100 mb-3">Closing Information</h3>
          <div class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm font-medium text-slate-500 dark:text-slate-400">Closed By</label>
                <p class="text-base font-semibold text-slate-900 dark:text-slate-100">{{ permit.closed_by_name || permit.closed_by }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-slate-500 dark:text-slate-400">Closed At</label>
                <p class="text-base font-semibold text-slate-900 dark:text-slate-100">{{ formatDate(permit.closed_at) }}</p>
              </div>
            </div>
            <div v-if="permit.closing_notes">
              <label class="text-sm font-medium text-slate-500 dark:text-slate-400">Closing Notes</label>
              <p class="text-slate-900 dark:text-slate-100 mt-2">{{ permit.closing_notes }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer Actions -->
      <DialogFooter v-if="permit">
        <Button variant="outline" @click="$emit('update:open', false)">Close</Button>
        <Button
          v-if="permit.status === 'APPROVED' || permit.status === 'CLOSED'"
          @click="openPrintPreview"
          class="bg-[var(--color-saipem-tertiary)] hover:bg-[var(--color-saipem-tertiary)]/90"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect width="12" height="8" x="6" y="14"/></svg>
          Print Permit
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';

const props = defineProps({
  open: Boolean,
  permitId: [String, Number]
});

const emit = defineEmits(['update:open']);

const permit = ref(null);
const loading = ref(false);
const error = ref(null);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';

const fetchPermitDetail = async () => {
  if (!props.permitId) return;

  loading.value = true;
  error.value = null;

  try {
    const response = await fetch(`${API_BASE_URL}/hse/ptw/${props.permitId}/`, {
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

const getStatusClass = (status) => {
  const classes = {
    'PENDING': 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400',
    'APPROVED': 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400',
    'IN_PROGRESS': 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400',
    'WAITING_FOR_CLOSE': 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400',
    'CLOSED': 'bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-400',
    'REJECTED': 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
  };
  return classes[status] || 'bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-400';
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleString();
};

const openPrintPreview = () => {
  // Open print preview in new tab
  const printUrl = `/permit-print/${props.permitId}`;
  window.open(printUrl, '_blank');
};

// Fetch permit when dialog opens
watch(() => props.open, (newVal) => {
  if (newVal) {
    fetchPermitDetail();
  }
});
</script>
