<template>
  <Login @login-success="onLoginSuccess" />
</template>

<script setup>
import { useRouter } from 'vue-router';
import Login from '@/components/Login.vue';
import { setAuthData } from '@/store/auth';

const router = useRouter();

const onLoginSuccess = (userData) => {
    setAuthData(userData);

    // Redirect based on role or accessible modules
    if (userData.role === 'Admin') {
        router.push('/');
    } else if (userData.accessible_modules && userData.accessible_modules.includes('hr')) {
        router.push('/hr');
    } else if (userData.accessible_modules && userData.accessible_modules.includes('asset')) {
        router.push('/assets');
    } else {
        router.push('/hse');
    }
};
</script>
