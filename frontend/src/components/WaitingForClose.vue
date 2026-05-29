<template>
  <div v-if="userRole !== 'Safety Officer' && userRole !== 'Admin'" class="text-amber-600 dark:text-amber-400 text-[14px] py-4 px-6 bg-amber-50 dark:bg-amber-900/20 border border-amber-100 dark:border-amber-700 rounded-md">
    ⚠️ Current role: {{ userRole || 'Not set' }} - Only Safety Officer or Admin can confirm close
  </div>

  <Card v-else class="mb-6">
    <CardHeader>
      <CardTitle>Waiting for Close Confirmation</CardTitle>
      <CardDescription>Confirm completion of work permits</CardDescription>
    </CardHeader>
    <CardContent>
      <DataTable
        :data="waitingForClosePTWs"
        :columns="columns"
        :bulk-actions="bulkActions"
        @bulk-action="handleBulkAction"
      />
    </CardContent>
  </Card>
</template>

<script setup>
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import DataTable from './waiting-for-close/data-table.vue';
import { createWaitingForCloseColumns } from './waiting-for-close/columns';

const props = defineProps({
    userRole: String,
    waitingForClosePTWs: Array
});

const emit = defineEmits(['confirm-close', 'view-details']);

const columns = createWaitingForCloseColumns({
  onView: (ptw) => emit('view-details', ptw),
  onConfirmClose: (id) => emit('confirm-close', id),
});

const bulkActions = [
  { key: 'confirm-close', label: 'Confirm Close All', variant: 'default' }
];

const handleBulkAction = (actionKey, rows) => {
  const ids = rows.map(row => row.id);
  if (actionKey === 'confirm-close') {
    ids.forEach(id => emit('confirm-close', id));
  }
};
</script>
