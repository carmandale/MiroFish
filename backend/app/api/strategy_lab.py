"""
Strategy Lab API
"""

import traceback

from flask import jsonify, request

from . import strategy_lab_bp
from ..models.project import ProjectManager
from ..models.strategy_lab import WorkflowMode
from ..services.strategy_lab import StrategyLabService
from ..utils.logger import get_logger

logger = get_logger("mirofish.api.strategy_lab")


def _get_strategy_lab_project(project_id: str):
    project = ProjectManager.get_project(project_id)
    if not project:
        return None, (
            jsonify({"success": False, "error": f"项目不存在: {project_id}"}),
            404,
        )
    if project.workflow_mode != WorkflowMode.STRATEGY_LAB:
        return None, (
            jsonify({"success": False, "error": f"项目不是 strategy_lab 工作流: {project_id}"}),
            400,
        )
    return project, None


@strategy_lab_bp.route("/project/<project_id>", methods=["GET"])
def get_project_overview(project_id: str):
    project, error = _get_strategy_lab_project(project_id)
    if error:
        return error

    return jsonify(
        {
            "success": True,
            "data": {
                "project": project.to_dict(),
                "strategy_lab": StrategyLabService.project_overview(project_id),
            },
        }
    )


@strategy_lab_bp.route("/project/<project_id>/templates", methods=["GET"])
def get_lane_templates(project_id: str):
    _, error = _get_strategy_lab_project(project_id)
    if error:
        return error

    templates = StrategyLabService.load_lane_templates(project_id)
    return jsonify({"success": True, "data": [item.to_dict() for item in templates]})


@strategy_lab_bp.route("/project/<project_id>/templates/seed", methods=["POST"])
def seed_lane_templates(project_id: str):
    _, error = _get_strategy_lab_project(project_id)
    if error:
        return error

    templates = StrategyLabService.seed_lane_templates(project_id)
    return jsonify({"success": True, "data": [item.to_dict() for item in templates]})


@strategy_lab_bp.route("/project/<project_id>/templates", methods=["PUT"])
def save_lane_templates(project_id: str):
    _, error = _get_strategy_lab_project(project_id)
    if error:
        return error

    data = request.get_json() or {}
    templates = data.get("templates")
    if not isinstance(templates, list):
        return jsonify({"success": False, "error": "请提供 templates 数组"}), 400

    try:
        saved = StrategyLabService.save_lane_templates(project_id, templates)
        return jsonify({"success": True, "data": [item.to_dict() for item in saved]})
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400


@strategy_lab_bp.route("/project/<project_id>/analysis/run/<lane_id>", methods=["POST"])
def run_private_analysis(project_id: str, lane_id: str):
    project, error = _get_strategy_lab_project(project_id)
    if error:
        return error
    if not project.graph_id:
        return jsonify({"success": False, "error": "项目尚未构建图谱"}), 400

    try:
        run_status = StrategyLabService.run_private_analysis_async(
            project_id=project_id,
            graph_id=project.graph_id,
            lane_id=lane_id,
        )
        return jsonify({"success": True, "data": run_status.to_dict()})
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400


@strategy_lab_bp.route("/project/<project_id>/analysis/run-all", methods=["POST"])
def run_private_analysis_for_all(project_id: str):
    project, error = _get_strategy_lab_project(project_id)
    if error:
        return error
    if not project.graph_id:
        return jsonify({"success": False, "error": "项目尚未构建图谱"}), 400

    data = StrategyLabService.run_all_private_analysis_async(project_id, project.graph_id)
    return jsonify({"success": True, "data": data})


@strategy_lab_bp.route("/project/<project_id>/status", methods=["GET"])
def get_lane_statuses(project_id: str):
    _, error = _get_strategy_lab_project(project_id)
    if error:
        return error

    return jsonify({"success": True, "data": StrategyLabService.list_lane_statuses(project_id)})


@strategy_lab_bp.route("/project/<project_id>/status/<lane_id>", methods=["GET"])
def get_lane_status(project_id: str, lane_id: str):
    _, error = _get_strategy_lab_project(project_id)
    if error:
        return error

    status = StrategyLabService.get_lane_status(project_id, lane_id)
    if not status:
        return jsonify({"success": False, "error": f"未找到 lane status: {lane_id}"}), 404
    return jsonify({"success": True, "data": status.to_dict()})


@strategy_lab_bp.route("/project/<project_id>/report", methods=["GET"])
def get_comparative_report(project_id: str):
    _, error = _get_strategy_lab_project(project_id)
    if error:
        return error

    report = StrategyLabService.get_comparative_report(project_id)
    if not report:
        return jsonify({"success": False, "error": "对比报告尚未生成"}), 404
    return jsonify({"success": True, "data": report})


@strategy_lab_bp.route("/project/<project_id>/report/compose", methods=["POST"])
def compose_comparative_report(project_id: str):
    _, error = _get_strategy_lab_project(project_id)
    if error:
        return error

    try:
        report = StrategyLabService.compose_comparative_report(project_id)
        return jsonify({"success": True, "data": report.to_dict()})
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400


@strategy_lab_bp.route("/project/<project_id>/sources/<citation_id>", methods=["GET"])
def inspect_source(project_id: str, citation_id: str):
    _, error = _get_strategy_lab_project(project_id)
    if error:
        return error

    try:
        payload = StrategyLabService.inspect_source(project_id, citation_id)
        return jsonify({"success": True, "data": payload})
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 404


@strategy_lab_bp.route("/project/<project_id>/interviews/<lane_id>", methods=["GET"])
def get_interviews(project_id: str, lane_id: str):
    _, error = _get_strategy_lab_project(project_id)
    if error:
        return error

    interview = StrategyLabService.load_interview_artifact(project_id, lane_id)
    if not interview:
        return jsonify({"success": False, "error": f"未找到 interview artifact: {lane_id}"}), 404
    return jsonify({"success": True, "data": interview.to_dict()})


@strategy_lab_bp.errorhandler(Exception)
def handle_strategy_lab_error(exc):
    logger.error("Strategy Lab API 失败: %s", exc)
    return jsonify(
        {
            "success": False,
            "error": str(exc),
            "traceback": traceback.format_exc(),
        }
    ), 500
