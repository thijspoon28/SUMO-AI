<template>
  <main>
    <p v-if="loading">Loading...</p>
    <p v-else-if="error"> {{ error.message }}</p>
    <template v-else>     
        <div v-for="(basho, index) in bashos" :key="index" class="year-box">
          <h1>{{ new Date( basho.start_date ).getFullYear() }}</h1>
          <p>Basho {{ new Date( basho.start_date ).toLocaleDateString()}}</p>
          <p>Basho {{ new Date( basho.start_date ).toLocaleDateString() }}</p>
          <p>Basho {{ new Date( basho.start_date ).toLocaleDateString() }}</p>
          <p>Basho {{ new Date( basho.start_date ).toLocaleDateString() }}</p>
          <p>Basho {{ new Date( basho.start_date ).toLocaleDateString() }}</p>
          <p>Basho {{ new Date( basho.start_date ).toLocaleDateString() }}</p>
        </div>
    </template>
  </main>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import useBasho from '@/composables/useBashos';
const { bashos, loading, error, fetchBashos } = useBasho();

onMounted(() => {
  fetchBashos()
})
</script>

<style>
main {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.year-box {
  display: flex;
  flex-direction: column;
  border: 1px solid black;
  width: 200px;
  margin: 10px
}
</style>
