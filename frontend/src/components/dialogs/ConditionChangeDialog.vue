<template>
  <Dialog :open="open" @update:open="$emit('update:open', $event)">
    <DialogContent class="max-w-2xl">
      <DialogHeader>
        <DialogTitle>Change System Condition</DialogTitle>
        <DialogDescription>
          Changing the system condition affects all PTW operations and safety protocols
        </DialogDescription>
      </DialogHeader>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <!-- Current Status -->
        <div class="bg-slate-50 dark:bg-slate-800 p-4 rounded-lg border border-slate-200 dark:border-slate-700">
          <p class="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-2">Current Status</p>
          <div class="flex items-center gap-2">
            <div :class="[
              'w-4 h-4 rounded-full',
              currentStatus === 'GREEN' ? 'bg-green-500' :
              currentStatus === 'YELLOW' ? 'bg-yellow-500' :
              'bg-red-500'
            ]"></div>
            <span class="font-semibold text-slate-900 dark:text-slate-100">CONDITION {{ currentStatus }}</span>
          </div>
        </div>

        <!-- New Status Selection -->
        <div class="space-y-2">
          <Label class="text-sm font-semibold">Change To <span class="text-red-500">*</span></Label>
          <div class="grid grid-cols-3 gap-3">
            <button
              v-for="status in ['GREEN', 'YELLOW', 'RED']"
              :key="status"
              type="button"
              @click="selectedStatus = status"
              :class="[
                'p-3 rounded-lg border-2 transition-all',
                selectedStatus === status
                  ? 'border-[var(--color-saipem-primary)] bg-slate-50 dark:bg-slate-700'
                  : 'border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600'
              ]"
            >
              <div class="flex items-center justify-center gap-2">
                <div :class="[
                  'w-3 h-3 rounded-full',
                  status === 'GREEN' ? 'bg-green-500' :
                  status === 'YELLOW' ? 'bg-yellow-500' :
                  'bg-red-500'
                ]"></div>
                <span class="font-semibold text-sm text-slate-900 dark:text-slate-100">{{ status }}</span>
              </div>
            </button>
          </div>
        </div>

        <!-- Impact Preview -->
        <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-200 dark:border-blue-700">
          <p class="text-sm font-semibold text-blue-900 dark:text-blue-100 mb-2">⚠️ Impact Preview</p>
          <ul class="text-sm text-blue-800 dark:text-blue-200 space-y-1 list-disc list-inside">
            <li v-if="selectedStatus === 'GREEN'">All PTW approvals enabled</li>
            <li v-if="selectedStatus === 'GREEN'">Normal operations resume</li>
            <li v-if="selectedStatus === 'YELLOW'">PTW approvals continue with caution</li>
            <li v-if="selectedStatus === 'YELLOW'">Heightened alert mode activated</li>
            <li v-if="selectedStatus === 'RED'">🚨 All new PTW approvals FROZEN</li>
            <li v-if="selectedStatus === 'RED'">🚨 Emergency protocols activated</li>
            <li v-if="selectedStatus === 'RED'">🚨 Evacuation procedures may be initiated</li>
          </ul>
        </div>

        <!-- Reason/Comment -->
        <div class="space-y-2">
          <Label for="reason" class="text-sm font-semibold">Reason for Change <span class="text-red-500">*</span></Label>
          <Textarea
            v-model="reason"
            placeholder="Explain why you're changing the system condition..."
            class="min-h-[80px]"
          />
          <p class="text-xs text-slate-500 dark:text-slate-400">This will be logged for audit purposes</p>
        </div>

        <!-- Confirmation Checkbox -->
        <div class="flex items-start gap-3 bg-red-50 dark:bg-red-900/20 p-3 rounded-lg border border-red-200 dark:border-red-700">
          <input
            v-model="confirmed"
            type="checkbox"
            id="confirm"
            class="mt-1 w-4 h-4 rounded border-slate-300 text-red-600 focus:ring-red-500"
          />
          <label for="confirm" class="text-sm text-red-900 dark:text-red-100">
            I understand the impact and confirm this change
          </label>
        </div>

        <DialogFooter>
          <Button type="button" variant="outline" @click="$emit('update:open', false)">Cancel</Button>
          <Button type="submit" :disabled="!selectedStatus || !reason.trim() || !confirmed || isSubmitting" class="bg-red-600 hover:bg-red-700">
            {{ isSubmitting ? 'Changing...' : 'Confirm Change' }}
          </Button>
        </DialogFooter>
      </form>
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
  currentStatus: String
});

const emit = defineEmits(['update:open', 'confirm']);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';
const selectedStatus = ref('');
const reason = ref('');
const confirmed = ref(false);
const isSubmitting = ref(false);

const handleSubmit = async () => {
  if (!selectedStatus.value || !reason.value.trim() || !confirmed.value) {
    toast.error('Error', { description: 'Please fill all required fields' });
    return;
  }

  isSubmitting.value = true;
  try {
    const response = await fetch(`${API_BASE_URL}/hse/status/override/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken() || ''
      },
      body: JSON.stringify({
        status: selectedStatus.value,
        override_reason: reason.value
      }),
      credentials: 'include'
    });

    if (response.ok) {
      toast.success('Status Updated', {
        description: `System condition changed to CONDITION ${selectedStatus.value}`
      });
      emit('confirm', selectedStatus.value);
      emit('update:open', false);
      selectedStatus.value = '';
      reason.value = '';
      confirmed.value = false;
    } else {
      const error = await response.json();
      toast.error('Failed', { description: error.detail || 'Failed to update status' });
    }
  } catch (error) {
    console.error('Error updating status:', error);
    toast.error('Error', { description: 'Server connection failed' });
  } finally {
    isSubmitting.value = false;
  }
};
</script>
