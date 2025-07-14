from __future__ import annotations

from typing import List

from .config import StageConfig, MultiStageDCFConfig


def enterprise_value(config: MultiStageDCFConfig) -> float:
    """Calculate enterprise value using a three-stage DCF."""
    revenue = config.initial_revenue
    invested = config.initial_invested_capital
    value = 0.0
    period = 0
    roic = config.stages[0].roic_start or config.wacc

    for stage in config.stages:
        for idx in range(stage.years):
            period += 1
            growth = 0.0
            margin = 0.0
            reinv_rate = None
            if stage.revenue_growth and idx < len(stage.revenue_growth):
                growth = stage.revenue_growth[idx]
            if stage.margin and idx < len(stage.margin):
                margin = stage.margin[idx]
            if stage.reinvestment_rate and idx < len(stage.reinvestment_rate):
                reinv_rate = stage.reinvestment_rate[idx]

            if stage.driver_source == "fade":
                if stage.roic_start is None or stage.roic_end is None:
                    raise ValueError("Fade stage requires roic_start and roic_end")
                roic = stage.roic_start - (
                    (stage.roic_start - stage.roic_end) * ((idx + 1) / stage.years)
                )
            elif stage.roic_start is not None:
                roic = stage.roic_start

            if reinv_rate is None:
                reinv_rate = growth / roic if roic else 0.0

            revenue_next = revenue * (1 + growth)
            ebit = revenue_next * margin
            nopat = ebit * (1 - config.tax_rate)
            invested_next = invested + (revenue_next - revenue) * reinv_rate
            fcf = nopat - (invested_next - invested)
            discount = (1 + config.wacc) ** period
            value += fcf / discount
            revenue = revenue_next
            invested = invested_next

        if stage.driver_source == "perpetual":
            g = stage.perp_growth or 0.0
            terminal_nopat = revenue * margin * (1 - config.tax_rate)
            terminal_reinv = g / roic if roic else 0.0
            terminal_fcf = terminal_nopat * (1 - terminal_reinv)
            terminal_value = terminal_fcf * (1 + g) / (config.wacc - g)
            value += terminal_value / ((1 + config.wacc) ** period)
            break

    return value
