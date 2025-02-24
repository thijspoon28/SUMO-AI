<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import navbar from './components/Navbar.vue';
import BreadCrumb from './components/BreadCrumb.vue';
</script>

<template>
  <header>
    <navbar />
    <BreadCrumb />
  </header>

  <RouterView />
</template>
