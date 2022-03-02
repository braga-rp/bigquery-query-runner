from typing import Dict
from jinjasql import JinjaSql


def parse_query(query_template: str, params: Dict) -> str:
    jinja = JinjaSql(param_style="pyformat")
    query, bind_params = jinja.prepare_query(query_template, params)

    quoted = {param: _quote_string(value) for param, value in bind_params.items()}

    return query % quoted


def _quote_string(value):
    if isinstance(value, str):
        return f"'{value}'"
    return value
