# Mini Scheduler

轻量级分布式任务调度系统（Mini Scheduler）

A lightweight distributed task scheduling system with live worker monitoring and live task logs.

---

## 1. 项目简介

本项目实现了一个轻量级分布式任务调度系统，用于模拟计算集群中的任务分配、节点监控与日志查看流程。

系统包含前后端两部分：

- **后端**：负责 Worker 注册、任务提交、资源感知调度、任务执行、状态流转、日志保存、心跳检测与离线判断
- **前端**：负责 Dashboard 可视化展示，包括集群概览、Worker 监控卡片、任务表格、日志弹窗与实时刷新

该项目重点体现以下能力：

- 基于剩余资源的任务调度（Bin Packing 思路）
- Worker 自动注册与 Heartbeat 心跳上报
- Pending / Running / Success / Failed 状态追踪
- 实时 Dashboard 短轮询更新
- Live Log Stream 与日志自动滚动优化
- 使用 AI 辅助进行 UI 布局与交互优化设计

---

## 2. 核心功能

### 后端功能

- Worker 启动后自动向 Master 注册
- Worker 定时上报 CPU、内存、运行任务等心跳信息
- 用户通过 REST API 提交任务：
  - `command`
  - `cpu_required`
  - `mem_required`
- Master 根据 Worker 剩余资源进行调度
- 当无可用资源时，任务进入 `PENDING`
- 后台定时扫描 Pending 任务，并在资源恢复后自动重调度
- 任务状态支持：
  - `PENDING`
  - `RUNNING`
  - `SUCCESS`
  - `FAILED`
- 任务执行过程中采集 stdout 日志，并提供日志查询接口
- Worker 心跳超时后自动标记为 `OFFLINE`

### 前端功能

- 顶部 Hero 区展示系统整体状态
- Summary Cards 展示：
  - Online Workers
  - Running Tasks
  - Pending Tasks
  - Failed Tasks
- Worker Monitoring 区域展示：
  - Worker ID
  - Host
  - CPU / Memory 使用率
  - Running Tasks
  - Capacity
  - ONLINE / OFFLINE 状态
- Task Execution Center 展示任务表格
- 点击任务可弹出日志窗口（Log Modal）
- 前端使用 **Short Polling** 实现实时刷新
- Worker 掉线后，前端自动显示 `OFFLINE` 并进行灰化处理
- 日志弹窗支持自动滚动到底部，并优化为“用户手动查看历史日志时不抢滚动”

---

## 3. 技术栈

### 后端
- Python
- FastAPI
- Uvicorn
- Pydantic
- Asyncio
- Subprocess

### 前端
- Vue 3
- Vite
- Element Plus
- Axios

---

## 4. 系统架构说明

### 后端结构

- `main.py`
  - API 路由
  - Dashboard 数据接口
  - Worker 注册 / Heartbeat
  - Task 创建 / 查询 / 日志接口
  - 启动后台任务（离线检测、Pending 重调度）
- `scheduler.py`
  - Worker 选择逻辑
  - 任务分配逻辑
- `schemas.py`
  - 请求体定义
- `state.py`
  - 内存态存储（workers / tasks / task_logs）
- `worker.py`
  - 模拟 Worker 启动后自动注册并发送心跳

### 前端结构

- `Dashboard.vue`
  - 页面整体布局
- `SummaryCards.vue`
  - 概览指标卡片
- `WorkerGrid.vue`
  - Worker 列表区域
- `WorkerCard.vue`
  - 单个 Worker 节点监控卡片
- `TaskTable.vue`
  - 任务表格
- `LogModal.vue`
  - 日志弹窗

---

## 5. 调度策略说明

本项目采用基于剩余资源的简单 Bin Packing 调度思想。

调度逻辑核心如下：

1. 仅选择状态为 `ONLINE` 的 Worker
2. 判断 Worker 剩余 CPU / 内存是否满足任务需求
3. 从满足条件的 Worker 中选择最合适的节点
4. 若无可用节点，则任务进入 `PENDING`
5. 后台任务周期性扫描 Pending 任务，并在资源恢复时自动重新分配

### 示例
若 Worker A 有 `4 CPU / 8 MEM`，连续提交两个任务，每个任务需要 `2 CPU / 4 MEM`，则两个任务都可以成功分配到 Worker A 上。

---

## 6. 实时交互说明

### Dashboard 实时刷新
前端使用 **Short Polling**（短轮询）方案，每 2 秒请求一次 `/api/dashboard`，以更新：

- 集群概览
- Worker 状态
- 任务列表

### 日志实时刷新
日志弹窗打开后，前端每 1 秒请求一次 `/api/tasks/{task_id}/logs`，以实现日志流刷新。

---

## 7. AI 辅助设计与优化说明

本项目使用 AI 工具辅助完成以下工作：

### 1）Dashboard UI 布局设计
通过 AI 辅助梳理页面模块结构，确定以下布局：

- 顶部 Hero 区
- Cluster Overview 区
- Worker Monitoring 区
- Task Execution Center 区
- Live Log Modal

### 2）日志自动滚动实现
初版方案为：
- 每次日志刷新后直接将滚动条移动到底部

该方案虽然可以看到最新日志，但存在问题：
- 用户如果主动向上滚动查看历史日志，会被强制拉回底部，体验较差

### 3）日志滚动优化
后续优化为：
- 仅当用户当前位于底部附近时，自动滚动到底部
- 如果用户主动滚动查看旧日志，则保留当前滚动位置，不抢滚动
- 日志弹窗关闭后，清理定时器，避免无意义轮询

该优化兼顾了：
- 实时性
- 可读性
- 交互体验
- 性能稳定性

---

## 8. 本地运行方式

### 后端启动

进入 `backend` 目录：

```bash
uvicorn app.main:app --reload
```

后端接口文档地址：

`http://127.0.0.1:8000/docs`

### 前端启动

进入 `frontend` 目录：

```bash
npm install
npm run dev
```

前端 Dashboard 地址：

`http://localhost:5173/`

### Worker 启动

在 `backend` 目录运行：

```bash
python worker.py
```

Worker 启动后会自动：

- 注册到 Master
- 周期性发送 Heartbeat

---

## 9. 演示方式

### 演示入口

- 前端主页面：`http://localhost:5173/`
- 后端 Swagger 文档：`http://127.0.0.1:8000/docs`

### 可演示内容

- 启动 Worker 后自动注册并显示为 `ONLINE`
- 提交任务后自动进入 `RUNNING`
- 任务执行完成后状态变为 `SUCCESS`
- 点击 `View Logs` 查看实时日志
- 停止 Worker 后，前端自动显示 `OFFLINE`
- 当 Worker 不可用时，任务进入 `PENDING`
- Worker 恢复后，Pending 任务自动重调度

---

## 10. 项目目录结构

```text
mini-scheduler/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── scheduler.py
│   │   ├── schemas.py
│   │   └── state.py
│   ├── worker.py
│   ├── demo_task.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── views/
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## 11. 说明

本项目为笔试作业实现，重点展示：

- 分布式任务调度的基础实现思路
- 实时监控 Dashboard 的前端组织能力
- 后端状态管理、日志流与心跳机制
- 使用 AI 辅助进行 UI 与交互优化的工程过程
