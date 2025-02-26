<template>
    <main>
      <h1 class="text-3xl font-bold underline">Year page!</h1>
      <p v-if="loading">Loading...</p>
      <p v-else-if="error"> {{ error.message }}</p>
      <template v-else>
        <p v-for="(person, index) in people" :key="index">
          {{ person.name }}
        </p>
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
  