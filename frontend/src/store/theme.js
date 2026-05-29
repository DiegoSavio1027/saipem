import { reactive } from 'vue';

export const themeState = reactive({
    isDark: false
});

export const initializeTheme = () => {
    // Check localStorage first
    const savedTheme = localStorage.getItem('hse-theme-preference');

    if (savedTheme) {
        themeState.isDark = savedTheme === 'dark';
    } else {
        // Check system preference
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        themeState.isDark = prefersDark;
    }

    applyTheme();

    // Listen for system preference changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('hse-theme-preference')) {
            themeState.isDark = e.matches;
            applyTheme();
        }
    });
};

export const toggleTheme = () => {
    themeState.isDark = !themeState.isDark;
    localStorage.setItem('hse-theme-preference', themeState.isDark ? 'dark' : 'light');
    applyTheme();
};

export const setTheme = (isDark) => {
    themeState.isDark = isDark;
    localStorage.setItem('hse-theme-preference', isDark ? 'dark' : 'light');
    applyTheme();
};

const applyTheme = () => {
    const html = document.documentElement;
    if (themeState.isDark) {
        html.classList.add('dark');
    } else {
        html.classList.remove('dark');
    }
};
