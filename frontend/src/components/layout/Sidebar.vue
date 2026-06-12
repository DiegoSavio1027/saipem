<template>
  <aside :class="['bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-700 h-screen flex-col hidden md:flex shrink-0 transition-all duration-300', isCollapsed ? 'w-20' : 'w-64']">
    <!-- Logo Area -->
    <div class="h-20 flex items-center justify-center border-b border-slate-100 dark:border-slate-800 shrink-0" :class="isCollapsed ? 'px-0' : 'px-6 justify-start'">
      <img :src="currentLogo" alt="Saipem Logo" class="h-8 w-auto object-contain" />
    </div>

    <!-- User Profile Area -->
    <div class="p-4 border-b border-slate-100 dark:border-slate-800 shrink-0" :class="isCollapsed ? 'px-2' : ''">
      <div class="flex items-center gap-3 py-2" :class="isCollapsed ? 'justify-center px-0' : 'px-3'">
        <div class="w-8 h-8 rounded-md bg-[var(--color-saipem-tertiary)] flex items-center justify-center text-white font-bold text-sm shrink-0" :title="isCollapsed ? userDisplayName : ''">
          {{ userInitial }}
        </div>
        <div v-if="!isCollapsed" class="flex flex-col overflow-hidden">
          <span class="text-sm font-semibold text-slate-900 dark:text-slate-100 leading-tight truncate">{{ userDisplayName }}</span>
          <span class="text-xs text-slate-500 dark:text-slate-400 leading-tight truncate">{{ userRole }}</span>
        </div>
      </div>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 p-4 space-y-2 overflow-y-auto overflow-x-hidden" :class="isCollapsed ? 'px-2' : ''">
      <!-- Admin Dashboard - Admin only -->
      <router-link v-if="userRole === 'Admin'" to="/" exact-active-class="bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100" :class="['flex items-center gap-3 py-2.5 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100 rounded-md font-medium transition-colors', isCollapsed ? 'justify-center px-0' : 'px-3']" :title="isCollapsed ? 'Admin Dashboard' : ''">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-[var(--color-saipem-tertiary)] shrink-0">
          <rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>
        </svg>
        <span v-if="!isCollapsed">Admin Dashboard</span>
      </router-link>

      <div v-if="hasHseAccess" class="space-y-2">
        <div v-if="!isCollapsed" class="px-3 py-2 text-xs font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2">
          HSE DEPARTMENT
        </div>
        <div v-else class="h-4 mb-2"></div>

        <!-- HSE Dashboard -->
        <router-link to="/hse" exact-active-class="bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100" :class="['flex items-center gap-3 py-2.5 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100 rounded-md font-medium transition-colors', isCollapsed ? 'justify-center px-0' : 'px-3']" :title="isCollapsed ? 'HSE Dashboard' : ''">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-[var(--color-saipem-tertiary)] shrink-0">
            <rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>
          </svg>
          <span v-if="!isCollapsed">HSE Dashboard</span>
        </router-link>

        <!-- Live POB Tracking -->
        <router-link to="/hse/live-pob" active-class="bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100" :class="['flex items-center gap-3 py-2.5 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100 rounded-md font-medium transition-colors', isCollapsed ? 'justify-center px-0' : 'px-3']" :title="isCollapsed ? 'Live POB Tracking' : ''">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          <span v-if="!isCollapsed">Live POB Tracking</span>
        </router-link>

        <!-- Permit To Work -->
        <router-link to="/hse/ptw" active-class="bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100" :class="['flex items-center gap-3 py-2.5 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100 rounded-md font-medium transition-colors', isCollapsed ? 'justify-center px-0' : 'px-3']" :title="isCollapsed ? 'Permit To Work' : ''">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" x2="8" y1="13" y2="13"/><line x1="16" x2="8" y1="17" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
          <span v-if="!isCollapsed">Permit To Work</span>
        </router-link>

        <!-- HSE Incidents -->
        <router-link to="/hse/incidents" active-class="bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100" :class="['flex items-center gap-3 py-2.5 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100 rounded-md font-medium transition-colors', isCollapsed ? 'justify-center px-0' : 'px-3']" :title="isCollapsed ? 'HSE Incidents' : ''">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
          <span v-if="!isCollapsed">HSE Incidents</span>
        </router-link>

        <!-- Analytics & Reports - Admin and Safety Officer only -->
        <router-link v-if="userRole === 'Admin' || userRole === 'Safety Officer'" to="/hse/analytics" active-class="bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100" :class="['flex items-center gap-3 py-2.5 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100 rounded-md font-medium transition-colors', isCollapsed ? 'justify-center px-0' : 'px-3']" :title="isCollapsed ? 'Analytics & Reports' : ''">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><line x1="12" x2="12" y1="20" y2="10"/><line x1="18" x2="18" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="16"/></svg>
          <span v-if="!isCollapsed">Analytics & Reports</span>
        </router-link>
      </div>

      <!-- Master Data Management - Admin and Safety Officer -->
      <div v-if="userRole === 'Admin' || userRole === 'Safety Officer'" class="pt-4 mt-4 border-t border-slate-200 dark:border-slate-700">
        <div v-if="!isCollapsed" class="px-3 py-2 text-xs font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2">
          MASTER DATA
        </div>
        <div v-else class="h-4 mb-2"></div>

        <!-- Vessel Registry - Admin only -->
        <router-link v-if="userRole === 'Admin'" to="/offshore/vessels" active-class="bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100" :class="['flex items-center gap-3 py-2.5 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100 rounded-md font-medium transition-colors', isCollapsed ? 'justify-center px-0' : 'px-3']" :title="isCollapsed ? 'Vessel Registry' : ''">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><path d="M2 21h20M4.5 18h15M6 13h12M8 9h8M10 5h4"/></svg>
          <span v-if="!isCollapsed">Vessel Registry</span>
        </router-link>

        <!-- User Management - Admin only -->
        <router-link v-if="userRole === 'Admin'" to="/admin/users" active-class="bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100" :class="['flex items-center gap-3 py-2.5 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100 rounded-md font-medium transition-colors', isCollapsed ? 'justify-center px-0' : 'px-3']" :title="isCollapsed ? 'User Management' : ''">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          <span v-if="!isCollapsed">User Management</span>
        </router-link>

        <!-- Deck Location -->
        <router-link to="/offshore/locations" active-class="bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100" :class="['flex items-center gap-3 py-2.5 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100 rounded-md font-medium transition-colors', isCollapsed ? 'justify-center px-0' : 'px-3']" :title="isCollapsed ? 'Deck Location' : ''">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z"/><circle cx="12" cy="10" r="3"/></svg>
          <span v-if="!isCollapsed">Deck Location</span>
        </router-link>
      </div>

      <!-- HR Department Section -->
      <div v-if="hasHRAccess" class="pt-4 mt-4 border-t border-slate-200 dark:border-slate-700">
        <div v-if="!isCollapsed" class="px-3 py-2 text-xs font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2">
          HR DEPARTMENT
        </div>
        <div v-else class="h-4 mb-2"></div>

        <!-- HR Dashboard -->
        <router-link to="/hr" exact-active-class="bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100" :class="['flex items-center gap-3 py-2.5 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100 rounded-md font-medium transition-colors', isCollapsed ? 'justify-center px-0' : 'px-3']" :title="isCollapsed ? 'HR Dashboard' : ''">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-[var(--color-saipem-tertiary)] shrink-0">
            <rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>
          </svg>
          <span v-if="!isCollapsed">HR Dashboard</span>
        </router-link>

        <!-- Personnel -->
        <router-link to="/hr/personnel" active-class="bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100" :class="['flex items-center gap-3 py-2.5 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100 rounded-md font-medium transition-colors', isCollapsed ? 'justify-center px-0' : 'px-3']" :title="isCollapsed ? 'Personnel' : ''">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          <span v-if="!isCollapsed">Personnel</span>
        </router-link>

        <!-- Roster -->
        <router-link to="/hr/roster" active-class="bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100" :class="['flex items-center gap-3 py-2.5 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100 rounded-md font-medium transition-colors', isCollapsed ? 'justify-center px-0' : 'px-3']" :title="isCollapsed ? 'Roster Matrix' : ''">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><line x1="16" x2="16" y1="3" y2="21"/><line x1="3" x2="21" y1="8" y2="8"/><line x1="3" x2="21" y1="14" y2="14"/></svg>
          <span v-if="!isCollapsed">Roster Matrix</span>
        </router-link>

        <!-- Payroll -->
        <router-link to="/hr/payroll" active-class="bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100" :class="['flex items-center gap-3 py-2.5 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100 rounded-md font-medium transition-colors', isCollapsed ? 'justify-center px-0' : 'px-3']" :title="isCollapsed ? 'Payroll Engine' : ''">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><circle cx="12" cy="12" r="1"/><path d="M12 1v6m0 6v6"/><path d="M4.22 4.22l4.24 4.24m2.12 2.12l4.24 4.24M1 12h6m6 0h6"/><path d="M4.22 19.78l4.24-4.24m2.12-2.12l4.24-4.24"/></svg>
          <span v-if="!isCollapsed">Payroll Engine</span>
        </router-link>
      </div>

      <!-- Asset Management Section -->
      <div v-if="hasAssetAccess" class="pt-4 mt-4 border-t border-slate-200 dark:border-slate-700">
        <div v-if="!isCollapsed" class="px-3 py-2 text-xs font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2">
          ASSET MANAGEMENT
        </div>
        <div v-else class="h-4 mb-2"></div>

        <!-- Asset Dashboard -->
        <router-link to="/assets/dashboard" exact-active-class="bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100" :class="['flex items-center gap-3 py-2.5 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100 rounded-md font-medium transition-colors', isCollapsed ? 'justify-center px-0' : 'px-3']" :title="isCollapsed ? 'Asset Dashboard' : ''">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-[var(--color-saipem-tertiary)] shrink-0">
            <rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>
          </svg>
          <span v-if="!isCollapsed">Asset Dashboard</span>
        </router-link>

        <!-- Work Orders -->
        <router-link to="/assets/work-orders" active-class="bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100" :class="['flex items-center gap-3 py-2.5 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100 rounded-md font-medium transition-colors', isCollapsed ? 'justify-center px-0' : 'px-3']" :title="isCollapsed ? 'Work Orders' : ''">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" x2="12" y1="11" y2="17"/><line x1="9" x2="15" y1="14" y2="14"/></svg>
          <span v-if="!isCollapsed">Work Orders</span>
        </router-link>

        <!-- Asset Registry -->
        <router-link to="/assets" active-class="bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100" :class="['flex items-center gap-3 py-2.5 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100 rounded-md font-medium transition-colors', isCollapsed ? 'justify-center px-0' : 'px-3']" :title="isCollapsed ? 'Asset Registry' : ''">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>
          <span v-if="!isCollapsed">Asset Registry</span>
        </router-link>

        <!-- Machinery & Equipment -->
        <router-link to="/assets/machinery" active-class="bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100" :class="['flex items-center gap-3 py-2.5 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100 rounded-md font-medium transition-colors', isCollapsed ? 'justify-center px-0' : 'px-3']" :title="isCollapsed ? 'Machinery & Equipment' : ''">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
          <span v-if="!isCollapsed">Machinery & Equip</span>
        </router-link>

        <!-- Inventory -->
        <router-link to="/assets/inventory" active-class="bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100" :class="['flex items-center gap-3 py-2.5 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100 rounded-md font-medium transition-colors', isCollapsed ? 'justify-center px-0' : 'px-3']" :title="isCollapsed ? 'Inventory' : ''">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>
          <span v-if="!isCollapsed">Inventory List</span>
        </router-link>

        <!-- Spare Parts -->
        <router-link to="/assets/spareparts" active-class="bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100" :class="['flex items-center gap-3 py-2.5 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100 rounded-md font-medium transition-colors', isCollapsed ? 'justify-center px-0' : 'px-3']" :title="isCollapsed ? 'Spare Parts' : ''">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>
          <span v-if="!isCollapsed">Spare Parts</span>
        </router-link>
      </div>
    </nav>
  </aside>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import logoDark from '@/assets/text-side-dark.png';
import logoLight from '@/assets/text-side-light.png';
import { authState } from '@/store/auth';
import { themeState } from '@/store/theme';

defineProps({
    isCollapsed: Boolean
});

const username = computed(() => authState.username);
const userRole = computed(() => authState.userRole);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';
const currentEmployee = ref(null);

const userDisplayName = computed(() => {
    // Use first_name + last_name from auth state if available
    if (authState.userData?.first_name && authState.userData?.last_name) {
        return `${authState.userData.first_name} ${authState.userData.last_name} (${authState.username})`;
    }
    return authState.username;
});

const userInitial = computed(() => {
    if (authState.userData?.first_name) {
        return authState.userData.first_name.charAt(0).toUpperCase();
    }
    return authState.username ? authState.username.charAt(0).toUpperCase() : 'U';
});

const currentLogo = computed(() => {
    return themeState.isDark ? logoLight : logoDark;
});

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
