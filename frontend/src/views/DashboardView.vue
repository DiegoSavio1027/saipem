<template>
  <DashboardLayout @open-modal="showModal = true">
      <!-- Weather & Global Status Area -->
      <div class="mb-6">
        <WeatherWidget />
      </div>

      <!-- Dashboard Stats - Only for Admin/Safety Officer -->
      <DashboardStats
          v-if="authState.userRole !== 'Worker'"
          :totalPob="totalPob"
          :liveFeeds="websocketState.liveFeeds"
          :activePermits="activePermits"
          :daysWithoutLTI="daysWithoutLTI"
          :nearMisses="nearMisses"
          :globalStatus="globalStatus"
          :vesselName="authState.selectedVessel?.name || 'All Vessels'"
      />

      <!-- Worker Dashboard -->
      <WorkerDashboard
          v-if="authState.userRole === 'Worker'"
          :myPTWs="myPTWs"
          @start-work="startWork"
          @mark-done="markAsDone"
          @edit="editPTW"
          @delete="deletePTW"
          @view="viewPTWDetails"
          @open-submit-modal="showModal = true"
      />

      <!-- Safety Officer/Admin Dashboard -->
      <PendingApprovals
          v-else
          :userRole="authState.userRole"
          :pendingPTWs="pendingPTWs"
          @approve="approvePTW"
          @reject="rejectPTW"
          @view-details="viewPTWDetails"
          @bulk-approve="bulkApprovePTW"
          @bulk-reject="bulkRejectPTW"
      />

      <!-- Waiting for Close PTWs -->
      <WaitingForClose
          v-if="authState.userRole !== 'Worker'"
          :userRole="authState.userRole"
          :waitingForClosePTWs="waitingForClosePTWs"
          @confirm-close="confirmClosePTW"
          @view-details="viewPTWDetails"
      />
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
    @approve="handleApproveWithSignature"
  />

  <RejectDialog
    :open="rejectDialogOpen"
    :permit-id="selectedPTW?.permit_id || ''"
    :ptw-id="selectedPTWId || 0"
    @update:open="rejectDialogOpen = $event"
    @reject="handleRejectWithReason"
  />

  <MarkDoneDialog
    :open="markDoneDialogOpen"
    :permit-id="selectedPTW?.permit_id || ''"
    :ptw-id="selectedPTWId || 0"
    @update:open="markDoneDialogOpen = $event"
    @mark-done="handleMarkDoneWithNotes"
  />

  <EditPTWDialog
    :open="editDialogOpen"
    :ptw="selectedPTW"
    @update:open="editDialogOpen = $event"
    @save="fetchInitialData"
  />

  <ConfirmCloseDialog
    :open="confirmCloseDialogOpen"
    :permit-id="selectedPTW?.permit_id || ''"
    :ptw-id="selectedPTWId || 0"
    @update:open="confirmCloseDialogOpen = $event"
    @confirm="handleConfirmClose"
  />

  <IncidentReportForm
    :open="showIncidentForm"
    :username="authState.username"
    @update:open="showIncidentForm = $event"
    @incident-reported="handleIncidentReported"
  />

  <ToolboxTalkDialog
    :open="toolboxTalkDialogOpen"
    :permit-id="selectedPTW?.permit_id || ''"
    :ptw-id="selectedPTWId || 0"
    @update:open="toolboxTalkDialogOpen = $event"
    @confirm="handleStartWorkConfirmed"
  />
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue';
import DashboardLayout from '@/layouts/DashboardLayout.vue';
import DashboardStats from '@/components/DashboardStats.vue';
import PendingApprovals from '@/components/PendingApprovals.vue';
import WaitingForClose from '@/components/WaitingForClose.vue';
import WorkerDashboard from '@/components/WorkerDashboard.vue';
import WeatherWidget from '@/components/WeatherWidget.vue';
import PtwModal from '@/components/PtwModal.vue';
import ViewPTWDialog from '@/components/ptw-dialogs/ViewPTWDialog.vue';
import ApproveSignatureDialog from '@/components/ptw-dialogs/ApproveSignatureDialog.vue';
import RejectDialog from '@/components/ptw-dialogs/RejectDialog.vue';
import ConfirmCloseDialog from '@/components/ptw-dialogs/ConfirmCloseDialog.vue';
import MarkDoneDialog from '@/components/ptw-dialogs/MarkDoneDialog.vue';
import EditPTWDialog from '@/components/ptw-dialogs/EditPTWDialog.vue';
import ToolboxTalkDialog from '@/components/ptw-dialogs/ToolboxTalkDialog.vue';
import IncidentReportForm from '@/components/IncidentReportForm.vue';
import { authState, getAccessToken } from '@/store/auth';
import { websocketState } from '@/store/websocket';
import { getCsrfToken } from '@/utils/csrf';
import { toast } from 'vue-sonner';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';

