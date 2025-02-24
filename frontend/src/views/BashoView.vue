<template>
  <main>
    <p v-if="loading">Loading...</p>
    <p v-else-if="error"> {{ error.message }}</p>
    <template v-else>     
        <div v-for="(person, index) in people" :key="index" class="year-box">
          <h1>Year: {{ index }}</h1>
          <p>Basho 1</p>
          <p>Basho 2</p>
          <p>Basho 3</p>
          <p>Basho 4</p>
          <p>Basho 5</p>
          <p>Basho 6</p>
        </div>
    </template>
  </main>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import usePeople from '@/composables/usePeople.ts'
const { people, loading, error, fetchPeople } = usePeople();

onMounted(() => {
  fetchPeople()
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
