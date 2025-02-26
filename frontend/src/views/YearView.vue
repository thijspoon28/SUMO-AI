<template>
  <div>
    <h1>Year: {{ year }}</h1>
    
    <!-- Display the bashos for the selected year -->
    <div v-if="bashosForYear.length > 0">
      <div v-for="(basho, index) in bashosForYear" :key="index" class="year-box">
        <RouterLink :to="{ name: 'basho', params: { year, basho: basho.id } }">
            Basho start date: {{ formatDate(basho.start_date) }}
          </RouterLink>
      </div>
    </div>
    <p v-else>No bashos found for this year.</p>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, watch, ref } from 'vue';
import { useRoute } from 'vue-router';
import useBashos from '@/composables/useBashos';

const route = useRoute();
const year = route.params.year as string;

const { bashos, appendNext, total } = useBashos();
const isLoading = ref(false); // Prevent multiple calls

// Computed property to filter bashos by year
const bashosForYear = computed(() => {
  return bashos.value.filter(basho => basho.date.substring(0, 4) === year);
});

// Function to keep fetching until data is fully loaded
const loadBashosForYear = async () => {
  if (isLoading.value) return; // Prevent multiple calls
  isLoading.value = true;

  console.log("Starting data fetch...");

  // Wait until we reach the total or no more data is available
  while (bashosForYear.value.length < total.value) {
    const currentLength = bashosForYear.value.length;
    console.log(`Fetching more data... (${currentLength}/${total.value})`);

    // If the current length hasn't changed, stop the loop (data is not increasing)
    if (currentLength === bashosForYear.value.length && currentLength >= total.value) {
      console.log("Stopping fetch loop: Data fully loaded or no more data to fetch.");
      break;
    }

    // Fetch more data
    await appendNext();

    // Optional: If no new data is added, break the loop to prevent infinite fetch
    if (bashosForYear.value.length === 6) {
      console.log("No new data fetched, stopping loop.");
      break;
    }
  }

  isLoading.value = false;
};

// Watch `bashos` and start loading when data is available
watch(
  () => bashos.value.length, // Watch bashos length changes
  (newLength) => {
    if (newLength > 0) {
      loadBashosForYear();
    }
  }
);

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString();
};

// Initial trigger on mount
onMounted(() => {
  appendNext();
  loadBashosForYear();
});
</script>

<style scoped>
.year-box {
  display: flex;
  flex-direction: column;
  border: 1px solid black;
  padding: 10px;
  margin-bottom: 10px;
  width: 200px;
}

p {
  margin: 5px 0;
}
</style>
