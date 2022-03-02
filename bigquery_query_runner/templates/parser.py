from typing import Dict, Sequence, Optional
from jinjasql import JinjaSql

PARAMETER_STYLE = "pyformat"


def parse_query(query_template: str, params_dict: Dict) -> str:
    jinja = JinjaSql(param_style=PARAMETER_STYLE)
    query, bind_params = jinja.prepare_query(query_template, params_dict)

    quoted = {param: _quote_string(value) for param, value in bind_params.items()}
    return query % quoted


def _quote_string(value):
    if isinstance(value, str):
        return f"'{value}'"
    return value


def split_parameters(parameters: Sequence[str]) -> Dict:
    parsed = dict()
    for parameter in parameters:
        name, value = parameter.split("=", 1)
        new_value = _to_int(value)
        if new_value:
            parsed.update({name: new_value})
            continue

        new_value = _to_float(value)
        if new_value:
            parsed.update({name: new_value})
            continue

        parsed.update({name: value})

    return parsed


def _to_int(value: str) -> Optional[int]:
    try:
        return int(value)
    except ValueError as exception:
        print(f"{exception}: could not convert {value} of type str into int")
        return None


def _to_float(value: str) -> Optional[float]:
    try:
        return float(value)
    except ValueError as exception:
        print(f"{exception}: could not convert {value} of type str into float")
        return None
