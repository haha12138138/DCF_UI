from dataclasses import dataclass
from typing import Literal, List, Optional

@dataclass
class StageConfig:
    years: int
    driver_source: Literal["consensus", "user", "fade", "perpetual"]
    revenue_growth: Optional[List[float]] = None
    margin: Optional[List[float]] = None
    reinvestment_rate: Optional[List[float]] = None
    roic_start: Optional[float] = None
    roic_end: Optional[float] = None
    perp_growth: Optional[float] = None

@dataclass
class MultiStageDCFConfig:
    stages: List[StageConfig]
    wacc: float
    tax_rate: float
    initial_revenue: float
    initial_invested_capital: float

