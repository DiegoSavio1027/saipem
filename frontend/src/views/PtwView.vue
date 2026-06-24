<template>
  <DashboardLayout>
    <div class="p-6 space-y-6">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 class="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">{{ authState.userRole === 'Worker' ? 'My Permits' : 'Permit To Work (PTW)' }}</h1>
          <p class="text-slate-500 dark:text-slate-400">{{ authState.userRole === 'Worker' ? 'View and manage your submitted permits' : 'Manage and review all work permits' }}</p>
        </div>
        <button @click="showModal = true" class="bg-[var(--color-saipem-tertiary)] hover:bg-[var(--color-saipem-tertiary)]/90 text-white px-4 py-2 rounded-md font-medium text-sm transition-colors shadow-sm flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M12 5v14"/></svg>
            Create PTW
        </button>
      </div>

      <!-- Latest Permit Card - Worker only -->
      <div v-if="authState.userRole === 'Worker' && ptwList.length > 0" class="bg-gradient-to-br from-orange-50 to-orange-100 dark:from-orange-900/20 dark:to-orange-800/20 p-6 rounded-xl border border-orange-200 dark:border-orange-700 shadow-sm">
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-orange-600 dark:text-orange-400">Latest Permit</p>
            <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 mt-2">{{ ptwList[0].permit_type_display || ptwList[0].permit_type }}</h3>
            <p class="text-sm text-slate-600 dark:text-slate-400 mt-1">
              {{ ptwList[0].work_order ? `${ptwList[0].work_order.wo_id} - ${ptwList[0].work_order.description}` : ptwList[0].wo_id }}
            </p>
            <div class="flex items-center gap-4 mt-3">
              <span class="text-xs text-slate-600 dark:text-slate-400">{{ ptwList[0].permit_id }}</span>
              <span :class="[
                'px-2 py-1 rounded text-xs font-semibold',
                ptwList[0].status === 'PENDING' ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400' :
                ptwList[0].status === 'APPROVED' ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400' :
                ptwList[0].status === 'WAITING_FOR_CLOSE' ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400' :
                ptwList[0].status === 'CLOSED' ? 'bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-400' :
                'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
              ]">
                {{ ptwList[0].status_display || ptwList[0].status }}
              </span>
            </div>
          </div>
          <button @click="viewDialogOpen = true; selectedPTW = ptwList[0]" class="px-4 py-2 bg-orange-600 hover:bg-orange-700 dark:bg-orange-700 dark:hover:bg-orange-800 text-white rounded-lg text-sm font-medium transition-colors shadow-sm">
            View Details
          </button>
        </div>
      </div>

      <div v-if="isLoading" class="p-12 flex justify-center bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700">
        <p class="text-slate-500 dark:text-slate-400 animate-pulse">Loading PTW data...</p>
      </div>

      <Card v-else class="mb-6">
        <CardHeader>
          <CardTitle>{{ authState.userRole === 'Worker' ? 'My Work Permits' : 'All Permits' }}</CardTitle>
          <CardDescription>{{ authState.userRole === 'Worker' ? 'View and manage your submitted permits' : 'View and manage all work permits' }}</CardDescription>
        </CardHeader>
        <CardContent>
          <DataTable
            :data="ptwList"
            :columns="columns"
            :bulk-actions="bulkActions"
            @bulk-action="handleBulkAction"
          />
        </CardContent>
      </Card>
    </div>
  </DashboardLayout>

  <PtwModal
      :show="showModal"
      :username="authState.username"
      :user-role="authState.userRole"
      :last-permit-id="lastPermitId"
      @close="showModal = false"
      @submit-ptw="submitPTW"
  />

  <!-- Modal Dialogs -->
  <ViewPTWDialog
    :open="viewDialogOpen"
    :ptw="selectedPTW"
    @update:open="viewDialogOpen = $event"
  />

  <ApproveSignatureDialog
    :open="approveDialogOpen"
    :permit-id="selectedPTW?.permit_id || ''"
    :ptw-id="selectedPTWId || 0"
    @update:open="approveDialogOpen = $event"
    @approve="approvePTW"
  />

  <RejectDialog
    :open="rejectDialogOpen"
    :permit-id="selectedPTW?.permit_id || ''"
    :ptw-id="selectedPTWId || 0"
    @update:open="rejectDialogOpen = $event"
    @reject="rejectPTW"
  />

  <ConfirmCloseDialog
    :open="confirmCloseDialogOpen"
    :permit-id="selectedPTW?.permit_id || ''"
    :ptw-id="selectedPTWId || 0"
    @update:open="confirmCloseDialogOpen = $event"
    @confirm="confirmClosePTW"
  />

  <MarkDoneDialog
    :open="markDoneDialogOpen"
    :permit-id="selectedPTW?.permit_id || ''"
    :ptw-id="selectedPTWId || 0"
    @update:open="markDoneDialogOpen = $event"
    @mark-done="markAsDone"
  />

  <EditPTWDialog
    :open="editDialogOpen"
    :ptw="selectedPTW"
    @update:open="editDialogOpen = $event"
    @save="fetchPtw"
  />

  <DeleteConfirmDialog
    :open="deleteDialogOpen"
    :permit-id="selectedPTW?.permit_id || ''"
    :permit-type="selectedPTW?.permit_type_display || selectedPTW?.permit_type || ''"
    @update:open="deleteDialogOpen = $event"
    @confirm="confirmDelete"
  />
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import DashboardLayout from '@/layouts/DashboardLayout.vue';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import DataTable from './ptw/data-table.vue';
import { createColumns } from './ptw/columns';
import PtwModal from '@/components/PtwModal.vue';
import ViewPTWDialog from '@/components/ptw-dialogs/ViewPTWDialog.vue';
import ApproveSignatureDialog from '@/components/ptw-dialogs/ApproveSignatureDialog.vue';
import RejectDialog from '@/components/ptw-dialogs/RejectDialog.vue';
import ConfirmCloseDialog from '@/components/ptw-dialogs/ConfirmCloseDialog.vue';
import MarkDoneDialog from '@/components/ptw-dialogs/MarkDoneDialog.vue';
import EditPTWDialog from '@/components/ptw-dialogs/EditPTWDialog.vue';
import DeleteConfirmDialog from '@/components/ptw-dialogs/DeleteConfirmDialog.vue';
import { authState, getAccessToken } from '@/store/auth';
import { getCsrfToken } from '@/utils/csrf';
import { toast } from 'vue-sonner';
import { ptwSocketState, initializePTWWebSocket, closePTWWebSocket } from '@/store/websocket';
import { addToQueue } from '@/utils/offlineSync';

