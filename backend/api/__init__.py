from fastapi import FastAPI
from pydantic import BaseModel

from ..dcf_engine.config import StageConfig, MultiStageDCFConfig
from ..dcf_engine.model import enterprise_value

app = FastAPI(title="DCF API")


class StageConfigModel(BaseModel):
    years: int
    driver_source: str
    revenue_growth: list[float] | None = None
    revenue: list[float] | None = None
    margin: list[float] | None = None
    ebit: list[float] | None = None
    nopat: list[float] | None = None
    reinvestment_rate: list[float] | None = None
    capex: list[float] | None = None
    fcf: list[float] | None = None
    wacc: list[float] | None = None
    roic_start: float | None = None
    roic_end: float | None = None
    perp_growth: float | None = None


class DCFConfigModel(BaseModel):
    stages: list[StageConfigModel]
    wacc: float
    tax_rate: float
    initial_revenue: float
    initial_invested_capital: float


@app.post("/dcf")
def run_dcf(config: DCFConfigModel) -> float:
    stages = [StageConfig(**stage.dict()) for stage in config.stages]
    ms_config = MultiStageDCFConfig(
        stages=stages,
        wacc=config.wacc,
        tax_rate=config.tax_rate,
        initial_revenue=config.initial_revenue,
        initial_invested_capital=config.initial_invested_capital,
    )
    value = enterprise_value(ms_config)
    return value

