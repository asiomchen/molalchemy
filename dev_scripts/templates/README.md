# Function Generator Templates

This directory contains Jinja2 templates used by the function generator script to create SQLAlchemy function classes.

## Structure

- `bingo_function.j2` - Template for Bingo cartridge functions
- `rdkit_function.j2` - Template for RDKit cartridge functions

## Template Variables

Each template receives the following variables:

- `func_name` - The name of the function class (e.g., `ExactStructure`)
- `description` - Function description for the docstring
- `params` - Formatted parameter documentation for the docstring
- `arg_inits` - Parameter list for the `__init__` method
- `arg_names` - Argument names for the super().__init__() call
- `return_type` - The SQLAlchemy return type
- `return_description` - Description of the return value

## Usage

The templates are used by `../gen_functions.py`:

```bash
# Generate bingo functions
python dev_scripts/gen_functions.py bingo

# Generate rdkit functions  
python dev_scripts/gen_functions.py rdkit
```

## Template Syntax

The templates use Jinja2 syntax with conditional logic for determining the correct SQLAlchemy type based on the return type string.

Example:
```jinja2
{% if '|' not in return_type %}
type = {{ return_type }}()
{% elif 'BingoMol' in return_type %}
type = BingoMol()
{% endif %}
```

## Customization

To modify the generated function structure, edit the appropriate template file. Changes will be applied to all functions the next time the generator is run.