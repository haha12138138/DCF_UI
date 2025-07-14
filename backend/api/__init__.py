from fastapi import FastAPI
from pydantic import BaseModel

from ..dcf_engine.config import StageConfig, MultiStageDCFConfig
from ..dcf_engine.model import enterprise_value

app = FastAPI(title="DCF API")


class StageConfigModel(BaseModel):
    driver_source: str
    wacc: float | list[float]
    years: int | None = None
    tax_rate: float | None = None
    initial_revenue: float | None = None
    initial_invested_capital: float | None = None
    revenue: list[float] | None = None
    operating_profit: list[float] | None = None
    ebit: list[float] | None = None
    ebitda: list[float] | None = None
    capex: list[float] | None = None
    revenue_growth: list[float] | None = None
    margin: list[float] | None = None
    perp_growth: float | None = None


class DCFConfigModel(BaseModel):
    stages: list[StageConfigModel]


@app.post("/dcf")
def run_dcf(config: DCFConfigModel) -> float:
    stages = [StageConfig(**stage.dict()) for stage in config.stages]
    ms_config = MultiStageDCFConfig(stages=stages)
    value = enterprise_value(ms_config)
    return value

