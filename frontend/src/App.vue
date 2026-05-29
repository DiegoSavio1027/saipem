<template>
  <div class="min-h-screen bg-background">
      <div v-if="authState.isAuthChecking" class="min-h-screen flex items-center justify-center bg-background">
          <p class="text-[18px] text-muted-foreground animate-pulse font-sans font-semibold">Memeriksa sesi...</p>
      </div>
      <router-view v-else />
      <Toaster richColors position="top-right" :closeButton="true" :duration="2500" :theme="themeState.isDark ? 'dark' : 'light'" />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { authState } from '@/store/auth';
import { initializeWebSocket } from '@/store/websocket';
import { initializeAudio } from '@/utils/notifications';
import { themeState } from '@/store/theme';
import { Toaster } from '@/components/ui/sonner';
import 'vue-sonner/style.css';

onMounted(() => {
    // Initialize WebSocket globally when app starts
    if (authState.isLoggedIn) {
        initializeWebSocket();
    }

    // Initialize audio on first user interaction
    const initAudioOnInteraction = async () => {
        await initializeAudio();
        // Remove listeners after first interaction
        document.removeEventListener('click', initAudioOnInteraction);
        document.removeEventListener('touchstart', initAudioOnInteraction);
        document.removeEventListener('keydown', initAudioOnInteraction);
    };

    document.addEventListener('click', initAudioOnInteraction);
    document.addEventListener('touchstart', initAudioOnInteraction);
    document.addEventListener('keydown', initAudioOnInteraction);
});
</script>
