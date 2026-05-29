<template>
  <header class="h-16 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-700 flex md:hidden items-center justify-between px-4 shrink-0 shadow-sm z-10 relative">
    <div class="flex items-center">
      <img :src="currentLogo" alt="Saipem Logo" class="h-6 w-auto object-contain" />
    </div>

    <div class="flex items-center gap-2">
        <Badge :variant="isConnected ? 'default' : 'destructive'" class="px-2 py-1 text-[10px] font-bold rounded-md border-none" :class="isConnected ? 'bg-[var(--color-saipem-success)] text-white' : ''">
            {{ isConnected ? 'LIVE' : 'OFFLINE' }}
        </Badge>

        <Button v-if="authState.userRole !== 'Worker'" @click="handleTestAlarm" size="sm" class="h-8 px-2 rounded-md bg-[var(--color-saipem-tertiary)] hover:bg-[var(--color-saipem-tertiary)]/90 text-[10px] font-semibold text-white shadow-sm">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="m3 11 18-5v12L3 14v-3z"/>
              <path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>
            </svg>
        </Button>

        <Button @click="toggleTheme" variant="ghost" size="sm" class="h-8 w-8 p-0 text-slate-500 dark:text-slate-400">
            <svg v-if="themeState.isDark" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>
            </svg>
        </Button>

        <Button @click="showLogoutModal = true" variant="ghost" size="sm" class="h-8 w-8 p-0 text-slate-500 dark:text-slate-400">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
        </Button>
    </div>
  </header>

  <LogoutConfirmModal :show="showLogoutModal" @close="showLogoutModal = false" @confirm="handleLogout" />
  <TestAlarmDialog :open="showTestAlarmDialog" @update:open="showTestAlarmDialog = $event" @activate="handleTestAlarmActivate" />
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import logoDark from '@/assets/text-side-dark.png';
import logoLight from '@/assets/text-side-light.png';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { authState, logout } from '@/store/auth';
import { themeState, toggleTheme } from '@/store/theme';
import { getCsrfToken } from '@/utils/csrf';
import { initializeAudio } from '@/utils/notifications';
import { toast } from 'vue-sonner';
import LogoutConfirmModal from '@/components/LogoutConfirmModal.vue';
import TestAlarmDialog from '@/components/dialogs/TestAlarmDialog.vue';

defineProps({
    isConnected: Boolean
});

const router = useRouter();
const showLogoutModal = ref(false);
const showTestAlarmDialog = ref(false);

const currentLogo = computed(() => {
    return themeState.isDark ? logoLight : logoDark;
});

const handleTestAlarmActivate = async (params) => {
    try {
        const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';
        const queryParams = new URLSearchParams({
            status: params.status,
            location: params.location
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
