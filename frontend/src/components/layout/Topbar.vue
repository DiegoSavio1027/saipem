<template>
  <header class="hidden md:flex h-20 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-700 items-center justify-between px-4 md:px-8 shrink-0 transition-all duration-300">
    <div class="flex items-center gap-4">
      <Button variant="ghost" size="icon" @click="$emit('toggle-sidebar')" class="text-slate-500 hover:text-slate-900 h-9 w-9 rounded-md shrink-0 border border-slate-200 bg-slate-50 hover:bg-slate-100 flex items-center justify-center p-0">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="3" x2="21" y1="6" y2="6"/><line x1="3" x2="21" y1="12" y2="12"/><line x1="3" x2="21" y1="18" y2="18"/>
        </svg>
      </Button>
      <h1 class="text-xl md:text-2xl font-heading font-bold text-slate-800 tracking-tight hidden sm:block">Overview</h1>
    </div>

    <div class="flex items-center gap-2 md:gap-6">
        <Badge :variant="isConnected ? 'default' : 'destructive'" class="px-2 md:px-3 py-1 md:py-1.5 text-xs font-semibold rounded-md border-none shadow-sm" :class="isConnected ? 'bg-[var(--color-saipem-success)] hover:bg-[var(--color-saipem-success)]/90 text-white' : ''">
            {{ isConnected ? 'LIVE' : 'OFFLINE' }}
        </Badge>

        <Button v-if="authState.userRole === 'Safety Officer'" @click="handleTestAlarm" class="h-10 px-3 md:px-5 rounded-md bg-[var(--color-saipem-tertiary)] hover:bg-[var(--color-saipem-tertiary)]/90 text-xs md:text-sm font-semibold text-white shadow-sm transition-colors flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-1 md:mr-2 shrink-0">
              <path d="m3 11 18-5v12L3 14v-3z"/>
              <path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>
            </svg>
            <span class="hidden sm:inline">Test Alarm</span>
            <span class="sm:hidden">Alarm</span>
        </Button>

        <!-- Vessel Selector (HR / Admin) -->
        <DropdownMenu v-if="authState.userRole === 'Admin' || authState.userRole === 'HR Staff'" :open="showVesselDropdown" @update:open="showVesselDropdown = $event">
            <DropdownMenuTrigger as-child>
                <Button variant="outline" class="flex items-center gap-2 px-3 md:px-4 py-2 text-xs md:text-sm font-medium">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-[var(--color-saipem-tertiary)]">
                        <path d="M2 21h20M4.5 18h15M6 13h12M8 9h8M10 5h4"/>
                    </svg>
                    <span class="hidden sm:inline text-slate-900 dark:text-white">{{ authState.selectedVessel?.name || 'All Vessels' }}</span>
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" class="w-56">
                <DropdownMenuItem @click="selectVessel(null)"
                                  :class="!authState.selectedVessel
                                    ? 'bg-orange-100 dark:bg-orange-900/30 text-[var(--color-saipem-tertiary)] font-semibold'
                                    : ''">
                    All Vessels
                </DropdownMenuItem>
                <DropdownMenuItem v-for="vessel in vessels" :key="vessel.asset_id"
                                  @click="selectVessel(vessel)"
                                  :class="authState.selectedVessel?.asset_id === vessel.asset_id
                                    ? 'bg-orange-100 dark:bg-orange-900/30 text-[var(--color-saipem-tertiary)] font-semibold'
                                    : ''">
                    {{ vessel.name }}
                </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>

        <!-- Locked Vessel Info (Assigned users) -->
        <div v-else class="flex items-center gap-2 px-3 md:px-4 py-2 border border-slate-200 dark:border-slate-700 rounded-md bg-slate-50 dark:bg-slate-800 text-xs md:text-sm font-medium">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-[var(--color-saipem-tertiary)] shrink-0">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
            <span class="hidden sm:inline text-slate-900 dark:text-white">{{ authState.assignedVessel?.name || 'Unassigned' }}</span>
            <span class="sm:hidden text-slate-900 dark:text-white">{{ (authState.assignedVessel?.name || 'Unassigned').substring(0, 3) }}</span>
        </div>

        <Button @click="toggleTheme" variant="ghost" class="text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100 rounded-md font-medium text-xs md:text-sm transition-colors h-10 px-2 md:px-4">
            <svg v-if="themeState.isDark" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-0 md:mr-2">
              <circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-0 md:mr-2">
              <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>
            </svg>
            <span class="hidden md:inline">{{ themeState.isDark ? 'Light' : 'Dark' }}</span>
        </Button>

        <div class="h-6 w-[1px] bg-slate-200 dark:bg-slate-700 hidden md:block"></div>

        <Button @click="showLogoutModal = true" variant="ghost" class="text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100 rounded-md font-medium text-xs md:text-sm transition-colors h-10 px-2 md:px-4">
            <span class="hidden sm:inline">Logout</span>
            <span class="sm:hidden">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
            </span>
        </Button>
    </div>
  </header>

  <LogoutConfirmModal :show="showLogoutModal" @close="showLogoutModal = false" @confirm="handleLogout" />
  <TestAlarmDialog :open="showTestAlarmDialog" @update:open="showTestAlarmDialog = $event" @activate="handleTestAlarmActivate" />
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from '@/components/ui/dropdown-menu';
import { authState, logout, setSelectedVessel } from '@/store/auth';
import { vessels, fetchVessels } from '@/store/vessel';
import { themeState, toggleTheme } from '@/store/theme';
import { getCsrfToken } from '@/utils/csrf';
import { initializeAudio } from '@/utils/notifications';
import { toast } from 'vue-sonner';
import LogoutConfirmModal from '@/components/LogoutConfirmModal.vue';
import TestAlarmDialog from '@/components/dialogs/TestAlarmDialog.vue';

