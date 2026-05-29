<script setup>
import { DropdownMenuRoot } from "reka-ui";

const props = defineProps({
  open: { type: Boolean, required: false },
  defaultOpen: { type: Boolean, required: false },
  modal: { type: Boolean, required: false, default: true },
});

const emit = defineEmits(['update:open']);
</script>

<template>
  <DropdownMenuRoot
    v-bind="props"
    @update:open="emit('update:open', $event)"
  >
    <slot />
  </DropdownMenuRoot>
</template>
