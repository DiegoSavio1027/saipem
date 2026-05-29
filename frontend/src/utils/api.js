import { getAccessToken } from '@/store/auth';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';

/**
 * Fetch wrapper that automatically adds JWT token to requests
 * @param {string} endpoint - API endpoint (e.g., '/api/incidents/')
 * @param {object} options - Fetch options
 * @returns {Promise<Response>}
 */
export const apiFetch = async (endpoint, options = {}) => {
    const token = getAccessToken();
    const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}${endpoint}`;

    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    // Add JWT token if available
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(url, {
        ...options,
        headers
    });

    // Handle 401 Unauthorized (token expired)
    if (response.status === 401) {
        // Clear tokens and redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
    }

    return response;
};

/**
 * GET request with JWT token
 */
export const apiGet = (endpoint, options = {}) => {
    return apiFetch(endpoint, {
        method: 'GET',
        ...options
    });
};

/**
 * POST request with JWT token
 */
export const apiPost = (endpoint, data, options = {}) => {
    return apiFetch(endpoint, {
        method: 'POST',
        body: JSON.stringify(data),
        ...options
    });
};

/**
 * PUT request with JWT token
 */
export const apiPut = (endpoint, data, options = {}) => {
    return apiFetch(endpoint, {
        method: 'PUT',
        body: JSON.stringify(data),
        ...options
    });
};

/**
 * PATCH request with JWT token
 */
export const apiPatch = (endpoint, data, options = {}) => {
    return apiFetch(endpoint, {
        method: 'PATCH',
        body: JSON.stringify(data),
        ...options
    });
};

/**
 * DELETE request with JWT token
 */
export const apiDelete = (endpoint, options = {}) => {
    return apiFetch(endpoint, {
        method: 'DELETE',
        ...options
    });
};
