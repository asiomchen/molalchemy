"""Auto-generated from `data/bingo/functions.json`. Do not edit manually.
This file defines internal Bingo PostgreSQL function wrappers for use with SQLAlchemy.
"""

from typing import Any

from sqlalchemy import types as sqltypes
from sqlalchemy.sql.functions import GenericFunction

from molalchemy.types import CString


class _exact_internal(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "_exact_internal"

    def __init__(
        self,
        arg_1: str | sqltypes.Text,
        arg_2: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_3: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        """Calls the rdkit cartridge function `_exact_internal`.

        Parameters
        ----------
        arg_1
        arg_2
        arg_3
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, arg_3, **kwargs)
        self.packagenames = ("bingo",)


class _get_block_count(GenericFunction):
    inherit_cache = True
    name = "_get_block_count"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the rdkit cartridge function `_get_block_count`.

        Parameters
        ----------

        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            SQLAlchemy function
        """
        super().__init__(**kwargs)
        self.packagenames = ("bingo",)


class _get_profiling_info(GenericFunction):
    type = CString()
    inherit_cache = True
    name = "_get_profiling_info"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the rdkit cartridge function `_get_profiling_info`.

        Parameters
        ----------

        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[CString]
            SQLAlchemy function
        """
        super().__init__(**kwargs)
        self.packagenames = ("bingo",)


class _get_structures_count(GenericFunction):
    inherit_cache = True
    name = "_get_structures_count"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the rdkit cartridge function `_get_structures_count`.

        Parameters
        ----------

        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[int | sqltypes.Integer]
            SQLAlchemy function
        """
        super().__init__(**kwargs)
        self.packagenames = ("bingo",)


class _gross_internal(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "_gross_internal"

    def __init__(
        self,
        arg_1: str | sqltypes.Text,
        arg_2: str | sqltypes.Text,
        arg_3: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        **kwargs: Any,
    ) -> None:
        """Calls the rdkit cartridge function `_gross_internal`.

        Parameters
        ----------
        arg_1
        arg_2
        arg_3
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, arg_3, **kwargs)
        self.packagenames = ("bingo",)


class _internal_func_011(GenericFunction):
    inherit_cache = True
    name = "_internal_func_011"

    def __init__(
        self,
        arg_1: int | sqltypes.Integer,
        arg_2: str | sqltypes.Text,
        arg_3: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        """Calls the rdkit cartridge function `_internal_func_011`.

        Parameters
        ----------
        arg_1
        arg_2
        arg_3
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[None | sqltypes.NullType]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, arg_3, **kwargs)
        self.packagenames = ("bingo",)


class _internal_func_012(GenericFunction):
    inherit_cache = True
    name = "_internal_func_012"

    def __init__(
        self, arg_1: int | sqltypes.Integer, arg_2: str | sqltypes.Text, **kwargs: Any
    ) -> None:
        """Calls the rdkit cartridge function `_internal_func_012`.

        Parameters
        ----------
        arg_1
        arg_2
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[None | sqltypes.NullType]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, **kwargs)
        self.packagenames = ("bingo",)


class _internal_func_check(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "_internal_func_check"

    def __init__(self, arg_1: int | sqltypes.Integer, **kwargs: Any) -> None:
        """Calls the rdkit cartridge function `_internal_func_check`.

        Parameters
        ----------
        arg_1
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(arg_1, **kwargs)
        self.packagenames = ("bingo",)


class _match_mass_great(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "_match_mass_great"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the rdkit cartridge function `_match_mass_great`.

        Parameters
        ----------

        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(**kwargs)
        self.packagenames = ("bingo",)


class _match_mass_less(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "_match_mass_less"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the rdkit cartridge function `_match_mass_less`.

        Parameters
        ----------

        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(**kwargs)
        self.packagenames = ("bingo",)


class _precache_database(GenericFunction):
    inherit_cache = True
    name = "_precache_database"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the rdkit cartridge function `_precache_database`.

        Parameters
        ----------

        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[str | sqltypes.Text]
            SQLAlchemy function
        """
        super().__init__(**kwargs)
        self.packagenames = ("bingo",)


class _print_profiling_info(GenericFunction):
    inherit_cache = True
    name = "_print_profiling_info"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the rdkit cartridge function `_print_profiling_info`.

        Parameters
        ----------

        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[None | sqltypes.NullType]
            SQLAlchemy function
        """
        super().__init__(**kwargs)
        self.packagenames = ("bingo",)


class _reset_profiling_info(GenericFunction):
    inherit_cache = True
    name = "_reset_profiling_info"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the rdkit cartridge function `_reset_profiling_info`.

        Parameters
        ----------

        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[None | sqltypes.NullType]
            SQLAlchemy function
        """
        super().__init__(**kwargs)
        self.packagenames = ("bingo",)


class _rexact_internal(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "_rexact_internal"

    def __init__(
        self,
        arg_1: str | sqltypes.Text,
        arg_2: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_3: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        """Calls the rdkit cartridge function `_rexact_internal`.

        Parameters
        ----------
        arg_1
        arg_2
        arg_3
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, arg_3, **kwargs)
        self.packagenames = ("bingo",)


class _rsmarts_internal(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "_rsmarts_internal"

    def __init__(
        self,
        arg_1: str | sqltypes.Text,
        arg_2: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_3: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        """Calls the rdkit cartridge function `_rsmarts_internal`.

        Parameters
        ----------
        arg_1
        arg_2
        arg_3
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, arg_3, **kwargs)
        self.packagenames = ("bingo",)


class _rsub_internal(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "_rsub_internal"

    def __init__(
        self,
        arg_1: str | sqltypes.Text,
        arg_2: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_3: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        """Calls the rdkit cartridge function `_rsub_internal`.

        Parameters
        ----------
        arg_1
        arg_2
        arg_3
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, arg_3, **kwargs)
        self.packagenames = ("bingo",)


class _sim_internal(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "_sim_internal"

    def __init__(
        self,
        arg_1: float | sqltypes.Float,
        arg_2: float | sqltypes.Float,
        arg_3: str | sqltypes.Text,
        arg_4: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_5: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        """Calls the rdkit cartridge function `_sim_internal`.

        Parameters
        ----------
        arg_1
        arg_2
        arg_3
        arg_4
        arg_5
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, arg_3, arg_4, arg_5, **kwargs)
        self.packagenames = ("bingo",)


class _smarts_internal(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "_smarts_internal"

    def __init__(
        self,
        arg_1: str | sqltypes.Text,
        arg_2: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_3: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        """Calls the rdkit cartridge function `_smarts_internal`.

        Parameters
        ----------
        arg_1
        arg_2
        arg_3
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, arg_3, **kwargs)
        self.packagenames = ("bingo",)


class _sub_internal(GenericFunction):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "_sub_internal"

    def __init__(
        self,
        arg_1: str | sqltypes.Text,
        arg_2: str | sqltypes.Text | bytes | sqltypes.LargeBinary,
        arg_3: str | sqltypes.Text,
        **kwargs: Any,
    ) -> None:
        """Calls the rdkit cartridge function `_sub_internal`.

        Parameters
        ----------
        arg_1
        arg_2
        arg_3
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, arg_3, **kwargs)
        self.packagenames = ("bingo",)
