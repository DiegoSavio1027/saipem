<script setup>
import { cn } from "@/lib/utils";

const props = defineProps({
  class: {
    type: [Boolean, null, String, Object, Array],
    required: false,
    skipCheck: true,
  },
});
</script>

<template>
  <tr
    data-slot="table-row"
    :class="
      cn(
        'hover:bg-muted/50 dark:hover:bg-slate-700 data-[state=selected]:bg-muted dark:data-[state=selected]:bg-slate-700 border-b dark:border-slate-700 transition-colors',
        props.class,
      )
    "
  >
    <slot />
  </tr>
</template>
