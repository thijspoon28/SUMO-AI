<template>
  <nav class="wrapper">
    <RouterLink to="/">Home</RouterLink>
    <RouterLink to="/bashos">Basho</RouterLink>
    <RouterLink to="">Current basho</RouterLink>
    <RouterLink v-if="!authStore.isAuthenticated()" to="/login">Login</RouterLink>
    <RouterLink v-if="authStore.isAuthenticated()" to="/account">Account</RouterLink>
    <RouterLink v-if="authStore.isAdmin()" to="/admin">Admin</RouterLink>
  </nav>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
</script>

<style>
.wrapper {
  background-color: #d8c7b2;
  display: flex;
  justify-content: space-around;
}

.wrapper * {
  padding: 1.2rem;
  flex-grow: 1;
  text-align: center;
}

.wrapper *:hover {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 5px;
}
</style>
