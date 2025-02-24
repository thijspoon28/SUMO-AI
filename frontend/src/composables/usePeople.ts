import { ref } from 'vue'
import api from '@/api/api.ts'
import type { Ref } from 'vue'
import type { AxiosError } from 'axios'
import type { PaginatedResult, Person } from '@/types'

export default function usePeople() {
  const people: Ref<Person[]> = ref([]);
  const loading: Ref<boolean> = ref(false);
  const error: Ref<AxiosError | null> = ref(null);

  const fetchPeople = async () => {
    loading.value = true;
    try {
      const { results } = await api.get<PaginatedResult<Person>>('/people')
      people.value = results
    } catch (err) {
      error.value = err as AxiosError;
    } finally {
      loading.value = false;
    }
  };

  return { people, loading, error, fetchPeople };
}
