<template>
  <el-card class="worker-card" :class="{ offline: worker.status === 'OFFLINE' }">
    <div class="worker-header">
      <div>
        <div class="worker-title">{{ worker.worker_id }}</div>
        <div class="worker-host">{{ worker.host || "Unknown host" }}</div>
      </div>

      <el-tag
        class="status-tag"
        :type="worker.status === 'ONLINE' ? 'success' : 'info'"
      >
        {{ worker.status }}
      </el-tag>
    </div>

    <div class="metric-row">
      <div class="metric-top">
        <span>CPU Usage</span>
        <span>{{ cpuPercent }}%</span>
      </div>
      <el-progress :percentage="cpuPercent" :show-text="false" />
    </div>

    <div class="metric-row">
      <div class="metric-top">
        <span>Memory Usage</span>
        <span>{{ memPercent }}%</span>
      </div>
      <el-progress :percentage="memPercent" :show-text="false" />
    </div>

    <div class="worker-footer">
      <div class="footer-item">
        <div class="footer-label">Running Tasks</div>
        <div class="footer-value">{{ worker.running_tasks?.length ?? 0 }}</div>
      </div>

      <div class="footer-item">
        <div class="footer-label">Capacity</div>
        <div class="footer-value">
          {{ worker.total_cpu }} CPU / {{ worker.total_mem }} MEM
        </div>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  worker: {
    type: Object,
    required: true,
  },
});

const cpuPercent = computed(() => {
  if (!props.worker.total_cpu) return 0;
  return Math.round((props.worker.used_cpu / props.worker.total_cpu) * 100);
});

const memPercent = computed(() => {
  if (!props.worker.total_mem) return 0;
  return Math.round((props.worker.used_mem / props.worker.total_mem) * 100);
});
</script>

<style scoped>
.worker-card {
  border-radius: 18px;
  border: 1px solid #e7edf5;
  box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06);
  min-height: 230px;
}

.worker-card.offline {
  opacity: 0.58;
  filter: grayscale(20%);
}

.worker-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.worker-title {
  font-size: 22px;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.1;
}

.worker-host {
  margin-top: 6px;
  font-size: 13px;
  color: #94a3b8;
}

.status-tag {
  font-weight: 600;
}

.metric-row {
  margin-bottom: 18px;
}

.metric-top {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #475569;
}

.worker-footer {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-top: 10px;
  padding-top: 14px;
  border-top: 1px solid #edf2f7;
}

.footer-item {
  background: #f8fafc;
  border: 1px solid #edf2f7;
  border-radius: 12px;
  padding: 10px 12px;
}

.footer-label {
  font-size: 12px;
  color: #94a3b8;
  margin-bottom: 4px;
}

.footer-value {
  font-size: 14px;
  font-weight: 700;
  color: #0f172a;
}
</style>