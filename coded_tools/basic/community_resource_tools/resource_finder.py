# Copyright © 2025-2026 Cognizant Technology Solutions Corp, www.cognizant.com.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# END COPYRIGHT

import asyncio
import logging
from typing import Any, Dict, List, Union

from neuro_san.interfaces.coded_tool import CodedTool

logger = logging.getLogger(__name__)


class ResourceFinder(CodedTool):
    """Searches authoritative sources and returns a short ranked list of resources.

    This is a light-weight, privacy-preserving stub implementation suitable for
    initial development and tests. Real deployments should integrate with
    local directories, 2-1-1 APIs, or municipal open-data endpoints.
    """

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        logger.info("ResourceFinder invoked with args: %s", args)
        location = args.get("location", "")
        service_type = args.get("service_type", "general")
        urgency = args.get("urgency", "flexible")

        # Create deterministic-ish dummy results based on inputs
        resources: List[Dict[str, Any]] = []
        for i in range(1, 4):
            rid = f"res-{service_type[:3]}-{i}"
            resources.append(
                {
                    "id": rid,
                    "name": f"{service_type.title()} Center {i}",
                    "address": f"{100 + i} Main St, near {location}",
                    "hours": "9:00-17:00",
                    "phone": f"+1-555-010{i}",
                    "source": "community_directory",
                    "distance_km": round(0.5 * i, 2),
                    "expected_wait": "variable",
                }
            )

        response = {"resources": resources, "query": {"location": location, "service_type": service_type, "urgency": urgency}}
        logger.debug("ResourceFinder response: %s", response)
        return response

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        return await asyncio.to_thread(self.invoke, args, sly_data)
