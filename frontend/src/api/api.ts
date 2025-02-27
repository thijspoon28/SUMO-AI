// api.ts
import { useAuthStore } from '@/stores/auth';
import ApiClient from './apiClient';

const api = new ApiClient(import.meta.env.VITE_API_BASE_URL);

export function initializeApiClient() {
    api.setAuthStore(useAuthStore());
}

export default api;
