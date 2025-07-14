from __future__ import annotations

from typing import Iterable, List

from .config import StageConfig, MultiStageDCFConfig


def _wacc_series(wacc: float | List[float], years: int) -> Iterable[float]:
    if isinstance(wacc, list):
        return [wacc[min(i, len(wacc) - 1)] for i in range(years)]
    return [wacc] * years


def enterprise_value(config: MultiStageDCFConfig) -> float:
    """Calculate enterprise value using a three-stage DCF."""
    # use initial settings from the first stage
    first = config.stages[0]
    revenue = first.initial_revenue or 0.0
    invested = first.initial_invested_capital or 0.0
    tax_rate = first.tax_rate or 0.0
    value = 0.0
    period = 0
    margin = 0.0
    roic = 0.0
    growth_last = 0.0

    for idx_stage, stage in enumerate(config.stages):
        if stage.driver_source == "perpetual":
            wacc_val = stage.wacc if not isinstance(stage.wacc, list) else stage.wacc[0]
            g = stage.perp_growth or 0.0
            stage_tax = stage.tax_rate if stage.tax_rate is not None else tax_rate
            nopat = revenue * margin * (1 - stage_tax)
            reinv = g / wacc_val if wacc_val else 0.0
            terminal_fcf = nopat * (1 - reinv)
            terminal_value = terminal_fcf * (1 + g) / (wacc_val - g)
            value += terminal_value / ((1 + wacc_val) ** period)
            break

        years = stage.years or 0
        for year_idx, wacc_year in enumerate(_wacc_series(stage.wacc, years)):
            period += 1

            if stage.driver_source == "consensus":
                stage_tax = stage.tax_rate if stage.tax_rate is not None else tax_rate
                revenue_next = stage.revenue[year_idx]
                ebit = stage.ebit[year_idx]
                capex = stage.capex[year_idx]
                margin = ebit / revenue_next if revenue_next else 0.0
                nopat = ebit * (1 - stage_tax)
                roic = nopat / invested if invested else 0.0
                invested_next = invested + capex
                fcf = nopat - capex
                growth = revenue_next / revenue - 1 if revenue else 0.0

            elif stage.driver_source == "user":
                stage_tax = stage.tax_rate if stage.tax_rate is not None else tax_rate
                growth = stage.revenue_growth[year_idx]
                revenue_next = revenue * (1 + growth)
                margin = stage.margin[year_idx]
                ebit = revenue_next * margin
                nopat = ebit * (1 - stage_tax)
                roic = nopat / invested if invested else 0.0
                reinv_rate = growth / roic if roic else 0.0
                capex = (revenue_next - revenue) * reinv_rate
                invested_next = invested + capex
                fcf = nopat - capex

            elif stage.driver_source == "fade":
                stage_tax = stage.tax_rate if stage.tax_rate is not None else tax_rate
                target_roic = stage.wacc if isinstance(stage.wacc, float) else stage.wacc[min(year_idx, len(stage.wacc) - 1)]
                roic = roic - (roic - target_roic) / (years - year_idx)
                next_growth = 0.0
                if idx_stage + 1 < len(config.stages):
                    next_stage = config.stages[idx_stage + 1]
                    next_growth = getattr(next_stage, "perp_growth", 0.0) or 0.0
                growth = growth_last - (growth_last - next_growth) / (years - year_idx)
                revenue_next = revenue * (1 + growth)
                ebit = revenue_next * margin
                nopat = ebit * (1 - stage_tax)
                reinv_rate = growth / roic if roic else 0.0
                capex = (revenue_next - revenue) * reinv_rate
                invested_next = invested + capex
                fcf = nopat - capex
            else:
                raise ValueError(f"Unknown stage type: {stage.driver_source}")

            discount = (1 + wacc_year) ** period
            value += fcf / discount
            revenue = revenue_next
            invested = invested_next
            growth_last = growth
            if stage.tax_rate is not None:
                tax_rate = stage.tax_rate

    return value
