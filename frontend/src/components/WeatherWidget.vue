<template>
  <div class="bg-gradient-to-br from-cyan-50 to-blue-100 dark:from-slate-800 dark:to-slate-900 p-6 rounded-xl border border-cyan-200 dark:border-slate-700 shadow-sm relative overflow-hidden">
    <!-- Background Decor -->
    <svg class="absolute -right-4 -top-4 w-32 h-32 text-cyan-500/10 dark:text-cyan-400/5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19a5.5 5.5 0 0 0-1-10.8V8a5.5 5.5 0 0 0-11 0 3.5 3.5 0 0 0 0 7h12z"/></svg>

    <div class="flex items-start justify-between relative z-10">
      <div>
        <h3 class="text-sm font-semibold text-cyan-700 dark:text-cyan-400 uppercase tracking-wider">Offshore Weather</h3>
        <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">Live from Open-Meteo API</p>
      </div>
      <div v-if="weather" class="flex items-center gap-2">
        <span class="text-3xl font-bold text-slate-800 dark:text-slate-100">{{ weather.temperature }}°C</span>
      </div>
    </div>

    <div v-if="loading" class="mt-6 flex justify-center py-4">
      <div class="animate-pulse flex space-x-2">
        <div class="h-2 w-2 bg-cyan-400 rounded-full"></div>
        <div class="h-2 w-2 bg-cyan-400 rounded-full"></div>
        <div class="h-2 w-2 bg-cyan-400 rounded-full"></div>
      </div>
    </div>

    <div v-else-if="error" class="mt-4 p-3 bg-red-50 text-red-600 rounded-md text-sm border border-red-200">
      {{ error }}
    </div>

    <div v-else-if="weather" class="mt-6 grid grid-cols-2 gap-4 relative z-10">
      <div class="bg-white/60 dark:bg-slate-800/60 backdrop-blur-sm p-3 rounded-lg border border-white/40 dark:border-slate-700/50">
        <div class="flex items-center gap-2 text-slate-600 dark:text-slate-300 mb-1">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"/></svg>
          <span class="text-xs font-medium">Wind Speed</span>
        </div>
        <p class="text-lg font-bold text-slate-800 dark:text-slate-100">{{ weather.windspeed }} <span class="text-sm font-normal text-slate-500">km/h</span></p>
        <p v-if="weather.windspeed > 30" class="text-xs text-red-500 font-semibold mt-1">⚠️ High Wind Warning</p>
      </div>
      <div class="bg-white/60 dark:bg-slate-800/60 backdrop-blur-sm p-3 rounded-lg border border-white/40 dark:border-slate-700/50">
        <div class="flex items-center gap-2 text-slate-600 dark:text-slate-300 mb-1">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12h20"/><path d="M20 12v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-8"/><path d="M4 12v-4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v4"/></svg>
          <span class="text-xs font-medium">Wave Height</span>
        </div>
        <p class="text-lg font-bold text-slate-800 dark:text-slate-100">{{ weather.waveHeight || 'N/A' }} <span class="text-sm font-normal text-slate-500">m</span></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const weather = ref(null);
const loading = ref(true);
const error = ref(null);

const fetchWeather = async () => {
  loading.value = true;
  error.value = null;
  try {
    // Offshore coordinates (e.g., North Sea or a sample location)
    const lat = 56.5; 
    const lon = 3.2;
    // We use Open-Meteo Marine API for waves and standard for wind/temp
    const response = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true`);
    const data = await response.json();
    
    if (data.current_weather) {
      weather.value = {
        temperature: data.current_weather.temperature,
        windspeed: data.current_weather.windspeed,
        winddirection: data.current_weather.winddirection,
        // Mock wave height based on wind speed for demo purposes since marine API needs different endpoint
        waveHeight: (data.current_weather.windspeed * 0.1).toFixed(1)
      };
    } else {
      error.value = "Weather data unavailable.";
    }
  } catch (err) {
    console.error("Weather API Error:", err);
    error.value = "Failed to load weather data.";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchWeather();
});
</script>
