# RDKit settings

MolAlchemy can establish a baseline for all [RDKit PostgreSQL cartridge
settings](https://rdkit.org/new_docs/Cartridge.html#configuration) each time a
connection is checked out of a synchronous SQLAlchemy pool:

```python
from sqlalchemy import create_engine

from molalchemy.rdkit import RdkitSettings, configure_engine

engine = configure_engine(
    create_engine("postgresql+psycopg://localhost/chemistry"),
    RdkitSettings(
        tanimoto_threshold=0.5,
        dice_threshold=0.5,
        do_chiral_sss=True,
        do_enhanced_stereo_sss=True,
        morgan_fp_size=2048,
    ),
)
```

Only non-`None` fields are changed. Reconfiguring the same engine replaces its
previous MolAlchemy listener; passing an empty `RdkitSettings()` removes that
listener. Reconfiguration disposes the existing pool so idle connections
cannot retain values from the previous baseline. Connections already checked
out continue normally and retain their current session values until returned.
Because the baseline is applied on every checkout, a request that changes an
RDKit GUC does not permanently change the next request's pooled connection.

The `set_*`, `get_*`, and `similarity_threshold` helpers remain useful for
intentional, session-local threshold changes. `configure_engine` is for a pool
baseline, while those helpers are for query or unit-of-work scope.

::: molalchemy.rdkit.settings
