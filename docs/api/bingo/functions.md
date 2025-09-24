# Chemical Functions

The `molalchemy.bingo.functions` module provides collections of Bingo PostgreSQL functions for molecular and reaction structure search and analysis.

These function classes wrap Bingo PostgreSQL functions, enabling various chemical structure operations including substructure search, exact matching, similarity search, format conversions, and chemical property calculations directly from SQLAlchemy queries.

Due to the differences in the naming conventions among Bingo functions, match of provided methods to the actual database functions may not be exact, but it conveys the intended functionality.

Currently, not all Bingo functions are implemented. The rest can be accessed via `sqlalchemy.func` directly.


## `molalchemy.bingo.functions.mol`
::: molalchemy.bingo.functions.mol
    options:
      heading_level: 3
      show_source: false
      show_bases: true
      show_root_heading: false
      members_order: source


## `molalchemy.bingo.functions.rxn`

::: molalchemy.bingo.functions.rxn
    options:
      heading_level: 3
      show_source: false
      show_bases: true
      show_root_heading: false
      members_order: source