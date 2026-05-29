<template>
  <DashboardLayout>
    <div class="p-6 space-y-6">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 class="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">Work Locations</h1>
          <p class="text-slate-500 dark:text-slate-400">Manage offshore rig zones and areas</p>
        </div>
        <button @click="openModal()" class="bg-[var(--color-saipem-tertiary)] hover:bg-[var(--color-saipem-tertiary)]/90 text-white px-4 py-2 rounded-md font-medium text-sm transition-colors shadow-sm flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M12 5v14"/></svg>
            Add Location
        </button>
      </div>

      <div v-if="isLoading" class="p-12 flex justify-center">
        <p class="text-slate-500 dark:text-slate-400 animate-pulse">Loading locations...</p>
      </div>
      <Card v-else class="mb-6">
        <CardHeader>
          <CardTitle>Available Zones</CardTitle>
          <CardDescription>All registered work locations on the offshore rig</CardDescription>
        </CardHeader>
        <CardContent>
          <DataTable
            :columns="tableColumns"
            :data="locations"
            :bulk-actions="bulkActions"
            @bulk-action="handleBulkAction"
          />
        </CardContent>
      </Card>
    </div>

    <!-- Modal Form -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm">
        <div class="bg-white dark:bg-slate-800 rounded-xl shadow-lg w-full max-w-md overflow-hidden animate-in fade-in zoom-in-95 duration-200">
            <div class="p-6 border-b border-slate-100 dark:border-slate-700 flex justify-between items-center">
                <h3 class="text-lg font-bold text-slate-900 dark:text-slate-100">{{ isEditing ? 'Edit Location' : 'Add New Location' }}</h3>
                <button @click="closeModal" class="text-slate-400 dark:text-slate-500 hover:text-slate-600 dark:hover:text-slate-400 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
                </button>
            </div>

            <form @submit.prevent="saveLocation" class="p-6 space-y-4">
                <div class="space-y-2">
                    <label class="text-sm font-semibold text-slate-700 dark:text-slate-300">Deck Name <span class="text-red-500">*</span></label>
                    <input v-model="formData.deck_name" type="text" required class="w-full h-10 px-3 rounded-md border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-[var(--color-saipem-tertiary)] focus:border-transparent transition-shadow text-sm" placeholder="e.g. Main Deck" />
                </div>

                <div class="space-y-2">
                    <label class="text-sm font-semibold text-slate-700 dark:text-slate-300">Risk Level <span class="text-red-500">*</span></label>
                    <select v-model="formData.risk_level" required class="w-full h-10 px-3 rounded-md border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-[var(--color-saipem-tertiary)] focus:border-transparent transition-shadow text-sm">
                        <option value="LOW">Low</option>
                        <option value="MEDIUM">Medium</option>
                        <option value="HIGH">High</option>
                    </select>
                </div>

                <div class="pt-4 flex gap-3 justify-end">
                    <button type="button" @click="closeModal" class="px-4 py-2 text-sm font-medium text-slate-700 dark:text-slate-300 bg-white dark:bg-slate-700 border border-slate-300 dark:border-slate-600 rounded-md hover:bg-slate-50 dark:hover:bg-slate-600 transition-colors">Cancel</button>
                    <button type="submit" :disabled="isSaving" class="px-4 py-2 text-sm font-medium text-white bg-[var(--color-saipem-tertiary)] rounded-md hover:bg-[var(--color-saipem-tertiary)]/90 transition-colors disabled:opacity-50 flex items-center gap-2">
                        <svg v-if="isSaving" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                        {{ isSaving ? 'Saving...' : 'Save Location' }}
                    </button>
                </div>
            </form>
        </div>
    </div>

    <!-- Delete Location Dialog -->
    <DeleteConfirmDialog
      :open="deleteDialogOpen"
      :permit-id="selectedLocation?.deck_name || ''"
      permit-type="Work Location"
      item-type="Location"
      @update:open="deleteDialogOpen = $event"
      @confirm="confirmDeleteLocation"
    />
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import DashboardLayout from '@/layouts/DashboardLayout.vue';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import DeleteConfirmDialog from '@/components/ptw-dialogs/DeleteConfirmDialog.vue';
import { toast } from 'vue-sonner';
import { getCsrfToken } from '@/utils/csrf';
import { authState } from '@/store/auth';
import DataTable from '@/views/work-location/data-table.vue';
import { columns } from '@/views/work-location/columns.ts';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';
const locations = ref([]);
const isLoading = ref(true);

