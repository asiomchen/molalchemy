"""Auto-generated from data/bingo_functions.json. Do not edit manually."""

from typing import Any

from sqlalchemy import types as sqltypes
from sqlalchemy.sql.functions import GenericFunction

from molalchemy.types import CString


class _exact_internal(GenericFunction):
    """
    Calls the rdkit cartridge function `_exact_internal`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text

    arg_2: str | sqltypes.Text | bytes | sqltypes.LargeBinary

    arg_3: str | sqltypes.Text



    Returns
    -------
    Function[sqltypes.Boolean]
        SQLAlchemy function
    """

    type = sqltypes.Boolean()

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        arg_1: str | sqltypes.Text,
        arg_2: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_3: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        super().__init__(arg_1, arg_2, arg_3, **kwargs)


class _get_block_count(GenericFunction):
    """
    Calls the rdkit cartridge function `_get_block_count`.


    Parameters
    ----------



    Returns
    -------
    Function[int | sqltypes.Integer]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class _get_profiling_info(GenericFunction):
    """
    Calls the rdkit cartridge function `_get_profiling_info`.


    Parameters
    ----------



    Returns
    -------
    Function[CString]
        SQLAlchemy function
    """

    type = CString()

    inherits_cache = True
    package = "bingo"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class _get_structures_count(GenericFunction):
    """
    Calls the rdkit cartridge function `_get_structures_count`.


    Parameters
    ----------



    Returns
    -------
    Function[int | sqltypes.Integer]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class _gross_internal(GenericFunction):
    """
    Calls the rdkit cartridge function `_gross_internal`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text

    arg_2: str | sqltypes.Text

    arg_3: str | sqltypes.Text | bytes | sqltypes.LargeBinary



    Returns
    -------
    Function[sqltypes.Boolean]
        SQLAlchemy function
    """

    type = sqltypes.Boolean()

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        arg_1: str | sqltypes.Text,
        arg_2: str | sqltypes.Text,
        arg_3: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        **kwargs: Any,
    ) -> None:
        super().__init__(arg_1, arg_2, arg_3, **kwargs)


class _internal_func_011(GenericFunction):
    """
    Calls the rdkit cartridge function `_internal_func_011`.


    Parameters
    ----------
    arg_1: int | sqltypes.Integer

    arg_2: str | sqltypes.Text

    arg_3: str | sqltypes.Text



    Returns
    -------
    Function[None | sqltypes.NullType]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        arg_1: int | sqltypes.Integer,
        arg_2: str | sqltypes.Text,
        arg_3: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        super().__init__(arg_1, arg_2, arg_3, **kwargs)


class _internal_func_012(GenericFunction):
    """
    Calls the rdkit cartridge function `_internal_func_012`.


    Parameters
    ----------
    arg_1: int | sqltypes.Integer

    arg_2: str | sqltypes.Text



    Returns
    -------
    Function[None | sqltypes.NullType]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(
        self, arg_1: int | sqltypes.Integer, arg_2: str | sqltypes.Text, **kwargs: Any
    ) -> None:
        super().__init__(arg_1, arg_2, **kwargs)


class _internal_func_check(GenericFunction):
    """
    Calls the rdkit cartridge function `_internal_func_check`.


    Parameters
    ----------
    arg_1: int | sqltypes.Integer



    Returns
    -------
    Function[sqltypes.Boolean]
        SQLAlchemy function
    """

    type = sqltypes.Boolean()

    inherits_cache = True
    package = "bingo"

    def __init__(self, arg_1: int | sqltypes.Integer, **kwargs: Any) -> None:
        super().__init__(arg_1, **kwargs)


