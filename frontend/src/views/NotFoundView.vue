<template>
    <div class="not-found-container">
        <h1>404</h1>
        <p>Page not found.</p>
        <router-link to="/" class="home-link">Go Home</router-link>
    </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.not-found-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    font-family: sans-serif;
    color: #333;
    padding-top: 10rem;
}

h1 {
    font-size: 3rem;
    margin-bottom: 0.5rem;
}

p {
    font-size: 1.25rem;
    margin-bottom: 1.5rem;
}

.home-link {
    font-size: 1rem;
    color: #007bff;
    text-decoration: none;
    border-bottom: 1px solid #007bff;
    transition: color 0.2s;
}

.home-link:hover {
    color: #0056b3;
}
</style>