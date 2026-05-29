<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-900 p-8">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h2 class="text-3xl font-bold text-slate-900 dark:text-white">Asset Management</h2>
        <p class="text-sm text-slate-600 dark:text-slate-400 mt-1">Equipment, vessels, and infrastructure tracking</p>
      </div>

      <!-- Coming Soon Card -->
      <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg shadow-sm p-8">
        <div class="text-center py-12">
          <div class="bg-blue-100 dark:bg-blue-950/20 w-24 h-24 rounded-full border border-blue-200 dark:border-blue-500/30 flex items-center justify-center mx-auto mb-6 text-blue-600 dark:text-blue-400 text-4xl">
            <i class="fa-solid fa-ship"></i>
          </div>
          <h3 class="text-2xl font-semibold text-slate-900 dark:text-white mb-3">Asset Module Coming Soon</h3>
          <p class="text-slate-600 dark:text-slate-400 mb-6 max-w-md mx-auto">
            The Asset Management module is currently under development. This module will include:
          </p>

          <!-- Feature List -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl mx-auto text-left">
            <div class="bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg p-4">
              <div class="flex items-start gap-3">
                <div class="bg-blue-100 dark:bg-blue-950/30 p-2 rounded-lg">
                  <i class="fa-solid fa-anchor text-blue-600 dark:text-blue-400"></i>
                </div>
                <div>
                  <h4 class="font-semibold text-slate-900 dark:text-white mb-1">Vessel Registry</h4>
                  <p class="text-sm text-slate-600 dark:text-slate-400">Complete fleet inventory and specifications</p>
                </div>
              </div>
            </div>

            <div class="bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg p-4">
              <div class="flex items-start gap-3">
                <div class="bg-blue-100 dark:bg-blue-950/30 p-2 rounded-lg">
                  <i class="fa-solid fa-wrench text-blue-600 dark:text-blue-400"></i>
                </div>
                <div>
                  <h4 class="font-semibold text-slate-900 dark:text-white mb-1">Maintenance Tracking</h4>
                  <p class="text-sm text-slate-600 dark:text-slate-400">Scheduled maintenance and repair logs</p>
                </div>
              </div>
            </div>

            <div class="bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg p-4">
              <div class="flex items-start gap-3">
                <div class="bg-blue-100 dark:bg-blue-950/30 p-2 rounded-lg">
                  <i class="fa-solid fa-clipboard-check text-blue-600 dark:text-blue-400"></i>
                </div>
                <div>
                  <h4 class="font-semibold text-slate-900 dark:text-white mb-1">Inspection Records</h4>
                  <p class="text-sm text-slate-600 dark:text-slate-400">Safety inspections and certifications</p>
                </div>
              </div>
            </div>

            <div class="bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg p-4">
              <div class="flex items-start gap-3">
                <div class="bg-blue-100 dark:bg-blue-950/30 p-2 rounded-lg">
                  <i class="fa-solid fa-chart-line text-blue-600 dark:text-blue-400"></i>
                </div>
                <div>
                  <h4 class="font-semibold text-slate-900 dark:text-white mb-1">Asset Analytics</h4>
                  <p class="text-sm text-slate-600 dark:text-slate-400">Utilization and performance metrics</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Status Badge -->
          <div class="mt-8 inline-flex items-center gap-2 bg-blue-50 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-500/30 text-blue-700 dark:text-blue-400 px-4 py-2 rounded-full text-sm font-medium">
            <i class="fa-solid fa-clock animate-pulse"></i>
            <span>In Development</span>
          </div>
        </div>
      </div>

      <!-- Quick Access Card -->
      <div class="mt-6 bg-blue-50 dark:bg-blue-950/10 border border-blue-200 dark:border-blue-500/20 rounded-lg p-6">
        <div class="flex items-start gap-4">
          <div class="bg-blue-100 dark:bg-blue-950/30 p-3 rounded-lg">
            <i class="fa-solid fa-info-circle text-blue-600 dark:text-blue-400 text-xl"></i>
          </div>
          <div class="flex-1">
            <h4 class="font-semibold text-slate-900 dark:text-white mb-2">Need Asset Management Now?</h4>
            <p class="text-sm text-slate-600 dark:text-slate-400 mb-3">
              While the integrated Asset module is being developed, you can access other modules:
            </p>
            <div class="flex flex-wrap gap-2">
              <router-link to="/" class="inline-flex items-center gap-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600 text-slate-700 dark:text-slate-300 px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                <i class="fa-solid fa-home"></i>
                <span>HSE Dashboard</span>
              </router-link>
              <router-link v-if="hasHRAccess" to="/hr/personnel" class="inline-flex items-center gap-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600 text-slate-700 dark:text-slate-300 px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                <i class="fa-solid fa-users"></i>
                <span>HR Module</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { authState } from '@/store/auth'

const hasHRAccess = computed(() => {
  return authState.accessibleModules && authState.accessibleModules.includes('hr')
})
</script>
