<template>
  <div class="worker-grid">
    <WorkerCard
      v-for="worker in workers"
      :key="worker.worker_id"
      :worker="worker"
    />
  </div>
</template>

<script setup>
import WorkerCard from "./WorkerCard.vue";

defineProps({
  workers: {
    type: Array,
    required: true,
  },
});
</script>

<style scoped>
.worker-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
  margin-top: 20px;
}
</style>