import { ref } from 'vue'
import type { Ref } from 'vue'
import type { AxiosError } from 'axios'
import type { Basho } from '@/types'
import { useBashoStore } from '@/stores/bashos'

export default function useBashos() {
  const bashos: Ref<Basho[]> = ref([]);
  const total: Ref<number> = ref(-1);
  const loading: Ref<boolean> = ref(false);
  const error: Ref<AxiosError | null> = ref(null);
  const bashosStore = useBashoStore();
  const batchNumber: Ref<number> = ref(0);

  const fetchNext = async () => {
    loading.value = true;
    try {
      batchNumber.value += 1;
      bashos.value = await bashosStore.getBatch(batchNumber.value);
      total.value = bashosStore.getTotal();
    } catch (err) {
      error.value = err as AxiosError;
    } finally {
      loading.value = false;
    }
  };

  const appendNext = async () => {
    loading.value = true;
    try {
      batchNumber.value += 1;
      const newBashos = await bashosStore.getBatch(batchNumber.value);
      total.value = bashosStore.getTotal();
      bashos.value = bashos.value.concat(newBashos);
    } catch (err) {
      error.value = err as AxiosError;
    } finally {
      loading.value = false;
    }
  };

  const fetchPrevious = async () => {
    loading.value = true;
    try {
      batchNumber.value -= batchNumber.value > 1 ? 1 : 0;
      bashos.value = await bashosStore.getBatch(batchNumber.value);
      total.value = bashosStore.getTotal();
    } catch (err) {
      error.value = err as AxiosError;
    } finally {
      loading.value = false;
    }
  };

  return { bashos, total, loading, error, appendNext, fetchNext, fetchPrevious };
}
