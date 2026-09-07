# Copyright © 2025-2026 Cognizant Technology Solutions Corp, www.cognizant.com.
# Licensed under the Apache License, Version 2.0

import asyncio
import logging
from typing import Any, Dict, Union

from neuro_san.interfaces.coded_tool import CodedTool

logger = logging.getLogger(__name__)


class Coordinator(CodedTool):
    """Produces short, privacy-preserving coordination plans and templates.

    The coordinator does not contact external services directly; it prepares checklists,
    scripts, and schedules that a human operator can carry out.
    """

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        logger.info("Coordinator invoked with args: %s", args)
        task = args.get("task", "general")
        details = args.get("details", {}) or {}

        if task == "volunteer_delivery":
            plan = {
                "task": task,
                "checklist": [
                    "Confirm recipient availability",
                    "Pack items securely",
                    "Follow safety guidelines",
                    "Record completion/check-in",
                ],
                "suggested_schedule": details.get("suggested_schedule", "Tomorrow morning 9:00-11:00"),
                "contact_script": "Hi, I'm calling from [Org]. I'm scheduled to deliver groceries tomorrow between 9-11. Is that still good?",  # noqa: E501
            }
        elif task == "appointment_booking":
            plan = {
                "task": task,
                "steps": [
                    "Call the resource phone during listed hours",
                    "Use this quick script: 'Hello, I'm calling to schedule an appointment for...'",
                    "Have these documents ready: proof of residency, photo ID",
                ],
            }
        else:
            plan = {"task": task, "note": "Provide specific task details to get a tailored plan."}

        logger.debug("Coordinator plan: %s", plan)
        return plan

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        return await asyncio.to_thread(self.invoke, args, sly_data)
