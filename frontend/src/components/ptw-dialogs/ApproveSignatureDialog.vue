<script setup lang="ts">
import { ref, watch, onMounted, nextTick } from 'vue'
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
  'approve': [signature: string]
}>()

const isOpen = ref(props.open)
const canvas = ref<HTMLCanvasElement | null>(null)
const isDrawing = ref(false)
const hasSignature = ref(false)
const isSubmitting = ref(false)

let ctx: CanvasRenderingContext2D | null = null

watch(() => props.open, (newVal) => {
  isOpen.value = newVal
  if (newVal) {
    nextTick(() => {
      initCanvas()
    })
  }
})

watch(isOpen, (newVal) => {
  if (!newVal) {
    clearSignature()
  }
  emit('update:open', newVal)
})

const initCanvas = () => {
  if (!canvas.value) return

  ctx = canvas.value.getContext('2d')
  if (!ctx) return

  // Set canvas size
  canvas.value.width = canvas.value.offsetWidth
  canvas.value.height = 200

  // Set drawing style
  ctx.strokeStyle = '#000000'
  ctx.lineWidth = 2
  ctx.lineCap = 'round'
  ctx.lineJoin = 'round'
}

const startDrawing = (e: MouseEvent | TouchEvent) => {
  if (!ctx || !canvas.value) return

  isDrawing.value = true
  hasSignature.value = true

  const rect = canvas.value.getBoundingClientRect()
  const x = 'touches' in e ? e.touches[0].clientX - rect.left : e.clientX - rect.left
  const y = 'touches' in e ? e.touches[0].clientY - rect.top : e.clientY - rect.top

  ctx.beginPath()
  ctx.moveTo(x, y)
}

const draw = (e: MouseEvent | TouchEvent) => {
  if (!isDrawing.value || !ctx || !canvas.value) return

  const rect = canvas.value.getBoundingClientRect()
  const x = 'touches' in e ? e.touches[0].clientX - rect.left : e.clientX - rect.left
  const y = 'touches' in e ? e.touches[0].clientY - rect.top : e.clientY - rect.top

  ctx.lineTo(x, y)
  ctx.stroke()
}

const stopDrawing = () => {
  if (!ctx) return
  isDrawing.value = false
  ctx.closePath()
}

const clearSignature = () => {
  if (!ctx || !canvas.value) return
  ctx.clearRect(0, 0, canvas.value.width, canvas.value.height)
  hasSignature.value = false
}

const handleApprove = async () => {
  if (!hasSignature.value) {
    toast.error('Signature Required', {
      description: 'Please sign before approving.'
    })
    return
  }

  if (!canvas.value) return

  isSubmitting.value = true

  try {
    // Convert canvas to base64 image
    const signatureData = canvas.value.toDataURL('image/png')

    emit('approve', signatureData)
    isOpen.value = false
  } catch (error) {
    toast.error('Error', {
      description: 'Failed to process signature.'
    })
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  if (isOpen.value) {
    nextTick(() => {
      initCanvas()
    })
  }
})
</script>

<template>
  <Dialog v-model:open="isOpen">
    <DialogContent class="max-w-lg">
      <DialogHeader>
        <DialogTitle>Approve Permit To Work</DialogTitle>
        <DialogDescription>
          Sign to approve PTW {{ permitId }}
        </DialogDescription>
      </DialogHeader>

      <div class="space-y-4">
        <div class="space-y-2">
          <label class="text-sm font-medium text-slate-700 dark:text-slate-300">
            Digital Signature <span class="text-red-500">*</span>
          </label>
          <div class="border-2 border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-800">
            <canvas
              ref="canvas"
              class="w-full cursor-crosshair touch-none"
              @mousedown="startDrawing"
              @mousemove="draw"
              @mouseup="stopDrawing"
              @mouseleave="stopDrawing"
              @touchstart.prevent="startDrawing"
              @touchmove.prevent="draw"
              @touchend.prevent="stopDrawing"
            />
          </div>
          <p class="text-xs text-slate-500 dark:text-slate-400">
            Sign in the area above using mouse or touchscreen
          </p>
        </div>

        <Button
          variant="outline"
          size="sm"
          @click="clearSignature"
          class="w-full"
        >
          Clear Signature
        </Button>
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
          @click="handleApprove"
          :disabled="!hasSignature || isSubmitting"
          class="bg-green-500 hover:bg-green-600 text-white"
        >
          <svg v-if="isSubmitting" class="animate-spin h-4 w-4 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ isSubmitting ? 'Processing...' : 'Approve' }}
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
