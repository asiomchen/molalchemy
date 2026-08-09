"""Auto-generated from `data/bingo/functions.json`. Do not edit manually.
This file defines internal Bingo PostgreSQL function wrappers for use with SQLAlchemy.
"""

from typing import Any

from sqlalchemy import types as sqltypes
from sqlalchemy.sql.functions import GenericFunction

from molalchemy.protocols import (
    FloatOperand,
    IntegerOperand,
    TextOperand,
    TextOrBinaryOperand,
)
from molalchemy.types import CString


class _exact_internal(GenericFunction[bool]):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "_exact_internal"

    def __init__(
        self,
        arg_1: TextOperand,
        arg_2: TextOrBinaryOperand,
        arg_3: TextOperand,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `_exact_internal`.

        Parameters
        ----------
        arg_1 : TextOperand
            Undocumented cartridge parameter.
        arg_2 : TextOrBinaryOperand
            Undocumented cartridge parameter.
        arg_3 : TextOperand
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, arg_3, **kwargs)
        self.packagenames = ("bingo",)


class _get_block_count(GenericFunction[int]):
    type = sqltypes.Integer()
    inherit_cache = True
    name = "_get_block_count"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `_get_block_count`.

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


class _get_profiling_info(GenericFunction[str]):
    type = CString()
    inherit_cache = True
    name = "_get_profiling_info"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `_get_profiling_info`.

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


class _get_structures_count(GenericFunction[int]):
    type = sqltypes.Integer()
    inherit_cache = True
    name = "_get_structures_count"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `_get_structures_count`.

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


class _gross_internal(GenericFunction[bool]):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "_gross_internal"

    def __init__(
        self,
        arg_1: TextOperand,
        arg_2: TextOperand,
        arg_3: TextOrBinaryOperand,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `_gross_internal`.

        Parameters
        ----------
        arg_1 : TextOperand
            Undocumented cartridge parameter.
        arg_2 : TextOperand
            Undocumented cartridge parameter.
        arg_3 : TextOrBinaryOperand
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, arg_3, **kwargs)
        self.packagenames = ("bingo",)


class _internal_func_011(GenericFunction[None]):
    type = sqltypes.NullType()
    inherit_cache = True
    name = "_internal_func_011"

    def __init__(
        self,
        arg_1: IntegerOperand,
        arg_2: TextOperand,
        arg_3: TextOperand,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `_internal_func_011`.

        Parameters
        ----------
        arg_1 : IntegerOperand
            Undocumented cartridge parameter.
        arg_2 : TextOperand
            Undocumented cartridge parameter.
        arg_3 : TextOperand
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[None | sqltypes.NullType]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, arg_3, **kwargs)
        self.packagenames = ("bingo",)


class _internal_func_012(GenericFunction[None]):
    type = sqltypes.NullType()
    inherit_cache = True
    name = "_internal_func_012"

    def __init__(
        self, arg_1: IntegerOperand, arg_2: TextOperand, **kwargs: Any
    ) -> None:
        """Calls the bingo cartridge function `_internal_func_012`.

        Parameters
        ----------
        arg_1 : IntegerOperand
            Undocumented cartridge parameter.
        arg_2 : TextOperand
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[None | sqltypes.NullType]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, **kwargs)
        self.packagenames = ("bingo",)


class _internal_func_check(GenericFunction[bool]):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "_internal_func_check"

    def __init__(self, arg_1: IntegerOperand, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `_internal_func_check`.

        Parameters
        ----------
        arg_1 : IntegerOperand
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(arg_1, **kwargs)
        self.packagenames = ("bingo",)


class _match_mass_great(GenericFunction[bool]):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "_match_mass_great"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `_match_mass_great`.

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


class _match_mass_less(GenericFunction[bool]):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "_match_mass_less"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `_match_mass_less`.

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


class _precache_database(GenericFunction[str]):
    type = sqltypes.Text()
    inherit_cache = True
    name = "_precache_database"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `_precache_database`.

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


class _print_profiling_info(GenericFunction[None]):
    type = sqltypes.NullType()
    inherit_cache = True
    name = "_print_profiling_info"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `_print_profiling_info`.

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


class _reset_profiling_info(GenericFunction[None]):
    type = sqltypes.NullType()
    inherit_cache = True
    name = "_reset_profiling_info"

    def __init__(self, **kwargs: Any) -> None:
        """Calls the bingo cartridge function `_reset_profiling_info`.

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


