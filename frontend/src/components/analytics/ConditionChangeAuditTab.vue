<template>
  <div class="space-y-6">
    <!-- Filters -->
    <div class="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700">
      <h3 class="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-4">Filters</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- Date Range -->
        <div class="space-y-2">
          <Label class="text-xs font-medium text-slate-700 dark:text-slate-300">Start Date</Label>
          <input
            v-model="filters.startDate"
            type="date"
            class="w-full px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-slate-100 text-sm focus:ring-2 focus:ring-[var(--color-saipem-primary)] focus:border-transparent"
          />
        </div>
        <div class="space-y-2">
          <Label class="text-xs font-medium text-slate-700 dark:text-slate-300">End Date</Label>
          <input
            v-model="filters.endDate"
            type="date"
            class="w-full px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-slate-100 text-sm focus:ring-2 focus:ring-[var(--color-saipem-primary)] focus:border-transparent"
          />
        </div>
        <div class="space-y-2">
          <Label class="text-xs font-medium text-slate-700 dark:text-slate-300">Changed By</Label>
          <Select v-model="filters.changedBy">
            <SelectTrigger class="w-full">
              <SelectValue placeholder="All users" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectItem value="">All users</SelectItem>
                <SelectItem v-for="employee in employees" :key="employee.emp_id" :value="employee.emp_id">
                  {{ employee.full_name }}
                </SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>
      </div>
      <div class="flex gap-2 mt-4">
        <Button @click="applyFilters" size="sm" class="bg-[var(--color-saipem-primary)] hover:bg-[var(--color-saipem-primary)]/90">
          Apply Filters
        </Button>
        <Button @click="clearFilters" size="sm" variant="outline">
          Clear
        </Button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[var(--color-saipem-primary)]"></div>
    </div>

    <!-- Audit Log Table -->
    <div v-else-if="auditLogs.length > 0" class="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-slate-50 dark:bg-slate-900 border-b border-slate-200 dark:border-slate-700">
            <tr>
              <th class="text-left py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Date & Time</th>
              <th class="text-center py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Previous Status</th>
              <th class="text-center py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">New Status</th>
              <th class="text-left py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Changed By</th>
              <th class="text-left py-3 px-4 font-semibold text-slate-900 dark:text-slate-100">Reason</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="log in auditLogs"
              :key="log.id"
              class="border-b border-slate-100 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors"
            >
              <td class="py-3 px-4 text-slate-900 dark:text-slate-100">
                {{ formatDateTime(log.created_at) }}
              </td>
              <td class="text-center py-3 px-4">
                <span :class="[
                  'px-2 py-1 rounded text-xs font-semibold uppercase',
                  log.previous_status === 'GREEN' ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400' :
                  log.previous_status === 'YELLOW' ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400' :
                  'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
                ]">
                  {{ log.previous_status }}
                </span>
              </td>
              <td class="text-center py-3 px-4">
                <span :class="[
                  'px-2 py-1 rounded text-xs font-semibold uppercase',
                  log.new_status === 'GREEN' ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400' :
                  log.new_status === 'YELLOW' ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400' :
                  'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
                ]">
                  {{ log.new_status }}
                </span>
              </td>
              <td class="py-3 px-4 text-slate-900 dark:text-slate-100">
                <div class="flex flex-col">
                  <span class="font-medium">{{ log.changed_by_name }}</span>
                  <span class="text-xs text-slate-500 dark:text-slate-400">{{ log.changed_by }}</span>
                </div>
              </td>
              <td class="py-3 px-4 text-slate-600 dark:text-slate-400 max-w-md">
                <p class="line-clamp-2">{{ log.override_reason }}</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="bg-slate-50 dark:bg-slate-900 px-4 py-3 border-t border-slate-200 dark:border-slate-700 flex items-center justify-between">
        <div class="text-sm text-slate-600 dark:text-slate-400">
          Showing {{ offset + 1 }} to {{ Math.min(offset + limit, totalCount) }} of {{ totalCount }} records
        </div>
        <div class="flex gap-2">
          <Button
            @click="previousPage"
            :disabled="offset === 0"
            size="sm"
            variant="outline"
            class="disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </Button>
          <Button
            @click="nextPage"
            :disabled="offset + limit >= totalCount"
            size="sm"
            variant="outline"
            class="disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </Button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="bg-white dark:bg-slate-800 p-12 rounded-xl border border-slate-200 dark:border-slate-700 text-center">
      <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mx-auto text-slate-400 dark:text-slate-600 mb-4">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
        <polyline points="14 2 14 8 20 8"/>
        <line x1="16" x2="8" y1="13" y2="13"/>
        <line x1="16" x2="8" y1="17" y2="17"/>
        <polyline points="10 9 9 9 8 9"/>
      </svg>
      <p class="text-slate-600 dark:text-slate-400 font-medium">No audit logs found</p>
      <p class="text-sm text-slate-500 dark:text-slate-500 mt-1">Try adjusting your filters</p>
    </div>

    <!-- Info Card -->
    <div class="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 p-6 rounded-xl border border-blue-200 dark:border-blue-700">
      <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">📋 About Condition Change Audit Log</h3>
      <div class="space-y-3 text-sm text-slate-700 dark:text-slate-300">
        <p>
          This audit log tracks all manual condition changes made by Safety Officers and Administrators.
          Every change is recorded with the reason, timestamp, and the person who made the change.
        </p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
          <div class="bg-white dark:bg-slate-800 p-3 rounded-lg border border-blue-200 dark:border-blue-700">
            <p class="font-semibold text-slate-900 dark:text-slate-100 mb-1">🟢 GREEN</p>
            <p class="text-xs text-slate-600 dark:text-slate-400">Normal operations, all systems go</p>
          </div>
          <div class="bg-white dark:bg-slate-800 p-3 rounded-lg border border-yellow-200 dark:border-yellow-700">
            <p class="font-semibold text-slate-900 dark:text-slate-100 mb-1">🟡 YELLOW</p>
            <p class="text-xs text-slate-600 dark:text-slate-400">Heightened alert, extra caution required</p>
          </div>
          <div class="bg-white dark:bg-slate-800 p-3 rounded-lg border border-red-200 dark:border-red-700">
            <p class="font-semibold text-slate-900 dark:text-slate-100 mb-1">🔴 RED</p>
            <p class="text-xs text-slate-600 dark:text-slate-400">Emergency mode, PTW approvals frozen</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { toast } from 'vue-sonner';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';

