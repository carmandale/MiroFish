<template>
  <div class="strategy-lab-view">
    <header class="topbar">
      <button class="brand" @click="router.push('/')">MIROFISH</button>
      <div class="topbar-actions">
        <button class="ghost-btn" :disabled="loading || actionLoading" @click="refreshAll">刷新</button>
        <button class="primary-btn" :disabled="!projectReady || actionLoading" @click="runAllAnalyses">
          运行五条路径工作流
        </button>
      </div>
    </header>

    <main class="layout">
      <aside class="sidebar">
        <section class="panel">
          <div class="panel-title">Project</div>
          <div class="meta-row">
            <span>ID</span>
            <code>{{ currentProjectId }}</code>
          </div>
          <div class="meta-row">
            <span>Status</span>
            <strong>{{ projectData?.status || 'loading' }}</strong>
          </div>
          <div class="meta-row">
            <span>Workflow</span>
            <strong>{{ projectData?.workflow_mode || 'strategy_lab' }}</strong>
          </div>
          <div class="meta-row">
            <span>Graph</span>
            <strong>{{ projectData?.graph_id ? 'ready' : 'pending' }}</strong>
          </div>
          <p class="project-requirement">{{ projectData?.simulation_requirement }}</p>
        </section>

        <section class="panel">
          <div class="panel-title">Lane Status</div>
          <div
            v-for="template in laneTemplates"
            :key="template.lane_id"
            class="lane-card"
            :class="{ active: selectedLaneId === template.lane_id }"
            @click="selectedLaneId = template.lane_id"
          >
            <div class="lane-header">
              <strong>{{ template.display_name }}</strong>
              <span class="status-pill" :class="statusClass(laneStatuses[template.lane_id]?.status)">
                {{ laneStatuses[template.lane_id]?.status || 'idle' }}
              </span>
            </div>
            <p class="lane-summary">{{ template.hypothesis }}</p>
            <div class="lane-actions">
              <button class="ghost-btn small" :disabled="!projectReady || actionLoading" @click.stop="runLane(template.lane_id)">
                运行工作流
              </button>
              <button class="ghost-btn small" :disabled="actionLoading" @click.stop="loadLaneInterview(template.lane_id)">
                访谈
              </button>
            </div>
          </div>
        </section>
      </aside>

      <section class="content">
        <section class="panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Lane Template Review</div>
              <p class="panel-subtitle">Review and refine the shaped lane hypotheses before rerunning analysis.</p>
            </div>
            <button class="ghost-btn" :disabled="actionLoading || !laneTemplates.length" @click="saveTemplates">
              保存模板
            </button>
          </div>

          <div v-if="selectedTemplate" class="template-editor">
            <label>
              <span>Display Name</span>
              <input v-model="selectedTemplate.display_name" type="text" />
            </label>
            <label>
              <span>Hypothesis</span>
              <textarea v-model="selectedTemplate.hypothesis" rows="3"></textarea>
            </label>
            <label>
              <span>Narrative Brief</span>
              <textarea v-model="selectedTemplate.narrative_brief" rows="4"></textarea>
            </label>
            <div class="chip-groups">
              <div class="chip-group">
                <span>Public Actors</span>
                <div class="chips">
                  <span v-for="item in selectedTemplate.public_actor_classes" :key="item" class="chip">{{ item }}</span>
                </div>
              </div>
              <div class="chip-group">
                <span>Public Events</span>
                <div class="chips">
                  <span v-for="item in selectedTemplate.public_event_classes" :key="item" class="chip">{{ item }}</span>
                </div>
              </div>
              <div class="chip-group">
                <span>Private Gates</span>
                <div class="chips">
                  <span v-for="item in selectedTemplate.procurement_gates" :key="item" class="chip">{{ item }}</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section class="panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Comparative Report</div>
              <p class="panel-subtitle">All five lanes must complete before the comparative output is considered done.</p>
            </div>
            <button class="ghost-btn" :disabled="actionLoading || !projectReady" @click="composeReport">
              组装报告
            </button>
          </div>

          <div v-if="comparativeRows.length" class="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Lane</th>
                  <th v-for="dimension in dimensions" :key="dimension">{{ dimension }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="row in comparativeRows" :key="row.lane_id">
                  <td>
                    <strong>{{ row.display_name }}</strong>
                    <p class="row-summary">{{ row.summary }}</p>
                  </td>
                  <td v-for="dimension in dimensions" :key="dimension">
                    <div class="metric-score">{{ row.metrics[dimension]?.score || '-' }}</div>
                    <div class="metric-judgment">{{ row.metrics[dimension]?.judgment || '-' }}</div>
                    <div class="metric-source">{{ row.metrics[dimension]?.source_label || '-' }}</div>
                    <div class="citation-links">
                      <button
                        v-for="citationId in row.metrics[dimension]?.citation_ids || []"
                        :key="citationId"
                        class="citation-link"
                        @click="inspectSource(citationId)"
                      >
                        {{ citationId }}
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="empty-state">对比报告尚未生成。先运行路径分析，再组装报告。</div>

          <article v-if="comparativeReport?.markdown_summary" class="markdown-card" v-html="comparativeReportHtml"></article>
        </section>

        <section class="split-panels">
          <div class="panel">
            <div class="panel-title">Transcript Viewer</div>
            <article class="markdown-card" v-html="transcriptHtml"></article>
          </div>

          <div class="panel">
            <div class="panel-title">Source Inspector</div>
            <div v-if="sourcePayload" class="source-card">
              <div class="meta-row">
                <span>Source Label</span>
                <strong>{{ sourcePayload.citation.source_label }}</strong>
              </div>
              <div class="meta-row">
                <span>Filename</span>
                <strong>{{ sourcePayload.citation.filename }}</strong>
              </div>
              <div class="meta-row">
                <span>Locator</span>
                <code>{{ sourcePayload.citation.locator }}</code>
              </div>
              <div v-if="sourcePayload.source?.kind" class="meta-row">
                <span>Kind</span>
                <code>{{ sourcePayload.source.kind }}</code>
              </div>
              <div v-if="sourcePayload.source?.path" class="meta-row">
                <span>Path</span>
                <code>{{ sourcePayload.source.path }}</code>
              </div>
              <div v-if="sourcePayload.source?.chunk" class="meta-row">
                <span>Chunk</span>
                <code>{{ sourcePayload.source.chunk.chunk_id }}</code>
              </div>
              <div v-if="sourcePayload.source?.chunk" class="meta-row">
                <span>Episode</span>
                <code>{{ sourcePayload.source.chunk.episode_uuid }}</code>
              </div>
              <p class="source-quote">{{ sourcePayload.citation.quote }}</p>
              <pre v-if="sourceArtifactPreview" class="source-artifact">{{ sourceArtifactPreview }}</pre>
            </div>
            <div v-else class="empty-state">点击报告中的 citation_id 以检查 provenance。</div>
          </div>
        </section>

        <p v-if="error" class="error-banner">{{ error }}</p>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { buildGraph, generateOntology, getProject } from '../api/graph'
import {
  composeComparativeReport,
  getLaneInterviews,
  getStrategyLabProject,
  inspectStrategySource,
  runAllLaneAnalyses,
  runLaneAnalysis,
  saveLaneTemplates,
} from '../api/strategyLab'
import { clearPendingUpload, getPendingUpload } from '../store/pendingUpload'
import { renderSafeMarkdown } from '../utils/safeMarkdown'

const props = defineProps({
  projectId: String,
})

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const actionLoading = ref(false)
const error = ref('')
const currentProjectId = ref(props.projectId || route.params.projectId)
const projectData = ref(null)
const laneTemplates = ref([])
const laneStatuses = ref({})
const comparativeReport = ref(null)
const selectedLaneId = ref('')
const transcriptMarkdown = ref('No strategy-lab interview transcript captured yet.')
const sourcePayload = ref(null)
let refreshTimer = null

const dimensions = [
  'time_to_cash',
  'durability_12_24m',
  'capability_fit',
  'required_investment',
  'failure_modes',
  'evidence_strength',
]

const selectedTemplate = computed(() => {
  return laneTemplates.value.find((item) => item.lane_id === selectedLaneId.value) || null
})

const projectReady = computed(() => Boolean(projectData.value?.graph_id))
const comparativeRows = computed(() => comparativeReport.value?.rows || [])
const comparativeReportHtml = computed(() => renderSafeMarkdown(comparativeReport.value?.markdown_summary || ''))
const transcriptHtml = computed(() => renderSafeMarkdown(transcriptMarkdown.value))
const sourceArtifactPreview = computed(() => {
  const artifact = sourcePayload.value?.source?.artifact
  if (!artifact) return ''
  return typeof artifact === 'string' ? artifact : JSON.stringify(artifact, null, 2)
})

const statusClass = (status = 'idle') => {
  if (status === 'completed') return 'success'
  if (status === 'failed') return 'danger'
  if (status === 'running') return 'running'
  return 'idle'
}

const refreshAll = async () => {
  if (!currentProjectId.value || currentProjectId.value === 'new') return
  await loadProjectAndOverview()
}

const handleNewProject = async () => {
  const pending = getPendingUpload()
  if (!pending.isPending || pending.workflowMode !== 'strategy_lab' || pending.files.length === 0) {
    error.value = '没有找到 strategy_lab 待上传数据，请返回首页重试。'
    return
  }

  loading.value = true
  try {
    const formData = new FormData()
    pending.files.forEach((file) => formData.append('files', file))
    formData.append('simulation_requirement', pending.simulationRequirement)
    formData.append('workflow_mode', 'strategy_lab')

    const response = await generateOntology(formData)
    if (!response.success) {
      error.value = response.error || '初始化 strategy_lab 项目失败'
      return
    }

    clearPendingUpload()
    currentProjectId.value = response.data.project_id
    projectData.value = response.data

    router.replace({
      name: 'StrategyLab',
      params: { projectId: response.data.project_id },
    })

    await ensureGraphBuilt()
    await loadOverview()
  } catch (err) {
    error.value = err.message || '初始化 strategy_lab 项目失败'
  } finally {
    loading.value = false
  }
}

const loadProjectAndOverview = async () => {
  loading.value = true
  error.value = ''

  try {
    const projectResponse = await getProject(currentProjectId.value)
    if (!projectResponse.success) {
      error.value = projectResponse.error || '加载项目失败'
      return
    }

    if (projectResponse.data.workflow_mode !== 'strategy_lab') {
      router.replace({ name: 'Process', params: { projectId: currentProjectId.value } })
      return
    }

    projectData.value = projectResponse.data
    await ensureGraphBuilt()
    await loadOverview()
  } catch (err) {
    error.value = err.message || '加载项目失败'
  } finally {
    loading.value = false
  }
}

const ensureGraphBuilt = async () => {
  if (!projectData.value) return
  if (projectData.value.graph_id) return
  if (!['ontology_generated', 'graph_building', 'graph_completed'].includes(projectData.value.status)) return

  const buildResponse = await buildGraph({ project_id: currentProjectId.value })
  if (!buildResponse.success) {
    error.value = buildResponse.error || '图谱构建启动失败'
    return
  }

  const latestProject = await getProject(currentProjectId.value)
  if (latestProject.success) {
    projectData.value = latestProject.data
  }
}

const loadOverview = async () => {
  const overviewResponse = await getStrategyLabProject(currentProjectId.value)
  if (!overviewResponse.success) {
    error.value = overviewResponse.error || '加载 strategy_lab 概览失败'
    return
  }

  laneTemplates.value = overviewResponse.data.strategy_lab.lane_templates || []
  laneStatuses.value = overviewResponse.data.strategy_lab.lane_statuses || {}
  comparativeReport.value = overviewResponse.data.strategy_lab.comparative_report

  if (!selectedLaneId.value && laneTemplates.value.length) {
    selectedLaneId.value = laneTemplates.value[0].lane_id
    await loadLaneInterview(selectedLaneId.value)
  }

  syncRefreshTimer()
}

const syncRefreshTimer = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }

  const hasRunningLane = Object.values(laneStatuses.value).some((item) => item?.status === 'running')
  if (hasRunningLane) {
    refreshTimer = setInterval(() => {
      loadOverview()
    }, 3000)
  }
}

