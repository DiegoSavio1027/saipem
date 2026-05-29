<script setup lang="ts">
import { ref, watch } from 'vue'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { toast } from 'vue-sonner'

const props = defineProps<{
  open: boolean
  permitId: string
  ptwId: number
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'markDone': [notes?: string]
}>()

const isOpen = ref(props.open)
const completionNotes = ref('')
const isSubmitting = ref(false)

watch(() => props.open, (newVal) => {
  isOpen.value = newVal
  if (!newVal) {
    completionNotes.value = ''
  }
})

watch(isOpen, (newVal) => {
  emit('update:open', newVal)
})

const handleMarkDone = async () => {
  isSubmitting.value = true

  try {
    emit('markDone', completionNotes.value || undefined)
    isOpen.value = false
  } catch (error) {
    toast.error('Error', {
      description: 'Failed to mark work as done.'
    })
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <Dialog v-model:open="isOpen">
    <DialogContent class="max-w-lg">
      <DialogHeader>
        <DialogTitle>Mark as Job Done</DialogTitle>
        <DialogDescription>
          Mark PTW {{ permitId }} as job done
        </DialogDescription>
      </DialogHeader>

      <div class="space-y-4">
        <div class="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-700 rounded-lg p-4">
          <p class="text-sm text-amber-900 dark:text-amber-200">
            You will mark this work as done. Make sure all work has been completed as planned.
          </p>
        </div>

        <div class="space-y-2">
          <label class="text-sm font-medium text-slate-700 dark:text-slate-300">
            Completion Notes (Optional)
          </label>
          <textarea
            v-model="completionNotes"
            placeholder="Add notes about work completion..."
            rows="3"
            class="w-full px-3 py-2 rounded-md border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent transition-shadow text-sm resize-none"
          />
        </div>
      </div>

      <DialogFooter>
        <Button
          variant="outline"
          @click="isOpen = false"
          :disabled="isSubmitting"
        >
          Cancel
        </Button>
        <Button
          @click="handleMarkDone"
          :disabled="isSubmitting"
          class="bg-amber-500 hover:bg-amber-600 text-white"
        >
          <svg v-if="isSubmitting" class="animate-spin h-4 w-4 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ isSubmitting ? 'Processing...' : 'Mark as Done' }}
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
