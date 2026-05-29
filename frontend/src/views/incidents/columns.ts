import type { ColumnDef } from '@tanstack/vue-table'
import { h } from 'vue'

export interface Incident {
  id: number
  incident_id: string
  severity: string
  severity_display: string
  location_name: string
  description: string
  incident_date: string
  status: string
  status_display: string
  employee_name: string
}

const getSeverityBadgeClass = (severity: string) => {
  const classes: Record<string, string> = {
    'SAFETY_OBSERVATION': 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-400',
    'NEAR_MISS': 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-400',
    'FIRST_AID': 'bg-orange-100 dark:bg-orange-900/30 text-orange-800 dark:text-orange-400',
    'LTI': 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-400'
  }
  return classes[severity] || 'bg-slate-100 dark:bg-slate-700 text-slate-800 dark:text-slate-300'
}

const getStatusBadgeClass = (status: string) => {
  const classes: Record<string, string> = {
    'PENDING_VERIFICATION': 'bg-purple-100 dark:bg-purple-900/30 text-purple-800 dark:text-purple-400',
    'OPEN': 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-400',
    'INVESTIGATING': 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-400',
    'CLOSED': 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400',
    'REJECTED': 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-400'
  }
  return classes[status] || 'bg-slate-100 dark:bg-slate-700 text-slate-800 dark:text-slate-300'
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

export const createColumns = (
  onView: (incident: Incident) => void,
  onInvestigate: (incident: Incident) => void,
  onClose: (incident: Incident) => void,
  onDelete: (incident: Incident) => void,
  userRole: string = 'Worker',
  onVerify?: (incident: Incident) => void
): ColumnDef<Incident>[] => [
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
    accessorKey: 'incident_id',
    header: 'Incident ID',
    cell: ({ row }) => {
      return h('div', { class: 'font-semibold text-slate-900 dark:text-slate-100' }, row.getValue('incident_id') || `#${row.original.id}`)
    },
  },
  {
    accessorKey: 'severity',
    header: 'Severity',
    cell: ({ row }) => {
      const severity = row.getValue('severity') as string
      return h('span', {
        class: `px-2 py-1 text-xs font-semibold rounded-full ${getSeverityBadgeClass(severity)}`
      }, row.original.severity_display)
    },
  },
  {
    accessorKey: 'location_name',
    header: 'Location',
    cell: ({ row }) => {
      return h('div', { class: 'text-sm text-slate-700 dark:text-slate-300' }, row.getValue('location_name'))
    },
  },
  {
    accessorKey: 'description',
    header: 'Description',
    cell: ({ row }) => {
      const description = row.getValue('description') as string
      return h('div', { class: 'text-sm max-w-xs truncate text-slate-700 dark:text-slate-300' }, description || '-')
    },
  },
  {
    accessorKey: 'incident_date',
    header: 'Date',
    cell: ({ row }) => {
      const date = row.getValue('incident_date') as string
      return h('div', { class: 'text-sm text-slate-700 dark:text-slate-300' }, formatDate(date))
    },
  },
  {
    accessorKey: 'status',
    header: 'Status',
    cell: ({ row }) => {
      const status = row.getValue('status') as string
      return h('span', {
        class: `px-2 py-1 text-xs font-semibold rounded-full ${getStatusBadgeClass(status)}`
      }, row.original.status_display)
    },
  },
  {
    id: 'actions',
    header: 'Actions',
    cell: ({ row }) => {
      const incident = row.original
      const status = incident.status
      const isWorker = userRole === 'Worker'

      const buttons = []

      buttons.push(
        h('button', {
          onClick: () => onView(incident),
          class: 'px-3 py-1.5 rounded-lg font-medium text-sm transition-colors bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-600'
        }, 'View')
      )

      if (!isWorker) {
        if (status === 'PENDING_VERIFICATION' && onVerify) {
          buttons.push(
            h('button', {
              onClick: () => onVerify(incident),
              class: 'px-3 py-1.5 rounded-lg font-medium text-sm transition-colors bg-purple-600 dark:bg-purple-700 text-white hover:bg-purple-700 dark:hover:bg-purple-800'
            }, 'Verify')
          )
        }

        if (status === 'OPEN') {
          buttons.push(
            h('button', {
              onClick: () => onInvestigate(incident),
              class: 'px-3 py-1.5 rounded-lg font-medium text-sm transition-colors bg-yellow-600 dark:bg-yellow-700 text-white hover:bg-yellow-700 dark:hover:bg-yellow-800'
            }, 'Investigate')
          )
        }

        if (status === 'INVESTIGATING') {
          buttons.push(
            h('button', {
              onClick: () => onClose(incident),
              class: 'px-3 py-1.5 rounded-lg font-medium text-sm transition-colors bg-green-600 dark:bg-green-700 text-white hover:bg-green-700 dark:hover:bg-green-800'
            }, 'Close')
          )
        }

        buttons.push(
          h('button', {
            onClick: () => onDelete(incident),
            class: 'px-3 py-1.5 rounded-lg font-medium text-sm transition-colors bg-red-600 dark:bg-red-700 text-white hover:bg-red-700 dark:hover:bg-red-800'
          }, 'Delete')
        )
      }

      return h('div', { class: 'flex items-center gap-2' }, buttons)
    },
  },
]
