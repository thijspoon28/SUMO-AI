import { ref } from 'vue'
import type { Ref } from 'vue'
import type { AxiosError } from 'axios'
import type { User } from '@/types'
import api from '@/api/api'

export default function useUser() {
  const user: Ref<User | undefined> = ref();
  const loading: Ref<boolean> = ref(false);
  const error: Ref<AxiosError | null> = ref(null);

  const fetchUser = async (userId: string) => {
    loading.value = true;
    try {
      user.value = await api.get<User>(`/users/${userId}`);
    } catch (err) {
      error.value = err as AxiosError;
    } finally {
      loading.value = false;
    }
  };

  return { user, loading, error, fetchUser };
}