const router = useRouter();
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';
const ptwList = ref([]);
const isLoading = ref(true);
const showModal = ref(false);

// Modal dialog states
const viewDialogOpen = ref(false);
const approveDialogOpen = ref(false);
const rejectDialogOpen = ref(false);
const confirmCloseDialogOpen = ref(false);
const markDoneDialogOpen = ref(false);
const editDialogOpen = ref(false);
const deleteDialogOpen = ref(false);

const selectedPTW = ref(null);
const selectedPTWId = ref(null);

const columns = createColumns(authState, {
  onView: (ptw) => {
    selectedPTW.value = ptw;
    viewDialogOpen.value = true;
  },
  onApprove: (id) => {
    const ptw = ptwList.value.find(p => p.id === id);
    if (ptw) {
      selectedPTW.value = ptw;
      selectedPTWId.value = id;
      approveDialogOpen.value = true;
    }
  },
  onReject: (id) => {
    const ptw = ptwList.value.find(p => p.id === id);
    if (ptw) {
      selectedPTW.value = ptw;
      selectedPTWId.value = id;
      rejectDialogOpen.value = true;
    }
  },
  onConfirmClose: (id) => {
    const ptw = ptwList.value.find(p => p.id === id);
    if (ptw) {
      selectedPTW.value = ptw;
      selectedPTWId.value = id;
      confirmCloseDialogOpen.value = true;
    }
  },
  onMarkDone: (id) => {
    const ptw = ptwList.value.find(p => p.id === id);
    if (ptw) {
      selectedPTW.value = ptw;
      selectedPTWId.value = id;
      markDoneDialogOpen.value = true;
    }
  },
  onEdit: (ptw) => editPTW(ptw),
  onDelete: (id) => deletePTW(id),
});

const lastPermitId = computed(() => {
    if (ptwList.value.length === 0) return null;
    const sorted = [...ptwList.value].sort((a, b) => {
        const numA = parseInt(a.permit_id.match(/\d+/)[0], 10);
        const numB = parseInt(b.permit_id.match(/\d+/)[0], 10);
        return numB - numA;
    });
    return sorted[0]?.permit_id;
});

const bulkActions = [
  { key: 'approve', label: 'Approve All', variant: 'default' },
  { key: 'reject', label: 'Reject All', variant: 'destructive' }
];

