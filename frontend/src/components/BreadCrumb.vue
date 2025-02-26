<template>
  <nav aria-label="breadcrumb">
    <ul class="breadcrumb">
      <li v-for="(crumb, index) in breadcrumbs" :key="index">
        <router-link v-if="crumb.path" :to="crumb.path">
          {{ crumb.name }}
        </router-link>
        <span v-else>{{ crumb.name }}</span>
      </li>
    </ul>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';

interface Breadcrumb {
  name: string;
  path?: string;  // `path` can be undefined for the last breadcrumb
}

const route = useRoute();

// Properly type route.meta and provide a fallback value if it's undefined
const breadcrumbs = computed<Breadcrumb[]>(() => {
  // Fallback to an empty array if `route.meta.breadcrumb` is undefined or not set
  return (route.meta.breadcrumb as Breadcrumb[]) || [];
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
