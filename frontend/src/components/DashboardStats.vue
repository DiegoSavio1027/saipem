<template>
  <div class="space-y-6 mb-12">
    <!-- Header Section -->
    <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-md shadow-sm p-6">
      <div class="grid grid-cols-2 gap-8">
        <!-- Left Side -->
        <div>
          <h3 class="text-lg font-bold text-slate-700 dark:text-slate-200 font-sans mb-2">HSE Compliance & Safety Center</h3>
          <p class="text-sm text-slate-700 dark:text-slate-300">ISO 45001 Compliance | Vessel: <span class="font-semibold">{{ vesselName }}</span></p>
        </div>
        <!-- Right Side -->
        <div class="text-right">
          <h3 class="text-[14px] font-semibold text-slate-500 dark:text-slate-400 font-sans tracking-wide uppercase mb-2">Global Status</h3>
          <div class="flex items-center justify-end gap-3">
            <!-- Status Display Only -->
            <div
              :class="globalStatus === 'GREEN' ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400' : globalStatus === 'YELLOW' ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400' : 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'"
              class="px-3 py-1 rounded-full text-sm font-semibold uppercase"
            >
              CONDITION {{ globalStatus }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Top Row: Metrics Cards -->
    <div class="grid grid-cols-4 gap-6">
        <!-- Live Headcount -->
        <Card class="bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 shadow-sm rounded-md hover:border-slate-300 dark:hover:border-slate-600 transition-colors">
            <CardHeader class="p-6 pb-2">
                <CardTitle class="text-[14px] font-semibold text-slate-500 dark:text-slate-400 font-sans tracking-wide uppercase">Live Headcount</CardTitle>
            </CardHeader>
            <CardContent class="p-6 pt-0">
                <p class="text-[64px] font-heading font-black text-slate-900 dark:text-slate-100 leading-none">{{ totalPob }}</p>
            </CardContent>
        </Card>

        <!-- Active Permit -->
        <Card class="bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 shadow-sm rounded-md hover:border-slate-300 dark:hover:border-slate-600 transition-colors">
            <CardHeader class="p-6 pb-2">
                <CardTitle class="text-[14px] font-semibold text-slate-500 dark:text-slate-400 font-sans tracking-wide uppercase">Active Permit</CardTitle>
            </CardHeader>
            <CardContent class="p-6 pt-0">
                <p class="text-[64px] font-heading font-black text-slate-900 dark:text-slate-100 leading-none">{{ activePermits }}</p>
            </CardContent>
        </Card>

        <!-- Days Without LTI -->
        <Card class="bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 shadow-sm rounded-md hover:border-slate-300 dark:hover:border-slate-600 transition-colors">
            <CardHeader class="p-6 pb-2">
                <CardTitle class="text-[14px] font-semibold text-slate-500 dark:text-slate-400 font-sans tracking-wide uppercase">Days Without LTI</CardTitle>
            </CardHeader>
            <CardContent class="p-6 pt-0">
                <p class="text-[64px] font-heading font-black text-green-600 dark:text-green-400 leading-none">{{ daysWithoutLTI }}</p>
            </CardContent>
        </Card>

        <!-- Near Misses Logged -->
        <Card class="bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 shadow-sm rounded-md hover:border-slate-300 dark:hover:border-slate-600 transition-colors">
            <CardHeader class="p-6 pb-2">
                <CardTitle class="text-[14px] font-semibold text-slate-500 dark:text-slate-400 font-sans tracking-wide uppercase">Near Misses Logged</CardTitle>
            </CardHeader>
            <CardContent class="p-6 pt-0">
                <p class="text-[64px] font-heading font-black text-amber-600 dark:text-amber-400 leading-none">{{ nearMisses }}</p>
            </CardContent>
        </Card>
    </div>

    <!-- Live POB Tracking - Split into 2 Cards -->
    <div class="grid grid-cols-2 gap-6">
        <!-- Left Card: Location Overview -->
        <Card class="bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 shadow-sm rounded-md hover:border-slate-300 dark:hover:border-slate-600 transition-colors">
            <CardHeader class="p-6 pb-2">
                <CardTitle class="text-[14px] font-semibold text-slate-500 dark:text-slate-400 font-sans tracking-wide uppercase">Vessel Deck Location Mapper</CardTitle>
            </CardHeader>
            <CardContent class="p-6 pt-0">
                <div class="grid grid-cols-2 gap-2">
                    <div
                        v-for="location in locations"
                        :key="location.name"
                        class="p-3 rounded border-2 transition-all hover:shadow-sm cursor-pointer flex items-center gap-3 relative"
                        @click="selectLocation(location.name)"
                        :class="selectedLocation === location.name ? 'border-[var(--color-saipem-tertiary)] bg-[var(--color-saipem-tertiary)]/5' : location.count > 0 ? 'border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700' : 'border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800'"
                    >
                        <!-- Icon Left -->
                        <div class="w-8 h-8 rounded-full flex items-center justify-center shrink-0" :class="location.count > 0 ? 'bg-[var(--color-saipem-tertiary)]/10 text-[var(--color-saipem-tertiary)]' : 'bg-slate-100 dark:bg-slate-700 text-slate-400 dark:text-slate-500'">
                            <component :is="getLocationIcon(location.name)" class="w-5 h-5" />
                        </div>

                        <!-- Content Right -->
                        <div class="flex-1 min-w-0">
                            <h3 class="font-semibold text-slate-900 dark:text-slate-100 text-[11px] leading-tight">{{ location.name }}</h3>
                            <div class="flex items-center gap-1 mt-0.5">
                                <span class="text-sm font-bold" :class="location.count > 0 ? 'text-[var(--color-saipem-tertiary)]' : 'text-slate-400 dark:text-slate-500'">
                                    {{ location.count }}
                                </span>
                                <span class="text-[8px] text-slate-500 dark:text-slate-400">personnel</span>
                            </div>
                        </div>

                        <!-- Status indicator -->
                        <div class="absolute top-1 right-1">
                            <div class="w-1.5 h-1.5 rounded-full" :class="location.count > 0 ? 'bg-green-500 animate-pulse' : 'bg-slate-300'"></div>
                        </div>
                    </div>
                </div>
            </CardContent>
        </Card>

        <!-- Right Card: Live Feeds -->
        <Card class="bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 shadow-sm rounded-md hover:border-slate-300 dark:hover:border-slate-600 transition-colors">
            <CardHeader class="p-6 pb-2">
                <CardTitle class="text-[14px] font-semibold text-slate-500 dark:text-slate-400 font-sans tracking-wide uppercase">Check-in/Check-out Feed</CardTitle>
            </CardHeader>
            <CardContent class="p-6 pt-0">
                <ScrollArea class="h-[200px] w-full rounded-md border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-3">
                    <div v-if="filteredFeeds.length === 0" class="flex flex-col items-center justify-center h-full text-slate-400 dark:text-slate-500">
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="mb-2 opacity-20">
                            <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
                            <circle cx="9" cy="7" r="4"/>
                        </svg>
                        <p class="text-[12px]">{{ selectedLocation ? 'No activity' : 'Waiting for movement...' }}</p>
                    </div>
                    <ul v-else class="flex flex-col-reverse gap-2">
                        <li v-for="(feed, index) in filteredFeeds" :key="index" class="bg-slate-50 dark:bg-slate-700 p-2 rounded-md border border-slate-100 dark:border-slate-600">
                            <div class="flex justify-between items-start gap-2">
                                <span class="text-[11px] text-slate-700 dark:text-slate-300 font-sans flex-1">
                                    <span
                                        :class="feed.action === 'IN' ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400' : 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'"
                                        class="px-2 py-0.5 rounded-full text-[10px] font-semibold"
                                    >
                                        {{ feed.action }}
                                    </span>
                                    <strong class="text-slate-900 dark:text-slate-100 ml-1">{{ feed.employee_name }}</strong> →
                                    <strong class="text-[var(--color-saipem-tertiary)]">{{ feed.location }}</strong>
                                </span>
                                <span class="text-[9px] text-slate-400 dark:text-slate-500 font-sans font-medium shrink-0">{{ feed.time }}</span>
                            </div>
                        </li>
                    </ul>
                </ScrollArea>
            </CardContent>
        </Card>
    </div>
  </div>
</template>

<script setup>
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { ref, computed, h, onMounted } from 'vue';
import { authState, getAccessToken } from '@/store/auth';

const props = defineProps({
    totalPob: Number,
    liveFeeds: Array,
    activePermits: {
        type: Number,
        default: 0
    },
    daysWithoutLTI: {
        type: Number,
        default: 0
    },
    nearMisses: {
        type: Number,
        default: 0
    },
    vesselName: {
        type: String,
        default: 'Saipem Vessel'
    },
    globalStatus: {
        type: String,
        default: 'GREEN',
        validator: (value) => ['GREEN', 'YELLOW', 'RED'].includes(value)
    }
});

const selectedLocation = ref(null);
const apiLocations = ref([]);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';

// Fetch locations from API
const fetchLocations = async () => {
    try {
        let url = `${API_BASE_URL}/offshore/locations/`;
        const vesselId = authState.assignedVessel?.asset_id || authState.assignedVessel?.id || authState.selectedVessel?.id;
        if (vesselId) {
            url += `?vessel_id=${vesselId}`;
        }
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${getAccessToken()}`
            },
            credentials: 'include'
        });
        if (response.ok) {
            apiLocations.value = await response.json();
        }
    } catch (error) {
        console.error('Error fetching locations:', error);
    }
};

onMounted(() => {
    fetchLocations();
});

// Define location icons as render functions
const getLocationIcon = (locationName) => {
    const icons = {
        'Engine Room': () => h('svg', {
            xmlns: 'http://www.w3.org/2000/svg',
            viewBox: '0 0 24 24',
            fill: 'none',
            stroke: 'currentColor',
            'stroke-width': '2',
            'stroke-linecap': 'round',
            'stroke-linejoin': 'round'
        }, [
            h('path', { d: 'M12 2v4' }),
            h('path', { d: 'm16 6-4 4-4-4' }),
            h('rect', { width: '20', height: '8', x: '2', y: '14', rx: '2' }),
            h('path', { d: 'M6 18h.01' }),
            h('path', { d: 'M10 18h.01' })
        ]),
        'Heli Deck': () => h('svg', {
            xmlns: 'http://www.w3.org/2000/svg',
            viewBox: '0 0 24 24',
            fill: 'none',
            stroke: 'currentColor',
            'stroke-width': '2',
            'stroke-linecap': 'round',
            'stroke-linejoin': 'round'
        }, [
            h('path', { d: 'M12 2v20' }),
            h('path', { d: 'M2 12h20' }),
            h('circle', { cx: '12', cy: '12', r: '9' })
        ]),
        'Main Deck': () => h('svg', {
            xmlns: 'http://www.w3.org/2000/svg',
            viewBox: '0 0 24 24',
            fill: 'none',
            stroke: 'currentColor',
            'stroke-width': '2',
            'stroke-linecap': 'round',
            'stroke-linejoin': 'round'
        }, [
            h('rect', { width: '18', height: '18', x: '3', y: '3', rx: '2' }),
            h('path', { d: 'M3 9h18' }),
            h('path', { d: 'M9 21V9' })
        ]),
        'Safe Zone': () => h('svg', {
            xmlns: 'http://www.w3.org/2000/svg',
            viewBox: '0 0 24 24',
            fill: 'none',
            stroke: 'currentColor',
            'stroke-width': '2',
            'stroke-linecap': 'round',
            'stroke-linejoin': 'round'
        }, [
            h('path', { d: 'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10' })
        ])
    };

    return icons[locationName] || icons['Main Deck'];
};

// Calculate personnel count per location
const locations = computed(() => {
    const locationMap = new Map();

    // Initialize locations from API
    apiLocations.value.forEach(loc => {
        locationMap.set(loc.name, { name: loc.name, count: 0 });
    });

    // Count current personnel in each location (only IN actions)
    const personnelStatus = new Map();

    // Process feeds in chronological order (oldest first)
    // Filter out EMERGENCY feeds and reverse to get oldest first
    const sortedFeeds = [...(props.liveFeeds || [])]
        .filter(feed => feed.action === 'IN' || feed.action === 'OUT');

    sortedFeeds.forEach((feed) => {
        const key = feed.employee_name;
        if (feed.action === 'IN') {
            personnelStatus.set(key, feed.location);
        } else if (feed.action === 'OUT') {
            personnelStatus.delete(key);
        }
    });

    // Count personnel per location
    personnelStatus.forEach((location) => {
        const loc = locationMap.get(location);
        if (loc) {
            loc.count++;
        }
    });

    return Array.from(locationMap.values());
});

// Filter feeds based on selected location
const filteredFeeds = computed(() => {
    if (!selectedLocation.value) {
        return props.liveFeeds || [];
    }
    return (props.liveFeeds || []).filter(feed => feed.location === selectedLocation.value);
});

const selectLocation = (locationName) => {
    if (selectedLocation.value === locationName) {
        selectedLocation.value = null;
    } else {
        selectedLocation.value = locationName;
    }
};

const formatTime = (timeString) => {
    if (!timeString) return '';
    // Extract just the time part (HH:MM:SS AM/PM)
    const parts = timeString.split(', ');
    return parts[1] || timeString;
};
</script>