const handleBulkAction = async (actionKey, rows) => {
  const ids = rows.map(row => row.id);
  if (actionKey === 'approve') {
    await bulkApprovePTW(ids);
  } else if (actionKey === 'reject') {
    await bulkRejectPTW(ids);
  }
};

const fetchPtw = async () => {
    try {
        const params = new URLSearchParams();
        if (authState.selectedVessel) {
            params.append('vessel', authState.selectedVessel.asset_id);
        }
        if (authState.userRole === 'Worker') {
            params.append('emp_id', authState.empId);
        }
        const queryString = params.toString() ? `?${params.toString()}` : '';
        const response = await fetch(`${API_BASE_URL}/hse/ptw/${queryString}`, {
            headers: {
                'Authorization': `Bearer ${getAccessToken()}`
            }
        });

        if (response.ok) {
            ptwList.value = await response.json();
        } else {
            toast.error("Failed", { description: "Failed to load PTW data." });
        }
    } catch (error) {
        toast.error("Error", { description: "Server connection failed." });
    } finally {
        isLoading.value = false;
    }
};

const submitPTW = async (formDataPayload) => {
    try {
        const response = await fetch(`${API_BASE_URL}/hse/ptw/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken() || '',
                'Authorization': `Bearer ${getAccessToken()}`
            },
            body: JSON.stringify(formDataPayload)
        });

        if (response.ok) {
            showModal.value = false;
            fetchPtw();
            toast.success("Success", { description: "PTW request sent successfully." });
        } else {
            const errorData = await response.json();
            const errorMsgs = Object.values(errorData).flat();
            const errorMsg = errorMsgs[0] || "Failed to send PTW request.";
            console.error("Error submitting PTW:", errorData);
            toast.error("Failed", { description: errorMsg });
        }
    } catch (error) {
        console.error("Error submitting PTW, queuing offline:", error);
        
        // Queue offline on connection failure
        addToQueue('PTW_CREATE', `${API_BASE_URL}/hse/ptw/`, formDataPayload, {
            'Authorization': `Bearer ${getAccessToken()}`,
            'X-CSRFToken': getCsrfToken() || ''
        });

        // Insert temporary mock permit into the list
        const mockPtw = {
            id: Date.now(),
            permit_id: 'PTW-QUEUED',
            emp_id: formDataPayload.emp_id,
            applicant: formDataPayload.emp_id,
            permit_type: formDataPayload.permit_type,
            permit_type_display: formDataPayload.permit_type.replace('_', ' '),
            wo_id: formDataPayload.wo_id,
            deck_location: formDataPayload.deck_location,
            deck_location_name: 'Queued (Offline)',
            status: 'PENDING',
            status_display: 'Offline Queued',
            created_at: new Date().toISOString()
        };
        ptwList.value = [mockPtw, ...ptwList.value];
        showModal.value = false;
    }
};

const viewPTW = (ptw) => {
    toast.info("PTW Details", { description: `Permit ID: ${ptw.permit_id} - ${ptw.applicant} - ${ptw.deck_location}` });
};

const approvePTW = async (signature) => {
    try {
        const response = await fetch(`${API_BASE_URL}/hse/ptw/${selectedPTWId.value}/approve/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken() || '',
                'Authorization': `Bearer ${getAccessToken()}`
            },
            body: JSON.stringify({ signature })
        });
        

        if (response.ok) {
            fetchPtw();
            toast.success("Approved", { description: "PTW approved successfully." });
        } else {
            const error = await response.json();
            console.error("Error approving PTW:", error);
            toast.error("Failed", { description: error.error || "Failed to approve PTW." });
        }
    } catch (error) {
        console.error("Failed to Approve:", error);
        toast.error("Error", { description: "Server connection failed." });
    }
};

