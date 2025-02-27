<template>
    <div class="controls" :key="componentKey">
      <p v-if="loading">Loading...</p>
      <p v-else-if="error">{{ error.message }}</p>
      <div v-else>
        <p>Basho: {{ basho?.id }}</p>
      </div>
    </div>
</template>
  
<script setup lang="ts">
import { useRoute } from 'vue-router';
import useBasho from '@/composables/useBasho';
import { onMounted, ref } from 'vue';

const route = useRoute();
// const year = route.params.year as string;
const bashoId = route.params.basho as string;
const { basho, loading, error, fetchBasho } = useBasho();
const componentKey = ref(0);

console.log("Basho ID:", bashoId);
onMounted(async ()=> {
    await fetchBasho(bashoId);
    componentKey.value++;
});

</script>
  
<style scoped>
  
</style>
  