from dataclasses import dataclass
from typing import Literal, List, Optional, Union

@dataclass
class StageConfig:
    driver_source: Literal["consensus", "user", "fade", "perpetual"]
    wacc: Union[float, List[float]]
    years: Optional[int] = None
    # optional per-stage tax and starting values
    tax_rate: Optional[float] = None
    initial_revenue: Optional[float] = None
    initial_invested_capital: Optional[float] = None
    # Stage 1 explicit consensus inputs
    revenue: Optional[List[float]] = None
    operating_profit: Optional[List[float]] = None
    ebit: Optional[List[float]] = None
    ebitda: Optional[List[float]] = None
    capex: Optional[List[float]] = None
    # Stage 1 user-growth inputs
    revenue_growth: Optional[List[float]] = None
    margin: Optional[List[float]] = None
    # perpetual stage
    perp_growth: Optional[float] = None

@dataclass
class MultiStageDCFConfig:
    stages: List[StageConfig]

