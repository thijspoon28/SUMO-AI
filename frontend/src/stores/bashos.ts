import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { Basho } from '@/types'

export const useBashosStore = defineStore('bashos', () => {
  const bashos = ref<Basho[]>([])

  function set(newBashos: Basho[]) {
    bashos.value = newBashos;
  }

  function getAll() {
    return bashos.value;
  }

  function get(bashoId: string) {
    return bashos.value.find(b => b.id == bashoId)
  }

  return { bashos, set, getAll, get }
})
