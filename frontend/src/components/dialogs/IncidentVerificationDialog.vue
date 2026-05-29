<template>
  <Dialog :open="open" @update:open="$emit('update:open', $event)">
    <DialogContent class="max-w-2xl">
      <DialogHeader>
        <DialogTitle>Verify Incident Report</DialogTitle>
        <DialogDescription>
          Review and verify this worker-reported incident before it affects system metrics
        </DialogDescription>
      </DialogHeader>

      <div v-if="incident" class="space-y-4">
        <!-- Incident Details -->
        <div class="bg-slate-50 dark:bg-slate-900 p-4 rounded-lg border border-slate-200 dark:border-slate-700 space-y-3">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-xs font-medium text-slate-600 dark:text-slate-400">Incident ID</p>
              <p class="text-sm font-semibold text-slate-900 dark:text-slate-100">{{ incident.incident_id }}</p>
            </div>
            <div>
              <p class="text-xs font-medium text-slate-600 dark:text-slate-400">Reported By</p>
              <p class="text-sm font-semibold text-slate-900 dark:text-slate-100">{{ incident.reported_by_name }}</p>
            </div>
            <div>
              <p class="text-xs font-medium text-slate-600 dark:text-slate-400">Severity</p>
              <span :class="[
                'px-2 py-1 rounded text-xs font-semibold inline-block',
                incident.severity === 'SAFETY_OBSERVATION' ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400' :
                incident.severity === 'NEAR_MISS' ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400' :
                incident.severity === 'FIRST_AID' ? 'bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400' :
                'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
              ]">
                {{ incident.severity_display }}
              </span>
            </div>
            <div>
              <p class="text-xs font-medium text-slate-600 dark:text-slate-400">Location</p>
              <p class="text-sm font-semibold text-slate-900 dark:text-slate-100">{{ incident.location_name }}</p>
            </div>
          </div>

          <div>
            <p class="text-xs font-medium text-slate-600 dark:text-slate-400 mb-1">Date & Time</p>
            <p class="text-sm text-slate-900 dark:text-slate-100">{{ formatDateTime(incident.incident_date) }}</p>
          </div>

          <div>
            <p class="text-xs font-medium text-slate-600 dark:text-slate-400 mb-1">Description</p>
            <p class="text-sm text-slate-900 dark:text-slate-100 whitespace-pre-wrap">{{ incident.description }}</p>
          </div>

          <div v-if="incident.proof_image">
            <p class="text-xs font-medium text-slate-600 dark:text-slate-400 mb-2">Proof Image</p>
            <img :src="incident.proof_image" class="max-h-[200px] rounded-lg border border-slate-200 dark:border-slate-700" />
          </div>
        </div>

        <!-- Impact Preview -->
        <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-200 dark:border-blue-700">
          <p class="text-sm font-semibold text-blue-900 dark:text-blue-100 mb-2">📊 Impact if Verified</p>
          <ul class="text-sm text-blue-800 dark:text-blue-200 space-y-1 list-disc list-inside">
            <li v-if="incident.severity === 'SAFETY_OBSERVATION'">No change to metrics</li>
            <li v-if="incident.severity === 'NEAR_MISS'">Near Misses count will increase by 1</li>
            <li v-if="incident.severity === 'FIRST_AID'">System condition will change to YELLOW ⚠️</li>
            <li v-if="incident.severity === 'LTI'">🚨 Days Without LTI will reset to 0, System condition will change to RED 🔴</li>
          </ul>
        </div>

        <!-- Verification Form -->
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- Reject Reason (shown only when rejecting) -->
          <div v-if="showRejectReason" class="space-y-2">
            <Label for="rejection_reason" class="text-sm font-semibold">Reason for Rejection <span class="text-red-500">*</span></Label>
            <Textarea
              v-model="rejectionReason"
              placeholder="Explain why you're rejecting this incident report..."
              class="min-h-[80px]"
            />
            <p class="text-xs text-slate-500 dark:text-slate-400">This will be visible to the reporter</p>
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" @click="$emit('update:open', false)">Cancel</Button>
            <Button
              type="button"
              @click="toggleRejectMode"
              variant="outline"
              class="text-red-600 hover:text-red-700 hover:bg-red-50 dark:hover:bg-red-900/20"
            >
              {{ showRejectReason ? 'Back' : 'Reject' }}
            </Button>
            <Button
              type="submit"
              :disabled="(showRejectReason && !rejectionReason.trim()) || isSubmitting"
              class="bg-green-600 hover:bg-green-700"
            >
              {{ isSubmitting ? 'Processing...' : (showRejectReason ? 'Confirm Rejection' : 'Verify & Approve') }}
            </Button>
          </DialogFooter>
        </form>
      </div>
    </DialogContent>
  </Dialog>
</template>

<script setup>
import { ref } from 'vue';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { toast } from 'vue-sonner';
import { getCsrfToken } from '@/utils/csrf';

const props = defineProps({
  open: Boolean,
  incident: Object
});

const emit = defineEmits(['update:open', 'verified']);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';
const showRejectReason = ref(false);
const rejectionReason = ref('');
const isSubmitting = ref(false);

const formatDateTime = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const toggleRejectMode = () => {
  showRejectReason.value = !showRejectReason.value;
  if (!showRejectReason.value) {
    rejectionReason.value = '';
  }
};

const handleSubmit = async () => {
  if (!props.incident) return;

  isSubmitting.value = true;
  try {
    const action = showRejectReason.value ? 'reject' : 'verify';
    const payload = { action };

    if (action === 'reject') {
      if (!rejectionReason.value.trim()) {
        toast.error('Rejection reason is required');
        isSubmitting.value = false;
        return;
      }
      payload.rejection_reason = rejectionReason.value;
    }

    const response = await fetch(`${API_BASE_URL}/hse/incidents/${props.incident.id}/verify/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken() || ''
      },
      body: JSON.stringify(payload),
      credentials: 'include'
    });

    if (response.ok) {
      const data = await response.json();
      const message = action === 'verify'
        ? 'Incident verified and metrics updated'
        : 'Incident rejected';

      toast.success(message);
      emit('verified', data);
      emit('update:open', false);
      showRejectReason.value = false;
      rejectionReason.value = '';
    } else {
      const error = await response.json();
      toast.error('Failed', { description: error.error || 'Failed to process incident' });
    }
  } catch (error) {
    console.error('Error verifying incident:', error);
    toast.error('Error', { description: 'Server connection failed' });
  } finally {
    isSubmitting.value = false;
  }
};
</script>
