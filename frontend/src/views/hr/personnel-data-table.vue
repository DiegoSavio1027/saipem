<script setup lang="ts" generic="TData, TValue">
import type {
  ColumnDef,
  ColumnFiltersState,
  SortingState,
  VisibilityState,
} from '@tanstack/vue-table'
import {
  FlexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useVueTable,
} from '@tanstack/vue-table'
import { ref, computed, watch } from 'vue'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

const props = defineProps<{
  columns: ColumnDef<TData, TValue>[]
  data: TData[]
}>()

const sorting = ref<SortingState>([])
const columnFilters = ref<ColumnFiltersState>([])
const columnVisibility = ref<VisibilityState>({})
const rowSelection = ref({})
const globalFilter = ref('')
const pageSize = ref('10')
const statusFilter = ref('')
const mcuStatusFilter = ref('')

const table = useVueTable({
  get data() { return props.data },
  get columns() { return props.columns },
  getCoreRowModel: getCoreRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
  onSortingChange: (updater) => {
    sorting.value = typeof updater === 'function' ? updater(sorting.value) : updater
  },
  onColumnFiltersChange: (updater) => {
    columnFilters.value = typeof updater === 'function' ? updater(columnFilters.value) : updater
  },
  onColumnVisibilityChange: (updater) => {
    columnVisibility.value = typeof updater === 'function' ? updater(columnVisibility.value) : updater
  },
  onRowSelectionChange: (updater) => {
    rowSelection.value = typeof updater === 'function' ? updater(rowSelection.value) : updater
  },
  onGlobalFilterChange: (updater) => {
    globalFilter.value = typeof updater === 'function' ? updater(globalFilter.value) : updater
  },
  state: {
    get sorting() { return sorting.value },
    get columnFilters() { return columnFilters.value },
    get columnVisibility() { return columnVisibility.value },
    get rowSelection() { return rowSelection.value },
    get globalFilter() { return globalFilter.value },
  },
})

watch(pageSize, (newSize) => {
  table.setPageSize(parseInt(newSize))
})

watch(statusFilter, (value) => {
  table.getColumn('roster_status')?.setFilterValue(value === 'ALL' ? undefined : value)
})

watch(mcuStatusFilter, (value) => {
  table.getColumn('mcu_status')?.setFilterValue(value === 'ALL' ? undefined : value)
})

watch(() => props.data, () => {
  table.resetPageIndex()
})
</script>

<template>
  <div class="space-y-4">
    <!-- Filters -->
    <div class="flex gap-4 flex-wrap items-end">
      <div class="flex-1 min-w-[200px]">
        <label class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1 block">Search</label>
        <Input
          v-model="globalFilter"
          placeholder="Search by name, role, or email..."
          class="w-full"
        />
      </div>

      <div>
        <label class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1 block">Status</label>
        <Select v-model="statusFilter">
          <SelectTrigger class="w-[180px]">
            <SelectValue placeholder="All Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="ALL">All Status</SelectItem>
            <SelectItem value="ONBOARD">ONBOARD</SelectItem>
            <SelectItem value="AVAILABLE">AVAILABLE</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div>
        <label class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1 block">MCU Status</label>
        <Select v-model="mcuStatusFilter">
          <SelectTrigger class="w-[180px]">
            <SelectValue placeholder="All MCU Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="ALL">All MCU Status</SelectItem>
            <SelectItem value="FIT">FIT</SelectItem>
            <SelectItem value="UNFIT">UNFIT</SelectItem>
            <SelectItem value="EXPIRED">EXPIRED</SelectItem>
            <SelectItem value="PENDING">PENDING</SelectItem>
          </SelectContent>
        </Select>
      </div>
    </div>

    <!-- Table -->
    <div class="border border-slate-200 dark:border-slate-700 rounded-lg overflow-hidden">
      <Table>
        <TableHeader>
          <TableRow v-for="headerGroup in table.getHeaderGroups()" :key="headerGroup.id">
            <TableHead v-for="header in headerGroup.headers" :key="header.id">
              <button
                v-if="!header.isPlaceholder"
                @click="header.column.getToggleSortingHandler?.()"
                class="flex items-center gap-2 hover:text-slate-900 dark:hover:text-white transition-colors"
              >
                <FlexRender :render="header.column.columnDef.header" :props="header.getContext()" />
                <span v-if="header.column.getIsSorted()" class="text-xs">
                  {{ header.column.getIsSorted() === 'desc' ? '↓' : '↑' }}
                </span>
              </button>
              <FlexRender v-else :render="header.column.columnDef.header" :props="header.getContext()" />
            </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <template v-if="table.getRowModel().rows?.length">
            <TableRow v-for="row in table.getRowModel().rows" :key="row.id" class="hover:bg-slate-50 dark:hover:bg-slate-800/50">
              <TableCell v-for="cell in row.getVisibleCells()" :key="cell.id">
                <FlexRender :render="cell.column.columnDef.cell" :props="cell.getContext()" />
              </TableCell>
            </TableRow>
          </template>
          <TableRow v-else>
            <TableCell :colspan="table.getAllColumns().length" class="h-24 text-center text-slate-500 dark:text-slate-400">
              No personnel found
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>

    <!-- Pagination -->
    <div class="flex items-center justify-between">
      <div class="text-sm text-slate-600 dark:text-slate-400">
        Page {{ table.getState().pagination.pageIndex + 1 }} of {{ table.getPageCount() }}
      </div>
      <div class="flex gap-2">
        <Button
          variant="outline"
          size="sm"
          @click="table.previousPage()"
          :disabled="!table.getCanPreviousPage()"
        >
          Previous
        </Button>
        <Button
          variant="outline"
          size="sm"
          @click="table.nextPage()"
          :disabled="!table.getCanNextPage()"
        >
          Next
        </Button>
      </div>
    </div>

    <!-- Page Size -->
    <div class="flex items-center gap-2">
      <label class="text-sm text-slate-600 dark:text-slate-400">Rows per page:</label>
      <Select v-model="pageSize">
        <SelectTrigger class="w-[100px]">
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="5">5</SelectItem>
          <SelectItem value="10">10</SelectItem>
          <SelectItem value="20">20</SelectItem>
          <SelectItem value="50">50</SelectItem>
        </SelectContent>
      </Select>
    </div>
  </div>
</template>
