<template>
  <DashboardLayout>
    <div class="p-6 space-y-6">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 class="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
            {{ authState.userRole === 'Worker' ? 'My Incidents' : 'HSE Incidents' }}
          </h1>
          <p class="text-slate-500 dark:text-slate-400">
            {{ authState.userRole === 'Worker' ? 'View and report your safety observations' : 'Manage and review all safety incidents' }}
          </p>
        </div>
        <div class="flex items-center gap-3">
          <!-- Change Global Status Button - Safety Officer and Admin only -->
          <button
            v-if="authState.userRole !== 'Worker'"
            @click="showConditionChangeDialog = true"
            :class="globalStatus === 'GREEN' ? 'bg-green-100 text-green-700 hover:bg-green-200' : globalStatus === 'YELLOW' ? 'bg-yellow-100 text-yellow-700 hover:bg-yellow-200' : 'bg-red-100 text-red-700 hover:bg-red-200'"
            class="px-3 py-2 rounded-md text-sm font-semibold uppercase transition-colors cursor-pointer flex items-center gap-2"
          >
            CONDITION {{ globalStatus }}
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="m6 9 6 6 6-6"/>
            </svg>
          </button>
          <!-- Report Incident Button - All users can report -->
          <button @click="openReportDialog" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md font-medium text-sm transition-colors shadow-sm flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M12 5v14"/></svg>
            Report Incident
          </button>
        </div>
      </div>

      <!-- Latest Incident Card - Worker only -->
      <div v-if="authState.userRole === 'Worker' && incidents.length > 0" class="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 p-6 rounded-xl border border-blue-200 dark:border-blue-700">
        <div class="flex items-start justify-between">
          <div>
            <p class="text-sm font-medium text-blue-600 dark:text-blue-400">Latest Incident</p>
            <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 mt-2">{{ incidents[0].severity_display }}</h3>
            <p class="text-sm text-slate-600 dark:text-slate-400 mt-1">{{ incidents[0].description }}</p>
            <div class="flex items-center gap-4 mt-3">
              <span class="text-xs text-slate-600 dark:text-slate-400">{{ formatIncidentDate(incidents[0].incident_date) }}</span>
              <span :class="[
                'px-2 py-1 rounded text-xs font-semibold',
                incidents[0].status === 'OPEN' ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400' :
                incidents[0].status === 'INVESTIGATING' ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400' :
                'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400'
              ]">
                {{ incidents[0].status_display }}
              </span>
            </div>
          </div>
          <button @click="viewIncident(incidents[0])" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors">
            View Details
          </button>
        </div>
      </div>

      <div v-if="isLoading" class="p-12 flex justify-center bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700">
        <p class="text-slate-500 dark:text-slate-400 animate-pulse">Loading incidents...</p>
      </div>

      <Card v-else class="mb-6">
        <CardHeader>
          <CardTitle>{{ authState.userRole === 'Worker' ? 'My Incidents' : 'All Incidents' }}</CardTitle>
          <CardDescription>{{ authState.userRole === 'Worker' ? 'Your reported safety observations' : 'View and manage all safety incidents' }}</CardDescription>
        </CardHeader>
        <CardContent>
          <DataTable
            :data="incidents"
            :columns="columns"
            :bulk-actions="bulkActions"
            @bulk-action="handleBulkAction"
          />
        </CardContent>
      </Card>
    </div>

    <!-- Report Incident Dialog -->
    <IncidentReportForm
      :open="isReportDialogOpen"
      @update:open="isReportDialogOpen = $event"
      :empId="authState.empId"
      @incident-reported="handleIncidentReported"
    />

    <!-- View Incident Dialog -->
    <IncidentDetailDialog
      :open="isViewDialogOpen"
      :incident="selectedIncident"
      @update:open="isViewDialogOpen = $event"
    />

    <!-- Delete Incident Dialog -->
    <DeleteConfirmDialog
      :open="isDeleteDialogOpen"
      :permit-id="selectedIncident?.incident_id || `#${selectedIncident?.id}`"
      :permit-type="`${selectedIncident?.severity_display} Incident`"
      item-type="Incident"
      @update:open="isDeleteDialogOpen = $event"
      @confirm="confirmDeleteIncident"
    />

    <!-- Condition Change Dialog -->
    <ConditionChangeDialog
      :open="showConditionChangeDialog"
      :current-status="globalStatus"
      @update:open="showConditionChangeDialog = $event"
      @confirm="handleConditionChange"
    />

    <!-- Incident Verification Dialog -->
    <IncidentVerificationDialog
      :open="isVerificationDialogOpen"
      :incident="selectedIncident"
      @update:open="isVerificationDialogOpen = $event"
      @verified="handleIncidentVerified"
    />
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue';
import { authState, getAccessToken } from '@/store/auth';
import { toast } from 'vue-sonner';
import DashboardLayout from '@/layouts/DashboardLayout.vue';
import IncidentReportForm from '@/components/IncidentReportForm.vue';
import IncidentDetailDialog from '@/components/dialogs/IncidentDetailDialog.vue';
import ConditionChangeDialog from '@/components/dialogs/ConditionChangeDialog.vue';
import DeleteConfirmDialog from '@/components/ptw-dialogs/DeleteConfirmDialog.vue';
import IncidentVerificationDialog from '@/components/dialogs/IncidentVerificationDialog.vue';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { getCsrfToken } from '@/utils/csrf';
import DataTable from '@/views/incidents/data-table.vue';
import { createColumns } from '@/views/incidents/columns';
import { incidentsSocketState, initializeIncidentsWebSocket, closeIncidentsWebSocket } from '@/store/websocket';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';

