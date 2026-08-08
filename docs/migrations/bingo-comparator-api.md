# Migrating the Bingo comparator API

This guide covers the breaking Bingo comparator changes introduced during the
v0.x API cleanup. No database schema migration is required: `BingoMol`,
`BingoBinaryMol`, `BingoReaction`, and `BingoBinaryReaction` retain their
existing PostgreSQL storage types and constructors.

The main migration is to make chemical equality explicit. Search predicates
also have more precise result and operand types, and molecule similarity is now
available directly from the comparator.

## Chemical equality is now explicit

The custom Bingo `__eq__` and `__ne__` implementations were removed. Normal
Python comparison operators now use PostgreSQL storage equality; named methods
perform Bingo chemical matching.

| Intent | Previous API | New API |
| --- | --- | --- |
| Molecule exact match | `column == query` | `column.equals(query)` |
| Molecule exact mismatch | `column != query` | `column.not_equals(query)` |
| Reaction exact match | `column == query` | `column.equals(query)` |
| Reaction exact mismatch | `column != query` | `column.not_equals(query)` |
| Storage equality | Operand-dependent | `column == query` |
| Storage inequality | Operand-dependent | `column != query` |

The old implementation could choose different behavior for literals and
table-bound expressions. The replacement rules above describe intent: migrate
every chemical comparison to a named method, regardless of operand shape.

For example:

```python
# Before: overloaded == requested a Bingo exact search.
stmt = select(Compound).where(Compound.structure == "OCC")

# After: chemical intent is explicit.
stmt = select(Compound).where(Compound.structure.equals("OCC"))

# Negated Bingo exact search.
different = select(Compound).where(
    Compound.structure.not_equals("OCC")
)
```

The explicit methods accept the same optional Bingo search parameters:

```python
stereo_match = Compound.structure.equals(query, "STE")
tautomer_match = Compound.structure.equals(query, "TAU")
```

The standalone helpers remain available:

```python
from molalchemy.bingo import functions as bingo_func

mol_predicate = bingo_func.mol_equals(Compound.structure, query, "STE")
rxn_predicate = bingo_func.rxn_equals(Reaction.reaction, query_reaction)
```

## Storage equality is not chemical equality

The meaning of native `==` and `!=` depends on the underlying PostgreSQL
storage type:

| MolAlchemy type | PostgreSQL storage | Native comparison |
| --- | --- | --- |
| `BingoMol` | `varchar` | Text equality |
| `BingoReaction` | `varchar` | Text equality |
| `BingoBinaryMol` | `bytea` | Binary equality |
| `BingoBinaryReaction` | `bytea` | Binary equality |

Chemically equivalent representations are not guaranteed to have equal
storage. For example, `CCO` and `OCC` match with Bingo exact search but compare
unequal with native text equality. Compact binary representations likewise
must not be used as a substitute for chemical equality.

This differs from RDKit molecule columns, where PostgreSQL implements native
`=` and explicit `@=` with the same chemical `mol_eq` function.

## Null comparisons

`None` now follows standard SQLAlchemy semantics without comparator-specific
branches:

```python
Compound.structure == None  # IS NULL
Compound.structure != None  # IS NOT NULL
```

Use `is_(None)` and `is_not(None)` if explicit SQL-style spelling is preferred.

## Similarity comparator

Molecule columns expose separate APIs for Boolean similarity searches and
numeric similarity scores. `similar_to()` is the comparator equivalent of
`bingo_func.mol_similar_to()`:

```python
predicate = Compound.structure.similar_to(
    query,
    minimum=0.7,
    maximum=1.0,
    metric="Tanimoto",
)
stmt = select(Compound).where(predicate)
```

`similar_to()` returns a Boolean range predicate. It does not return a numeric
similarity score. Use `similarity_score()` or
`bingo_func.mol_similarity_score()` when the score itself is needed:

```python
score = Compound.structure.similarity_score(query, metric="Tanimoto")
functional_score = bingo_func.mol_similarity_score(
    Compound.structure, query, metric="Tanimoto"
)
```

The cartridge-level `getsimilarity()` wrapper remains available. The older
`mol_similarity()` predicate also remains as a compatibility spelling and
retains its `bottom` and `top` keyword names; new code should use
`mol_similar_to()` with `minimum` and `maximum`.

## Boolean expression results

Molecule and reaction search methods now return `ColumnElement[bool]` backed by
SQLAlchemy `Boolean`. This applies to substructure, SMARTS, exact, negated
exact, and similarity predicates.

They can be composed and labeled like ordinary SQLAlchemy predicates:

```python
aromatic = Compound.structure.has_substructure("c1ccccc1")
not_ethanol = Compound.structure.not_equals("CCO")

stmt = select(Compound).where(aromatic & not_ethanol)
labeled = select(aromatic.label("is_aromatic"))
```

## SQL expression operands

Search inputs can be Python literals, explicit bind parameters, Core columns,
subquery columns, or ORM mapped attributes. Scalars remain bound parameters;
SQL expressions remain expressions.

```python
# ORM column-to-column exact search
predicate = Compound.structure.equals(Compound.reference_structure)

# A mapped attribute can also supply search parameters.
configured = Compound.structure.equals(
    Compound.reference_structure,
    Compound.exact_parameters,
)
```

This behavior is shared by comparator methods and standalone helpers. It also
applies to the query, similarity bounds, and metric operands where their typed
interfaces accept SQL expressions.

## Typed column helpers

Direct comparator calls remain the runtime API. Use the typed helpers when an
editor or static analyzer needs the cartridge-specific method surface:

```python
from molalchemy.helpers import bingo_col, bingo_rxn_col

mol_predicate = bingo_col(Compound.structure).equals(query)
similarity = bingo_col(Compound.structure).similar_to(query, minimum=0.8)
rxn_predicate = bingo_rxn_col(Reaction.reaction).has_substructure(query_reaction)
```

Both helpers validate the MolAlchemy column type and return the original
SQLAlchemy column at runtime. They accept Core columns and ORM mapped
attributes.

The old generated `BingoMolProxy` and `BingoRxnProxy` exports were
removed. Their replacements are typed protocols normally accessed through
`bingo_col()` and `bingo_rxn_col()`.

## Unchanged APIs

The following APIs do not require migration:

- `has_substructure()` and `has_smarts()` method names and parameters.
- The prefixed standalone helpers such as `mol_has_substructure()`,
  `mol_has_smarts()`, `rxn_has_substructure()`, and `rxn_has_smarts()`.
- Bingo type constructors, indexes, conversions, descriptors, imports,
  exports, and property functions.

## Migration checklist

1. Replace chemical `column == query` with `column.equals(query)`.
2. Replace chemical `column != query` with `column.not_equals(query)`.
3. Keep `== None`/`!= None`, or use `is_(None)`/`is_not(None)`.
4. Treat native equality as text or binary storage equality only.
5. Use `similar_to()`/`mol_similar_to()` for predicates and
   `similarity_score()`/`mol_similarity_score()` for numeric scores.
6. Replace removed proxy imports with `bingo_col()` or `bingo_rxn_col()`.
