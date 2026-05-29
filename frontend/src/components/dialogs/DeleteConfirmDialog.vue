<template>
  <Dialog :open="open" @update:open="$emit('update:open', $event)">
    <DialogContent class="max-w-sm">
      <DialogHeader>
        <DialogTitle>Delete Incident</DialogTitle>
        <DialogDescription>Are you sure you want to delete this incident?</DialogDescription>
      </DialogHeader>

      <div class="bg-red-50 border border-red-200 rounded-lg p-3 text-sm text-red-800">
        <p class="font-semibold">⚠️ This action cannot be undone.</p>
        <p class="mt-1">Incident {{ incident?.incident_id || `#${incident?.id}` }} will be permanently deleted.</p>
      </div>

      <DialogFooter>
        <Button @click="$emit('update:open', false)" variant="outline">Cancel</Button>
        <Button @click="handleConfirm" :disabled="isDeleting" class="bg-red-600 hover:bg-red-700">
          {{ isDeleting ? 'Deleting...' : 'Delete Incident' }}
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

<script setup>
import { ref } from 'vue';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { toast } from 'vue-sonner';
import { getCsrfToken } from '@/utils/csrf';

const props = defineProps({
  open: Boolean,
  incident: Object
});

const emit = defineEmits(['update:open', 'confirmed']);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';
const isDeleting = ref(false);

const handleConfirm = async () => {
  isDeleting.value = true;
  try {
    const response = await fetch(`${API_BASE_URL}/hse/incidents/${props.incident.id}/`, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': getCsrfToken() || ''
      },
      credentials: 'include'
    });

    if (response.ok) {
      toast.success('Incident deleted successfully');
      emit('confirmed');
      emit('update:open', false);
    } else {
      toast.error('Failed to delete incident');
    }
  } catch (error) {
    console.error('Error deleting incident:', error);
    toast.error('Error deleting incident');
  } finally {
    isDeleting.value = false;
  }
};
</script>
