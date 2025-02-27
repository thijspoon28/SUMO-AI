<template>
    <div class="controls">
      <p v-if="loading">Loading...</p>
      <p v-else-if="error">{{ error.message }}</p>
      <div v-else>
        <p>Basho: {{ bashoId }}</p>
    </div>
    </div>
</template>
  
<script setup lang="ts">
import { useRoute } from 'vue-router';
import useBasho from '@/composables/useBasho';
import type { Basho } from '@/types';

const route = useRoute();
const year = route.params.year as string;
const bashoId = route.params.basho as string;
const { basho, loading, error, fetchBasho } = useBasho();
const bashoById = fetchBasho(bashoId);


console.log(year, bashoId, basho.value);

  
</script>
  
<style scoped>
  
</style>
  