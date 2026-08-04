# Migrating the RDKit comparator API

This guide covers the breaking RDKit comparator changes introduced during the
v0.x API cleanup. No database schema migration is required: `RdkitMol`,
`RdkitReaction`, `RdkitBitFingerprint`, and `RdkitSparseFingerprint` retain
their existing PostgreSQL storage types and constructors.

The changes affect how cartridge operations are written and how SQLAlchemy
types their result expressions.

## Fingerprint methods

The old fingerprint methods mixed threshold predicates and K-nearest-neighbor
distances under ambiguous names. Replace them as follows:

| Previous API | New API | Result | Typical placement |
| --- | --- | --- | --- |
| `fp.tanimoto(query)` | `fp.tanimoto_matches(query)` | Boolean | `WHERE` |
| `fp.dice(query)` | `fp.dice_matches(query)` | Boolean | `WHERE` |
| `fp.nearest_neighbors(query)` | `fp.tanimoto_distance(query)` | Float | `ORDER BY` |
| `fp.nearest_neighbors(query, "dice")` | `fp.dice_distance(query)` | Float | `ORDER BY` |

There are no compatibility aliases. Calls using `tanimoto()`, `dice()`, or
`nearest_neighbors()` must be updated.

### Threshold searches

The `%` and `#` operators are Boolean predicates controlled by the RDKit
similarity threshold settings.

```python
# Before
stmt = select(Molecule).where(Molecule.fingerprint.tanimoto(query_fp))

# After
stmt = select(Molecule).where(
    Molecule.fingerprint.tanimoto_matches(query_fp)
)
```

Use `dice_matches()` for the Dice `#` predicate.

### KNN ordering

The `<%>` and `<#>` operators return floating-point distances. They belong in
`ORDER BY`, not `WHERE`.

```python
# Before: the name and Boolean typing obscured that this was a distance.
stmt = select(Molecule).where(
    Molecule.fingerprint.nearest_neighbors(query_fp)
)

# After: order from nearest to farthest by Tanimoto distance.
stmt = (
    select(Molecule)
    .order_by(Molecule.fingerprint.tanimoto_distance(query_fp))
    .limit(20)
)

# Dice KNN distance
dice_stmt = select(Molecule).order_by(
    Molecule.fingerprint.dice_distance(query_fp)
)
```

Distance expressions can also be selected and labeled:

```python
distance = Molecule.fingerprint.tanimoto_distance(query_fp).label("distance")
stmt = select(Molecule.name, distance).order_by(distance)
```

## Molecule equality

Custom Python `__eq__` and `__ne__` implementations were removed so SQLAlchemy
can handle comparisons and `None` normally. This does **not** make RDKit
molecule equality textual or binary.

For the PostgreSQL RDKit `mol` type, the operator spellings are aliases for the
same chemical comparison functions:

| Python API | SQL operator | RDKit function |
| --- | --- | --- |
| `column == query` | `=` | `mol_eq` |
| `column.equals(query)` | `@=` | `mol_eq` |
| `column != query` | `<>` | `mol_ne` |
| `column.not_equals(query)` | `@<>` | `mol_ne` |

Both forms are chemically aware. Equivalent SMILES representations compare as
equal, and chirality handling follows the `rdkit.do_chiral_sss` setting. The
named methods remain available when explicit chemical intent is preferable.

Null comparisons use standard SQL:

```python
Molecule.structure == None  # IS NULL
Molecule.structure != None  # IS NOT NULL
```

## Expression result types

Molecule and reaction search methods now produce `ColumnElement[bool]` backed
by SQLAlchemy `Boolean`. Fingerprint KNN methods produce
`ColumnElement[float]` backed by SQLAlchemy `Float`.

This makes Boolean composition and distance ordering accurately reflect the
database behavior:

```python
predicate = Molecule.structure.has_substructure("c1ccccc1")
stmt = select(Molecule).where(predicate & Molecule.structure.not_equals("c1ccccc1"))

distance = Molecule.fingerprint.dice_distance(query_fp)
stmt = select(Molecule).order_by(distance)
```

## Typed column helpers

Direct comparator calls remain the runtime API. SQLAlchemy currently exposes
dynamically installed comparator methods as `Any` to static analyzers. Use the
helpers when precise editor and `ty` information is needed:

```python
from molalchemy.helpers import rdkit_col, rdkit_fp_col, rdkit_rxn_col

mol_predicate = rdkit_col(Molecule.structure).equals(other_molecule)
rxn_predicate = rdkit_rxn_col(Reaction.reaction).has_substructure(query_reaction)
fp_predicate = rdkit_fp_col(Molecule.fingerprint).dice_matches(other_fingerprint)
fp_distance = rdkit_fp_col(Molecule.fingerprint).tanimoto_distance(query_fp)
```

`rdkit_fp_col()` is new. All three helpers return the original SQLAlchemy
column at runtime after validating its MolAlchemy type. They accept Core
columns and ORM mapped attributes, including column-to-column operands.

The old generated `RdkitMolProxy` and `RdkitRxnProxy` exports were removed.
Their replacement protocols describe real method arguments and result types;
users normally access them through the helper functions rather than importing
the protocols directly.

## Accepted operands

The typed comparator interface reflects the corresponding bind processors:

- Molecules accept SMILES strings, `rdkit.Chem.Mol`, and SQL expressions.
- Reactions accept reaction strings,
  `rdkit.Chem.rdChemReactions.ChemicalReaction`, and SQL expressions.
- Fingerprints accept bytes and SQL expressions.
- Core columns and ORM `InstrumentedAttribute` objects are valid SQL operands.

## Unchanged APIs

Constructors, conversions, descriptors, fingerprint generators, score
functions, aggregates, settings, indexes, and database/file workflows remain
standalone functions. Existing calls to those functions do not require changes.
