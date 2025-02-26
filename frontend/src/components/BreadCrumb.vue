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

const breadcrumbs = computed<Breadcrumb[]>(() => {
  // Get breadcrumbs from route metadata or fallback to an empty array
  let crumbs = (route.meta.breadcrumb as Breadcrumb[]) || [];

  // Replace the "Year" breadcrumb with the actual year from route params
  return crumbs.map(crumb => {
    if (crumb.name === 'Year' && route.params.year) {
      return { ...crumb, name: route.params.year as string, path: `/bashos/${route.params.year}` };
    }
    return crumb;
  });
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
