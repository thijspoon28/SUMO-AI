import { ref } from 'vue'
import type { Ref } from 'vue'
import type { AxiosError } from 'axios'
import type { Basho } from '@/types'
import { useBashoStore } from '@/stores/bashos'

export default function useBasho() {
  const bashos: Ref<Basho[]> = ref([]);
  const loading: Ref<boolean> = ref(false);
  const error: Ref<AxiosError | null> = ref(null);
  const bashosStore = useBashoStore();

  const fetchBashos = async () => {
    loading.value = true;
    try {
      bashos.value = await bashosStore.getAll();
    } catch (err) {
      error.value = err as AxiosError;
    } finally {
      loading.value = false;
    }
  };

  return { bashos, loading, error, fetchBashos };
}
