import { ref } from 'vue'
import type { Ref } from 'vue'
import type { AxiosError } from 'axios'
import type { User } from '@/types'
import api from '@/api/api'

export default function useUsers() {
  const users: Ref<User[]> = ref([]);
  const loading: Ref<boolean> = ref(false);
  const error: Ref<AxiosError | null> = ref(null);

  const fetchUsers = async () => {
    loading.value = true;
    try {
      users.value = await api.get<User[]>(`/users`);
    } catch (err) {
      error.value = err as AxiosError;
    } finally {
      loading.value = false;
    }
  };

  return { users, loading, error, fetchUsers };
}
