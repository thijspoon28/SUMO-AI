import { ref } from 'vue'
import type { Ref } from 'vue'
import type { AxiosError } from 'axios'
import type { Basho } from '@/types'
import { useBashoStore } from '@/stores/bashos'

export default function useBasho() {
  const basho: Ref<Basho | undefined> = ref();
  const loading: Ref<boolean> = ref(false);
  const error: Ref<AxiosError | null> = ref(null);
  const bashosStore = useBashoStore();

  const fetchBasho = async (bashoId: string) => {
    loading.value = true;
    try {
      basho.value = await bashosStore.get(bashoId);
    } catch (err) {
      error.value = err as AxiosError;
    } finally {
      loading.value = false;
    }
  };

  return { basho, loading, error, fetchBasho };
}
