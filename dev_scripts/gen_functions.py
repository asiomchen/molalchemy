#!/usr/bin/env python3
"""
Unified function generator script that uses external Jinja templates.

This script generates SQLAlchemy function classes from JSON definitions,
using separate Jinja2 template files for better maintainability.
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


def json_to_function_code(func_name: str, data: dict, template) -> str:
    """Generate function code from JSON data using Jinja template.

    Parameters
    ----------
    func_name : str
        Name of the function class to generate
    data : dict
        Function metadata from JSON
    template : jinja2.Template
        Jinja template for rendering the function

    Returns
    -------
    str
        Generated Python code for the function class
    """
    description = data["description"]
    params_list = []
    doc_param_list = []
    arg_names = []

    # Process function arguments
    for param in data["args"]:
        param_str = f"{param['name']}: {param['type']}"
        if param["default"] is not None:
            param_str += f" = {param['default']}"
        params_list.append(param_str)

        # Add parameter description for docstring
        param_doc = f"{param['name']}"
        if param["description"]:
            param_doc += f"\n\t    {param['description']}"
        doc_param_list.append(param_doc)
        arg_names.append(param["name"])

    # Format parameters for template
    doc_params = "\n        ".join(doc_param_list)
    params = ", ".join(params_list)
    if len(params) > 0:
        params += ", "
    if len(arg_names) > 0:
        arg_names_str = ", ".join(arg_names) + ", "
    else:
        arg_names_str = ""

    # Render the template
    generated_code = template.render(
        func_name=func_name,
        description=description,
        params=doc_params,
        arg_inits=params,
        arg_names=arg_names_str,
        return_type=data["return_type"]["type"],
        return_description=data["return_type"]["description"],
    )
    return generated_code


def load_headers_and_extras(
    target: str,
) -> tuple[dict[str, str], dict[str, str], dict[str, list[str]]]:
    """Load header files, extra content, and configuration.

    Parameters
    ----------
    target : str
        Target system (e.g., 'bingo', 'rdkit')

    Returns
    -------
    tuple[Dict[str, str], Dict[str, str], Dict[str, List[str]]]
        Headers, extra content after headers, and extra members
    """
    headers: dict[str, str] = defaultdict(str)
    after_headers: dict[str, str] = defaultdict(str)
    extra_members: dict[str, list[str]] = defaultdict(list)

    data_path = Path(f"data/{target}")

    # Load headers
    for file in data_path.glob("*_header.txt"):
        group_name = file.stem.replace("_header", "")
        headers[group_name] += file.read_text()

    # Load extra content
    for file in data_path.glob("*_extra.txt"):
        group_name = file.stem.replace("_extra", "")
        after_headers[group_name] += file.read_text()

    # For compatibility with existing files
    for file in data_path.glob("extra.py_"):
        after_headers["general"] += file.read_text()

    # Load configuration
    config_path = data_path / "config.json"
    if config_path.exists():
        with config_path.open("r") as f:
            config = json.load(f)

        for group, group_config in config.items():
            extra_members_list = group_config.get("extra_members", [])
            extra_members[group].extend(extra_members_list)

    return headers, after_headers, extra_members


def generate_functions(
    target: str = "bingo",
    allowed_groups: set[str] = {"general", "internal"},
    template_dir: str = "dev_scripts/templates",
) -> None:
    """Generate function modules from JSON definitions using external templates.

    Parameters
    ----------
    target : str, default="bingo"
        Target system to generate functions for
    allowed_groups : Set[str], default={"general", "internal"}
        Set of allowed function groups
    template_dir : str, default="dev_scripts/templates"
        Directory containing Jinja templates
    """
    print(f"Generating {target} functions...")

    # Setup paths
    data_path = Path(f"data/{target}/functions.json")
    module_path = Path(f"src/molalchemy/{target}/functions")
    template_path = Path(template_dir)

    if not data_path.exists():
        print(f"Error: Function definitions not found at {data_path}")
        return

    if not template_path.exists():
        print(f"Error: Template directory not found at {template_path}")
        return

    # Load headers, extras, and configuration
    headers, after_headers, extra_members = load_headers_and_extras(target)

    # Setup Jinja environment
    env = Environment(
        loader=FileSystemLoader(template_path), trim_blocks=True, lstrip_blocks=True
    )

    # Load the function template
    template_name = f"{target}_function.j2"
    try:
        template = env.get_template(template_name)
    except Exception as e:
        print(f"Error loading template {template_name}: {e}")
        return

    # Load function definitions
    with data_path.open("r") as f:
        data: dict = json.load(f)

    if not data:
        print(f"No function definitions found in {data_path}")
        return

    groups = defaultdict(list)
    group_members = defaultdict(list)

    # Generate function code
    for func_name, func_data in data.items():
        try:
            code = json_to_function_code(func_name, func_data, template)
            group = func_data.get("group", "general")
            if group not in allowed_groups:
                group = "general"
            groups[group].append(code)
            group_members[group].append(func_name)
        except Exception as e:
            print(f"Error generating code for {func_name}: {e}")
            continue

    # Add extra members to groups
    for group, members in extra_members.items():
        group_members[group].extend(members)

    # Create module directory
    module_path.mkdir(parents=True, exist_ok=True)

    # Write group modules
    for group, codes in groups.items():
        if not codes:
            continue

        module_code_parts = []
        if headers[group]:
            module_code_parts.append(headers[group])
        if after_headers[group]:
            module_code_parts.append(after_headers[group])
        module_code_parts.extend(codes)

        module_code = "\n\n".join(module_code_parts)
        group_module_path = module_path / f"{group}.py"

        with group_module_path.open("w") as f:
            f.write(module_code)
        print(f"Wrote {group_module_path} with {len(codes)} functions.")

    # Update __init__.py file
    init_path = module_path / "__init__.py"
    all_members = []

    with init_path.open("w") as f:
        # Write imports
        INIT_HEADER = Path(f"data/{target}/init.txt").read_text()
        f.write(INIT_HEADER + "\n\n")
        for group, members in sorted(group_members.items()):
            if members:
                f.write(f"from .{group} import " + ", ".join(sorted(members)) + "\n")
                all_members.extend(members)

        # Write __all__
        f.write("\n__all__ = [\n")
        for name in sorted(all_members):
            f.write(f"    '{name}',\n")
        f.write("]\n")

    print(f"Updated {init_path} with {len(all_members)} total functions.")


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = "bingo"

    if target not in ["bingo", "rdkit"]:
        print(f"Error: Unknown target '{target}'. Supported targets: bingo, rdkit")
        sys.exit(1)

    try:
        generate_functions(target)
        print(f"Successfully generated {target} functions!")
    except Exception as e:
        print(f"Error generating {target} functions: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
