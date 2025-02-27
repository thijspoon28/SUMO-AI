import { ref } from 'vue'
import { defineStore } from 'pinia'
import { defaultResult, type Basho, type PaginatedResult } from '@/types'
import api from '@/api/api'

export const useBashoStore = defineStore('bashos', () => {
  const bashos = ref<PaginatedResult<Basho>>(defaultResult<Basho>());
  let _batchSize = 50;

  function setBatchSize(batchSize: number) {
    _batchSize = batchSize;
  }

  function appendInfo(data: PaginatedResult<Basho>) {
    if (!bashos.value._started) {
      bashos.value = data;
      return
    }

    bashos.value.total = data.total;
    bashos.value.skip += data.records.length;
    bashos.value.records = bashos.value.records.concat(data.records);
  }

  function batchUp(batchNumber: number) {
    return bashos.value.records.slice((batchNumber - 1) * _batchSize, batchNumber * _batchSize);
  }

  function getTotal() {
    return bashos.value.total;
  }

  async function getBatch(batchNumber: number) {
    console.log(batchNumber, bashos.value._started)
    if (batchNumber < 1) throw new Error(`batchNumber must be higher than 0, got ${batchNumber}`);

    if (!bashos.value._started) {
      const response = await api.get<PaginatedResult<Basho>>(`/bashos`, { params: { skip: 0, limit: _batchSize } });

      bashos.value._started = true;

      appendInfo(response);
      return bashos.value.records;
    }

    let result = batchUp(batchNumber);

    if (result.length < _batchSize) {
      const response = await api.get<PaginatedResult<Basho>>(`/bashos`,
        { params: { skip: bashos.value.skip, limit: _batchSize } });

      appendInfo(response);
      result = batchUp(batchNumber);
    }

    return result;
  }

  async function get(bashoId: string) {
    let basho = bashos.value.records.find(b => b.id == bashoId);
    
    if (basho && basho.matches != undefined) return basho;

    const result = await api.get<Basho>(`/bashos/${bashoId}`);

    basho = result;
    update(basho);

    return basho;
  }

  function update(basho: Basho) {
    bashos.value.records.map(b => b.id == basho.id ? basho : b)
  }

  return { getBatch, get, setBatchSize, getTotal }
})
