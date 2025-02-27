// api.ts
import { useAuthenticationStore } from '@/stores/authenticate';
import ApiClient from './apiClient';

const api = new ApiClient('http://localhost:8000/api/latest');

export function initializeApiClient() {
    api.setAuthenticationStore(useAuthenticationStore());
}

export default api;
