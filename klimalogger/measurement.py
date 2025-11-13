from __future__ import annotations

import logging
from dataclasses import dataclass

log = logging.getLogger(__name__)


@dataclass
class Measurements:
    temperature: float | None = None
    relative_humidity: float | None = None
