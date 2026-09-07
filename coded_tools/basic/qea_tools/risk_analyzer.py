# Copyright © 2025-2026 Cognizant Technology Solutions Corp
# Licensed under the Apache License, Version 2.0

import asyncio
import logging
from typing import Any, Dict, List, Union

from neuro_san.interfaces.coded_tool import CodedTool

logger = logging.getLogger(__name__)


class RiskAnalyzer(CodedTool):
    """Analyzes failure patterns and suggests mitigations."""

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        logger.info("RiskAnalyzer invoked with args: %s", args)
        failures: List[Dict[str, Any]] = args.get("recent_failures", []) or []
        test_type = args.get("test_type", "integration")

        probable_causes: List[Dict[str, Any]] = []

        # Simple heuristics based on failure descriptions
        for f in failures:
            desc = str(f.get("description", "")).lower()
            if "timeout" in desc or "latency" in desc:
                probable_causes.append({"cause": "timing/latency", "mitigation": "increase timeouts, add retries, investigate slow dependencies", "confidence": "high"})
            elif "order" in desc or "race" in desc:
                probable_causes.append({"cause": "order_dependency/race", "mitigation": "isolate test, reset state between runs, add deterministic setup", "confidence": "high"})
            elif "flaky" in desc or "intermittent" in desc:
                probable_causes.append({"cause": "flaky external dependency", "mitigation": "mock dependency or add retry logic", "confidence": "medium"})
            else:
                probable_causes.append({"cause": "unknown", "mitigation": "collect more logs and traces; reproduce locally", "confidence": "low"})

        if not failures:
            probable_causes.append({"cause": "no_data", "mitigation": "provide sample failure outputs or logs", "confidence": "low"})

        recommendations = {"test_type": test_type, "probable_causes": probable_causes}
        return recommendations

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        return await asyncio.to_thread(self.invoke, args, sly_data)
