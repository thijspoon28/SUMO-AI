import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios, { type InternalAxiosRequestConfig } from 'axios';

export const useAuthenticationStore = defineStore('authentication', () => {
    const accessToken = ref<string | null>(null);
    const refreshToken = ref<string | null>(null);

    const accessTokenKey = "access_token";
    const refreshTokenKey = "refresh_token";

    function saveTokens(aToken: string, rToken: string) {
        accessToken.value = aToken;
        refreshToken.value = rToken;
        localStorage.setItem(accessTokenKey, aToken);
        localStorage.setItem(refreshTokenKey, rToken);
    }

    function clearTokens() {
        accessToken.value = null;
        refreshToken.value = null;
        localStorage.removeItem(accessTokenKey);
        localStorage.removeItem(refreshTokenKey);
    }

    async function refreshTokens() {
        try {
            if (!refreshToken.value) {
                throw new Error("No refresh token available");
            }
            
            const response = await axios.post('/auth/refresh', {
                refresh_token: refreshToken.value
            });
            
            saveTokens(response.data.access_token, response.data.refresh_token);
            return response.data.access_token;
        } catch (error) {
            console.error("Failed to refresh token", error);
            clearTokens();
            return null;
        }
    }

    function loadTokens() {
        accessToken.value = localStorage.getItem(accessTokenKey);
        refreshToken.value = localStorage.getItem(refreshTokenKey);
    }

    async function applyHeaders(config: InternalAxiosRequestConfig) {
        loadTokens();
        
        if (!accessToken.value && refreshToken.value) {
            accessToken.value = await refreshTokens();
        }

        if (accessToken.value) {
            config.headers.Authorization = `Bearer ${accessToken.value}`;
        }

        return config;
    }

    return { applyHeaders, saveTokens, clearTokens, refreshTokens };
});
