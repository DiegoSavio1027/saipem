<script setup>
import { DropdownMenuContent } from "reka-ui";
import { cn } from "@/lib/utils";

const props = defineProps({
  align: { type: String, required: false, default: "start" },
  alignOffset: { type: Number, required: false, default: 0 },
  avoidCollisions: { type: Boolean, required: false, default: true },
  collisionPadding: { type: Number, required: false, default: 8 },
  loop: { type: Boolean, required: false, default: false },
  side: { type: String, required: false, default: "bottom" },
  sideOffset: { type: Number, required: false, default: 4 },
  class: {
    type: [Boolean, null, String, Object, Array],
    required: false,
    skipCheck: true,
  },
});
</script>

<template>
  <DropdownMenuContent
    data-slot="dropdown-menu-content"
    :align="align"
    :align-offset="alignOffset"
    :avoid-collisions="avoidCollisions"
    :collision-padding="collisionPadding"
    :loop="loop"
    :side="side"
    :side-offset="sideOffset"
    :class="cn(
      'z-50 min-w-[8rem] overflow-hidden rounded-md border border-slate-200 bg-white p-1 text-slate-950 shadow-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-50',
      props.class
    )"
  >
    <slot />
  </DropdownMenuContent>
</template>
