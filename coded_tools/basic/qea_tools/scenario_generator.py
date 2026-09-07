# Copyright © 2025-2026 Cognizant Technology Solutions Corp
# Licensed under the Apache License, Version 2.0

import asyncio
import logging
from typing import Any, Dict, List, Union

from neuro_san.interfaces.coded_tool import CodedTool

logger = logging.getLogger(__name__)


class ScenarioGenerator(CodedTool):
    """Generates prioritized test scenarios and acceptance criteria."""

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        logger.info("ScenarioGenerator invoked with args: %s", args)
        system = args.get("system", "system")
        goal = args.get("goal", "verify behavior")

        scenarios: List[Dict[str, Any]] = []

        # core functional scenario
        scenarios.append(
            {
                "id": "scen-functional-1",
                "title": f"Basic functional: {system} {goal}",
                "preconditions": ["service up", "clean test data"],
                "steps": ["Call endpoint with valid payload", "Assert 200 and expected fields"],
                "expected": "Response matches contract and side effects applied",
                "automation_recommendation": "automated",
                "confidence": "high",
            }
        )

        # integration scenario
        scenarios.append(
            {
                "id": "scen-integration-1",
                "title": "Integration with downstream service",
                "preconditions": ["downstream mock available"],
                "steps": ["Simulate downstream success and failure", "Verify retry and error handling"],
                "expected": "Graceful degradation and retries",
                "automation_recommendation": "automated",
                "confidence": "medium",
            }
        )

        # load scenario
        scenarios.append(
            {
                "id": "scen-load-1",
                "title": "Load: baseline throughput",
                "preconditions": ["provisioned test environment"],
                "steps": ["Generate concurrent users", "Measure p95 latency and error rate"],
                "expected": "Latency within SLA and error rate low",
                "automation_recommendation": "automated (performance)",
                "confidence": "medium",
            }
        )

        return {"scenarios": scenarios, "assumptions": ["No external outages"], "system": system, "goal": goal}

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        return await asyncio.to_thread(self.invoke, args, sly_data)
