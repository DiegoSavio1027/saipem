<template>
  <Dialog :open="open" @update:open="$emit('update:open', $event)">
    <DialogContent class="sm:max-w-[500px]">
      <DialogHeader>
        <DialogTitle>Toolbox Talk Checklist</DialogTitle>
        <DialogDescription>
          Please complete the pre-job safety checklist before starting the work for Permit ID: {{ permitId }}.
        </DialogDescription>
      </DialogHeader>

      <div class="space-y-4 py-4">
        <div class="flex items-start space-x-3">
          <Checkbox id="hazard" v-model:checked="checklist.hazard" />
          <Label for="hazard" class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
            All hazards have been identified and discussed with the team.
          </Label>
        </div>
        <div class="flex items-start space-x-3">
          <Checkbox id="ppe" v-model:checked="checklist.ppe" />
          <Label for="ppe" class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
            Appropriate PPE is available and being worn by all team members.
          </Label>
        </div>
        <div class="flex items-start space-x-3">
          <Checkbox id="emergency" v-model:checked="checklist.emergency" />
          <Label for="emergency" class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
            Emergency procedures and assembly points have been communicated.
          </Label>
        </div>
        <div class="flex items-start space-x-3">
          <Checkbox id="tools" v-model:checked="checklist.tools" />
          <Label for="tools" class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
            All tools and equipment have been inspected and are safe to use.
          </Label>
        </div>
      </div>

      <DialogFooter>
        <Button type="button" variant="outline" @click="$emit('update:open', false)">
          Cancel
        </Button>
        <Button type="button" :disabled="!allChecked" @click="handleConfirm">
          Confirm & Start Work
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';

const props = defineProps({
  open: Boolean,
  permitId: String,
  ptwId: Number
});

const emit = defineEmits(['update:open', 'confirm']);

const checklist = ref({
  hazard: false,
  ppe: false,
  emergency: false,
  tools: false
});

const allChecked = computed(() => {
  return checklist.value.hazard && checklist.value.ppe && checklist.value.emergency && checklist.value.tools;
});

watch(() => props.open, (isOpen) => {
  if (isOpen) {
    checklist.value = {
      hazard: false,
      ppe: false,
      emergency: false,
      tools: false
    };
  }
});

const handleConfirm = () => {
  emit('confirm', props.ptwId);
  emit('update:open', false);
};
</script>
