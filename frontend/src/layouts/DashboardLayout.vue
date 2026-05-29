<template>
  <div class="flex h-screen w-full bg-background overflow-hidden text-foreground font-sans">
    
    <Sidebar :isCollapsed="isCollapsed" />
    
    <div class="flex flex-col flex-1 w-full h-full overflow-hidden relative">

      <Topbar :isConnected="websocketState.isConnected" :isCollapsed="isCollapsed" @toggle-sidebar="isCollapsed = !isCollapsed" @open-modal="$emit('openModal')" />
      <MobileHeader :isConnected="websocketState.isConnected" />

      <main class="flex-1 overflow-y-auto p-4 md:p-8">
        <slot />
        <Footer />
      </main>

      <MobileBottomNav @open-modal="$emit('openModal')" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import Sidebar from '@/components/layout/Sidebar.vue';
import Topbar from '@/components/layout/Topbar.vue';
import MobileHeader from '@/components/layout/MobileHeader.vue';
import MobileBottomNav from '@/components/layout/MobileBottomNav.vue';
import Footer from '@/components/layout/Footer.vue';
import { websocketState, initializeWebSocket, closeWebSocket } from '@/store/websocket';

defineEmits(['openModal']);

const isCollapsed = ref(false);

onMounted(() => {
  initializeWebSocket();
});

onUnmounted(() => {
  closeWebSocket();
});
</script>
