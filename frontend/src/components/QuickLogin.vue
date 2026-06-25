<template>
    <div v-if="isDevelopment && showQuickLogin" class="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-md">
        <p class="text-[13px] font-medium text-blue-900 mb-3">Quick Login (Development Only)</p>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
            <Button
                v-for="account in accounts"
                :key="account.id"
                type="button"
                @click="quickLogin(account)"
                :disabled="isLoading"
                class="h-auto py-2 text-[11px] bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors flex flex-col items-center justify-center text-center"
            >
                <span class="font-bold">{{ account.role }}</span>
                <span class="text-[9px] opacity-80 font-normal mt-0.5">{{ account.description }}</span>
            </Button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Button } from '@/components/ui/button';

const props = defineProps({
    onQuickLogin: Function
});

const isDevelopment = ref(false);
const showQuickLogin = ref(false);
const accounts = ref([]);
const isLoading = ref(false);

const DEV_ENDPOINT = import.meta.env.VITE_DEV_QUICK_LOGIN_ENDPOINT || 'http://localhost:8989/api/v1/auth/dev/quick-login-accounts/';

onMounted(async () => {
    isDevelopment.value = import.meta.env.VITE_NODE_ENV === 'development';

    if (isDevelopment.value) {
        try {
            const response = await fetch(DEV_ENDPOINT);
            if (response.ok) {
                const data = await response.json();
                accounts.value = Object.entries(data.accounts).map(([key, account]) => ({
                    id: key,
                    ...account
                }));
                showQuickLogin.value = true;
            }
        } catch (err) {
            console.log('Dev quick login not available');
        }
    }
});

const quickLogin = (account) => {
    if (props.onQuickLogin) {
        props.onQuickLogin({
            username: account.username,
            password: account.password
        });
    }
};
</script>
