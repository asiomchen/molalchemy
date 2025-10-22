import json
from collections import defaultdict
from pathlib import Path

from jinja2 import Environment

HEADERS = """
\"\"\"Auto-generated from data/bingo_functions.json. Do not edit manually.\"\"\"
from molalchemy.types import CString
from molalchemy.bingo.types import BingoBinaryMol, BingoBinaryReaction, BingoMol, BingoReaction
from sqlalchemy import types as sqltypes
from sqlalchemy.sql import cast, text
from sqlalchemy import Cast
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.sql.functions import GenericFunction
from typing import Any, Literal

AnyBingoMol = BingoMol | BingoBinaryMol

\n\n
"""
AFTER_HEADERS = defaultdict(str)
EXTRA_MEMBERS = defaultdict(list)
AFTER_HEADERS["general"] = Path("data/extra_bingo.py_").open("r").read()
EXTRA_MEMBERS["general"] = [
    "has_substructure",
    "matches_smarts",
    "mol_equals",
    "similarity",
]

DATA_PATH = Path("data/bingo_functions.json")

MODULE_PATH = "src/molalchemy/bingo/functions"

_TEMPLATE = """
class {{ func_name }}(GenericFunction):
    \"""
    {{ description }}
    \n
    Parameters
    ----------
    {{ params }}
    \n
    Returns
    -------
    Function[{{ return_type }}]
        {{ return_description }}
    \"""
    {% if '|' not in return_type %}
    type = {{ return_type }}()
    {% elif 'BingoMol' in return_type %}
    type = BingoMol()
    {% elif 'BingoBinaryMol' in return_type %}
    type = BingoBinaryMol()
    {% elif 'BingoReaction' in return_type %}
    type = BingoReaction()
    {% elif 'BingoBinaryReaction' in return_type %}
    type = BingoBinaryReaction()
    {% endif %}
    inherit_cache = True
    name = "{{ func_name.lower() }}"
    def __init__(self, {{ arg_inits }}**kwargs: Any) -> None:
        \"""
        {{ description }}
        \n
        Parameters
        ----------
        {{ params }}

        Returns
        -------
        Function[{{ return_type }}]
            {{ return_description }}
        \"""
        super().__init__({{ arg_names }}**kwargs)
        self.packagenames = ("bingo",)

"""


ENV = Environment()
TEMPLATE = ENV.from_string(_TEMPLATE)

with DATA_PATH.open("r") as f:
    data = json.load(f)


def json_to_function_code(func_name: str, test_data: dict) -> str:
    global TEMPLATE
    description = test_data["description"]
    params_list = []
    doc_param_list = []
    arg_names = []
    for param in test_data["args"]:
        param_str = f"{param['name']}: {param['type']}"
        if param["default"] is not None:
            param_str += f" = {param['default']}"
        params_list.append(param_str)
        param_str += f"  \n{param['description']}"
        doc_param_list.append(param_str)
        arg_names.append(param["name"])
    doc_params = "    ".join(doc_param_list)
    print(doc_params)
    params = ", ".join(params_list)
    if len(params) > 0:
        params += ", "
    if len(arg_names) > 0:
        arg_names_str = ", ".join(arg_names) + ", "
    else:
        arg_names_str = ""
    generated_code = TEMPLATE.render(
        func_name=func_name,
        description=description,
        params=doc_params,
        arg_inits=params,
        arg_names=arg_names_str,
        return_type=test_data["return_type"]["type"],
        return_description=test_data["return_type"]["description"],
    )
    return generated_code


groups = defaultdict(list)
group_members = defaultdict(list)

allowed_groups = {"general", "internal"}
for func_name, func_data in data.items():
    code = json_to_function_code(func_name, func_data)
    group = func_data.get("group", "general")
    if group not in allowed_groups:
        group = "general"
    groups[group].append(code)
    group_members[group].append(func_name)

for group in EXTRA_MEMBERS:
    group_members[group].extend(EXTRA_MEMBERS[group])

for group, codes in groups.items():
    module_code = HEADERS + AFTER_HEADERS[group] + "\n".join(codes)
    module_path = Path(f"{MODULE_PATH}/{group}.py")
    with module_path.open("w") as f:
        f.write(module_code)
    print(f"Wrote {module_path} with {len(codes)} functions.")

# update init file
init_path = Path(f"{MODULE_PATH}/__init__.py")
_all = []
with init_path.open("w") as f:
    for group, members in group_members.items():
        f.write(f"from .{group} import " + ", ".join(members) + "\n")
        _all.extend(members)
    f.write("\n__all__ = [\n")
    for name in _all:
        f.write(f"    '{name}',\n")
    f.write("]\n")
    print(f"Updated {init_path}.")
