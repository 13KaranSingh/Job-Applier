from pathlib import Path

import yaml


def load_operator_config(path: str = "config/operator.yaml") -> dict:
    return yaml.safe_load(Path(path).read_text())