const saveTemplates = async () => {
  actionLoading.value = true
  error.value = ''
  try {
    const response = await saveLaneTemplates(currentProjectId.value, laneTemplates.value)
    if (!response.success) {
      error.value = response.error || '保存模板失败'
      return
    }
    laneTemplates.value = response.data
  } catch (err) {
    error.value = err.message || '保存模板失败'
  } finally {
    actionLoading.value = false
  }
}

const runLane = async (laneId) => {
  actionLoading.value = true
  error.value = ''
  try {
    const response = await runLaneAnalysis(currentProjectId.value, laneId)
    if (!response.success) {
      error.value = response.error || '路径运行失败'
      return
    }
    laneStatuses.value[laneId] = response.data
    syncRefreshTimer()
  } catch (err) {
    error.value = err.message || '路径运行失败'
  } finally {
    actionLoading.value = false
  }
}

const runAllAnalyses = async () => {
  actionLoading.value = true
  error.value = ''
  try {
    const response = await runAllLaneAnalyses(currentProjectId.value)
    if (!response.success) {
      error.value = response.error || '批量运行失败'
      return
    }
    await loadOverview()
  } catch (err) {
    error.value = err.message || '批量运行失败'
  } finally {
    actionLoading.value = false
  }
}

const composeReport = async () => {
  actionLoading.value = true
  error.value = ''
  try {
    const response = await composeComparativeReport(currentProjectId.value)
    if (!response.success) {
      error.value = response.error || '组装对比报告失败'
      return
    }
    comparativeReport.value = response.data
  } catch (err) {
    error.value = err.message || '组装对比报告失败'
  } finally {
    actionLoading.value = false
  }
}

