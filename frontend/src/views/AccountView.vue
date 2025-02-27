<template>
  <div class="account-container">
    <h1>Account</h1>
    <p>Welcome to your account page!</p>
    <p v-if="loading">Loading your profile...</p>
    <p v-else-if="error" class="error-message">{{ error }}</p>
    <div v-else>
      <p class="username">Username: {{ user?.username }}</p>
    </div>
    <button @click="logout" :disabled="isLoading">
      {{ isLoading ? 'Logging out...' : 'Logout' }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import useUser from '@/composables/useUser';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const isLoading = ref(false);
const router = useRouter();

const { user, loading, error, fetchUser } = useUser();

const logout = async () => {
  isLoading.value = true;
  try {
    await authStore.logout();
    router.push("/");
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchUser(authStore.getUserId());
});
</script>

<style scoped>
.account-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h1 {
  margin-bottom: 1rem;
  color: #2c2c2c;
  font-size: 1.6rem;
  font-weight: 600;
}

p {
  margin-bottom: 1.5rem;
}

.username {
  font-weight: 500;
  color: #2c2c2c;
  margin: 0.5rem 0;
}

.error-message {
  color: #e53935;
  font-weight: bold;
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
</style>
