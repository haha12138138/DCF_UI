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
    margin = 0.0

    for stage in config.stages:
        for idx in range(stage.years):
            period += 1
            # determine discount rate
            stage_wacc = config.wacc
            if stage.wacc and idx < len(stage.wacc):
                stage_wacc = stage.wacc[idx]

            # revenue and growth
            if stage.revenue and idx < len(stage.revenue):
                revenue_next = stage.revenue[idx]
                growth = revenue_next / revenue - 1
            else:
                growth = 0.0
                if stage.revenue_growth and idx < len(stage.revenue_growth):
                    growth = stage.revenue_growth[idx]
                revenue_next = revenue * (1 + growth)

            # EBIT and margin
            if stage.ebit and idx < len(stage.ebit):
                ebit = stage.ebit[idx]
                margin = ebit / revenue_next if revenue_next else 0.0
            else:
                if stage.margin and idx < len(stage.margin):
                    margin = stage.margin[idx]
                ebit = revenue_next * margin

            # NOPAT
            if stage.nopat and idx < len(stage.nopat):
                nopat = stage.nopat[idx]
            else:
                nopat = ebit * (1 - config.tax_rate)

            # ROIC updates for fade stage
            if stage.driver_source == "fade":
                if stage.roic_start is None or stage.roic_end is None:
                    raise ValueError("Fade stage requires roic_start and roic_end")
                roic = stage.roic_start - (
                    (stage.roic_start - stage.roic_end) * ((idx + 1) / stage.years)
                )
            elif stage.roic_start is not None and stage.driver_source != "perpetual":
                roic = stage.roic_start

            # capex / reinvestment
            if stage.capex and idx < len(stage.capex):
                capex = stage.capex[idx]
            else:
                reinv_rate = None
                if stage.reinvestment_rate and idx < len(stage.reinvestment_rate):
                    reinv_rate = stage.reinvestment_rate[idx]
                if reinv_rate is None:
                    reinv_rate = growth / roic if roic else 0.0
                capex = (revenue_next - revenue) * reinv_rate

            if stage.fcf and idx < len(stage.fcf):
                fcf = stage.fcf[idx]
                invested_next = invested + capex
            else:
                invested_next = invested + capex
                fcf = nopat - capex

            discount = (1 + stage_wacc) ** period
            value += fcf / discount
            revenue = revenue_next
            invested = invested_next

        if stage.driver_source == "perpetual":
            g = stage.perp_growth or 0.0
            terminal_nopat = revenue * margin * (1 - config.tax_rate)
            terminal_reinv = g / roic if roic else 0.0
            terminal_fcf = terminal_nopat * (1 - terminal_reinv)
            stage_wacc = config.wacc
            if stage.wacc and len(stage.wacc) > 0:
                stage_wacc = stage.wacc[0]
            terminal_value = terminal_fcf * (1 + g) / (config.wacc - g)
            value += terminal_value / ((1 + stage_wacc) ** period)
            break

    return value
