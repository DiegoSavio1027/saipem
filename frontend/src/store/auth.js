import { reactive } from 'vue';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';

export const authState = reactive({
    isLoggedIn: false,
    isAuthChecking: true,
    username: '',
    userRole: '',
    empId: '',
    accessibleModules: [],
    assignedVessel: null,  // { asset_id: '', name: '' }
    selectedVessel: null   // For Admin: currently selected vessel
});

// JWT Token Management
export const getAccessToken = () => localStorage.getItem('access_token');
export const getRefreshToken = () => localStorage.getItem('refresh_token');

export const setTokens = (accessToken, refreshToken) => {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
};

export const clearTokens = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_data');
};

// Check authentication using JWT
export const checkAuth = async () => {
    authState.isAuthChecking = true;
    const token = getAccessToken();

    console.log('[AUTH] Checking authentication...', { hasToken: !!token });

    if (!token) {
        console.log('[AUTH] No token found, user not authenticated');
        authState.isLoggedIn = false;
        authState.isAuthChecking = false;
        return false;
    }

    try {
        console.log('[AUTH] Verifying token with backend...');
        const response = await fetch(`${API_BASE_URL}/auth/me/`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        console.log('[AUTH] Backend response:', { status: response.status, ok: response.ok });

        if (response.ok) {
            const data = await response.json();
            console.log('[AUTH] Token valid, user authenticated:', data.username);
            authState.username = data.username;
            authState.userRole = data.role;
            authState.empId = data.username;
            authState.accessibleModules = data.accessible_modules || [];
            authState.assignedVessel = data.assigned_vessel || null;

            // For Admin, initialize selectedVessel from localStorage or default to null
            if (data.role === 'Admin') {
                const savedVessel = localStorage.getItem('hse-selected-vessel');
                authState.selectedVessel = savedVessel ? JSON.parse(savedVessel) : null;
            } else {
                // Non-Admin: selectedVessel = assignedVessel
                authState.selectedVessel = authState.assignedVessel;
            }

            authState.isLoggedIn = true;

            // Store user data
            localStorage.setItem('user_data', JSON.stringify(data));
            return true;
        } else {
            // Token invalid or expired
            const errorText = await response.text();
            console.error('[AUTH] Token verification failed:', { status: response.status, error: errorText });
            clearTokens();
            authState.isLoggedIn = false;
            return false;
        }
    } catch (err) {
        console.error("[AUTH] Auth check failed with error:", err);
        authState.isLoggedIn = false;
        return false;
    } finally {
        authState.isAuthChecking = false;
    }
};

// Set auth data from login response
export const setAuthData = (data) => {
    authState.username = data.username;
    authState.userRole = data.role;
    authState.empId = data.username;
    authState.accessibleModules = data.accessible_modules || [];
    authState.assignedVessel = data.assigned_vessel || null;

    // For Admin, initialize selectedVessel from localStorage or default to null
    if (data.role === 'Admin') {
        const savedVessel = localStorage.getItem('hse-selected-vessel');
        authState.selectedVessel = savedVessel ? JSON.parse(savedVessel) : null;
    } else {
        // Non-Admin: selectedVessel = assignedVessel
        authState.selectedVessel = authState.assignedVessel;
    }

    authState.isLoggedIn = true;

    // Store user data
    localStorage.setItem('user_data', JSON.stringify(data));
};

// Set selected vessel (Admin only)
export const setSelectedVessel = (vessel) => {
    authState.selectedVessel = vessel;
    if (authState.userRole === 'Admin') {
        localStorage.setItem('hse-selected-vessel', JSON.stringify(vessel));
    }
};

// Logout
export const logout = () => {
    clearTokens();
    authState.isLoggedIn = false;
    authState.username = '';
    authState.userRole = '';
    authState.empId = '';
    authState.accessibleModules = [];
    authState.assignedVessel = null;
    authState.selectedVessel = null;
};
