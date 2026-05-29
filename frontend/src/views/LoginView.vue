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

    // Redirect based on user role
    if (userData.role === 'Admin') {
        router.push('/');
    } else if (userData.role === 'Worker') {
        router.push('/hse');
    } else if (userData.role === 'Safety Officer') {
        router.push('/hse');
    } else {
        router.push('/hse');
    }
};
</script>
