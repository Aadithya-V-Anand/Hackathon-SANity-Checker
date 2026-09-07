# Copyright © 2025-2026 Cognizant Technology Solutions Corp
# Licensed under the Apache License, Version 2.0

import asyncio
import logging
from typing import Any, Dict, Union

from neuro_san.interfaces.coded_tool import CodedTool

logger = logging.getLogger(__name__)


class EnvPlanner(CodedTool):
    """Generates environment and observability planning guidance."""

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        logger.info("EnvPlanner invoked with args: %s", args)
        scale = args.get("scale", "small")
        observability = args.get("observability", "basic")

        components = ["app_servers", "database", "message_queue"]
        if scale in ("medium", "large"):
            components.append("cache_cluster")

        sizes = {
            "app_servers": "t3.medium" if scale == "small" else "t3.large",
            "database": "db.t3.medium" if scale == "small" else "db.m6g.large",
        }

        observability_hooks = ["metrics: p95 latency, error rate", "logs: structured JSON", "traces: distributed tracing"]

        cost_hint = "use spot instances for noncritical workers" if scale != "small" else "low-cost tier"

        plan = {"components": components, "sizes": sizes, "observability": observability_hooks, "cost_hint": cost_hint}
        return plan

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        return await asyncio.to_thread(self.invoke, args, sly_data)
