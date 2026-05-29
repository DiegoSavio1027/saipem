<template>
  <div class="space-y-6">
    <!-- Header with Submit Button -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white dark:bg-slate-800 p-6 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm">
      <div>
        <h2 class="text-xl font-bold text-slate-900 dark:text-slate-100">My Permits</h2>
        <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">Manage your work permit requests</p>
      </div>
      <button @click="$emit('open-submit-modal')" class="w-full sm:w-auto bg-[var(--color-saipem-tertiary)] hover:bg-[var(--color-saipem-tertiary)]/90 text-white px-6 py-3 rounded-lg font-semibold text-sm transition-colors shadow-md hover:shadow-lg flex items-center justify-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M12 5v14"/></svg>
        Submit New PTW
      </button>
    </div>

    <!-- PTW Table -->
    <Card>
      <CardHeader>
        <CardTitle>My Work Permits</CardTitle>
        <CardDescription>View and manage your submitted permits</CardDescription>
      </CardHeader>
      <CardContent>
        <DataTable
          title="My Work Permits"
          :data="myPTWs"
          :columns="columns"
        />
      </CardContent>
    </Card>

    <!-- Permit Detail Dialog -->
    <PermitDetailDialog
      v-model:open="showDetailDialog"
      :permit-id="selectedPermitId"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import DataTable from './worker-dashboard/data-table.vue';
import PermitDetailDialog from './PermitDetailDialog.vue';
import { createWorkerColumns } from './worker-dashboard/columns';

const props = defineProps({
    myPTWs: Array
});

const emit = defineEmits(['start-work', 'mark-done', 'edit', 'delete', 'open-submit-modal']);

const showDetailDialog = ref(false);
const selectedPermitId = ref(null);

const handleView = (row) => {
  selectedPermitId.value = row.id;
  showDetailDialog.value = true;
};

const columns = createWorkerColumns({
  onStartWork: (id) => emit('start-work', id),
  onMarkDone: (id) => emit('mark-done', id),
  onEdit: (row) => emit('edit', row),
  onDelete: (id) => emit('delete', id),
  onView: handleView,
});
</script>
