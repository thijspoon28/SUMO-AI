<template>
  <main>
    <div class="container">
      <div v-for="year in sortedYears" :key="year">
        <RouterLink to="/basho/year">{{ year }}</RouterLink>
        <div v-for="(basho, index) in groupedBashos[year]" :key="index" class="year-box">
          <p>Basho start date: {{ formatDate(basho.start_date) }}</p>
        </div>
      </div>
    </div>

    <div class="controls">
      <p v-if="loading">Loading...</p>
      <p v-else-if="error">{{ error.message }}</p>
      <div v-else>
        <p>Showing {{ bashos.length }} / {{ total }} bashos</p>
        <button v-if="bashos.length != total" @click="appendNext">Load More</button>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted } from "vue";
import useBashos from "@/composables/useBashos";

const { bashos, loading, error, appendNext, total } = useBashos();

onMounted(() => {
  appendNext();
});

// Compute grouped bashos by year
const groupedBashos = computed(() => {
  const grouped: Record<string, typeof bashos.value> = {};
  
  // Sort bashos in descending order (newest first)
  const sortedBashos = [...bashos.value].sort((a, b) => parseInt(b.date) - parseInt(a.date));

  sortedBashos.forEach((basho) => {
    const year = basho.date.substring(0, 4);
    if (!grouped[year]) grouped[year] = [];
    grouped[year].push(basho);
  });

  return grouped;
});

// Create a sorted list of years in descending order
const sortedYears = computed(() => {
  return Object.keys(groupedBashos.value).sort((a, b) => parseInt(b) - parseInt(a));
});

// Format date utility
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString();
};
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