const showModal = ref(false);
const isEditing = ref(false);
const isSaving = ref(false);
const formData = ref({ id: null, deck_name: '', risk_level: 'MEDIUM' });

const deleteDialogOpen = ref(false);
const selectedLocation = ref(null);

const tableColumns = computed(() => columns(
  (location) => openModal(location),
  (id) => deleteLocation(id)
));

const fetchLocations = async () => {
    isLoading.value = true;
    try {
        const vesselId = authState.selectedVessel?.asset_id || authState.assignedVessel?.asset_id;
        const url = vesselId
            ? `${API_BASE_URL}/offshore/locations/?vessel_id=${vesselId}`
            : `${API_BASE_URL}/offshore/locations/`;

        const response = await fetch(url, {
            credentials: 'include'
        });

        if (response.ok) {
            locations.value = await response.json();
        } else {
            toast.error("Failed", { description: "Failed to load Work Location data." });
        }
    } catch (error) {
        toast.error("Error", { description: "Server connection failed." });
    } finally {
        isLoading.value = false;
    }
};

const bulkActions = [
  { key: 'delete', label: 'Delete Selected', variant: 'destructive' }
];

const handleBulkAction = async (actionKey, rows) => {
  if (actionKey === 'delete') {
    if (!confirm(`Are you sure you want to delete ${rows.length} location(s)?`)) {
      return;
    }

    try {
      for (const location of rows) {
        await fetch(`${API_BASE_URL}/offshore/locations/${location.id}/`, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': getCsrfToken(),
          },
          credentials: 'include'
        });
      }

      toast.success(`${rows.length} location(s) deleted successfully`);
      fetchLocations();
    } catch (error) {
      console.error('Error deleting locations:', error);
      toast.error('Failed to delete locations');
    }
  }
};

onMounted(() => {
    fetchLocations();
});

// Watch for vessel changes and re-fetch locations
watch(() => authState.selectedVessel?.asset_id || authState.assignedVessel?.asset_id, (newVesselId) => {
    if (newVesselId) {
        fetchLocations();
    }
});

const openModal = (loc = null) => {
    if (loc) {
        isEditing.value = true;
        formData.value = { ...loc };
    } else {
        isEditing.value = false;
        formData.value = { id: null, deck_name: '', risk_level: 'MEDIUM' };
    }
    showModal.value = true;
};

const closeModal = () => {
    showModal.value = false;
    formData.value = { id: null, deck_name: '', risk_level: 'MEDIUM' };
};

const saveLocation = async () => {
    isSaving.value = true;
    const isUpdate = isEditing.value;
    const url = isUpdate ? `${API_BASE_URL}/offshore/locations/${formData.value.id}/` : `${API_BASE_URL}/offshore/locations/`;
    const method = isUpdate ? 'PUT' : 'POST';

    try {
        const vesselId = authState.selectedVessel?.asset_id || authState.assignedVessel?.asset_id;
        const payload = {
            deck_name: formData.value.deck_name,
            risk_level: formData.value.risk_level
        };

        if (!isUpdate && vesselId) {
            payload.vessel = vesselId;
        }

        const response = await fetch(url, {
            method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify(payload),
            credentials: 'include'
        });

        if (response.ok) {
            toast.success(isUpdate ? "Updated" : "Success", {
                description: `Work location ${formData.value.deck_name} successfully ${isUpdate ? 'updated' : 'added'}.`
            });
            closeModal();
            fetchLocations();
        } else {
            const data = await response.json();
            const errorMsg = data.deck_name ? data.deck_name[0] : 'Validation error occurred.';
            toast.error("Failed to Save", { description: errorMsg });
        }
    } catch (error) {
        toast.error("Error", { description: "Server connection failed." });
    } finally {
        isSaving.value = false;
    }
};

const deleteLocation = (id) => {
    const location = locations.value.find(loc => loc.id === id);
    if (location) {
        selectedLocation.value = location;
        deleteDialogOpen.value = true;
    }
};

const confirmDeleteLocation = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/offshore/locations/${selectedLocation.value.id}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCsrfToken(),
            },
            credentials: 'include'
        });

        if (response.ok || response.status === 204) {
            deleteDialogOpen.value = false;
            fetchLocations();
            toast.success("Deleted", { description: "Work location deleted successfully." });
        } else {
            toast.error("Failed", { description: "Failed to delete work location." });
        }
    } catch (error) {
        toast.error("Error", { description: "Server connection failed." });
    }
};
</script>