const totalPob = computed(() => {
    if (!websocketState.liveFeeds || websocketState.liveFeeds.length === 0) {
        return 0;
    }

    const personnelStatus = new Map();
    const sortedFeeds = [...websocketState.liveFeeds].reverse();

    sortedFeeds.forEach(feed => {
        const key = feed.employee_name;
        if (feed.action === 'IN') {
            personnelStatus.set(key, feed.location);
        } else if (feed.action === 'OUT') {
            personnelStatus.delete(key);
        }
    });

    return personnelStatus.size;
});
const pendingPTWs = ref([]);
const waitingForClosePTWs = ref([]);
const allPTWs = ref([]);
const showModal = ref(false);

// HSE Metrics
const activePermits = ref(0);
const daysWithoutLTI = ref(0);
const nearMisses = ref(0);
const globalStatus = ref('GREEN');
const showIncidentForm = ref(false);

const myPTWs = computed(() => {
    return allPTWs.value.filter(ptw => ptw.emp_id === authState.username);
});

// Modal dialog states
const viewDialogOpen = ref(false);
const approveDialogOpen = ref(false);
const rejectDialogOpen = ref(false);
const confirmCloseDialogOpen = ref(false);
const markDoneDialogOpen = ref(false);
const editDialogOpen = ref(false);
const toolboxTalkDialogOpen = ref(false);

const selectedPTW = ref(null);
const selectedPTWId = ref(null);

const lastPermitId = computed(() => {
    if (allPTWs.value.length === 0) return null;
    const sorted = [...allPTWs.value].sort((a, b) => {
        const numA = parseInt(a.permit_id.match(/\d+/)[0], 10);
        const numB = parseInt(b.permit_id.match(/\d+/)[0], 10);
        return numB - numA;
    });
    return sorted[0]?.permit_id;
});

const fetchInitialData = async () => {
    try {
        const vesselParam = authState.selectedVessel ? `?vessel=${authState.selectedVessel.asset_id}` : '';
        const response = await fetch(`${API_BASE_URL}/hse/ptw/${vesselParam}`, {
            headers: {
                'Authorization': `Bearer ${getAccessToken()}`
            }
        });
        if (response.ok) {
            const data = await response.json();
            allPTWs.value = data;

            const pending = data.filter(item => item.status === 'PENDING');
            pendingPTWs.value = pending;

            const waitingForClose = data.filter(item => item.status === 'WAITING_FOR_CLOSE');
            waitingForClosePTWs.value = waitingForClose;

            // Update activePermits count (APPROVED or IN_PROGRESS)
            const activePTWs = data.filter(item => item.status === 'APPROVED' || item.status === 'IN_PROGRESS');
            activePermits.value = activePTWs.length;
        }
    } catch (error) {
        console.error("Failed to fetch data:", error);
    }
};

const fetchHSEStatus = async () => {
    try {
        const vesselParam = authState.selectedVessel ? `?vessel=${authState.selectedVessel.asset_id}` : '';
        const response = await fetch(`${API_BASE_URL}/hse/status/current/${vesselParam}`, {
            headers: {
                'Authorization': `Bearer ${getAccessToken()}`
            }
        });
        if (response.ok) {
            const data = await response.json();
            activePermits.value = data.active_permits || 0;
            daysWithoutLTI.value = data.days_without_lti || 0;
            nearMisses.value = data.near_misses_count || 0;
            globalStatus.value = data.global_status || 'GREEN';
        }
    } catch (error) {
        console.error("Failed to fetch HSE status:", error);
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
            await fetchInitialData();
            showModal.value = false;
            toast.success("Success", { description: "PTW request sent successfully. Waiting for Safety Officer approval." });
        } else {
            const errorData = await response.json();
            const errorMsgs = Object.values(errorData).flat();
            const errorMsg = errorMsgs[0] || "Failed to send PTW request.";
            console.error("Error submitting PTW:", errorData);
            toast.error("Failed", { description: errorMsg });
        }
    } catch (error) {
        console.error("Error submitting PTW:", error);
    }
};