const inspectSource = async (citationId) => {
  try {
    const response = await inspectStrategySource(currentProjectId.value, citationId)
    if (response.success) {
      sourcePayload.value = response.data
    }
  } catch (err) {
    error.value = err.message || '加载 source inspector 失败'
  }
}

const loadLaneInterview = async (laneId) => {
  selectedLaneId.value = laneId
  try {
    const response = await getLaneInterviews(currentProjectId.value, laneId)
    if (response.success) {
      transcriptMarkdown.value = response.data.transcript_markdown
      return
    }
  } catch (err) {
    // ignore and keep placeholder copy
  }
  transcriptMarkdown.value = 'No strategy-lab interview transcript captured yet.'
}

onMounted(async () => {
  if (currentProjectId.value === 'new') {
    await handleNewProject()
  } else {
    await loadProjectAndOverview()
  }
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})
</script>

<style scoped>
.strategy-lab-view {
  min-height: 100vh;
  background: #f6f4ef;
  color: #161616;
  font-family: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 28px;
  border-bottom: 1px solid rgba(22, 22, 22, 0.08);
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(18px);
  position: sticky;
  top: 0;
  z-index: 10;
}

.brand {
  border: none;
  background: transparent;
  font-size: 1.1rem;
  font-weight: 800;
  letter-spacing: 0.1em;
  cursor: pointer;
}