class _match_mass_great(GenericFunction):
    """
    Calls the rdkit cartridge function `_match_mass_great`.


    Parameters
    ----------



    Returns
    -------
    Function[sqltypes.Boolean]
        SQLAlchemy function
    """

    type = sqltypes.Boolean()

    inherits_cache = True
    package = "bingo"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class _match_mass_less(GenericFunction):
    """
    Calls the rdkit cartridge function `_match_mass_less`.


    Parameters
    ----------



    Returns
    -------
    Function[sqltypes.Boolean]
        SQLAlchemy function
    """

    type = sqltypes.Boolean()

    inherits_cache = True
    package = "bingo"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class _precache_database(GenericFunction):
    """
    Calls the rdkit cartridge function `_precache_database`.


    Parameters
    ----------



    Returns
    -------
    Function[str | sqltypes.Text]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class _print_profiling_info(GenericFunction):
    """
    Calls the rdkit cartridge function `_print_profiling_info`.


    Parameters
    ----------



    Returns
    -------
    Function[None | sqltypes.NullType]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class _reset_profiling_info(GenericFunction):
    """
    Calls the rdkit cartridge function `_reset_profiling_info`.


    Parameters
    ----------



    Returns
    -------
    Function[None | sqltypes.NullType]
        SQLAlchemy function
    """

    inherits_cache = True
    package = "bingo"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class _rexact_internal(GenericFunction):
    """
    Calls the rdkit cartridge function `_rexact_internal`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text

    arg_2: str | sqltypes.Text | bytes | sqltypes.LargeBinary

    arg_3: str | sqltypes.Text



    Returns
    -------
    Function[sqltypes.Boolean]
        SQLAlchemy function
    """

    type = sqltypes.Boolean()

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        arg_1: str | sqltypes.Text,
        arg_2: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_3: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        super().__init__(arg_1, arg_2, arg_3, **kwargs)


class _rsmarts_internal(GenericFunction):
    """
    Calls the rdkit cartridge function `_rsmarts_internal`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text

    arg_2: str | sqltypes.Text | bytes | sqltypes.LargeBinary

    arg_3: str | sqltypes.Text



    Returns
    -------
    Function[sqltypes.Boolean]
        SQLAlchemy function
    """

    type = sqltypes.Boolean()

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        arg_1: str | sqltypes.Text,
        arg_2: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_3: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        super().__init__(arg_1, arg_2, arg_3, **kwargs)


class _rsub_internal(GenericFunction):
    """
    Calls the rdkit cartridge function `_rsub_internal`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text

    arg_2: str | sqltypes.Text | bytes | sqltypes.LargeBinary

    arg_3: str | sqltypes.Text



    Returns
    -------
    Function[sqltypes.Boolean]
        SQLAlchemy function
    """

    type = sqltypes.Boolean()

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        arg_1: str | sqltypes.Text,
        arg_2: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_3: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        super().__init__(arg_1, arg_2, arg_3, **kwargs)


class _sim_internal(GenericFunction):
    """
    Calls the rdkit cartridge function `_sim_internal`.


    Parameters
    ----------
    arg_1: float | sqltypes.Float

    arg_2: float | sqltypes.Float

    arg_3: str | sqltypes.Text

    arg_4: str | sqltypes.Text | bytes | sqltypes.LargeBinary

    arg_5: str | sqltypes.Text



    Returns
    -------
    Function[sqltypes.Boolean]
        SQLAlchemy function
    """

    type = sqltypes.Boolean()

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        arg_1: float | sqltypes.Float,
        arg_2: float | sqltypes.Float,
        arg_3: str | sqltypes.Text,
        arg_4: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_5: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        super().__init__(arg_1, arg_2, arg_3, arg_4, arg_5, **kwargs)


class _smarts_internal(GenericFunction):
    """
    Calls the rdkit cartridge function `_smarts_internal`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text

    arg_2: str | sqltypes.Text | bytes | sqltypes.LargeBinary

    arg_3: str | sqltypes.Text



    Returns
    -------
    Function[sqltypes.Boolean]
        SQLAlchemy function
    """

    type = sqltypes.Boolean()

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        arg_1: str | sqltypes.Text,
        arg_2: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_3: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        super().__init__(arg_1, arg_2, arg_3, **kwargs)


class _sub_internal(GenericFunction):
    """
    Calls the rdkit cartridge function `_sub_internal`.


    Parameters
    ----------
    arg_1: str | sqltypes.Text

    arg_2: str | sqltypes.Text | bytes | sqltypes.LargeBinary

    arg_3: str | sqltypes.Text



    Returns
    -------
    Function[sqltypes.Boolean]
        SQLAlchemy function
    """

    type = sqltypes.Boolean()

    inherits_cache = True
    package = "bingo"

    def __init__(
        self,
        arg_1: str | sqltypes.Text,
        arg_2: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_3: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        super().__init__(arg_1, arg_2, arg_3, **kwargs)
