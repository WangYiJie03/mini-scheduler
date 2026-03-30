<template>
  <div class="summary-grid">
    <el-card class="summary-card">
      <div class="summary-label">Online Workers</div>
      <div class="summary-value">{{ summary.online_workers ?? 0 }}</div>
      <div class="summary-meta">Active worker nodes</div>
    </el-card>

    <el-card class="summary-card">
      <div class="summary-label">Running Tasks</div>
      <div class="summary-value">{{ summary.running_tasks ?? 0 }}</div>
      <div class="summary-meta">Currently executing</div>
    </el-card>

    <el-card class="summary-card">
      <div class="summary-label">Pending Tasks</div>
      <div class="summary-value">{{ summary.pending_tasks ?? 0 }}</div>
      <div class="summary-meta">Waiting for resources</div>
    </el-card>

    <el-card class="summary-card">
      <div class="summary-label">Failed Tasks</div>
      <div class="summary-value">{{ summary.failed_tasks ?? 0 }}</div>
      <div class="summary-meta">Requires attention</div>
    </el-card>
  </div>
</template>

<script setup>
defineProps({
  summary: {
    type: Object,
    required: true,
  },
});
</script>

<style scoped>
.summary-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.summary-card {
  border-radius: 16px;
  border: 1px solid #e7edf5;
  box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
}

.summary-label {
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  margin-bottom: 10px;
}

.summary-value {
  font-size: 38px;
  line-height: 1;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 12px;
}

.summary-meta {
  font-size: 12px;
  color: #94a3b8;
}
</style>