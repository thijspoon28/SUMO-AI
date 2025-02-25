<script setup lang="ts">
import { RouterView } from 'vue-router'
import NavBar from './components/NavBar.vue';
import BreadCrumb from './components/BreadCrumb.vue';
</script>

<template>
  <header>
    <NavBar />
    <BreadCrumb />
  </header>

  <RouterView />
</template>