class _rexact_internal(GenericFunction[bool]):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "_rexact_internal"

    def __init__(
        self,
        arg_1: TextOperand,
        arg_2: TextOrBinaryOperand,
        arg_3: TextOperand,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `_rexact_internal`.

        Parameters
        ----------
        arg_1 : TextOperand
            Undocumented cartridge parameter.
        arg_2 : TextOrBinaryOperand
            Undocumented cartridge parameter.
        arg_3 : TextOperand
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, arg_3, **kwargs)
        self.packagenames = ("bingo",)


class _rsmarts_internal(GenericFunction[bool]):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "_rsmarts_internal"

    def __init__(
        self,
        arg_1: TextOperand,
        arg_2: TextOrBinaryOperand,
        arg_3: TextOperand,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `_rsmarts_internal`.

        Parameters
        ----------
        arg_1 : TextOperand
            Undocumented cartridge parameter.
        arg_2 : TextOrBinaryOperand
            Undocumented cartridge parameter.
        arg_3 : TextOperand
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, arg_3, **kwargs)
        self.packagenames = ("bingo",)


class _rsub_internal(GenericFunction[bool]):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "_rsub_internal"

    def __init__(
        self,
        arg_1: TextOperand,
        arg_2: TextOrBinaryOperand,
        arg_3: TextOperand,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `_rsub_internal`.

        Parameters
        ----------
        arg_1 : TextOperand
            Undocumented cartridge parameter.
        arg_2 : TextOrBinaryOperand
            Undocumented cartridge parameter.
        arg_3 : TextOperand
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, arg_3, **kwargs)
        self.packagenames = ("bingo",)


class _sim_internal(GenericFunction[bool]):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "_sim_internal"

    def __init__(
        self,
        arg_1: FloatOperand,
        arg_2: FloatOperand,
        arg_3: TextOperand,
        arg_4: TextOrBinaryOperand,
        arg_5: TextOperand,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `_sim_internal`.

        Parameters
        ----------
        arg_1 : FloatOperand
            Undocumented cartridge parameter.
        arg_2 : FloatOperand
            Undocumented cartridge parameter.
        arg_3 : TextOperand
            Undocumented cartridge parameter.
        arg_4 : TextOrBinaryOperand
            Undocumented cartridge parameter.
        arg_5 : TextOperand
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, arg_3, arg_4, arg_5, **kwargs)
        self.packagenames = ("bingo",)


class _smarts_internal(GenericFunction[bool]):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "_smarts_internal"

    def __init__(
        self,
        arg_1: TextOperand,
        arg_2: TextOrBinaryOperand,
        arg_3: TextOperand,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `_smarts_internal`.

        Parameters
        ----------
        arg_1 : TextOperand
            Undocumented cartridge parameter.
        arg_2 : TextOrBinaryOperand
            Undocumented cartridge parameter.
        arg_3 : TextOperand
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, arg_3, **kwargs)
        self.packagenames = ("bingo",)


class _sub_internal(GenericFunction[bool]):
    type = sqltypes.Boolean()
    inherit_cache = True
    name = "_sub_internal"

    def __init__(
        self,
        arg_1: TextOperand,
        arg_2: TextOrBinaryOperand,
        arg_3: TextOperand,
        **kwargs: Any,
    ) -> None:
        """Calls the bingo cartridge function `_sub_internal`.

        Parameters
        ----------
        arg_1 : TextOperand
            Undocumented cartridge parameter.
        arg_2 : TextOrBinaryOperand
            Undocumented cartridge parameter.
        arg_3 : TextOperand
            Undocumented cartridge parameter.
        kwargs : Any
            Additional keyword arguments passed to the `GenericFunction`.

        Returns
        -------
        Function[sqltypes.Boolean]
            SQLAlchemy function
        """
        super().__init__(arg_1, arg_2, arg_3, **kwargs)
        self.packagenames = ("bingo",)