defineProps({
    isConnected: Boolean,
    isCollapsed: Boolean
});
defineEmits(['openModal', 'toggle-sidebar']);

const router = useRouter();
const showLogoutModal = ref(false);
const showTestAlarmDialog = ref(false);
const showVesselDropdown = ref(false);

// Fetch vessels on mount if user can select vessels
if (!authState.assignedVessel) {
    fetchVessels();
}

const selectVessel = (vessel) => {
    setSelectedVessel(vessel);
    showVesselDropdown.value = false;
    window.location.reload();
};

const handleTestAlarmActivate = async (params) => {
    try {
        const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';
        const queryParams = new URLSearchParams({
            status: params.status,
            location: params.location,
            vessel: params.vessel
        });

        const response = await fetch(`${API_BASE_URL}/hse/test-trigger/?${queryParams}`, {
            method: 'GET',
            credentials: 'include'
        });

        if (response.ok) {
            const data = await response.json();
            toast.error("🚨 MUSTER DRILL ACTIVATED", {
                description: `${params.status === 'RED' ? 'CONDITION RED' : 'CONDITION YELLOW'} - ${data.active_workers_in_danger} workers in danger zones. All PTW operations locked.`,
                duration: 10000
            });
        } else {
            toast.error("Failed", { description: "Failed to trigger alarm. Make sure you have access." });
        }
    } catch (error) {
        console.error("Test Alarm failed:", error);
        toast.error("Error", { description: "Failed to connect to alarm server." });
    }
};

const handleTestAlarm = async () => {
    // Initialize audio on first user interaction
    await initializeAudio();
    showTestAlarmDialog.value = true;
};

const handleLogout = async () => {
    try {
        const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';
        const response = await fetch(`${API_BASE_URL}/auth/logout/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken() || ''
            },
            credentials: 'include'
        });
        if (response.ok) {
            logout();
            showLogoutModal.value = false;
            toast.success("Logout Successful", { description: "You have logged out of the system." });
            router.push('/login');
        }
    } catch (error) {
        console.error("Logout failed:", error);
        toast.error("Logout Failed", { description: "An error occurred during logout." });
    }
};
</script>
