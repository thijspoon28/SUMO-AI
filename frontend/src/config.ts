const API_URL = import.meta.env.VITE_API_BASE_URL || '/api/latest';

function getApiBaseUrl() {
    // If running in Docker/production, use relative URL
    if (window.location.hostname !== 'localhost' || window.location.port !== '5173') {
        return '/api/latest';
    }
    // If in development mode, use the full URL
    return API_URL;
}

export const API_BASE_URL = getApiBaseUrl();
