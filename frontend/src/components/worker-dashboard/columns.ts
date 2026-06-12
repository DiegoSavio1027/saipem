import { h } from 'vue'
import type { ColumnDef } from '@tanstack/vue-table'
import { Button } from '@/components/ui/button'

export interface PTW {
  id: number
  permit_id: string
  emp_id: string
  permit_type: string
  permit_type_display?: string
  wo_id: string
  deck_location?: string
  status: 'PENDING' | 'APPROVED' | 'IN_PROGRESS' | 'WAITING_FOR_CLOSE' | 'REJECTED' | 'CLOSED'
  status_display?: string
  employee?: {
    emp_id: string
    full_name: string
    job_role: string
  }
  work_order?: {
    wo_id: string
    description: string
  }
}

export const createWorkerColumns = (
  actions: {
    onStartWork: (id: number) => void
    onMarkDone: (id: number) => void
    onEdit: (row: PTW) => void
    onDelete: (id: number) => void
    onView: (row: PTW) => void
  }
): ColumnDef<PTW>[] => [
  {
    accessorKey: 'permit_id',
    header: 'Permit ID',
    cell: ({ row }) => h('div', { class: 'font-medium text-slate-900 dark:text-slate-100' }, row.getValue('permit_id')),
  },
  {
    accessorKey: 'permit_type',
    header: 'Permit Type',
    cell: ({ row }) => {
      const ptw = row.original
      const displayType = ptw.permit_type_display || ptw.permit_type
      const permitTypeColors: Record<string, string> = {
        'HOT_WORK': 'bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400',
        'CONFINED_SPACE': 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400',
        'WORKING_AT_HEIGHT': 'bg-sky-100 dark:bg-sky-900/30 text-sky-700 dark:text-sky-400',
        'ISOLATION': 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400',
      }
      const colorClass = permitTypeColors[ptw.permit_type] || 'bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300'
      return h('span', {
        class: `inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold ${colorClass}`
      }, displayType)
    },
  },
  {
    accessorKey: 'wo_id',
    header: 'Work Order',
    cell: ({ row }) => {
      const ptw = row.original
      let displayText = ptw.wo_id
      if (ptw.work_order) {
        displayText = `${ptw.work_order.wo_id} - ${ptw.work_order.description}`
      }
      return h('div', { class: 'font-semibold text-[var(--color-saipem-tertiary)]' }, displayText)
    },
  },
  {
    accessorKey: 'deck_location_name',
    header: 'Location',
    cell: ({ row }) => {
      const ptw = row.original
      const locationName = ptw.deck_location_name || ptw.deck_location || '-'
      return h('div', { class: 'text-slate-600 dark:text-slate-400' }, locationName)
    },
  },
  {
    accessorKey: 'status',
    header: 'Status',
    cell: ({ row }) => {
      const status = row.getValue('status') as string
      const statusColors: Record<string, string> = {
        'APPROVED': 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400',
        'IN_PROGRESS': 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400',
        'PENDING': 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400',
        'WAITING_FOR_CLOSE': 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400',
        'REJECTED': 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400',
        'CLOSED': 'bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300',
      }
      return h('span', {
        class: `inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold ${statusColors[status] || 'bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300'}`
      }, status)
    },
  },
  {
    id: 'actions',
    header: () => h('div', { class: 'text-right' }, 'Actions'),
    cell: ({ row }) => {
      const ptw = row.original
      const buttons = []

      if (ptw.status === 'APPROVED') {
        buttons.push(
          h(Button, {
            size: 'sm',
            class: 'h-[36px] px-4 rounded-md bg-green-500 hover:bg-green-600 text-white font-medium shadow-sm transition-colors',
            onClick: () => actions.onStartWork(ptw.id)
          }, () => 'Start Work'),
          h(Button, {
            size: 'sm',
            variant: 'outline',
            class: 'h-[36px] px-4 rounded-md border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 font-medium shadow-sm transition-colors ml-2',
            onClick: () => actions.onView(ptw)
          }, () => 'View')
        )
      } else if (ptw.status === 'IN_PROGRESS') {
        buttons.push(
          h(Button, {
            size: 'sm',
            class: 'h-[36px] px-4 rounded-md bg-amber-500 hover:bg-amber-600 text-white font-medium shadow-sm transition-colors',
            onClick: () => actions.onMarkDone(ptw.id)
          }, () => 'Mark as Job Done')
        )
      } else if (ptw.status === 'PENDING') {
        buttons.push(
          h(Button, {
            size: 'sm',
            variant: 'outline',
            class: 'h-[36px] px-4 rounded-md border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 font-medium shadow-sm transition-colors',
            onClick: () => actions.onEdit(ptw)
          }, () => 'Edit'),
          h(Button, {
            size: 'sm',
            variant: 'destructive',
            class: 'h-[36px] px-4 rounded-md bg-red-500 hover:bg-red-600 text-white font-medium shadow-sm transition-colors ml-2',
            onClick: () => actions.onDelete(ptw.id)
          }, () => 'Delete')
        )
      } else {
        buttons.push(
          h(Button, {
            size: 'sm',
            variant: 'outline',
            class: 'h-[36px] px-4 rounded-md border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 font-medium shadow-sm transition-colors',
            onClick: () => actions.onView(ptw)
          }, () => 'View')
        )
      }

      return h('div', { class: 'flex items-center justify-end gap-2' }, buttons)
    },
    enableSorting: false,
    enableHiding: false,
  },
]
