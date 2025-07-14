import json
import os
import sys

sys.path.append(os.path.abspath('.'))

from backend.dcf_engine.config import StageConfig, MultiStageDCFConfig
from backend.dcf_engine.model import enterprise_value


def test_enterprise_value_sample():
    with open('sample_config.json', 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    stages = [StageConfig(**s) for s in data['stages']]
    cfg = MultiStageDCFConfig(stages=stages)
    value = enterprise_value(cfg)
    assert round(value, 2) == 177.21

