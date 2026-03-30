<template>
  <div class="page-shell">
    <div class="page-container">
      <section class="hero-section">
        <div class="hero-left">
          <div class="hero-badge">REAL-TIME SCHEDULER</div>
          <h1 class="hero-title">Mini Scheduler Dashboard</h1>
          <p class="hero-subtitle">
            Real-time task orchestration and worker monitoring across the cluster.
          </p>
        </div>

        <div class="hero-right">
          <el-card class="hero-status-card">
            <div class="hero-status-label">Cluster Status</div>
            <div class="hero-status-value">
              {{ (dashboardData.summary?.online_workers ?? 0) > 0 ? "Healthy" : "Idle" }}
            </div>
            <div class="hero-status-meta">
              Auto Refresh · Every 2s
            </div>
          </el-card>
        </div>
      </section>

      <section class="overview-section">
        <div class="section-header">
          <div>
            <h2 class="section-title">Cluster Overview</h2>
            <p class="section-subtitle">
              Live worker capacity, health status, and task activity.
            </p>
          </div>
          <el-button @click="fetchDashboard">Refresh Dashboard</el-button>
        </div>

        <div class="overview-grid">
          <div class="summary-panel">
            <SummaryCards :summary="dashboardData.summary || {}" />
          </div>

          <div class="worker-panel">
            <div class="panel-title">Worker Monitoring</div>
            <WorkerGrid :workers="dashboardData.workers || []" />
          </div>
        </div>
      </section>

      <section class="tasks-section">
        <div class="section-header">
          <div>
            <h2 class="section-title">Task Execution Center</h2>
            <p class="section-subtitle">
              Submitted jobs, runtime state, worker assignment, and log access.
            </p>
          </div>
        </div>

        <TaskTable
          :tasks="dashboardData.tasks || []"
          @view-logs="handleViewLogs"
        />
      </section>

      <LogModal
        v-model:visible="logModalVisible"
        :task-id="selectedTaskId"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import http from "../api/http";
import SummaryCards from "../components/SummaryCards.vue";
import WorkerGrid from "../components/WorkerGrid.vue";
import TaskTable from "../components/TaskTable.vue";
import LogModal from "../components/LogModal.vue";

const dashboardData = ref({});
const logModalVisible = ref(false);
const selectedTaskId = ref(null);

let dashboardTimer = null;

async function fetchDashboard() {
  try {
    const res = await http.get("/api/dashboard");
    dashboardData.value = res.data;
  } catch (error) {
    console.error("Failed to fetch dashboard:", error);
  }
}

function handleViewLogs(taskId) {
  selectedTaskId.value = taskId;
  logModalVisible.value = true;
}

onMounted(() => {
  fetchDashboard();
  dashboardTimer = setInterval(fetchDashboard, 2000);
});

onBeforeUnmount(() => {
  if (dashboardTimer) {
    clearInterval(dashboardTimer);
    dashboardTimer = null;
  }
});
</script>

<style scoped>
.page-shell {
  min-height: 100vh;
  background: #f5f7fb;
  padding: 24px;
}

.page-container {
  max-width: 1440px;
  margin: 0 auto;
}

.hero-section {
  display: grid;
  grid-template-columns: 1.5fr 0.8fr;
  gap: 20px;
  align-items: stretch;
  background: linear-gradient(135deg, #f8fbff 0%, #eef4ff 100%);
  border: 1px solid #e6ecf5;
  border-radius: 20px;
  padding: 28px;
  margin-bottom: 24px;
}

.hero-badge {
  display: inline-block;
  font-size: 12px;
  font-weight: 700;
  color: #3b82f6;
  letter-spacing: 0.08em;
  margin-bottom: 12px;
}

.hero-title {
  margin: 0;
  font-size: 40px;
  line-height: 1.1;
  font-weight: 800;
  color: #0f172a;
}

.hero-subtitle {
  margin-top: 14px;
  font-size: 15px;
  color: #5b6472;
  max-width: 680px;
}

.hero-right {
  display: flex;
  align-items: stretch;
}

.hero-status-card {
  width: 100%;
  border-radius: 18px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.hero-status-label {
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 8px;
}

.hero-status-value {
  font-size: 30px;
  font-weight: 800;
  color: #0f172a;
}

.hero-status-meta {
  margin-top: 10px;
  font-size: 13px;
  color: #64748b;
}

.overview-section,
.tasks-section {
  background: #ffffff;
  border: 1px solid #e8edf3;
  border-radius: 20px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.section-title {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: #0f172a;
}

.section-subtitle {
  margin-top: 6px;
  font-size: 14px;
  color: #6b7280;
}

.overview-grid {
  display: grid;
  grid-template-columns: 1fr 1.3fr;
  gap: 20px;
  align-items: start;
}

.summary-panel,
.worker-panel {
  background: #f8fafc;
  border: 1px solid #e9eef5;
  border-radius: 18px;
  padding: 18px;
}

.panel-title {
  font-size: 16px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 14px;
}
</style>