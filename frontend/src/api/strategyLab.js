import service from './index'

export function getStrategyLabProject(projectId) {
  return service({
    url: `/api/strategy-lab/project/${projectId}`,
    method: 'get',
  })
}

export function getLaneTemplates(projectId) {
  return service({
    url: `/api/strategy-lab/project/${projectId}/templates`,
    method: 'get',
  })
}

export function seedLaneTemplates(projectId) {
  return service({
    url: `/api/strategy-lab/project/${projectId}/templates/seed`,
    method: 'post',
  })
}

export function saveLaneTemplates(projectId, templates) {
  return service({
    url: `/api/strategy-lab/project/${projectId}/templates`,
    method: 'put',
    data: { templates },
  })
}

export function runLaneAnalysis(projectId, laneId) {
  return service({
    url: `/api/strategy-lab/project/${projectId}/analysis/run/${laneId}`,
    method: 'post',
  })
}

export function runAllLaneAnalyses(projectId) {
  return service({
    url: `/api/strategy-lab/project/${projectId}/analysis/run-all`,
    method: 'post',
  })
}

export function getLaneStatuses(projectId) {
  return service({
    url: `/api/strategy-lab/project/${projectId}/status`,
    method: 'get',
  })
}

export function getComparativeReport(projectId) {
  return service({
    url: `/api/strategy-lab/project/${projectId}/report`,
    method: 'get',
  })
}

export function composeComparativeReport(projectId) {
  return service({
    url: `/api/strategy-lab/project/${projectId}/report/compose`,
    method: 'post',
  })
}

export function inspectStrategySource(projectId, citationId) {
  return service({
    url: `/api/strategy-lab/project/${projectId}/sources/${encodeURIComponent(citationId)}`,
    method: 'get',
  })
}

export function getLaneInterviews(projectId, laneId) {
  return service({
    url: `/api/strategy-lab/project/${projectId}/interviews/${laneId}`,
    method: 'get',
  })
}
