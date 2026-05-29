<template>
  <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm" @click.self="$emit('close')">
    <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4 overflow-hidden">
      <div class="p-6">
        <div class="flex items-center gap-4 mb-4">
          <div class="flex-shrink-0 w-12 h-12 rounded-full bg-red-100 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-red-600">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
              <polyline points="16 17 21 12 16 7"/>
              <line x1="21" x2="9" y1="12" y2="12"/>
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-slate-900">Confirm Logout</h3>
            <p class="text-sm text-slate-500 mt-1">Are you sure you want to logout?</p>
          </div>
        </div>

        <p class="text-slate-600 text-sm mb-6">
          You will be logged out of the system and must login again to access the dashboard.
        </p>

        <div class="flex gap-3 justify-end">
          <Button @click="$emit('close')" variant="outline" class="h-10 px-4 rounded-md border-slate-300 text-slate-700 hover:bg-slate-50 font-medium">
            Cancel
          </Button>
          <Button @click="$emit('confirm')" class="h-10 px-4 rounded-md bg-red-500 hover:bg-red-600 text-white font-medium">
            Yes, Logout
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Button } from '@/components/ui/button';

defineProps({
  show: Boolean
});

defineEmits(['close', 'confirm']);
</script>
