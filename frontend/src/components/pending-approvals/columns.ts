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
  status: string
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

export const createPendingColumns = (
  actions: {
    onView: (row: PTW) => void
    onApprove: (id: number) => void
    onReject: (id: number) => void
  }
): ColumnDef<PTW>[] => [
  {
    id: 'select',
    header: ({ table }) => h('input', {
      type: 'checkbox',
      checked: table.getIsAllPageRowsSelected(),
      onChange: (e: any) => table.toggleAllPageRowsSelected(!!e.target.checked),
      class: 'w-4 h-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500'
    }),
    cell: ({ row }) => h('input', {
      type: 'checkbox',
      checked: row.getIsSelected(),
      onChange: (e: any) => row.toggleSelected(!!e.target.checked),
      class: 'w-4 h-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500'
    }),
    enableSorting: false,
    enableHiding: false,
  },
  {
    accessorKey: 'permit_id',
    header: 'Permit ID',
    cell: ({ row }) => h('div', { class: 'font-medium text-slate-900' }, row.getValue('permit_id')),
  },
  {
    accessorKey: 'applicant',
    header: 'Applicant',
    cell: ({ row }) => {
      const ptw = row.original
      const fullName = ptw.employee?.full_name || ptw.emp_id
      return h('div', { class: 'text-slate-600' }, fullName)
    },
  },
  {
    accessorKey: 'permit_type',
    header: 'Permit Type',
    cell: ({ row }) => {
      const ptw = row.original
      const displayType = ptw.permit_type_display || ptw.permit_type
      const permitTypeColors: Record<string, string> = {
        'HOT_WORK': 'bg-orange-100 text-orange-700',
        'CONFINED_SPACE': 'bg-purple-100 text-purple-700',
        'WORKING_AT_HEIGHT': 'bg-sky-100 text-sky-700',
        'ISOLATION': 'bg-yellow-100 text-yellow-700',
      }
      const colorClass = permitTypeColors[ptw.permit_type] || 'bg-slate-100 text-slate-700'
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
    accessorKey: 'deck_location',
    header: 'Location',
    cell: ({ row }) => {
      const ptw = row.original
      const locationName = ptw.deck_location || '-'
      return h('div', { class: 'text-slate-600' }, locationName)
    },
  },
  {
    accessorKey: 'status',
    header: 'Status',
    cell: ({ row }) => {
      const status = row.getValue('status') as string
      const statusColors: Record<string, string> = {
        'APPROVED': 'bg-green-100 text-green-700',
        'PENDING': 'bg-amber-100 text-amber-700',
        'WAITING_FOR_CLOSE': 'bg-blue-100 text-blue-700',
        'REJECTED': 'bg-red-100 text-red-700',
        'CLOSED': 'bg-slate-100 text-slate-700',
      }
      return h('span', {
        class: `inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold ${statusColors[status] || 'bg-slate-100 text-slate-700'}`
      }, status)
    },
  },
  {
    id: 'actions',
    header: () => h('div', { class: 'text-right' }, 'Actions'),
    cell: ({ row }) => {
      const ptw = row.original
      return h('div', { class: 'flex items-center justify-end gap-2' }, [
        h(Button, {
          size: 'sm',
          variant: 'outline',
          class: 'h-8 px-3 text-xs',
          onClick: () => actions.onView(ptw)
        }, () => 'View'),
        h(Button, {
          size: 'sm',
          variant: 'destructive',
          class: 'h-8 px-3 text-xs ml-2',
          onClick: () => actions.onReject(ptw.id)
        }, () => 'Reject'),
        h(Button, {
          size: 'sm',
          class: 'h-8 px-3 text-xs bg-[var(--color-saipem-success)] hover:bg-[var(--color-saipem-success)]/90 text-white ml-2',
          onClick: () => actions.onApprove(ptw.id)
        }, () => 'Approve'),
      ])
    },
    enableSorting: false,
    enableHiding: false,
  },
]
