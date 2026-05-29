<template>
  <Dialog :open="open" @update:open="$emit('update:open', $event)">
    <DialogContent class="max-w-2xl">
      <DialogHeader>
        <DialogTitle>Edit Incident</DialogTitle>
        <DialogDescription>Update incident information and status</DialogDescription>
      </DialogHeader>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <!-- Status -->
        <div class="space-y-2">
          <Label for="status" class="text-sm font-semibold">Status <span class="text-red-500">*</span></Label>
          <Select v-model="formData.status">
            <SelectTrigger class="w-full">
              <SelectValue placeholder="Select status" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectItem value="OPEN">Open</SelectItem>
                <SelectItem value="INVESTIGATING">Investigating</SelectItem>
                <SelectItem value="CLOSED">Closed</SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>

        <!-- Investigation Notes -->
        <div class="space-y-2">
          <Label for="investigation_notes" class="text-sm font-semibold">Investigation Notes</Label>
          <Textarea
            v-model="formData.investigation_notes"
            placeholder="Add investigation notes..."
            class="min-h-[100px]"
          />
        </div>

        <!-- Closed By (if status is CLOSED) -->
        <div v-if="formData.status === 'CLOSED'" class="space-y-2">
          <Label for="closed_by" class="text-sm font-semibold">Closed By <span class="text-red-500">*</span></Label>
          <Select v-model="formData.closed_by">
            <SelectTrigger class="w-full">
              <SelectValue placeholder="Select employee" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectItem v-for="employee in employees" :key="employee.emp_id" :value="employee.emp_id">
                  {{ employee.full_name }} ({{ employee.emp_id }})
                </SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>

        <!-- Read-only fields for reference -->
        <div class="border-t border-slate-200 pt-4 space-y-3">
          <p class="text-xs font-semibold text-slate-500 uppercase">Incident Information (Read-only)</p>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <Label class="text-xs text-slate-500">Severity</Label>
              <p class="text-sm font-medium text-slate-900">{{ incident?.severity_display }}</p>
            </div>
            <div>
              <Label class="text-xs text-slate-500">Location</Label>
              <p class="text-sm font-medium text-slate-900">{{ incident?.location_name }}</p>
            </div>
          </div>

          <div>
            <Label class="text-xs text-slate-500">Description</Label>
            <p class="text-sm text-slate-900">{{ incident?.description }}</p>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <Label class="text-xs text-slate-500">Employee Involved</Label>
              <p class="text-sm font-medium text-slate-900">{{ incident?.employee_name || '-' }}</p>
            </div>
            <div>
              <Label class="text-xs text-slate-500">Incident Date</Label>
              <p class="text-sm font-medium text-slate-900">{{ formatDate(incident?.incident_date) }}</p>
            </div>
          </div>
        </div>

        <DialogFooter>
          <Button type="button" variant="outline" @click="$emit('update:open', false)">Cancel</Button>
          <Button type="submit" :disabled="isSubmitting">
            {{ isSubmitting ? 'Updating...' : 'Update Incident' }}
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { toast } from 'vue-sonner';
import { getCsrfToken } from '@/utils/csrf';

const props = defineProps({
  open: Boolean,
  incident: Object
});

const emit = defineEmits(['update:open', 'incident-updated']);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';
const isSubmitting = ref(false);
const employees = ref([]);

const formData = ref({
  status: '',
  investigation_notes: '',
  closed_by: ''
});

const fetchEmployees = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/hse/employees/`, { credentials: 'include' });
    if (response.ok) {
      employees.value = await response.json();
    }
  } catch (error) {
    console.error('Failed to fetch employees:', error);
  }
};

watch(() => props.open, (newVal) => {
  if (newVal) {
    fetchEmployees();
  }
});

watch(() => props.incident, (newIncident) => {
  if (newIncident) {
    formData.value = {
      status: newIncident.status || '',
      investigation_notes: newIncident.investigation_notes || '',
      closed_by: newIncident.closed_by || ''
    };
  }
}, { immediate: true });

const handleSubmit = async () => {
  if (!formData.value.status) {
    toast.error('Please select a status');
    return;
  }

  isSubmitting.value = true;
  try {
    const payload = {
      status: formData.value.status,
      investigation_notes: formData.value.investigation_notes
    };

    if (formData.value.status === 'CLOSED') {
      payload.closed_by = formData.value.closed_by;
      payload.closed_date = new Date().toISOString();
    }

    const response = await fetch(`${API_BASE_URL}/hse/incidents/${props.incident.id}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken() || ''
      },
      credentials: 'include',
      body: JSON.stringify(payload)
    });

    if (response.ok) {
      emit('incident-updated');
      emit('update:open', false);
    } else {
      const error = await response.json();
      toast.error('Failed to update incident', { description: JSON.stringify(error) });
    }
  } catch (error) {
    console.error('Error updating incident:', error);
    toast.error('Error updating incident');
  } finally {
    isSubmitting.value = false;
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '-';
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