.topbar-actions {
  display: flex;
  gap: 12px;
}

.layout {
  display: grid;
  grid-template-columns: 320px minmax(0, 1fr);
  gap: 20px;
  padding: 20px 28px 28px;
}

.sidebar,
.content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.panel {
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid rgba(22, 22, 22, 0.08);
  border-radius: 22px;
  padding: 20px;
  box-shadow: 0 18px 40px rgba(22, 22, 22, 0.06);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
  margin-bottom: 18px;
}

.panel-title {
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #8b5e3c;
  margin-bottom: 12px;
}

.panel-subtitle {
  margin: 4px 0 0;
  color: #666;
  font-size: 0.92rem;
}

.meta-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
  font-size: 0.92rem;
}

.project-requirement,
.lane-summary,
.row-summary,
.source-quote {
  color: #444;
  line-height: 1.5;
}

.lane-card {
  border: 1px solid rgba(22, 22, 22, 0.08);
  border-radius: 18px;
  padding: 14px;
  cursor: pointer;
  transition: transform 0.18s ease, border-color 0.18s ease;
  margin-bottom: 12px;
}

.lane-card.active,
.lane-card:hover {
  transform: translateY(-1px);
  border-color: #b17244;
}

.lane-header {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  align-items: flex-start;
}

.lane-actions {
  display: flex;
  gap: 10px;
  margin-top: 12px;
}

