import type { ColumnDef } from '@tanstack/vue-table'
import { h } from 'vue'

export interface WorkLocation {
  id: number
  deck_name: string
  risk_level: string
}

export const columns = (
  onEdit: (location: WorkLocation) => void,
  onDelete: (id: number) => void
): ColumnDef<WorkLocation>[] => [
  {
    id: 'select',
    header: ({ table }) =>
      h('input', {
        type: 'checkbox',
        checked: table.getIsAllPageRowsSelected(),
        indeterminate: table.getIsSomePageRowsSelected(),
        onChange: table.getToggleAllPageRowsSelectedHandler(),
        class: 'w-4 h-4 rounded border-slate-300 text-[var(--color-saipem-primary)] focus:ring-[var(--color-saipem-primary)]'
      }),
    cell: ({ row }) =>
      h('input', {
        type: 'checkbox',
        checked: row.getIsSelected(),
        disabled: !row.getCanSelect(),
        onChange: row.getToggleSelectedHandler(),
        class: 'w-4 h-4 rounded border-slate-300 text-[var(--color-saipem-primary)] focus:ring-[var(--color-saipem-primary)]'
      }),
    enableSorting: false,
    enableHiding: false,
  },
  {
    accessorKey: 'deck_name',
    header: 'Deck Name',
    cell: ({ row }) => {
      return h('div', { class: 'font-semibold' }, row.getValue('deck_name'))
    },
  },
  {
    accessorKey: 'risk_level',
    header: 'Risk Level',
    cell: ({ row }) => {
      const riskLevel = row.getValue('risk_level') as string
      const riskLevelClass = {
        'LOW': 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
        'MEDIUM': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
        'HIGH': 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
      }[riskLevel] || 'bg-slate-100 text-slate-800'
      return h('span', { class: `px-3 py-1 rounded-full text-xs font-semibold ${riskLevelClass}` }, riskLevel || '-')
    },
  },
  {
    id: 'actions',
    header: 'Actions',
    cell: ({ row }) => {
      const location = row.original
      return h('div', { class: 'flex items-center gap-2' }, [
        h('button', {
          onClick: () => onEdit(location),
          class: 'px-4 py-2 rounded-lg font-medium text-sm transition-colors bg-slate-100 text-slate-700 hover:bg-slate-200'
        }, 'Edit'),
        h('button', {
          onClick: () => onDelete(location.id),
          class: 'px-4 py-2 rounded-lg font-medium text-sm transition-colors bg-red-600 text-white hover:bg-red-700'
        }, 'Delete'),
      ])
    },
  },
]
