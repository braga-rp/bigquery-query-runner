import os
from typing import Sequence, Dict, Optional, Callable


def report_output(output_paths):
    print("results saved at:")
    for output_path in output_paths:
        print(output_path)


def get_env(name, default=None) -> Callable[[], str]:
    def run():
        return os.environ.get(name, default)
    return run


def split_parameters(parameters: Sequence[str]) -> Dict:
    parsed = dict()
    for parameter in parameters:
        name, value = parameter.split("=", 1)
        new_value = to_int(value)
        if new_value:
            parsed.update({name: new_value})
            continue

        new_value = to_float(value)
        if new_value:
            parsed.update({name: new_value})
            continue

        parsed.update({name: value})

    return parsed


def to_int(value: str) -> Optional[int]:
    try:
        return int(value)
    except Exception:
        return None


def to_float(value) -> Optional[float]:
    try:
        return float(value)
    except Exception:
        return None