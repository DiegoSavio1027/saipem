<template>
  <Dialog :open="open" @update:open="$emit('update:open', $event)">
    <DialogContent class="sm:max-w-md">
      <DialogHeader>
        <DialogTitle class="flex items-center gap-2 text-red-600">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="m3 11 18-5v12L3 14v-3z"/>
            <path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>
          </svg>
          Activate Muster Drill
        </DialogTitle>
        <DialogDescription>
          Configure emergency drill parameters. This will trigger evacuation protocols.
        </DialogDescription>
      </DialogHeader>

      <div class="space-y-4 py-4">
        <!-- Vessel Selector -->
        <div class="space-y-2">
          <label class="text-sm font-semibold text-slate-700">Target Vessel</label>
          <Select v-model="selectedVessel">
            <SelectTrigger>
              <SelectValue placeholder="Select vessel" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="ALL">
                <div class="flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M2 21h20M4.5 18h15M6 13h12M8 9h8M10 5h4"/>
                  </svg>
                  <span class="font-semibold">All Vessels</span>
                </div>
              </SelectItem>
              <SelectItem v-for="vessel in vessels" :key="vessel.asset_id" :value="vessel.asset_id">
                <div class="flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M2 21h20M4.5 18h15M6 13h12M8 9h8M10 5h4"/>
                  </svg>
                  <span>{{ vessel.name }}</span>
                </div>
              </SelectItem>
            </SelectContent>
          </Select>
        </div>

        <!-- Location Selector -->
        <div class="space-y-2">
          <label class="text-sm font-semibold text-slate-700">Target Location</label>
          <Select v-model="selectedLocation">
            <SelectTrigger>
              <SelectValue placeholder="Select location" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="ALL">
                <div class="flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M3 3h18v18H3z"/>
                  </svg>
                  <span class="font-semibold">All Locations</span>
                </div>
              </SelectItem>
              <SelectItem v-for="location in locations" :key="location.id" :value="location.name">
                <div class="flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z"/>
                    <circle cx="12" cy="10" r="3"/>
                  </svg>
                  <span>{{ location.name }}</span>
                </div>
              </SelectItem>
            </SelectContent>
          </Select>
        </div>

        <!-- Status Selector -->
        <div class="space-y-2">
          <label class="text-sm font-semibold text-slate-700">Emergency Status</label>
          <Select v-model="selectedStatus">
            <SelectTrigger>
              <SelectValue placeholder="Select status level" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="YELLOW">
                <div class="flex items-center gap-2">
                  <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
                  <span>CONDITION YELLOW - Warning</span>
                </div>
              </SelectItem>
              <SelectItem value="RED">
                <div class="flex items-center gap-2">
                  <div class="w-3 h-3 rounded-full bg-red-500"></div>
                  <span>CONDITION RED - Emergency</span>
                </div>
              </SelectItem>
            </SelectContent>
          </Select>
        </div>

        <!-- Warning Message -->
        <div class="bg-red-50 border border-red-200 rounded-lg p-3">
          <p class="text-sm text-red-800 font-medium">⚠️ Warning</p>
          <p class="text-xs text-red-600 mt-1">
            This will activate emergency protocols and lock all PTW operations.
          </p>
        </div>
      </div>

      <DialogFooter class="gap-2">
        <Button variant="outline" @click="$emit('update:open', false)">
          Cancel
        </Button>
        <Button
          @click="handleActivate"
          :disabled="!selectedStatus || !selectedLocation"
          class="bg-red-600 hover:bg-red-700 text-white"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2">
            <path d="m3 11 18-5v12L3 14v-3z"/>
          </svg>
          Activate Drill
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

const props = defineProps({
  open: Boolean
});

const emit = defineEmits(['update:open', 'activate']);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';

const selectedStatus = ref('RED');
const selectedLocation = ref('ALL');
const selectedVessel = ref('ALL');
const locations = ref([]);
const vessels = ref([]);

const fetchLocations = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/offshore/locations/`, {
      credentials: 'include'
    });
    if (response.ok) {
      locations.value = await response.json();
    }
  } catch (error) {
    console.error('Error fetching locations:', error);
  }
};

const fetchVessels = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/offshore/vessels/`, {
      credentials: 'include'
    });
    if (response.ok) {
      vessels.value = await response.json();
    }
  } catch (error) {
    console.error('Error fetching vessels:', error);
  }
};

const handleActivate = () => {
  emit('activate', {
    status: selectedStatus.value,
    location: selectedLocation.value,
    vessel: selectedVessel.value
  });
  emit('update:open', false);
};

onMounted(() => {
  fetchLocations();
  fetchVessels();
});
</script>
