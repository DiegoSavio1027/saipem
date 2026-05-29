<template>
    <div class="min-h-screen flex items-center justify-center p-4 bg-slate-50 dark:bg-slate-900">
        <Card class="w-full max-w-md bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm rounded-md animate-in fade-in zoom-in-95 duration-300">
            <CardHeader class="text-center pb-8 pt-8">
                <img :src="currentLogo" alt="Saipem Logo" class="h-[80px] w-auto object-contain mx-auto mb-6" />
            </CardHeader>
            <CardContent class="p-8 pt-0">
                <QuickLogin :onQuickLogin="handleQuickLogin" />

                <div v-if="error" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700 text-red-600 dark:text-red-400 p-4 rounded-md mb-6 text-[14px] text-center font-medium">
                    {{ error }}
                </div>
        
                <form @submit.prevent="handleLogin" class="space-y-6">
                    <div class="space-y-2">
                        <Label for="username" class="text-[14px] font-medium text-slate-700 dark:text-slate-300">Username</Label>
                        <Input id="username" v-model="username" type="text" required class="h-[48px] bg-white dark:bg-slate-700 border-slate-300 dark:border-slate-600 text-slate-900 dark:text-slate-100 rounded-md placeholder:text-slate-400 dark:placeholder:text-slate-500 focus-visible:ring-[var(--color-saipem-tertiary)] focus-visible:border-[var(--color-saipem-tertiary)] text-[15px]" />
                    </div>
                    
                    <div class="space-y-2">
                        <Label for="password" class="text-[14px] font-medium text-slate-700 dark:text-slate-300">Password</Label>
                        <Input id="password" v-model="password" type="password" required class="h-[48px] bg-white dark:bg-slate-700 border-slate-300 dark:border-slate-600 text-slate-900 dark:text-slate-100 rounded-md placeholder:text-slate-400 dark:placeholder:text-slate-500 focus-visible:ring-[var(--color-saipem-tertiary)] focus-visible:border-[var(--color-saipem-tertiary)] text-[15px]" />
                    </div>
                    
                    <Button type="submit" :disabled="isLoading" class="w-full h-[52px] rounded-md bg-[var(--color-saipem-tertiary)] hover:bg-[var(--color-saipem-tertiary)]/90 text-white font-semibold text-[16px] mt-6 shadow-sm transition-colors">
                        {{ isLoading ? 'Authenticating...' : 'Login' }}
                    </Button>
                </form>
            </CardContent>
        </Card>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import logoDark from '@/assets/text-side-dark.png';
import logoLight from '@/assets/text-side-light.png';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import QuickLogin from '@/components/QuickLogin.vue';
import { toast } from 'vue-sonner';
import { themeState } from '@/store/theme';
import { setTokens, setAuthData } from '@/store/auth';

const emit = defineEmits(['login-success']);
const router = useRouter();

const username = ref('');
const password = ref('');
const isLoading = ref(false);
const error = ref('');

const currentLogo = computed(() => {
    return themeState.isDark ? logoLight : logoDark;
});

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';

const handleLogin = async () => {
    isLoading.value = true;
    error.value = '';

    try {
        const payload = {
            username: username.value,
            password: password.value
        };

        const response = await fetch(`${API_BASE_URL}/auth/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const responseData = await response.json();

        if (response.ok) {
            // Store JWT tokens
            setTokens(responseData.access, responseData.refresh);

            // Set auth data in store (fixes token persistence on refresh)
            setAuthData(responseData.user);

            toast.success("Login Successful", { description: `Welcome, ${responseData.user.first_name || username.value}!` });
            emit('login-success', responseData.user);

            // Redirect berdasarkan accessible_modules
            const modules = responseData.user.accessible_modules || [];

            // Admin dengan multiple modules - redirect ke dashboard untuk pilih module
            if (modules.length > 1) {
                router.push('/');
            } else if (modules.includes('hr')) {
                // Redirect ke HR module (sudah di Vue)
                router.push('/hr/personnel');
            } else if (modules.includes('asset')) {
                // Redirect ke Asset module (sudah di Vue)
                router.push('/assets');
            } else if (modules.includes('hse')) {
                // Redirect ke HSE dashboard
                router.push('/');
            } else {
                // Default ke HSE dashboard
                router.push('/');
            }
        } else {
            error.value = responseData.error || 'Invalid username or password.';
            toast.error("Login Failed", { description: error.value });
        }
    } catch (err) {
        error.value = 'Failed to connect to server.';
        toast.error("Error", { description: "Server error occurred." });
    } finally {
        isLoading.value = false;
    }
};

const handleQuickLogin = (credentials) => {
    username.value = credentials.username;
    password.value = credentials.password;
    // Auto-submit after a short delay to show the filled values
    setTimeout(() => {
        handleLogin();
    }, 300);
};
</script>
