<template>
    <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-50 dark:bg-slate-900 animate-in fade-in duration-300">
        <Card class="w-full max-w-md bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm rounded-md animate-in fade-in zoom-in-95 duration-300">
            <CardHeader class="text-center pb-6 pt-8">
                <img :src="currentLogo" alt="Saipem Logo" class="h-[60px] w-auto object-contain mx-auto mb-6 opacity-80" />
                
                <div class="flex justify-center mb-4">
                    <div class="flex items-center justify-center w-16 h-16 rounded-full bg-slate-100 dark:bg-slate-700/50">
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-slate-500 dark:text-slate-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                        </svg>
                    </div>
                </div>

                <CardTitle class="text-2xl font-semibold text-slate-900 dark:text-white">Access Restricted</CardTitle>
                <CardDescription class="text-slate-500 dark:text-slate-400 mt-2">
                    Your account is currently Off-Roster or Available.
                </CardDescription>
            </CardHeader>
            <CardContent class="p-8 pt-0 space-y-6">
                
                <div class="bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-md p-4 space-y-3">
                    <div class="flex justify-between items-center text-[14px]">
                        <span class="text-slate-500 dark:text-slate-400 font-medium">Employee ID</span>
                        <span class="font-semibold text-slate-900 dark:text-slate-200">{{ authState.empId }}</span>
                    </div>
                    <div class="flex justify-between items-center text-[14px]">
                        <span class="text-slate-500 dark:text-slate-400 font-medium">Role</span>
                        <span class="font-medium text-slate-900 dark:text-slate-200">{{ authState.userRole }}</span>
                    </div>
                    <div class="flex justify-between items-center text-[14px] pt-3 border-t border-slate-200 dark:border-slate-700">
                        <span class="text-slate-500 dark:text-slate-400 font-medium">Vessel</span>
                        <span class="text-slate-400 dark:text-slate-500 font-medium italic">Unassigned</span>
                    </div>
                </div>

                <p class="text-[14px] text-center text-slate-600 dark:text-slate-400">
                    You must be assigned to an active vessel roster to access the operational dashboard. Please contact HR for scheduling.
                </p>

                <Button @click="handleLogout" variant="outline" class="w-full h-[48px] border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700">
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                        <polyline points="16 17 21 12 16 7"></polyline>
                        <line x1="21" y1="12" x2="9" y2="12"></line>
                    </svg>
                    Sign Out
                </Button>
            </CardContent>
        </Card>
    </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { authState, logout } from '@/store/auth';
import { themeState } from '@/store/theme';
import logoDark from '@/assets/text-side-dark.png';
import logoLight from '@/assets/text-side-light.png';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

const router = useRouter();

const currentLogo = computed(() => {
    return themeState.isDark ? logoLight : logoDark;
});

const handleLogout = () => {
    logout();
    router.push('/login');
};
</script>
