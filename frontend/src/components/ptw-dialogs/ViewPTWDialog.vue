<script setup lang="ts">
import { ref, watch } from 'vue'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'

interface PTW {
  id: number
  permit_id: string
  emp_id: string
  permit_type: string
  permit_type_display?: string
  wo_id: string
  deck_location?: string
  status: string
  status_display?: string
  created_at?: string
  approved_by?: string
  approved_by_name?: string
  approved_at?: string
  signature?: string
  rejected_by?: string
  rejected_by_name?: string
  rejected_at?: string
  rejection_reason?: string
  closed_by?: string
  closed_by_name?: string
  closed_at?: string
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

const props = defineProps<{
  open: boolean
  ptw: PTW | null
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
}>()

const isOpen = ref(props.open)

watch(() => props.open, (newVal) => {
  isOpen.value = newVal
})

watch(isOpen, (newVal) => {
  emit('update:open', newVal)
})

const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    'APPROVED': 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400',
    'PENDING': 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400',
    'WAITING_FOR_CLOSE': 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400',
    'REJECTED': 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400',
    'CLOSED': 'bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-400',
  }
  return colors[status] || 'bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-400'
}

const formatDate = (dateString?: string) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const openPrintPreview = () => {
  if (props.ptw) {
    const printUrl = `/permit-print/${props.ptw.id}`
    window.open(printUrl, '_blank')
  }
}
</script>

<template>
  <Dialog v-model:open="isOpen">
    <DialogContent class="max-w-2xl max-h-[90vh] overflow-y-auto">
      <DialogHeader>
        <DialogTitle>Permit To Work Details</DialogTitle>
        <DialogDescription>
          Complete information about the permit to work
        </DialogDescription>
      </DialogHeader>

      <div v-if="ptw" class="space-y-6">
        <!-- Basic Information -->
        <div class="space-y-4">
          <h3 class="text-sm font-semibold text-slate-900 dark:text-slate-100 border-b border-slate-200 dark:border-slate-700 pb-2">Basic Information</h3>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm font-medium text-slate-500 dark:text-slate-400">Permit ID</p>
              <p class="text-sm text-slate-900 dark:text-slate-100 font-semibold">{{ ptw.permit_id }}</p>
            </div>

            <div>
              <p class="text-sm font-medium text-slate-500 dark:text-slate-400">Status</p>
              <span :class="`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold ${getStatusColor(ptw.status)}`">
                {{ ptw.status }}
              </span>
            </div>

            <div>
              <p class="text-sm font-medium text-slate-500 dark:text-slate-400">Applicant</p>
              <p class="text-sm text-slate-900 dark:text-slate-100">{{ ptw.employee?.full_name || ptw.emp_id }}</p>
            </div>

            <div>
              <p class="text-sm font-medium text-slate-500 dark:text-slate-400">Permit Type</p>
              <p class="text-sm text-slate-900 dark:text-slate-100">{{ ptw.permit_type_display || ptw.permit_type }}</p>
            </div>

            <div class="col-span-2">
              <p class="text-sm font-medium text-slate-500 dark:text-slate-400">Work Order</p>
              <p class="text-sm text-slate-900 dark:text-slate-100 font-semibold text-[var(--color-saipem-tertiary)]">{{ ptw.work_order?.wo_id }} - {{ ptw.work_order?.description }}</p>
            </div>

            <div v-if="ptw.deck_location" class="col-span-2">
              <p class="text-sm font-medium text-slate-500 dark:text-slate-400">Location</p>
              <p class="text-sm text-slate-900 dark:text-slate-100">{{ ptw.deck_location }}</p>
            </div>
          </div>
        </div>

        <!-- Approval/Rejection Info -->
        <div v-if="ptw.status !== 'PENDING'" class="space-y-4">
          <h3 class="text-sm font-semibold text-slate-900 dark:text-slate-100 border-b border-slate-200 dark:border-slate-700 pb-2">Approval Information</h3>

          <div v-if="ptw.status === 'APPROVED' || ptw.status === 'WAITING_FOR_CLOSE' || ptw.status === 'CLOSED'" class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm font-medium text-slate-500 dark:text-slate-400">Approved By</p>
              <p class="text-sm text-slate-900 dark:text-slate-100">{{ ptw.approved_by_name || ptw.approved_by || '-' }}</p>
            </div>

            <div>
              <p class="text-sm font-medium text-slate-500 dark:text-slate-400">Approval Date</p>
              <p class="text-sm text-slate-900 dark:text-slate-100">{{ formatDate(ptw.approved_at) }}</p>
            </div>

            <!-- Signature -->
            <div v-if="ptw.signature" class="col-span-2">
              <p class="text-sm font-medium text-slate-500 dark:text-slate-400 mb-2">Digital Signature</p>
              <div class="border-2 border-slate-200 dark:border-slate-700 rounded-lg p-4 bg-slate-50 dark:bg-slate-800 inline-block">
                <img :src="ptw.signature" alt="Signature" class="max-w-xs h-20 object-contain" />
              </div>
            </div>
          </div>

          <div v-if="ptw.status === 'REJECTED'" class="space-y-2">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-sm font-medium text-slate-500 dark:text-slate-400">Rejected By</p>
                <p class="text-sm text-slate-900 dark:text-slate-100">{{ ptw.rejected_by_name || ptw.rejected_by || '-' }}</p>
              </div>

              <div>
                <p class="text-sm font-medium text-slate-500 dark:text-slate-400">Rejection Date</p>
                <p class="text-sm text-slate-900 dark:text-slate-100">{{ formatDate(ptw.rejected_at) }}</p>
              </div>
            </div>

            <div>
              <p class="text-sm font-medium text-slate-500 dark:text-slate-400">Rejection Reason</p>
              <p class="text-sm text-slate-900 dark:text-slate-100 whitespace-pre-wrap bg-red-50 dark:bg-red-900/20 p-3 rounded-md">{{ ptw.rejection_reason || '-' }}</p>
            </div>
          </div>

          <div v-if="ptw.status === 'CLOSED'" class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm font-medium text-slate-500 dark:text-slate-400">Closed By</p>
              <p class="text-sm text-slate-900 dark:text-slate-100">{{ ptw.closed_by_name || ptw.closed_by || '-' }}</p>
            </div>

            <div>
              <p class="text-sm font-medium text-slate-500 dark:text-slate-400">Closing Date</p>
              <p class="text-sm text-slate-900 dark:text-slate-100">{{ formatDate(ptw.closed_at) }}</p>
            </div>
          </div>
        </div>

        <!-- Created At -->
        <div class="pt-4 border-t border-slate-200 dark:border-slate-700">
          <p class="text-xs text-slate-500 dark:text-slate-400">Created at: {{ formatDate(ptw.created_at) }}</p>
        </div>
      </div>

      <div class="flex justify-between pt-4">
        <Button
          v-if="ptw && (ptw.status === 'APPROVED' || ptw.status === 'CLOSED')"
          @click="openPrintPreview"
          class="bg-[var(--color-saipem-tertiary)] hover:bg-[var(--color-saipem-tertiary)]/90"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect width="12" height="8" x="6" y="14"/></svg>
          Print Permit
        </Button>
        <div v-else></div>
        <Button variant="outline" @click="isOpen = false">
          Close
        </Button>
      </div>
    </DialogContent>
  </Dialog>
</template>
