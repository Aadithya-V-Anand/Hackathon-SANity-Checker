# Copyright © 2025-2026 Cognizant Technology Solutions Corp, www.cognizant.com.
# Licensed under the Apache License, Version 2.0

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, Union

from neuro_san.interfaces.coded_tool import CodedTool

logger = logging.getLogger(__name__)


class VerificationAgent(CodedTool):
    """Verifies contact details and operational status with simple heuristics.

    This stub marks high confidence when phone and website are present, medium when only one is present,
    and low when neither is listed.
    """

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        logger.info("VerificationAgent invoked: %s", args)
        resource = args.get("resource_record", {}) or {}

        has_phone = bool(resource.get("phone"))
        has_website = bool(resource.get("website"))

        if has_phone and has_website:
            confidence = "high"
        elif has_phone or has_website:
            confidence = "medium"
        else:
            confidence = "low"

        result = {
            "resource_id": resource.get("id"),
            "verification_confidence": confidence,
            "verified_at": datetime.utcnow().isoformat() + "Z",
            "source": resource.get("source", "unknown"),
        }
        logger.debug("VerificationAgent result: %s", result)
        return result

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        return await asyncio.to_thread(self.invoke, args, sly_data)
