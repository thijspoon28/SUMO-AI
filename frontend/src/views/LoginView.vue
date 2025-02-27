<template>
    <div class="login-container">
        <h2>Login</h2>
        <p v-if="error" class="error-message">{{ error }}</p>
        <form @submit.prevent="login">
            <div class="form-group">
                <label for="username">Username</label>
                <input 
                    id="username"
                    v-model="username" 
                    type="text" 
                    placeholder="Username..." 
                    required
                >
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input 
                    id="password"
                    v-model="password" 
                    type="password" 
                    placeholder="Password..." 
                    required
                >
            </div>
            <button type="submit" :disabled="isLoading">
                {{ isLoading ? 'Logging in...' : 'Login' }}
            </button>
        </form>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRoute, useRouter } from 'vue-router';

const authStore = useAuthStore();
const route = useRoute();
const router = useRouter();

// Form data
const username = ref('');
const password = ref('');
const error = ref('');
const isLoading = ref(false);

const login = async () => {
    if (!username.value || !password.value) {
        error.value = 'Please enter both username and password';
        return;
    }

    try {
        isLoading.value = true;
        error.value = '';
        
        await authStore.login(username.value, password.value);
        
        // Redirect to originally requested page or home
        const redirectPath = route.query.redirect as string || '/';
        router.push(redirectPath);
    } catch (err) {
        error.value = err instanceof Error 
            ? err.message 
            : 'Failed to login. Please check your credentials and try again.';
    } finally {
        isLoading.value = false;
    }
};
</script>

<style scoped>
.login-container {
    max-width: 400px;
    margin: 2rem auto;
    padding: 2rem;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
    margin-top: 0;
    margin-bottom: 1.5rem;
    text-align: center;
}

.form-group {
    margin-bottom: 1rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: bold;
}

input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid black;
    border-radius: 4px;
    font-size: 1rem;
    box-sizing: border-box;
}

button {
    width: 100%;
    padding: 0.75rem;
    background-color: lightgray;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
}

button:hover {
    background-color: #c0c0c0;
}

button:disabled {
    background-color: #e0e0e0;
    cursor: not-allowed;
}

.error-message {
    color: #e53935;
    margin-bottom: 1rem;
    text-align: center;
}
</style>
