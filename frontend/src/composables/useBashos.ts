import { ref } from 'vue'
import api from '@/api/api.ts'
import type { Ref } from 'vue'
import type { AxiosError } from 'axios'
import type { Basho } from '@/types'
import { useBashosStore } from '@/stores/bashos'

export default function useBasho() {
  const bashos: Ref<Basho[]> = ref([]);
  const loading: Ref<boolean> = ref(false);
  const error: Ref<AxiosError | null> = ref(null);
  const bashosStore = useBashosStore();

  const fetchBashos = async () => {
    loading.value = true;
    try {
      const bashoStored = bashosStore.getAll();
      if (bashoStored.length > 0) {
        bashos.value = bashoStored;
      } else {
        const results = await api.get<Basho[]>('/bashos');
        bashosStore.set(results);
        bashos.value = results;
      }
    } catch (err) {
      error.value = err as AxiosError;
    } finally {
      loading.value = false;
    }
  };

  return { bashos, loading, error, fetchBashos };
}
