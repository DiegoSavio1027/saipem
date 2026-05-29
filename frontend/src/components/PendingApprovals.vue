<template>
  <div v-if="userRole !== 'Safety Officer' && userRole !== 'Admin'" class="text-amber-600 dark:text-amber-400 text-[14px] py-4 px-6 bg-amber-50 dark:bg-amber-900/20 border border-amber-100 dark:border-amber-700 rounded-md">
    ⚠️ Current role: {{ userRole || 'Not set' }} - Only Safety Officer or Admin can see pending approvals
  </div>

  <Card v-else class="mb-6">
    <CardHeader>
      <CardTitle>Pending PTW Approvals</CardTitle>
      <CardDescription>Review and approve pending work permits</CardDescription>
    </CardHeader>
    <CardContent>
      <DataTable
        :data="pendingPTWs"
        :columns="columns"
        :bulk-actions="bulkActions"
        @bulk-action="handleBulkAction"
      />
    </CardContent>
  </Card>
</template>

<script setup>
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import DataTable from './pending-approvals/data-table.vue';
import { createPendingColumns } from './pending-approvals/columns';

const props = defineProps({
    userRole: String,
    pendingPTWs: Array
});

const emit = defineEmits(['approve', 'reject', 'view-details', 'bulk-approve', 'bulk-reject']);

const columns = createPendingColumns({
  onView: (ptw) => emit('view-details', ptw),
  onApprove: (id) => emit('approve', id),
  onReject: (id) => emit('reject', id),
});

const bulkActions = [
  { key: 'approve', label: 'Approve All', variant: 'default' },
  { key: 'reject', label: 'Reject All', variant: 'destructive' }
];

const handleBulkAction = (actionKey, rows) => {
  const ids = rows.map(row => row.id);
  if (actionKey === 'approve') {
    emit('bulk-approve', ids);
  } else if (actionKey === 'reject') {
    emit('bulk-reject', ids);
  }
};
</script>
