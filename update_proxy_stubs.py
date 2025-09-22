#!/usr/bin/env python3
"""
Script to create BingoMolProxy and BingoRxnProxy stubs in a separate proxy.py file.

This script reads the comparator classes and creates a new proxy.py file with
stub methods that match the comparator method signatures and docstrings.
The proxy classes provide type hinting and autocomplete functionality.
"""

import ast
from pathlib import Path
from typing import Any


def extract_method_info(class_node: ast.ClassDef) -> list[dict[str, Any]]:
    """
    Extract method information from an AST class node.

    Parameters
    ----------
    class_node : ast.ClassDef
        The AST node representing a class.

    Returns
    -------
    List[Dict[str, Any]]
        List of dictionaries containing method information.
    """
    methods = []

    for node in class_node.body:
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            # Extract method signature
            args = []
            for arg in node.args.args[1:]:  # Skip 'self'
                arg_name = arg.arg
                arg_type = "str"  # Default type
                default_value = ""

                # Check if there's a default value
                defaults_offset = len(node.args.args) - len(node.args.defaults) - 1
                arg_index = node.args.args.index(arg) - 1
                if arg_index >= defaults_offset and node.args.defaults:
                    default_idx = arg_index - defaults_offset
                    if default_idx < len(node.args.defaults):
                        default = node.args.defaults[default_idx]
                        if isinstance(default, ast.Constant):
                            if isinstance(default.value, str):
                                default_value = f'="{default.value}"'
                            else:
                                default_value = f"={default.value}"

                args.append(f"{arg_name}: {arg_type}{default_value}")

            # Extract docstring
            docstring = ""
            if (
                node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str)
            ):
                docstring = node.body[0].value.value

            methods.append(
                {"name": node.name, "args": args, "docstring": docstring.strip()}
            )

    return methods


def generate_proxy_method(method_info: dict[str, Any]) -> str:
    """
    Generate a proxy stub method from method information.

    Parameters
    ----------
    method_info : Dict[str, Any]
        Dictionary containing method information.

    Returns
    -------
    str
        Generated proxy stub method as a string.
    """
    method_name = method_info["name"]
    args = method_info["args"]
    docstring = method_info["docstring"]

    # Convert method signature
    args_str = ", ".join(args) if args else ""

    # Format the docstring with proper indentation
    if docstring:
        # Split docstring into lines and add proper indentation
        docstring_lines = docstring.split("\n")
        formatted_docstring = '        """' + docstring_lines[0]
        for line in docstring_lines[1:]:
            formatted_docstring += "\n        " + line
        formatted_docstring += '\n        """'
    else:
        formatted_docstring = '        """Stub method."""'

    # Generate the method stub
    stub = f"""    @staticmethod
    def {method_name}({args_str}):
{formatted_docstring}
        pass"""

    return stub


def create_proxy_file(
    mol_methods: list[dict[str, Any]], rxn_methods: list[dict[str, Any]]
):
    """
    Create a separate proxy.py file with proxy stubs.

    Parameters
    ----------
    mol_methods : List[Dict[str, Any]]
        List of molecular comparator methods.
    rxn_methods : List[Dict[str, Any]]
        List of reaction comparator methods.
    """
    proxy_path = Path("src/molalchemy/bingo/proxy.py")

    # Generate file header
    header = '''"""
Proxy classes for Bingo database operations.

This module contains proxy classes that provide stub methods for type hinting
and autocomplete functionality. The actual implementation is delegated to
the corresponding function classes in the functions module.

This file is auto-generated from the comparator classes.
Do not edit manually - use the update_proxy_stubs.py script instead.
"""

'''

    # Generate BingoMolProxy class
    mol_proxy_methods = []
    for method_info in mol_methods:
        mol_proxy_methods.append(generate_proxy_method(method_info))

    mol_proxy_class = f"""class BingoMolProxy:
    \"\"\"
    Proxy class for molecular operations using Bingo database.
    
    This class provides stub methods for type hinting and autocomplete functionality.
    The actual implementation is delegated to the corresponding function class.
    \"\"\"

{chr(10).join(mol_proxy_methods)}
    """

    # Generate BingoRxnProxy class
    rxn_proxy_methods = []
    for method_info in rxn_methods:
        rxn_proxy_methods.append(generate_proxy_method(method_info))

    rxn_proxy_class = f"""class BingoRxnProxy:
    \"\"\"
    Proxy class for chemical reaction operations using Bingo database.
    
    This class provides stub methods for type hinting and autocomplete functionality.
    The actual implementation is delegated to the corresponding function class.
    \"\"\"

{chr(10).join(rxn_proxy_methods)}
    """

    # Write the complete proxy file
    with open(proxy_path, "w") as f:
        f.write(header)
        f.write(mol_proxy_class)
        f.write("\n\n\n")
        f.write(rxn_proxy_class)
        f.write("\n")

    print(f"Created {proxy_path} with proxy stubs!")


def main():
    """Main function to create proxy stubs from comparators."""
    # Read the comparators file
    comparators_path = Path("src/molalchemy/bingo/comparators.py")

    if not comparators_path.exists():
        print(f"Error: {comparators_path} not found!")
        return

    with open(comparators_path) as f:
        source_code = f.read()

    # Parse the AST
    tree = ast.parse(source_code)

    # Extract class information
    mol_methods = []
    rxn_methods = []

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            if node.name == "BingoMolComparator":
                mol_methods = extract_method_info(node)
                print(f"Found {len(mol_methods)} methods in BingoMolComparator")
            elif node.name == "BingoRxnComparator":
                rxn_methods = extract_method_info(node)
                print(f"Found {len(rxn_methods)} methods in BingoRxnComparator")

    if mol_methods or rxn_methods:
        create_proxy_file(mol_methods, rxn_methods)
    else:
        print("No methods found to generate stubs for!")


if __name__ == "__main__":
    main()