.status-pill {
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.status-pill.success {
  background: rgba(40, 167, 69, 0.12);
  color: #1d7a35;
}

.status-pill.danger {
  background: rgba(196, 58, 58, 0.12);
  color: #b53434;
}

.status-pill.running {
  background: rgba(210, 132, 48, 0.14);
  color: #9d5f11;
}

.status-pill.idle {
  background: rgba(22, 22, 22, 0.06);
  color: #666;
}

.ghost-btn,
.primary-btn {
  border-radius: 999px;
  padding: 10px 16px;
  font-weight: 700;
  cursor: pointer;
  border: 1px solid rgba(22, 22, 22, 0.12);
}

.ghost-btn {
  background: #fff;
}

.primary-btn {
  background: #161616;
  color: #fff;
}

.ghost-btn.small {
  padding: 8px 12px;
  font-size: 0.82rem;
}

.ghost-btn:disabled,
.primary-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.template-editor {
  display: grid;
  gap: 16px;
}

.template-editor label {
  display: grid;
  gap: 8px;
  font-size: 0.9rem;
}

.template-editor input,
.template-editor textarea {
  border-radius: 14px;
  border: 1px solid rgba(22, 22, 22, 0.12);
  padding: 12px 14px;
  font: inherit;
  background: #fff;
}

.chip-groups {
  display: grid;
  gap: 14px;
}

.chip-group {
  display: grid;
  gap: 8px;
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip {
  border-radius: 999px;
  padding: 6px 10px;
  background: rgba(177, 114, 68, 0.12);
  color: #7b4b22;
  font-size: 0.8rem;
}

.table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 14px 12px;
  border-bottom: 1px solid rgba(22, 22, 22, 0.08);
  vertical-align: top;
  text-align: left;
}

th {
  font-size: 0.74rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #8b5e3c;
}

.metric-score {
  font-weight: 700;
  margin-bottom: 6px;
}

.metric-judgment {
  color: #555;
  font-size: 0.88rem;
  margin-bottom: 8px;
}

.metric-source {
  color: #8b5e3c;
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: 8px;
}

.citation-links {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.citation-link {
  border: none;
  background: rgba(22, 22, 22, 0.06);
  border-radius: 999px;
  padding: 4px 8px;
  cursor: pointer;
  font-size: 0.74rem;
}

.markdown-card :deep(h1),
.markdown-card :deep(h2),
.markdown-card :deep(h3) {
  margin-top: 0;
}

.markdown-card :deep(p),
.markdown-card :deep(li),
.markdown-card :deep(blockquote) {
  line-height: 1.6;
  color: #444;
}

.markdown-card :deep(code) {
  background: rgba(22, 22, 22, 0.06);
  border-radius: 6px;
  padding: 2px 6px;
}

.split-panels {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
}

.source-card {
  display: grid;
  gap: 10px;
}

.source-artifact {
  margin: 0;
  padding: 12px;
  border-radius: 12px;
  background: rgba(22, 22, 22, 0.04);
  color: #444;
  font-size: 0.78rem;
  line-height: 1.5;
  overflow: auto;
  white-space: pre-wrap;
  word-break: break-word;
}

.empty-state {
  color: #666;
  padding: 12px 0;
}

.error-banner {
  margin: 0;
  padding: 14px 16px;
  border-radius: 16px;
  background: rgba(196, 58, 58, 0.12);
  color: #b53434;
}

@media (max-width: 1080px) {
  .layout {
    grid-template-columns: 1fr;
  }

  .split-panels {
    grid-template-columns: 1fr;
  }
}
</style>