const approvePTW = async (ptw_id) => {
    const ptw = allPTWs.value.find(p => p.id === ptw_id);
    if (ptw) {
        selectedPTW.value = ptw;
        selectedPTWId.value = ptw_id;
        approveDialogOpen.value = true;
    }
};

const handleApproveWithSignature = async (signature) => {
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
            fetchInitialData();
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

const rejectPTW = async (ptw_id) => {
    const ptw = allPTWs.value.find(p => p.id === ptw_id);
    if (ptw) {
        selectedPTW.value = ptw;
        selectedPTWId.value = ptw_id;
        rejectDialogOpen.value = true;
    }
};

const handleRejectWithReason = async (rejection_reason) => {
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
            fetchInitialData();
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

const viewPTWDetails = (ptw) => {
    selectedPTW.value = ptw;
    viewDialogOpen.value = true;
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
        fetchInitialData();
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
        fetchInitialData();
        toast.success("Success", { description: `${successCount} PTW rejected successfully.` });
    } catch (error) {
        console.error("Failed Bulk Reject:", error);
        toast.error("Failed", { description: "Failed to perform bulk reject." });
    }
};

const markAsDone = async (ptw_id) => {
    const ptw = allPTWs.value.find(p => p.id === ptw_id);
    if (ptw) {
        selectedPTW.value = ptw;
        selectedPTWId.value = ptw_id;
        markDoneDialogOpen.value = true;
    }
};

const startWork = async (ptw_id) => {
    const ptw = allPTWs.value.find(p => p.id === ptw_id);
    if (ptw) {
        selectedPTW.value = ptw;
        selectedPTWId.value = ptw_id;
        toolboxTalkDialogOpen.value = true;
    }
};

const handleStartWorkConfirmed = async (ptw_id) => {
    try {
        const response = await fetch(`${API_BASE_URL}/hse/ptw/${ptw_id}/start_work/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken() || '',
                'Authorization': `Bearer ${getAccessToken()}`
            }
        });

        if (response.ok) {
            fetchInitialData();
            toast.success("Success", { description: "Work started successfully. You are now checked in." });
        } else {
            const error = await response.json();
            toast.error("Failed", { description: error.error || "Failed to start work." });
        }
    } catch (error) {
        console.error("Error starting work:", error);
        toast.error("Error", { description: "Server connection failed." });
    }
};

const handleMarkDoneWithNotes = async (completion_notes) => {
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
            fetchInitialData();
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

const confirmClosePTW = async (ptw_id) => {
    const ptw = allPTWs.value.find(p => p.id === ptw_id);
    if (ptw) {
        selectedPTW.value = ptw;
        selectedPTWId.value = ptw_id;
        confirmCloseDialogOpen.value = true;
    }
};

const handleConfirmClose = async (closing_notes) => {
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
            fetchInitialData();
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

const editPTW = (ptw) => {
    selectedPTW.value = ptw;
    selectedPTWId.value = ptw.id;
    editDialogOpen.value = true;
};

const deletePTW = async (ptw_id) => {
    if (!confirm("Are you sure you want to delete this PTW?")) return;

    try {
        const response = await fetch(`${API_BASE_URL}/hse/ptw/${ptw_id}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCsrfToken() || '',
                'Authorization': `Bearer ${getAccessToken()}`
            }
        });

        if (response.ok || response.status === 204) {
            fetchInitialData();
            toast.success("Deleted", { description: "PTW deleted successfully." });
        } else {
             console.error("Error deleting PTW:", await response.text());
             toast.error("Failed", { description: "Failed to delete PTW." });
        }
    } catch (error) {
        console.error("Failed to Delete:", error);
    }
};

const initializeDashboard = async () => {
    await fetchInitialData();
    await fetchHSEStatus();
};

const handleIncidentReported = async (data) => {
    // Refresh HSE metrics from backend
    await fetchHSEStatus();
    showIncidentForm.value = false;
};

const handleStatusChanged = async (newStatus) => {
    globalStatus.value = newStatus;
    await fetchHSEStatus();
};

onMounted(async () => {
    await initializeDashboard();

    // Refresh HSE status every 10 seconds
    const statusInterval = setInterval(() => {
        fetchHSEStatus();
    }, 10000);

    // Store interval ID for cleanup
    window.dashboardStatusInterval = statusInterval;
});

onUnmounted(() => {
    // Cleanup interval
    if (window.dashboardStatusInterval) {
        clearInterval(window.dashboardStatusInterval);
        window.dashboardStatusInterval = null;
    }
});
</script>
