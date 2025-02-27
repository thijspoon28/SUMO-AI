import { ref } from 'vue';
import { defineStore } from 'pinia';
import { type InternalAxiosRequestConfig } from 'axios';
import type { TokenPair } from '@/types';
import rawApi from '@/api/rawApi';

export const useAuthStore = defineStore('auth', () => {
    const accessToken = ref<string | null>(null);
    const refreshToken = ref<string | null>(null);

    const accessTokenKey = "access_token";
    const refreshTokenKey = "refresh_token";

    async function login(username: string, password: string) {
        const response = await rawApi.post<TokenPair>('/auth/login', { username, password });

        if (response.status != 200) {
            alert(response.data);
            return
        }

        saveTokens(response.data.accessToken, response.data.refreshToken);
    }

    async function signUp(username: string, password: string) {
        const response = await rawApi.post('/users', { username, password });

        if (response.status != 201) {
            alert(response.data);
            return
        }

        await login(username, password);
    }

    function logout() {
        clearTokens();
    }

    function getUserId() {
        if (!isAuthenticated()) return "NotFound";
        const decodedPayload = decodeToken(accessToken.value!);

        return decodedPayload.user_id;
    }

    function isAuthenticated() {
        loadTokens();

        if (!accessToken.value) return false;
        if (isTokenExpired(accessToken.value)) return false;

        return true;
    }

    function isAdmin() {
        if (!isAuthenticated()) return false;
        const decodedPayload = decodeToken(accessToken.value!);

        return decodedPayload.is_admin == true;
    }

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

            const response = await rawApi.post('/auth/refresh', {
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

        if (accessToken.value && isTokenExpired(accessToken.value)) {
            accessToken.value = await refreshTokens();
        }

        else if (!accessToken.value && refreshToken.value) {
            accessToken.value = await refreshTokens();
        }

        if (accessToken.value) {
            config.headers.Authorization = `Bearer ${accessToken.value}`;
        }

        return config;
    }

    function decodeToken(token: string) {
        try {
            const payload = token.split('.')[1];
            const decodedPayload = JSON.parse(atob(payload));
            return decodedPayload;
        } catch (error) {
            console.error('Error parsing JWT token:', error);
            return true;
        }
    }

    function isTokenExpired(token: string): boolean {
        const decodedPayload = decodeToken(token);
        return decodedPayload.exp < Math.floor(Date.now() / 1000);
    }

    return { applyHeaders, saveTokens, clearTokens, refreshTokens, isAuthenticated, isAdmin, login, signUp, logout, getUserId };
});
