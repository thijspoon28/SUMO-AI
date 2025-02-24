<template>
    <nav aria-label="breadcrumb">
      <ul class="breadcrumb">
        <li v-for="(crumb, index) in breadcrumbs" :key="crumb.path">
          <router-link v-if="index < breadcrumbs.length - 1" :to="crumb.path">
            {{ crumb.name }}
          </router-link>
          <span v-else>{{ crumb.name }}</span>
        </li>
      </ul>
    </nav>
  </template>
  
<script setup lang="ts">
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

// Compute breadcrumb paths
const breadcrumbs = computed(() => {
  const matchedRoutes = route.matched;
  return matchedRoutes.map((r) => ({
    name: r.name as string,
    path: r.path,
  }));
});
</script>

<style scoped>
.breadcrumb {
  list-style: none;
  display: flex;
  gap: 8px;
  justify-content: center;
}

.breadcrumb li {
  display: flex;
  align-items: center;
}

.breadcrumb li:hover {
    cursor: pointer;
}

.breadcrumb li:not(:last-child)::after {
  content: '>';
  margin-left: 8px;
}
</style>
