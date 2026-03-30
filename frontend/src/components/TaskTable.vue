<template>
  <div class="task-panel">
    <div class="task-panel-header">
      <div>
        <div class="task-panel-title">Tasks</div>
        <div class="task-panel-subtitle">
          Live job status, worker assignment, and log access
        </div>
      </div>

      <div class="task-panel-badge">
        {{ tasks.length }} Total
      </div>
    </div>

    <el-table
      :data="tasks"
      class="task-table"
      style="width: 100%"
      empty-text="No tasks submitted yet"
    >
      <el-table-column prop="task_id" label="Task ID" min-width="240">
        <template #default="{ row }">
          <div class="task-id-cell">{{ row.task_id }}</div>
        </template>
      </el-table-column>

      <el-table-column prop="command" label="Command" min-width="220">
        <template #default="{ row }">
          <div class="command-cell">{{ row.command }}</div>
        </template>
      </el-table-column>

      <el-table-column prop="status" label="Status" width="130">
        <template #default="{ row }">
          <el-tag class="status-tag" :type="statusType(row.status)">
            {{ row.status }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column prop="assigned_worker_id" label="Worker" width="140">
        <template #default="{ row }">
          <span class="worker-cell">{{ row.assigned_worker_id || "-" }}</span>
        </template>
      </el-table-column>

      <el-table-column label="Resources" width="150">
        <template #default="{ row }">
          <div class="resource-cell">
            {{ row.cpu_required }} CPU / {{ row.mem_required }} MEM
          </div>
        </template>
      </el-table-column>

      <el-table-column label="Action" width="130">
        <template #default="{ row }">
          <el-button
            class="logs-btn"
            size="small"
            plain
            @click="$emit('view-logs', row.task_id)"
          >
            View Logs
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
defineProps({
  tasks: {
    type: Array,
    required: true,
  },
});

defineEmits(["view-logs"]);

function statusType(status) {
  if (status === "SUCCESS") return "success";
  if (status === "FAILED") return "danger";
  if (status === "RUNNING") return "warning";
  return "info";
}
</script>

<style scoped>
.task-panel {
  background: #ffffff;
  border: 1px solid #e7edf5;
  border-radius: 18px;
  padding: 18px;
  box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
}

.task-panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.task-panel-title {
  font-size: 22px;
  font-weight: 800;
  color: #0f172a;
}

.task-panel-subtitle {
  margin-top: 4px;
  font-size: 13px;
  color: #7b8794;
}

.task-panel-badge {
  font-size: 12px;
  font-weight: 700;
  color: #475569;
  background: #f8fafc;
  border: 1px solid #e7edf5;
  border-radius: 999px;
  padding: 8px 12px;
}

.task-id-cell {
  font-family: monospace;
  font-size: 13px;
  color: #334155;
}

.command-cell {
  font-size: 13px;
  color: #0f172a;
  word-break: break-all;
}

.worker-cell,
.resource-cell {
  font-size: 13px;
  color: #475569;
  font-weight: 600;
}

.status-tag {
  font-weight: 700;
}

.logs-btn {
  border-radius: 10px;
}

:deep(.task-table) {
  border-radius: 14px;
  overflow: hidden;
}

:deep(.task-table .el-table__header-wrapper th) {
  background: #f8fafc !important;
  color: #475569;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.02em;
}

:deep(.task-table .el-table__row td) {
  padding-top: 14px;
  padding-bottom: 14px;
}

:deep(.task-table .el-table__row:hover > td) {
  background: #f8fbff !important;
}
</style>