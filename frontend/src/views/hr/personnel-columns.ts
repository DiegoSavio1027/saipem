import type { ColumnDef } from '@tanstack/vue-table'
import { h } from 'vue'
import { Pencil, Trash2 } from '@lucide/vue'

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
      return h('span', { class: 'font-mono font-bold text-[var(--color-saipem-tertiary)]' }, row.getValue('emp_id'))
    },
  },
  {
    accessorKey: 'full_name',
    header: 'Full Name',
    cell: ({ row }) => {
      return h('span', { class: 'font-bold text-slate-900 dark:text-white' }, row.getValue('full_name'))
    },
  },
  {
    accessorKey: 'job_role',
    header: 'Job Role',
    cell: ({ row }) => {
      return h('span', { class: 'text-slate-600 dark:text-slate-400 text-xs' }, row.getValue('job_role'))
    },
  },
  {
    accessorKey: 'email',
    header: 'Email',
    cell: ({ row }) => {
      const email = row.getValue('email') as string
      return h('span', { class: 'text-slate-500 dark:text-slate-400 text-xs font-mono' }, email || '—')
    },
  },
  {
    accessorKey: 'roster_status',
    header: 'Status',
    cell: ({ row }) => {
      const status = row.getValue('roster_status') as string
      const isOnboard = status === 'ONBOARD'
      return h('span', {
        class: `px-2.5 py-1 rounded-full text-xs font-black tracking-wide ${
          isOnboard
            ? 'bg-orange-100 dark:bg-orange-950/30 text-orange-700 dark:text-orange-400 border border-orange-200 dark:border-orange-800/40'
            : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700'
        }`
      }, status)
    },
  },
  {
    accessorKey: 'mcu_status',
    header: 'MCU Status',
    cell: ({ row }) => {
      const status = (row.getValue('mcu_status') as string) || 'PENDING'
      let colorClass = 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700'

      if (status === 'FIT') {
        colorClass = 'bg-green-100 dark:bg-green-950/30 text-green-700 dark:text-green-400 border border-green-200 dark:border-green-800/40'
      } else if (status === 'UNFIT') {
        colorClass = 'bg-red-100 dark:bg-red-950/30 text-red-700 dark:text-red-400 border border-red-200 dark:border-red-800/40'
      } else if (status === 'EXPIRED') {
        colorClass = 'bg-amber-100 dark:bg-amber-950/30 text-amber-700 dark:text-amber-400 border border-amber-200 dark:border-amber-800/40'
      } else if (status === 'PENDING') {
        colorClass = 'bg-blue-100 dark:bg-blue-950/30 text-blue-700 dark:text-blue-400 border border-blue-200 dark:border-blue-800/40'
      }

      return h('span', {
        class: `px-2.5 py-1 rounded-full text-xs font-black tracking-wide ${colorClass}`
      }, status)
    },
  },
  {
    accessorKey: 'mcu_expiry',
    header: 'MCU Expiry',
    cell: ({ row }) => {
      const expiry = row.getValue('mcu_expiry') as string
      return h('span', { class: 'text-slate-500 dark:text-slate-400 text-xs font-mono' }, expiry || '—')
    },
  },
  {
    id: 'actions',
    header: 'Actions',
    cell: ({ row }) => {
      return h('div', { class: 'flex items-center gap-1.5 justify-center' }, [
        h('button', {
          class: 'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 dark:text-slate-400 hover:text-[var(--color-saipem-tertiary)] hover:bg-orange-50 dark:hover:bg-orange-950/20 border border-transparent hover:border-orange-200 dark:hover:border-orange-900/40 transition-all',
          onClick: () => {
            const event = new CustomEvent('edit-personnel', { detail: row.original })
            window.dispatchEvent(event)
          }
        }, [
          h(Pencil, { class: 'w-3.5 h-3.5' }),
          'Edit'
        ]),
        h('button', {
          class: 'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 dark:text-slate-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/20 border border-transparent hover:border-red-200 dark:hover:border-red-900/40 transition-all',
          onClick: () => {
            const event = new CustomEvent('delete-personnel', { detail: row.original.emp_id })
            window.dispatchEvent(event)
          }
        }, [
          h(Trash2, { class: 'w-3.5 h-3.5' }),
          'Delete'
        ])
      ])
    },
  },
]
