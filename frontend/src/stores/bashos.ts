import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { Basho } from '@/types'
import api from '@/api/api'

export const useBashoStore = defineStore('bashos', () => {
  const bashos = ref<Basho[]>([])

  function set(newBashos: Basho[]) {
    bashos.value = newBashos;
  }

  async function getAll() {
    if (bashos.value.length > 0)
      return bashos.value;

    const result = await api.get<Basho[]>('/bashos');
    set(result);

    return result;
  }

  async function get(bashoId: string) {
    let basho = bashos.value.find(b => b.id == bashoId);

    if (!basho) return undefined;
    const result = await api.get<Basho>(`/bashos/${bashoId}`);
    
    basho = result;
    update(basho)

    return basho;
  }

  function update(basho: Basho) {
    bashos.value.map(b => b.id == basho.id ? basho : b)
  }

  return { bashos, set, getAll, get }
})
