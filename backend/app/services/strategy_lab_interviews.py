"""
Strategy Lab narrative interview capture.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple

from ..config import Config
from ..models.strategy_lab import InterviewArtifact
from ..utils.logger import get_logger
from .simulation_manager import SimulationState
from .simulation_runner import SimulationRunner
from .strategy_lab import StrategyLabService

logger = get_logger("mirofish.strategy_lab_interviews")


class StrategyLabInterviewService:
    """Capture strategy-lab interviews while the simulation env is still alive."""

    MAX_INTERVIEWS = 3

    @classmethod
    def capture_for_simulation(
        cls,
        state: SimulationState,
    ) -> Tuple[InterviewArtifact, str, str]:
        if state.workflow_mode.value != "strategy_lab":
            raise ValueError("当前 simulation 不是 strategy_lab 工作流")
        if not state.lane_id:
            raise ValueError("strategy_lab simulation 缺少 lane_id")
        if not state.lane_context_path:
            raise ValueError("strategy_lab simulation 缺少 lane_context_path")
        if not os.path.exists(state.lane_context_path):
            raise ValueError(f"lane_context_path 不存在: {state.lane_context_path}")
        if not SimulationRunner.check_env_alive(state.simulation_id):
            raise ValueError(f"模拟环境未运行或已关闭，无法捕获 strategy-lab 访谈: {state.simulation_id}")

        lane_context = StrategyLabService.load_lane_context(state.lane_context_path)
        sim_config = cls._load_simulation_config(state.simulation_id)
        selected_agents = cls._select_agents(sim_config)
        interviews = cls._build_interview_requests(lane_context, selected_agents)

        result = SimulationRunner.interview_agents_batch(
            simulation_id=state.simulation_id,
            interviews=interviews,
            platform=None,
            timeout=180.0,
        )
        if not result.get("success"):
            raise ValueError(result.get("error") or "strategy-lab 访谈执行失败")

        parsed_results = cls._parse_results(
            lane_context.display_name,
            lane_context.interview_personas,
            selected_agents,
            result.get("result", {}).get("results", {}),
        )

        run_dir = Path(state.lane_context_path).parent
        run_id = run_dir.name
        interview_artifact = InterviewArtifact(
            lane_id=state.lane_id,
            run_id=run_id,
            transcript_markdown=cls._render_transcript_markdown(
                lane_context.display_name,
                parsed_results,
            ),
            created_at=state.updated_at,
        )

        interview_path = run_dir / "interviews.json"
        narrative_summary_path = run_dir / "narrative_summary.json"
        cls._atomic_write_json(
            interview_path,
            {
                **interview_artifact.to_dict(),
                "interview_count": len(parsed_results),
                "results": parsed_results,
            },
        )
        cls._atomic_write_json(
            narrative_summary_path,
            {
                "lane_id": state.lane_id,
                "run_id": run_id,
                "simulation_id": state.simulation_id,
                "public_discourse_only": True,
                "status": "narrative_captured",
                "summary_markdown": cls._render_narrative_summary(
                    lane_context.display_name,
                    parsed_results,
                ),
                "created_at": state.updated_at,
            },
        )

        logger.info(
            "Captured strategy-lab interviews: simulation=%s lane=%s count=%s",
            state.simulation_id,
            state.lane_id,
            len(parsed_results),
        )
        return interview_artifact, str(interview_path), str(narrative_summary_path)

    @classmethod
    def _load_simulation_config(cls, simulation_id: str) -> Dict[str, Any]:
        config_path = os.path.join(
            Config.OASIS_SIMULATION_DATA_DIR,
            simulation_id,
            "simulation_config.json",
        )
        if not os.path.exists(config_path):
            raise ValueError(f"simulation_config.json 不存在: {simulation_id}")
        with open(config_path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    @classmethod
    def _select_agents(cls, sim_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        agent_configs = sim_config.get("agent_configs") or []
        if not agent_configs:
            raise ValueError("simulation_config.json 缺少 agent_configs，无法选择采访对象")

        sorted_agents = sorted(
            agent_configs,
            key=lambda item: (
                float(item.get("influence_weight", 0.0)),
                float(item.get("activity_level", 0.0)),
            ),
            reverse=True,
        )
        return sorted_agents[: cls.MAX_INTERVIEWS]

    @classmethod
    def _build_interview_requests(
        cls,
        lane_context,
        selected_agents: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        personas = lane_context.interview_personas or ["market_participant"] * len(selected_agents)
        requests: List[Dict[str, Any]] = []
        for index, agent in enumerate(selected_agents):
            persona = personas[index] if index < len(personas) else personas[-1]
            requests.append(
                {
                    "agent_id": agent["agent_id"],
                    "prompt": (
                        f"你正在参与 {lane_context.display_name} 的公共舆论模拟。"
                        f"请以 {persona} 的关注点回答：围绕 {lane_context.display_name}，"
                        f"市场最在意的公开信号是什么？哪些公开事件会强化或削弱这条路径？"
                        f"请结合这条路径的 narrative brief：{lane_context.narrative_brief}"
                    ),
                }
            )
        return requests

    @classmethod
    def _parse_results(
        cls,
        lane_display_name: str,
        personas: List[str],
        selected_agents: List[Dict[str, Any]],
        results: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        parsed_results: List[Dict[str, Any]] = []
        for index, agent in enumerate(selected_agents):
            agent_id = agent["agent_id"]
            persona = personas[index] if index < len(personas) else "market_participant"
            twitter_response = (results.get(f"twitter_{agent_id}") or {}).get("response", "")
            reddit_response = (results.get(f"reddit_{agent_id}") or {}).get("response", "")
            parsed_results.append(
                {
                    "lane": lane_display_name,
                    "persona": persona,
                    "agent_id": agent_id,
                    "entity_name": agent.get("entity_name", f"Agent {agent_id}"),
                    "entity_type": agent.get("entity_type", "Unknown"),
                    "twitter_response": twitter_response or "（该平台未获得回复）",
                    "reddit_response": reddit_response or "（该平台未获得回复）",
                }
            )
        return parsed_results

    @staticmethod
    def _render_transcript_markdown(
        lane_display_name: str,
        parsed_results: List[Dict[str, Any]],
    ) -> str:
        lines = [
            f"# {lane_display_name} Narrative Interviews",
            "",
            "These transcripts were captured before environment teardown.",
            "",
        ]
        for item in parsed_results:
            lines.extend(
                [
                    f"## {item['entity_name']} ({item['persona']})",
                    f"- Agent ID: {item['agent_id']}",
                    f"- Entity Type: {item['entity_type']}",
                    "",
                    "### Twitter",
                    item["twitter_response"],
                    "",
                    "### Reddit",
                    item["reddit_response"],
                    "",
                ]
            )
        return "\n".join(lines).strip() + "\n"

    @staticmethod
    def _render_narrative_summary(
        lane_display_name: str,
        parsed_results: List[Dict[str, Any]],
    ) -> str:
        participants = ", ".join(item["entity_name"] for item in parsed_results)
        return (
            f"## {lane_display_name}\n\n"
            f"- Public-discourse-only narrative capture\n"
            f"- Interviewed participants: {participants}\n"
            f"- Interview count: {len(parsed_results)}\n"
            "- Use these transcripts as narrative input for private analysis, not as procurement prediction.\n"
        )

    @staticmethod
    def _atomic_write_json(path: Path, data: Dict[str, Any]) -> None:
        temp_path = path.parent / f".{path.name}.tmp"
        temp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(temp_path, path)
