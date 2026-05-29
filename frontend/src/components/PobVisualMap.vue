<template>
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <!-- Visual Map -->
    <Card class="bg-white dark:bg-slate-800">
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg>
          Location Overview
        </CardTitle>
        <CardDescription>Current personnel distribution across locations</CardDescription>
      </CardHeader>
      <CardContent>
        <div class="grid grid-cols-2 gap-4">
          <div
            v-for="location in locations"
            :key="location.name"
            class="relative p-6 rounded-lg border-2 transition-all hover:shadow-lg cursor-pointer"
            :class="getLocationClass(location)"
            @click="selectLocation(location.name)"
          >
            <div class="flex flex-col items-center justify-center space-y-3">
              <div class="w-12 h-12 rounded-full flex items-center justify-center" :class="getIconBgClass(location)">
                <component :is="getLocationIcon(location.name)" class="w-6 h-6" :class="getIconColorClass(location)" />
              </div>
              <div class="text-center">
                <h3 class="font-semibold text-slate-900 dark:text-slate-100 text-sm">{{ location.name }}</h3>
                <div class="flex items-center justify-center gap-2 mt-2">
                  <span class="text-2xl font-bold" :class="getCountColorClass(location)">
                    {{ location.count }}
                  </span>
                  <span class="text-xs text-slate-500 dark:text-slate-400">personnel</span>
                </div>
              </div>
            </div>

            <!-- Status indicator -->
            <div class="absolute top-2 right-2">
              <div
                class="w-3 h-3 rounded-full"
                :class="location.count > 0 ? 'bg-green-500 animate-pulse' : 'bg-slate-300'"
              ></div>
            </div>
          </div>
        </div>

        <!-- Legend -->
        <div class="mt-6 pt-4 border-t border-slate-200 dark:border-slate-700">
          <div class="flex items-center justify-center gap-6 text-xs text-slate-600 dark:text-slate-400">
            <div class="flex items-center gap-2">
              <div class="w-3 h-3 rounded-full bg-green-500"></div>
              <span>Active</span>
            </div>
            <div class="flex items-center gap-2">
              <div class="w-3 h-3 rounded-full bg-slate-300"></div>
              <span>Empty</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Location Details -->
    <Card class="bg-white dark:bg-slate-800">
      <CardHeader>
        <CardTitle>{{ selectedLocationName || 'All Locations' }}</CardTitle>
        <CardDescription>Personnel currently in this location</CardDescription>
      </CardHeader>
      <CardContent>
        <ScrollArea class="h-[400px]">
          <div v-if="filteredPersonnel.length === 0" class="flex flex-col items-center justify-center h-[300px] text-slate-400 dark:text-slate-500">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="mb-4 opacity-20">
              <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
              <circle cx="9" cy="7" r="4"/>
              <path d="M22 21v-2a4 4 0 0 0-3-3.87"/>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
            </svg>
            <p>No personnel in this location</p>
          </div>
          <div v-else class="space-y-3">
            <div
              v-for="person in filteredPersonnel"
              :key="person.employee_name + person.time"
              class="p-4 rounded-lg border border-slate-200 dark:border-slate-700 hover:border-[var(--color-saipem-tertiary)] transition-colors bg-slate-50 dark:bg-slate-700"
            >
              <div class="flex items-center justify-between gap-3">
                <div class="flex items-center gap-3 flex-1 min-w-0">
                  <div class="w-10 h-10 rounded-full bg-[var(--color-saipem-tertiary)]/10 text-[var(--color-saipem-tertiary)] flex items-center justify-center font-semibold text-sm">
                    {{ getInitials(person.employee_name) }}
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-2">
                      <p class="font-semibold text-slate-900 dark:text-slate-100">{{ person.employee_name }}</p>
                      <span
                        :class="person.action === 'IN' ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400' : 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'"
                        class="px-2 py-0.5 rounded-full text-[10px] font-semibold"
                      >
                        {{ person.action }}
                      </span>
                    </div>
                  </div>
                </div>
                <div class="text-right shrink-0">
                  <p class="text-xs text-slate-400">{{ person.time }}</p>
                </div>
              </div>
            </div>
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  </div>
</template>

<script setup>
import { ref, computed, h, onMounted } from 'vue';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';

const props = defineProps({
  liveFeeds: {
    type: Array,
    default: () => []
  }
});

const selectedLocationName = ref(null);
const apiLocations = ref([]);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';

// Fetch locations from API
const fetchLocations = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/offshore/locations/`, {
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
    locationMap.set(loc.name, { name: loc.name, count: 0, personnel: [] });
  });

  // Count current personnel in each location (only IN actions)
  const personnelStatus = new Map();

  // Process feeds in chronological order (oldest first)
  // Filter out EMERGENCY feeds
  const sortedFeeds = [...props.liveFeeds]
    .filter(feed => feed.action === 'IN' || feed.action === 'OUT');

  sortedFeeds.forEach(feed => {
    const key = feed.employee_name;
    if (feed.action === 'IN') {
      personnelStatus.set(key, { location: feed.location, ...feed });
    } else if (feed.action === 'OUT') {
      personnelStatus.delete(key);
    }
  });

  // Count personnel per location
  personnelStatus.forEach((person) => {
    const loc = locationMap.get(person.location);
    if (loc) {
      loc.count++;
      loc.personnel.push(person);
    }
  });

  return Array.from(locationMap.values());
});

const filteredPersonnel = computed(() => {
  if (!selectedLocationName.value) {
    // Show all personnel
    return locations.value.flatMap(loc => loc.personnel);
  }

  const location = locations.value.find(loc => loc.name === selectedLocationName.value);
  return location ? location.personnel : [];
});

const selectLocation = (locationName) => {
  if (selectedLocationName.value === locationName) {
    selectedLocationName.value = null;
  } else {
    selectedLocationName.value = locationName;
  }
};

const getLocationClass = (location) => {
  if (selectedLocationName.value === location.name) {
    return 'border-[var(--color-saipem-tertiary)] bg-[var(--color-saipem-tertiary)]/5';
  }
  return location.count > 0 ? 'border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800' : 'border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900';
};

const getIconBgClass = (location) => {
  if (location.count > 0) {
    return 'bg-[var(--color-saipem-tertiary)]/10';
  }
  return 'bg-slate-100 dark:bg-slate-700';
};

const getIconColorClass = (location) => {
  if (location.count > 0) {
    return 'text-[var(--color-saipem-tertiary)]';
  }
  return 'text-slate-400 dark:text-slate-500';
};

const getCountColorClass = (location) => {
  if (location.count > 0) {
    return 'text-[var(--color-saipem-tertiary)]';
  }
  return 'text-slate-400 dark:text-slate-500';
};

const getInitials = (name) => {
  if (!name) return '?';
  const parts = name.split(' ');
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }
  return name.substring(0, 2).toUpperCase();
};
</script>
