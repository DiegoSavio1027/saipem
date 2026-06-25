<template>
  <DashboardLayout>
    <div class="p-6 space-y-6">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 class="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">Live POB Tracking</h1>
          <p class="text-slate-500 dark:text-slate-400">Real-time personnel movement monitoring</p>
        </div>
      </div>

      <!-- Visual Map -->
      <PobVisualMap :liveFeeds="websocketState.liveFeeds" />

      <!-- Live Feeds -->
      <div class="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm overflow-hidden">
        <div class="p-6 border-b border-slate-100 dark:border-slate-700 flex justify-between items-center bg-slate-50/50 dark:bg-slate-700/50">
          <h2 class="font-semibold text-slate-900 dark:text-slate-100 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            Live Feeds
          </h2>
        </div>
        <div class="p-0">
          <div v-if="websocketState.liveFeeds.length === 0" class="p-12 flex flex-col items-center justify-center text-slate-400 dark:text-slate-500">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="mb-4 opacity-20"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            <p>Waiting for location updates...</p>
          </div>
          <div v-else class="divide-y divide-slate-100 dark:divide-slate-700 flex flex-col-reverse gap-0">
            <div v-for="(feed, index) in websocketState.liveFeeds" :key="index"
                 :class="feed.action === 'EMERGENCY' ? 'bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500' : 'hover:bg-slate-50 dark:hover:bg-slate-700'"
                 class="p-4 transition-colors flex items-center justify-between gap-4">
              <div class="flex items-center gap-4 flex-1 min-w-0">
                <div
                  :class="feed.action === 'EMERGENCY' ? 'bg-red-500 text-white animate-pulse' : 'bg-[var(--color-saipem-tertiary)]/10 text-[var(--color-saipem-tertiary)]'"
                  class="w-10 h-10 rounded-full flex items-center justify-center shrink-0">
                  <svg v-if="feed.action === 'EMERGENCY'" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>
                    <line x1="12" y1="9" x2="12" y2="13"/>
                    <line x1="12" y1="17" x2="12.01" y2="17"/>
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
                    <circle cx="9" cy="7" r="4"/>
                  </svg>
                </div>
                <p class="text-sm font-medium text-slate-900 dark:text-slate-100 truncate">
                  <span v-if="feed.action === 'EMERGENCY'"
                    class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-red-600 text-white animate-pulse"
                  >
                    🚨 EMERGENCY
                  </span>
                  <span v-else
                    :class="feed.action === 'IN' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
                    class="px-2 py-0.5 rounded-full text-[10px] font-semibold"
                  >
                    {{ feed.action }}
                  </span>
                  <span class="font-semibold ml-1" :class="feed.action === 'EMERGENCY' ? 'text-red-700' : ''">{{ feed.employee_name }}</span> →
                  <span :class="feed.action === 'EMERGENCY' ? 'text-red-600 font-bold' : 'text-[var(--color-saipem-tertiary)]'">{{ feed.location }}</span>
                </p>
              </div>
              <p class="text-xs text-slate-500 dark:text-slate-400 font-sans font-medium shrink-0">{{ feed.time }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { onMounted } from 'vue';
import DashboardLayout from '@/layouts/DashboardLayout.vue';
import PobVisualMap from '@/components/PobVisualMap.vue';
import { websocketState } from '@/store/websocket';
import { authState } from '@/store/auth';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';

const fetchInitialPob = async () => {
  try {
    let url = `${API_BASE_URL}/hse/pob/?current=true`;
    
    const vesselId = authState.assignedVessel?.asset_id || authState.assignedVessel?.id || authState.selectedVessel?.id;
    if (vesselId) {
      url += `&vessel=${vesselId}`;
    }
    
    const response = await fetch(url, {
      credentials: 'include'
    });
    
    if (response.ok) {
      const data = await response.json();
      
      const formattedData = data.map(log => ({
        action: log.action,
        employee_name: log.employee_name,
        location: log.location_name || (typeof log.deck_location === 'object' ? log.deck_location.deck_name : log.deck_location),
        time: new Date(log.timestamp).toLocaleString(),
        timestamp: log.timestamp
      }));

      // Append fetched data that doesn't already exist from websocket
      formattedData.forEach(newFeed => {
        const isDuplicate = websocketState.liveFeeds.some(feed =>
            feed.employee_name === newFeed.employee_name &&
            feed.action === newFeed.action &&
            feed.location === newFeed.location &&
            feed.timestamp === newFeed.timestamp
        );
        if (!isDuplicate) {
          websocketState.liveFeeds.push(newFeed);
        }
      });
    }
  } catch (error) {
    console.error('Failed to fetch initial POB data:', error);
  }
};

onMounted(() => {
  fetchInitialPob();
});
</script>
