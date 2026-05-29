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

interface Props {
  open: boolean
  permitId: string
  permitType?: string
  itemType?: string
}

const props = withDefaults(defineProps<Props>(), {
  permitType: 'Permit to Work',
  itemType: 'Permit'
})

const emit = defineEmits<{
  'update:open': [value: boolean]
  'confirm': []
}>()

const isOpen = ref(props.open)
const isDeleting = ref(false)

watch(() => props.open, (newVal) => {
  isOpen.value = newVal
})

watch(isOpen, (newVal) => {
  emit('update:open', newVal)
})

const handleConfirm = async () => {
  isDeleting.value = true
  emit('confirm')
  // Dialog will close after deletion is handled
}

const handleCancel = () => {
  isOpen.value = false
}
</script>

<template>
  <Dialog v-model:open="isOpen">
    <DialogContent class="max-w-md">
      <DialogHeader>
        <DialogTitle>Delete {{ itemType }}</DialogTitle>
        <DialogDescription>
          Are you sure you want to delete this {{ itemType.toLowerCase() }}?
        </DialogDescription>
      </DialogHeader>

      <div class="space-y-4 py-4">
        <div class="bg-red-50 border border-red-200 rounded-lg p-4">
          <p class="text-sm text-red-800">
            <strong>Warning:</strong> This action cannot be undone. The {{ itemType.toLowerCase() }} <strong>{{ permitId }}</strong> will be permanently deleted.
          </p>
        </div>

        <div class="text-sm text-slate-600">
          <p><strong>{{ itemType }} Type:</strong> {{ permitType }}</p>
          <p><strong>{{ itemType }} ID:</strong> {{ permitId }}</p>
        </div>
      </div>

      <DialogFooter class="gap-2">
        <Button
          variant="outline"
          @click="handleCancel"
          :disabled="isDeleting"
        >
          Cancel
        </Button>
        <Button
          variant="destructive"
          @click="handleConfirm"
          :disabled="isDeleting"
        >
          <span v-if="isDeleting" class="inline-block animate-spin mr-2">⏳</span>
          {{ isDeleting ? 'Deleting...' : `Delete ${itemType}` }}
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
