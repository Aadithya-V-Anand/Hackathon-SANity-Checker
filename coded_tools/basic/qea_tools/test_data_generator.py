# Copyright © 2025-2026 Cognizant Technology Solutions Corp
# Licensed under the Apache License, Version 2.0

import asyncio
import logging
from typing import Any, Dict, List, Union

from neuro_san.interfaces.coded_tool import CodedTool

logger = logging.getLogger(__name__)


class TestDataGenerator(CodedTool):
    """Outlines privacy-preserving test data generation strategies."""

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        logger.info("TestDataGenerator invoked with args: %s", args)
        domains: List[str] = args.get("data_domains", []) or []
        privacy = args.get("privacy_level", "high")

        strategies: List[Dict[str, Any]] = []

        for d in domains:
            strategies.append(
                {
                    "domain": d,
                    "methods": [
                        "synthetic: schema-aware generation",
                        "masked_sample: sample + anonymize production data",
                        "edge_seeding: inject edge cases and corrupt records",
                    ],
                    "example_pseudocode": f"generate_{d}_records(count=1000, edge_cases=True)",
                    "privacy_note": "Prefer synthetic or strongly anonymized samples; do not export raw PII without authorization",
                }
            )

        return {"privacy_level": privacy, "strategies": strategies}

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        return await asyncio.to_thread(self.invoke, args, sly_data)
