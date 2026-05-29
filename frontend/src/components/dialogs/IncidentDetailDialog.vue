<template>
  <Dialog :open="open" @update:open="$emit('update:open', $event)">
    <DialogContent class="max-w-2xl">
      <DialogHeader>
        <DialogTitle>Incident Details</DialogTitle>
        <DialogDescription>View incident information</DialogDescription>
      </DialogHeader>

      <div v-if="incident" class="space-y-4">
        <!-- ID and Severity -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <Label class="text-xs font-semibold text-slate-500 dark:text-slate-400">Incident ID</Label>
            <p class="text-sm font-medium text-slate-900 dark:text-slate-100">{{ incident.incident_id || `#${incident.id}` }}</p>
          </div>
          <div>
            <Label class="text-xs font-semibold text-slate-500 dark:text-slate-400">Severity</Label>
            <span :class="getSeverityBadgeClass(incident.severity)" class="px-2 py-1 text-xs font-semibold rounded-full inline-block">
              {{ incident.severity_display }}
            </span>
          </div>
        </div>

        <!-- Location and Status -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <Label class="text-xs font-semibold text-slate-500 dark:text-slate-400">Location</Label>
            <p class="text-sm font-medium text-slate-900 dark:text-slate-100">{{ incident.location_name }}</p>
          </div>
          <div>
            <Label class="text-xs font-semibold text-slate-500 dark:text-slate-400">Status</Label>
            <span :class="getStatusBadgeClass(incident.status)" class="px-2 py-1 text-xs font-semibold rounded-full inline-block">
              {{ incident.status_display }}
            </span>
          </div>
        </div>

        <!-- Description -->
        <div>
          <Label class="text-xs font-semibold text-slate-500 dark:text-slate-400">Description</Label>
          <p class="text-sm text-slate-900 dark:text-slate-100 mt-1">{{ incident.description }}</p>
        </div>

        <!-- Employee and Reporter -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <Label class="text-xs font-semibold text-slate-500 dark:text-slate-400">Employee Involved</Label>
            <p class="text-sm font-medium text-slate-900 dark:text-slate-100">{{ incident.employee_name || '-' }}</p>
          </div>
          <div>
            <Label class="text-xs font-semibold text-slate-500 dark:text-slate-400">Reported By</Label>
            <p class="text-sm font-medium text-slate-900 dark:text-slate-100">{{ incident.reported_by_name || incident.reported_by }}</p>
          </div>
        </div>

        <!-- Dates -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <Label class="text-xs font-semibold text-slate-500 dark:text-slate-400">Incident Date</Label>
            <p class="text-sm font-medium text-slate-900 dark:text-slate-100">{{ formatDate(incident.incident_date) }}</p>
          </div>
          <div>
            <Label class="text-xs font-semibold text-slate-500 dark:text-slate-400">Reported Date</Label>
            <p class="text-sm font-medium text-slate-900 dark:text-slate-100">{{ formatDate(incident.reported_date) }}</p>
          </div>
        </div>

        <!-- Investigation Notes -->
        <div v-if="incident.investigation_notes">
          <Label class="text-xs font-semibold text-slate-500 dark:text-slate-400">Investigation Notes</Label>
          <p class="text-sm text-slate-900 dark:text-slate-100 mt-1">{{ incident.investigation_notes }}</p>
        </div>

        <!-- Proof Image -->
        <div v-if="incident.proof_image">
          <Label class="text-xs font-semibold text-slate-500 dark:text-slate-400">Proof Image</Label>
          <img :src="incident.proof_image" alt="Incident proof" class="mt-2 max-h-[300px] rounded-lg border border-slate-200 dark:border-slate-700" />
        </div>
      </div>

      <DialogFooter>
        <Button @click="$emit('update:open', false)" variant="outline">Close</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

<script setup>
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';

defineProps({
  open: Boolean,
  incident: Object
});

defineEmits(['update:open']);

const getSeverityBadgeClass = (severity) => {
  const classes = {
    'SAFETY_OBSERVATION': 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-400',
    'NEAR_MISS': 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-400',
    'FIRST_AID': 'bg-orange-100 dark:bg-orange-900/30 text-orange-800 dark:text-orange-400',
    'LTI': 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-400'
  };
  return classes[severity] || 'bg-slate-100 dark:bg-slate-700 text-slate-800 dark:text-slate-400';
};

const getStatusBadgeClass = (status) => {
  const classes = {
    'OPEN': 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-400',
    'INVESTIGATING': 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-400',
    'CLOSED': 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400'
  };
  return classes[status] || 'bg-slate-100 dark:bg-slate-700 text-slate-800 dark:text-slate-400';
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};
</script>
