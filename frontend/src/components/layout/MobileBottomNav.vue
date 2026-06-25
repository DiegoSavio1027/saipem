<template>
  <nav class="md:hidden fixed bottom-0 w-full bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-700 flex justify-around p-3 z-50">
    <!-- Admin Dashboard (Admin only) -->
    <router-link v-if="authState.userRole === 'Admin'" to="/" exact-active-class="text-[var(--color-saipem-tertiary)]" class="flex flex-col items-center gap-1 text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 transition-colors">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>
      <span class="text-[10px] font-semibold">Dashboard</span>
    </router-link>

    <!-- HSE Department Links -->
    <template v-if="hasHseAccess">
      <!-- HSE Dashboard -->
      <router-link to="/hse" exact-active-class="text-[var(--color-saipem-tertiary)]" class="flex flex-col items-center gap-1 text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>
        <span class="text-[10px] font-semibold">HSE Dash</span>
      </router-link>

      <!-- Permit To Work -->
      <router-link to="/hse/ptw" active-class="text-[var(--color-saipem-tertiary)]" class="flex flex-col items-center gap-1 text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" x2="8" y1="13" y2="13"/><line x1="16" x2="8" y1="17" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
        <span class="text-[10px] font-semibold">PTW</span>
      </router-link>

      <router-link to="/hse/incidents" active-class="text-[var(--color-saipem-tertiary)]" class="flex flex-col items-center gap-1 text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
        <span class="text-[10px] font-semibold">Incidents</span>
      </router-link>

      <router-link to="/hse/live-pob" active-class="text-[var(--color-saipem-tertiary)]" class="flex flex-col items-center gap-1 text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        <span class="text-[10px] font-semibold">Live POB</span>
      </router-link>

      <router-link v-if="authState.userRole === 'Admin' || authState.userRole === 'Safety Officer'" to="/hse/analytics" active-class="text-[var(--color-saipem-tertiary)]" class="flex flex-col items-center gap-1 text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><line x1="12" x2="12" y1="20" y2="10"/><line x1="18" x2="18" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="16"/></svg>
        <span class="text-[10px] font-semibold">Analytics</span>
      </router-link>
    </template>

    <!-- HR Department Links -->
    <template v-if="hasHRAccess">
      <router-link to="/hr" exact-active-class="text-[var(--color-saipem-tertiary)]" class="flex flex-col items-center gap-1 text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>
        <span class="text-[10px] font-semibold">HR Dash</span>
      </router-link>

      <router-link to="/hr/personnel" active-class="text-[var(--color-saipem-tertiary)]" class="flex flex-col items-center gap-1 text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        <span class="text-[10px] font-semibold">Personnel</span>
      </router-link>

      <router-link to="/hr/roster" active-class="text-[var(--color-saipem-tertiary)]" class="flex flex-col items-center gap-1 text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><line x1="16" x2="16" y1="3" y2="21"/><line x1="3" x2="21" y1="8" y2="8"/><line x1="3" x2="21" y1="14" y2="14"/></svg>
        <span class="text-[10px] font-semibold">Roster</span>
      </router-link>

      <router-link to="/hr/payroll" active-class="text-[var(--color-saipem-tertiary)]" class="flex flex-col items-center gap-1 text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><circle cx="12" cy="12" r="1"/><path d="M12 1v6m0 6v6"/><path d="M4.22 4.22l4.24 4.24m2.12 2.12l4.24 4.24M1 12h6m6 0h6"/><path d="M4.22 19.78l4.24-4.24m2.12-2.12l4.24-4.24"/></svg>
        <span class="text-[10px] font-semibold">Payroll</span>
      </router-link>
    </template>

    <!-- Asset Management Links -->
    <template v-if="hasAssetAccess">
      <router-link to="/assets" exact-active-class="text-[var(--color-saipem-tertiary)]" class="flex flex-col items-center gap-1 text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>
        <span class="text-[10px] font-semibold">Asset Dash</span>
      </router-link>

      <router-link to="/assets/work-orders" active-class="text-[var(--color-saipem-tertiary)]" class="flex flex-col items-center gap-1 text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" x2="12" y1="11" y2="17"/><line x1="9" x2="15" y1="14" y2="14"/></svg>
        <span class="text-[10px] font-semibold">Work Orders</span>
      </router-link>

      <router-link to="/assets/registry" active-class="text-[var(--color-saipem-tertiary)]" class="flex flex-col items-center gap-1 text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>
        <span class="text-[10px] font-semibold">Registry</span>
      </router-link>

      <router-link to="/assets/machinery" active-class="text-[var(--color-saipem-tertiary)]" class="flex flex-col items-center gap-1 text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
        <span class="text-[10px] font-semibold">Machinery</span>
      </router-link>
    </template>
  </nav>
</template>

<script setup>
import { computed } from 'vue';
import { authState } from '@/store/auth';

defineEmits(['openModal']);

const hasHseAccess = computed(() => {
    return authState.accessibleModules && authState.accessibleModules.includes('hse');
});

const hasHRAccess = computed(() => {
    return authState.accessibleModules && authState.accessibleModules.includes('hr');
});

const hasAssetAccess = computed(() => {
    return authState.accessibleModules && authState.accessibleModules.includes('asset');
});
</script>
