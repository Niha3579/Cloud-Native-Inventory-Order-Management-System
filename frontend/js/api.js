// js/api.js
// Dynamically set the base URL to whatever host FastAPI is running on
const API_BASE_URL = window.location.origin; 

const api = {
    async fetch(endpoint, options = {}) {
        const token = localStorage.getItem('authToken');
        
        // Default headers
        const headers = {
            ...options.headers
        };

        // Add JSON content type if it's not a FormData object (like for file uploads or FastAPI OAuth2 forms)
        if (!(options.body instanceof FormData)) {
            headers['Content-Type'] = 'application/json';
        }

        // Attach Bearer token if it exists
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                ...options,
                headers
            });
            
            if (!response.ok) {
                // Try to parse FastAPI's detailed error validation message
                const errorData = await response.json().catch(() => ({}));
                const errorMessage = errorData.detail || `API Error: ${response.status}`;
                throw new Error(errorMessage);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Request Failed:', error);
            throw error;
        }
    }
};