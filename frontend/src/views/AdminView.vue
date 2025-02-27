<template>
    <div class="admin-container">
        <h1>Admin Panel</h1>
        <p v-if="loading" class="loading-message">Loading users...</p>
        <p v-else-if="error" class="error-message">{{ error }}</p>
        <table v-else>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in users" :key="user.id">
                    <td>{{ user.id }}</td>
                    <td>{{ user.username }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup lang="ts">
import useUsers from '@/composables/useUsers';
import { onMounted } from 'vue';

const { users, loading, error, fetchUsers } = useUsers();

onMounted(() => {
    fetchUsers()
});
</script>

<style scoped>
.admin-container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 2rem;
    text-align: center;
    font-family: sans-serif;
    color: #333;
}

h1 {
    margin-bottom: 1.5rem;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
}

thead {
    background-color: #f4f4f4;
}

th,
td {
    padding: 0.75rem;
    border: 1px solid #ddd;
}

.loading-message {
    font-style: italic;
    color: #777;
}

.error-message {
    color: #b71c1c;
    font-weight: bold;
}
</style>