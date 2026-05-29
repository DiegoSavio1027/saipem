<script setup>
import { DropdownMenuTrigger } from "reka-ui";

const props = defineProps({
  asChild: { type: Boolean, required: false },
  as: { type: null, required: false },
  disabled: { type: Boolean, required: false },
});
</script>

<template>
  <DropdownMenuTrigger data-slot="dropdown-menu-trigger" v-bind="props">
    <slot />
  </DropdownMenuTrigger>
</template>
