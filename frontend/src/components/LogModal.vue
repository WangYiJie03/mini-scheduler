<template>
  <el-dialog
    :model-value="visible"
    title="Task Logs"
    width="700px"
    @close="handleClose"
  >
    <div class="log-box" ref="logBoxRef">
      <div v-for="(line, index) in logs" :key="index" class="log-line">
        {{ line }}
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, watch, nextTick, onBeforeUnmount } from "vue";
import http from "../api/http";

const props = defineProps({
  visible: Boolean,
  taskId: String,
});

const emit = defineEmits(["update:visible"]);

const logs = ref([]);
const logBoxRef = ref(null);
let logTimer = null;

async function fetchLogs() {
  if (!props.taskId) return;

  try {
    const logEl = logBoxRef.value;
    let shouldAutoScroll = true;

    if (logEl) {
      const distanceFromBottom =
        logEl.scrollHeight - logEl.scrollTop - logEl.clientHeight;
      shouldAutoScroll = distanceFromBottom < 40;
    }

    const res = await http.get(`/api/tasks/${props.taskId}/logs`);
    logs.value = res.data.logs || [];

    await nextTick();

    if (logBoxRef.value && shouldAutoScroll) {
      logBoxRef.value.scrollTop = logBoxRef.value.scrollHeight;
    }
  } catch (error) {
    console.error("Failed to fetch logs:", error);
  }
}

watch(
  () => props.visible,
  (newVal) => {
    if (newVal && props.taskId) {
        if (logTimer) clearInterval(logTimer);
        fetchLogs();
        logTimer = setInterval(fetchLogs, 1000);
    }else {
      logs.value = [];
      if (logTimer) {
        clearInterval(logTimer);
        logTimer = null;
      }
    }
  }
);

function handleClose() {
  emit("update:visible", false);
}

onBeforeUnmount(() => {
  if (logTimer) clearInterval(logTimer);
});
</script>

<style scoped>
.log-box {
  height: 350px;
  overflow-y: auto;
  background: #111827;
  color: #e5e7eb;
  padding: 12px;
  border-radius: 8px;
  font-family: monospace;
  font-size: 13px;
}

.log-line {
  white-space: pre-wrap;
  margin-bottom: 6px;
}
</style>