import { ref } from 'vue';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';

export const vessels = ref([]);

export const fetchVessels = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/offshore/vessels/`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });
        if (response.ok) {
            vessels.value = await response.json();
        }
    } catch (error) {
        console.error('Failed to fetch vessels:', error);
    }
};
