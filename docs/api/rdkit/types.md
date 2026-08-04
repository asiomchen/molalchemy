# Data Types

The `molalchemy.rdkit.types` module provides SQLAlchemy UserDefinedType classes for working with chemical molecules using the RDKit PostgreSQL cartridge.

These data types enable seamless integration between Python and PostgreSQL for chemical data using RDKit's powerful cheminformatics capabilities, providing efficient storage and specialized comparison operators for molecular searching.

## Molecule equality

Equality on an RDKit `mol` column is chemical, even when expressed with normal
SQLAlchemy operators. PostgreSQL's RDKit cartridge implements `=` with
`mol_eq` and `<>` with `mol_ne`; it does not compare the original SMILES text
or serialized molecule bytes. Consequently, equivalent representations such
as `CCO` and `OCC` compare equal.

```python
# Compiles with PostgreSQL `=` and uses RDKit's chemical `mol_eq` function.
stmt = select(Molecule).where(Molecule.structure == "OCC")

# Explicit cartridge spelling. `@=` is also implemented by `mol_eq`.
explicit_stmt = select(Molecule).where(Molecule.structure.equals("OCC"))
```

The operator pairs have the same RDKit backend semantics:

| Python API | SQL operator | RDKit function |
| --- | --- | --- |
| `column == query` | `=` | `mol_eq` |
| `column.equals(query)` | `@=` | `mol_eq` |
| `column != query` | `<>` | `mol_ne` |
| `column.not_equals(query)` | `@<>` | `mol_ne` |

The explicit methods remain useful for readability and for the typed helper
form, but they do not provide a stricter kind of molecular equality. Equality
follows RDKit cartridge settings: for example, stereochemistry is ignored by
default and is considered when `rdkit.do_chiral_sss` is enabled. Isotopically
different molecules compare unequal.

Comparisons with `None` retain standard SQL behavior: `column == None` and
`column != None` compile to `IS NULL` and `IS NOT NULL`, respectively.

This differs from Bingo columns, whose native `==` and `!=` compare the stored
text or compact binary representation. Use Bingo's explicit `.equals()` and
`.not_equals()` methods for chemical equality. Also use the explicit methods
for RDKit `reaction` columns: the cartridge implements reaction `@=` and `@<>`,
but its native reaction `=` operator is only an unimplemented catalog shell.

## Type Classes

::: molalchemy.rdkit.types
    options:
      heading_level: 3
      show_source: false
      show_bases: true
      show_root_heading: false
      members_order: source