let abortController = new AbortController();

const incidents = ref([]);
const isLoading = ref(false);
const isReportDialogOpen = ref(false);
const isViewDialogOpen = ref(false);
const isDeleteDialogOpen = ref(false);
const isVerificationDialogOpen = ref(false);
const showConditionChangeDialog = ref(false);
const selectedIncident = ref(null);
const globalStatus = ref('GREEN');

const columns = createColumns(
  (incident) => viewIncident(incident),
  (incident) => investigateIncident(incident),
  (incident) => closeIncident(incident),
  (incident) => deleteIncident(incident),
  authState.userRole,
  (incident) => verifyIncident(incident)
);

const bulkActions = authState.userRole !== 'Worker' ? [
  { key: 'investigate', label: 'Mark as Investigating', variant: 'default' },
  { key: 'close', label: 'Close Selected', variant: 'default' }
] : [];

const handleBulkAction = async (actionKey, rows) => {
  if (actionKey === 'investigate') {
    if (!confirm(`Are you sure you want to mark ${rows.length} incident(s) as investigating?`)) {
      return;
    }

    try {
      for (const incident of rows) {
        if (incident.status === 'OPEN') {
          await fetch(`${API_BASE_URL}/hse/incidents/${incident.id}/`, {
            method: 'PATCH',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCsrfToken() || '',
              'Authorization': `Bearer ${getAccessToken()}`
            },
            body: JSON.stringify({ status: 'INVESTIGATING' }),
            credentials: 'include'
          });
        }
      }

      toast.success(`${rows.length} incident(s) marked as investigating`);
      fetchIncidents();
    } catch (error) {
      console.error('Error updating incidents:', error);
      toast.error('Failed to update incidents');
    }
  } else if (actionKey === 'close') {
    if (!confirm(`Are you sure you want to close ${rows.length} incident(s)?`)) {
      return;
    }

    try {
      for (const incident of rows) {
        if (incident.status === 'INVESTIGATING') {
          await fetch(`${API_BASE_URL}/hse/incidents/${incident.id}/`, {
            method: 'PATCH',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCsrfToken() || '',
              'Authorization': `Bearer ${getAccessToken()}`
            },
            body: JSON.stringify({ status: 'CLOSED' }),
            credentials: 'include'
          });
        }
      }

      toast.success(`${rows.length} incident(s) closed successfully`);
      fetchIncidents();
    } catch (error) {
      console.error('Error closing incidents:', error);
      toast.error('Failed to close incidents');
    }
  }
};

