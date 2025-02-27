<template>
    <main>
        <BashoNav />
        <DivisionSelect />
    </main>
</template>

<script setup lang="ts">
import BashoNav from '@/components/BashoNav.vue';
import DivisionSelect from '@/components/DivisionSelect.vue'

</script>

<style scoped lang="css">
main {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}
</style>