const rejectPTW = async (rejection_reason) => {
    try {
        const response = await fetch(`${API_BASE_URL}/hse/ptw/${selectedPTWId.value}/reject/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken() || '',
                'Authorization': `Bearer ${getAccessToken()}`
            },
            body: JSON.stringify({ rejection_reason })
        });

        if (response.ok) {
            fetchPtw();
            toast.success("Rejected", { description: "PTW rejected successfully." });
        } else {
            const error = await response.json();
            console.error("Error rejecting PTW:", error);
            toast.error("Failed", { description: error.error || "Failed to reject PTW." });
        }
    } catch (error) {
        console.error("Failed to Reject:", error);
        toast.error("Error", { description: "Server connection failed." });
    }
};

const editPTW = (ptw) => {
    selectedPTW.value = ptw;
    selectedPTWId.value = ptw.id;
    editDialogOpen.value = true;
};

const deletePTW = (ptw_id) => {
    const ptw = ptwList.value.find(p => p.id === ptw_id);
    if (ptw) {
      selectedPTW.value = ptw;
      selectedPTWId.value = ptw_id;
      deleteDialogOpen.value = true;
    }
};

const confirmDelete = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/hse/ptw/${selectedPTWId.value}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCsrfToken() || '',
                'Authorization': `Bearer ${getAccessToken()}`
            }
        });

        if (response.ok || response.status === 204) {
            deleteDialogOpen.value = false;
            fetchPtw();
            toast.success("Deleted", { description: "PTW deleted successfully." });
        } else {
             console.error("Error deleting PTW:", await response.text());
             toast.error("Failed", { description: "Failed to delete PTW." });
        }
    } catch (error) {
        console.error("Failed to Delete:", error);
        toast.error("Error", { description: "Server connection failed." });
    }
};

const markAsDone = async (completion_notes) => {
    try {
        const response = await fetch(`${API_BASE_URL}/hse/ptw/${selectedPTWId.value}/mark_done/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken() || '',
                'Authorization': `Bearer ${getAccessToken()}`
            },
            body: JSON.stringify({ completion_notes })
        });

        if (response.ok) {
            fetchPtw();
            toast.success("Success", { description: "PTW marked as job done. Waiting for Safety Officer confirmation." });
        } else {
            const error = await response.json();
            console.error("Error marking PTW as done:", error);
            toast.error("Failed", { description: error.error || "Failed to mark PTW as job done." });
        }
    } catch (error) {
        console.error("Failed to Mark as Done:", error);
        toast.error("Error", { description: "Server connection failed." });
    }
};

const confirmClosePTW = async (closing_notes) => {
    try {
        const response = await fetch(`${API_BASE_URL}/hse/ptw/${selectedPTWId.value}/confirm_close/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken() || '',
                'Authorization': `Bearer ${getAccessToken()}`
            },
            body: JSON.stringify({ closing_notes })
        });

        if (response.ok) {
            fetchPtw();
            toast.success("Success", { description: "PTW closed successfully. Worker returned to Safe Zone." });
        } else {
            const error = await response.json();
            console.error("Error confirming close:", error);
            toast.error("Failed", { description: error.error || "Failed to close PTW." });
        }
    } catch (error) {
        console.error("Failed to Confirm Close:", error);
        toast.error("Error", { description: "Server connection failed." });
    }
};

const bulkApprovePTW = async (ptw_ids) => {
    try {
        let successCount = 0;
        for (const ptw_id of ptw_ids) {
            const response = await fetch(`${API_BASE_URL}/hse/ptw/${ptw_id}/approve/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken() || '',
                    'Authorization': `Bearer ${getAccessToken()}`
                }
            });
            if (response.ok) {
                successCount++;
            }
        }
        fetchPtw();
        toast.success("Success", { description: `${successCount} PTW approved successfully.` });
    } catch (error) {
        console.error("Failed Bulk Approve:", error);
        toast.error("Failed", { description: "Failed to perform bulk approve." });
    }
};

const bulkRejectPTW = async (ptw_ids) => {
    try {
        let successCount = 0;
        for (const ptw_id of ptw_ids) {
            const response = await fetch(`${API_BASE_URL}/hse/ptw/${ptw_id}/reject/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken() || '',
                    'Authorization': `Bearer ${getAccessToken()}`
                }
            });
            if (response.ok) {
                successCount++;
            }
        }
        fetchPtw();
        toast.success("Success", { description: `${successCount} PTW rejected successfully.` });
    } catch (error) {
        console.error("Failed Bulk Reject:", error);
        toast.error("Failed", { description: "Failed to perform bulk reject." });
    }
};

onMounted(async () => {
    await fetchPtw();
    initializePTWWebSocket();
    window.addEventListener('offline-sync-complete', fetchPtw);
});

onUnmounted(() => {
    closePTWWebSocket();
    window.removeEventListener('offline-sync-complete', fetchPtw);
});

watch(() => ptwSocketState.lastUpdate, () => {
    if (ptwSocketState.lastUpdate > 0) {
        fetchPtw();
    }
});
</script>
