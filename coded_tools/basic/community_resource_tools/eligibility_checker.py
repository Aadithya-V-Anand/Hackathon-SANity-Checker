# Copyright © 2025-2026 Cognizant Technology Solutions Corp, www.cognizant.com.
# Licensed under the Apache License, Version 2.0

import asyncio
import logging
from typing import Any, Dict, Union

from neuro_san.interfaces.coded_tool import CodedTool

logger = logging.getLogger(__name__)


class EligibilityChecker(CodedTool):
    """Assesses likely eligibility for a resource using non-sensitive attributes.

    This is a heuristic stub: real implementations should load program rules
    and integrate with authoritative eligibility services.
    """

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        logger.info("EligibilityChecker invoked with args: %s", args)
        resource_id = args.get("resource_id")
        household = args.get("household", {}) or {}

        # Simple heuristics: if household_size>4 or income_bracket in ["low","very_low"] then likely
        hs = int(household.get("household_size", 1))
        income = str(household.get("income_bracket", "unknown")).lower()

        if income in ("very_low", "low") or hs >= 4:
            eligibility = "likely"
        elif income in ("medium",) and hs <= 2:
            eligibility = "needs_documents"
        else:
            eligibility = "unlikely"

        required_docs = []
        if eligibility in ("likely", "needs_documents"):
            required_docs = ["proof_of_residency", "photo_id", "proof_of_income"]

        result = {"resource_id": resource_id, "eligibility": eligibility, "required_documents": required_docs}
        logger.debug("EligibilityChecker result: %s", result)
        return result

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        return await asyncio.to_thread(self.invoke, args, sly_data)