const fetchIncidents = async () => {
  isLoading.value = true;
  try {
    const params = new URLSearchParams();
    if (authState.selectedVessel) {
      params.append('vessel', authState.selectedVessel.asset_id);
    }
    if (authState.userRole === 'Worker') {
      params.append('emp_id', authState.empId);
    }
    const queryString = params.toString() ? `?${params.toString()}` : '';
    const response = await fetch(`${API_BASE_URL}/hse/incidents/${queryString}`, {
      headers: {
        'Authorization': `Bearer ${getAccessToken()}`
      },
      credentials: 'include',
      signal: abortController.signal
    });
    if (response.ok) {
      incidents.value = await response.json();
    } else {
      toast.error('Failed to load incidents');
    }
  } catch (error) {
    if (error.name !== 'AbortError') {
      console.error('Error fetching incidents:', error);
      toast.error('Error loading incidents');
    }
  } finally {
    isLoading.value = false;
  }
};

const fetchSystemStatus = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/hse/status/current/`, {
      headers: {
        'Authorization': `Bearer ${getAccessToken()}`
      },
      credentials: 'include'
    });
    if (response.ok) {
      const data = await response.json();
      globalStatus.value = data.global_status;
    }
  } catch (error) {
    console.error('Error fetching system status:', error);
  }
};

const openReportDialog = () => {
  isReportDialogOpen.value = true;
};

const formatIncidentDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const viewIncident = (incident) => {
  selectedIncident.value = incident;
  isViewDialogOpen.value = true;
};

const investigateIncident = async (incident) => {
  try {
    const response = await fetch(`${API_BASE_URL}/hse/incidents/${incident.id}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken() || '',
        'Authorization': `Bearer ${getAccessToken()}`
      },
      body: JSON.stringify({ status: 'INVESTIGATING' }),
      credentials: 'include'
    });

    if (response.ok) {
      toast.success('Incident marked as investigating');
      fetchIncidents();
    } else {
      toast.error('Failed to update incident');
    }
  } catch (error) {
    console.error('Error updating incident:', error);
    toast.error('Error updating incident');
  }
};

const closeIncident = async (incident) => {
  try {
    const response = await fetch(`${API_BASE_URL}/hse/incidents/${incident.id}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken() || '',
        'Authorization': `Bearer ${getAccessToken()}`
      },
      body: JSON.stringify({ status: 'CLOSED' }),
      credentials: 'include'
    });

    if (response.ok) {
      toast.success('Incident closed successfully');
      fetchIncidents();
    } else {
      toast.error('Failed to close incident');
    }
  } catch (error) {
    console.error('Error closing incident:', error);
    toast.error('Error closing incident');
  }
};

const deleteIncident = (incident) => {
  selectedIncident.value = incident;
  isDeleteDialogOpen.value = true;
};

const verifyIncident = (incident) => {
  selectedIncident.value = incident;
  isVerificationDialogOpen.value = true;
};

const confirmDeleteIncident = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/hse/incidents/${selectedIncident.value.id}/`, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': getCsrfToken() || '',
        'Authorization': `Bearer ${getAccessToken()}`
      },
      credentials: 'include'
    });

    if (response.ok || response.status === 204) {
      isDeleteDialogOpen.value = false;
      fetchIncidents();
      toast.success('Incident deleted successfully');
    } else {
      toast.error('Failed to delete incident');
    }
  } catch (error) {
    console.error('Error deleting incident:', error);
    toast.error('Error deleting incident');
  }
};

const handleIncidentReported = () => {
  fetchIncidents();
  toast.success('Incident reported successfully');
};

const handleIncidentVerified = () => {
  fetchIncidents();
  fetchSystemStatus();
  toast.success('Incident verified and metrics updated');
};

const handleConditionChange = (newStatus) => {
  globalStatus.value = newStatus;
  fetchSystemStatus();

  if (newStatus === 'RED') {
    toast.error("🚨 EMERGENCY MODE ACTIVATED", {
      description: "All new PTW approvals are frozen. Evacuation protocols may be initiated.",
      duration: 10000
    });
  } else if (newStatus === 'YELLOW') {
    toast.warning("⚠️ HEIGHTENED ALERT", {
      description: "System is in warning mode. Extra caution required.",
      duration: 5000
    });
  }
};

onMounted(() => {
  abortController = new AbortController();
  fetchIncidents();
  fetchSystemStatus();
  initializeIncidentsWebSocket();
});

onBeforeUnmount(() => {
  abortController.abort();
  closeIncidentsWebSocket();
});

watch(() => incidentsSocketState.lastUpdate, () => {
  if (incidentsSocketState.lastUpdate > 0) {
    fetchIncidents();
    fetchSystemStatus();
  }
});
</script>
