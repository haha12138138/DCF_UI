import json
import argparse

from .dcf_engine.config import StageConfig, MultiStageDCFConfig
from .dcf_engine.model import enterprise_value


def load_config(path: str) -> MultiStageDCFConfig:
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    stages = [StageConfig(**s) for s in data["stages"]]
    return MultiStageDCFConfig(
        stages=stages,
        wacc=data["wacc"],
        tax_rate=data["tax_rate"],
        initial_revenue=data["initial_revenue"],
        initial_invested_capital=data["initial_invested_capital"],
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run DCF model from JSON config")
    parser.add_argument("config", help="Path to config JSON")
    args = parser.parse_args()
    cfg = load_config(args.config)
    value = enterprise_value(cfg)
    print(f"Enterprise value: {value:.2f}")


if __name__ == "__main__":
    main()

