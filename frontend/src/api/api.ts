// api.ts
import { useAuthStore } from '@/stores/auth';
import ApiClient from './apiClient';
import { API_BASE_URL } from '@/config';

const api = new ApiClient(API_BASE_URL);

export function initializeApiClient() {
    api.setAuthStore(useAuthStore());
}

export default api;
