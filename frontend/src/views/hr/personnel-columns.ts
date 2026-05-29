import type { ColumnDef } from '@tanstack/vue-table'
import { h } from 'vue'
import { Edit, Trash2 } from '@lucide/vue'

export interface Personnel {
  emp_id: string
  full_name: string
  job_role: string
  email: string
  roster_status: string
  mcu_status: string
  mcu_expiry: string
}

export const personnelColumns: ColumnDef<Personnel>[] = [
  {
    accessorKey: 'emp_id',
    header: 'EMP ID',
    cell: ({ row }) => {
      return h('span', { class: 'font-mono text-red-600 dark:text-red-400' }, row.getValue('emp_id'))
    },
  },
  {
    accessorKey: 'full_name',
    header: 'Full Name',
    cell: ({ row }) => {
      return h('span', { class: 'font-semibold text-slate-900 dark:text-white' }, row.getValue('full_name'))
    },
  },
  {
    accessorKey: 'job_role',
    header: 'Job Role',
    cell: ({ row }) => {
      return h('span', { class: 'text-slate-600 dark:text-slate-400' }, row.getValue('job_role'))
    },
  },
  {
    accessorKey: 'email',
    header: 'Email',
    cell: ({ row }) => {
      const email = row.getValue('email') as string
      return h('span', { class: 'text-slate-600 dark:text-slate-400' }, email || '-')
    },
  },
  {
    accessorKey: 'roster_status',
    header: 'Status',
    cell: ({ row }) => {
      const status = row.getValue('roster_status') as string
      const isOnboard = status === 'ONBOARD'
      return h('span', {
        class: `px-3 py-1 rounded-full text-xs font-semibold ${
          isOnboard
            ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400'
            : 'bg-slate-100 dark:bg-slate-700 text-slate-800 dark:text-slate-400'
        }`
      }, status)
    },
  },
  {
    accessorKey: 'mcu_status',
    header: 'MCU Status',
    cell: ({ row }) => {
      const status = row.getValue('mcu_status') as string || 'PENDING'
      let colorClass = 'bg-slate-100 dark:bg-slate-700 text-slate-800 dark:text-slate-400'

      if (status === 'FIT') {
        colorClass = 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400'
      } else if (status === 'UNFIT' || status === 'EXPIRED') {
        colorClass = 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-400'
      } else if (status === 'PENDING') {
        colorClass = 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-400'
      }

      return h('span', {
        class: `px-3 py-1 rounded-full text-xs font-semibold ${colorClass}`
      }, status)
    },
  },
  {
    accessorKey: 'mcu_expiry',
    header: 'MCU Expiry',
    cell: ({ row }) => {
      const expiry = row.getValue('mcu_expiry') as string
      return h('span', { class: 'text-slate-600 dark:text-slate-400' }, expiry || '-')
    },
  },
  {
    id: 'actions',
    header: 'Action',
    cell: ({ row }) => {
      return h('div', { class: 'flex items-center gap-2 justify-center' }, [
        h('button', {
          class: 'text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 text-sm font-semibold flex items-center gap-1',
          onClick: () => {
            const event = new CustomEvent('edit-personnel', { detail: row.original })
            window.dispatchEvent(event)
          }
        }, [
          h(Edit, { class: 'w-4 h-4' }),
          'Edit'
        ]),
        h('button', {
          class: 'text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 text-sm font-semibold flex items-center gap-1',
          onClick: () => {
            const event = new CustomEvent('delete-personnel', { detail: row.original.emp_id })
            window.dispatchEvent(event)
          }
        }, [
          h(Trash2, { class: 'w-4 h-4' }),
          'Delete'
        ])
      ])
    },
  },
]
