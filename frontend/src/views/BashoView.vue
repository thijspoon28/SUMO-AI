<template>
  <main>
    <template class="container">     
      <div v-for="(basho, index) in bashos" :key="index" class="year-box">
        <h1>{{ new Date( basho.start_date ).getFullYear() }}</h1>
        <p>Basho {{ new Date( basho.start_date ).toLocaleDateString() }}</p>
        <p>Basho {{ new Date( basho.start_date ).toLocaleDateString() }}</p>
        <p>Basho {{ new Date( basho.start_date ).toLocaleDateString() }}</p>
        <p>Basho {{ new Date( basho.start_date ).toLocaleDateString() }}</p>
        <p>Basho {{ new Date( basho.start_date ).toLocaleDateString() }}</p>
        <p>Basho {{ new Date( basho.start_date ).toLocaleDateString() }}</p>
      </div>
    </template>
    <div class="controls">
      <p v-if="loading">Loading...</p>
      <p v-else-if="error"> {{ error.message }}</p>
      <div v-else>
        <p>Showing {{ bashos.length }} / {{ total }} bashos</p>
        <button v-if="bashos.length != total" :onclick="appendNext">Load More</button>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import useBashos from '@/composables/useBashos';
const { bashos, loading, error, appendNext, total } = useBashos();

onMounted(() => {
  appendNext()
})
</script>

<style scoped>
.container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  margin-bottom: 120px;
}

.controls button {
  background-color: lightgray;
  padding: .2rem .7rem;
}

.year-box {
  display: flex;
  flex-direction: column;
  border: 1px solid black;
  width: 200px;
  margin: 10px
}
</style>
