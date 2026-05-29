<template>
  <Dialog :open="open" @update:open="$emit('update:open', $event)">
    <DialogContent class="max-w-2xl">
      <DialogHeader>
        <DialogTitle>Edit PTW - {{ ptw?.permit_id }}</DialogTitle>
        <DialogDescription>
          Update permit details. Only PENDING permits can be edited.
        </DialogDescription>
      </DialogHeader>

      <div v-if="ptw" class="space-y-4 max-h-[60vh] overflow-y-auto">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <Label class="text-sm font-semibold text-slate-700">Permit ID</Label>
            <p class="text-sm text-slate-600 mt-1">{{ ptw.permit_id }}</p>
          </div>
          <div>
            <Label class="text-sm font-semibold text-slate-700">Status</Label>
            <p class="text-sm text-slate-600 mt-1">{{ ptw.status_display || ptw.status }}</p>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <Label class="text-sm font-semibold text-slate-700">Permit Type</Label>
            <p class="text-sm text-slate-600 mt-1">{{ ptw.permit_type_display || ptw.permit_type }}</p>
          </div>
          <div>
            <Label class="text-sm font-semibold text-slate-700">Work Order</Label>
            <p class="text-sm text-slate-600 mt-1">{{ ptw.wo_id }}</p>
          </div>
        </div>

        <div>
          <Label for="location" class="text-sm font-semibold text-slate-700">Location</Label>
          <Select v-model="editData.deck_location">
            <SelectTrigger class="w-full mt-1">
              <SelectValue placeholder="Select location" />
            </SelectTrigger>
            <SelectContent class="w-full">
              <SelectGroup>
                <SelectItem v-for="loc in locations" :key="loc.id" :value="loc.name">
                  {{ loc.name }}
                </SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>

        <div>
          <Label class="text-sm font-semibold text-slate-700">Applicant</Label>
          <p class="text-sm text-slate-600 mt-1">{{ ptw.employee?.full_name || ptw.emp_id }}</p>
        </div>

        <div>
          <Label class="text-sm font-semibold text-slate-700">Created</Label>
          <p class="text-sm text-slate-600 mt-1">{{ formatDate(ptw.created_at) }}</p>
        </div>
      </div>

      <DialogFooter>
        <Button variant="outline" @click="$emit('update:open', false)">Cancel</Button>
        <Button @click="handleSave" :disabled="isSaving">
          {{ isSaving ? 'Saving...' : 'Save Changes' }}
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { authState } from '@/store/auth';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { toast } from 'vue-sonner';
import { getCsrfToken } from '@/utils/csrf';

const props = defineProps({
  open: Boolean,
  ptw: Object,
});

const emit = defineEmits(['update:open', 'save']);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';
const editData = ref({ deck_location: '' });
const isSaving = ref(false);
const locations = ref([]);

const fetchLocations = async () => {
  try {
    // Get vessel from authState (assigned vessel for non-admin, selected vessel for admin)
    const vesselId = authState.selectedVessel?.asset_id || authState.assignedVessel?.asset_id;

    if (!vesselId) {
      console.warn('No vessel assigned. Cannot fetch locations.');
      locations.value = [];
      return;
    }

    const response = await fetch(`${API_BASE_URL}/offshore/locations/?vessel_id=${vesselId}`, {
      credentials: 'include'
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    locations.value = data;
  } catch (error) {
    console.error('Failed to fetch locations:', error);
    locations.value = [];
  }
};

onMounted(() => {
  fetchLocations();
});

watch(() => props.ptw, (newPtw) => {
  if (newPtw) {
    editData.value = {
      deck_location: newPtw.deck_location || ''
    };
  }
}, { immediate: true });

const formatDate = (dateString) => {
  if (!dateString) return '-';
  return new Date(dateString).toLocaleString();
};

const handleSave = async () => {
  if (!props.ptw) return;

  isSaving.value = true;
  try {
    const response = await fetch(`${API_BASE_URL}/hse/ptw/${props.ptw.id}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken() || ''
      },
      body: JSON.stringify({
        deck_location: editData.value.deck_location
      }),
      credentials: 'include'
    });

    if (response.ok) {
      toast.success("Updated", { description: "PTW updated successfully." });
      emit('save');
      emit('update:open', false);
    } else {
      const error = await response.json();
      toast.error("Failed", { description: error.detail || "Failed to update PTW." });
    }
  } catch (error) {
    console.error("Error updating PTW:", error);
    toast.error("Error", { description: "Server connection failed." });
  } finally {
    isSaving.value = false;
  }
};
</script>
