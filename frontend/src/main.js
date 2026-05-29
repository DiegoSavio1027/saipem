import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { initializeTheme } from './store/theme'
import { checkAuth } from './store/auth'

const app = createApp(App)

// Initialize theme before mounting
initializeTheme()

// Setup global fetch wrapper FIRST (before checkAuth)
const originalFetch = window.fetch;
window.fetch = function(...args) {
    const [resource, config] = args;
    const token = localStorage.getItem('access_token');

    // Add token to ALL requests (not just /api/)
    if (token && typeof resource === 'string' && (resource.includes('localhost:8989') || resource.startsWith('/'))) {
        const headers = {
            ...((config && config.headers) || {}),
            'Authorization': `Bearer ${token}`
        };

        return originalFetch(resource, { ...config, headers }).then(response => {
            // Handle 401 Unauthorized - redirect to login
            if (response.status === 401) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/login';
            }
            return response;
        });
    }

    return originalFetch(...args);
};

// Initialize auth state before mounting (check if user has valid token)
checkAuth()

app.use(router)
app.mount('#app')