const loading = ref(true);
const auditLogs = ref([]);
const employees = ref([]);
const totalCount = ref(0);
const limit = ref(20);
const offset = ref(0);

const filters = ref({
  startDate: '',
  endDate: '',
  changedBy: ''
});

const formatDateTime = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
};

const fetchAuditLogs = async () => {
  loading.value = true;
  try {
    const params = new URLSearchParams({
      limit: limit.value.toString(),
      offset: offset.value.toString()
    });

    if (filters.value.startDate) {
      params.append('start_date', new Date(filters.value.startDate).toISOString());
    }
    if (filters.value.endDate) {
      const endDate = new Date(filters.value.endDate);
      endDate.setHours(23, 59, 59, 999);
      params.append('end_date', endDate.toISOString());
    }
    if (filters.value.changedBy) {
      params.append('changed_by', filters.value.changedBy);
    }

    const response = await fetch(`${API_BASE_URL}/hse/status/history/?${params}`, {
      credentials: 'include'
    });

    if (response.ok) {
      const data = await response.json();
      auditLogs.value = data.results;
      totalCount.value = data.count;
    } else {
      toast.error('Failed to load audit logs');
    }
  } catch (error) {
    console.error('Error fetching audit logs:', error);
    toast.error('Error loading audit logs');
  } finally {
    loading.value = false;
  }
};

const fetchEmployees = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/hse/employees/`, { credentials: 'include' });
    if (response.ok) {
      const data = await response.json();
      // Filter only Safety Officers and Admins
      employees.value = data.filter(emp =>
        emp.job_role === 'Safety Officer' || emp.job_role === 'Admin'
      );
    }
  } catch (error) {
    console.error('Failed to fetch employees:', error);
  }
};

const applyFilters = () => {
  offset.value = 0;
  fetchAuditLogs();
};

const clearFilters = () => {
  filters.value = {
    startDate: '',
    endDate: '',
    changedBy: ''
  };
  offset.value = 0;
  fetchAuditLogs();
};

const nextPage = () => {
  if (offset.value + limit.value < totalCount.value) {
    offset.value += limit.value;
    fetchAuditLogs();
  }
};

const previousPage = () => {
  if (offset.value > 0) {
    offset.value = Math.max(0, offset.value - limit.value);
    fetchAuditLogs();
  }
};

onMounted(() => {
  fetchAuditLogs();
  fetchEmployees();
});
</script>
