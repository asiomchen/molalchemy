from sqlalchemy import Index


class RdkitIndex(Index):
    """Custom index for RdkitMol and RdkitBitFingerprint types using GIST

    This index is designed to optimize queries on columns of type RdkitMol
    and RdkitBitFingerprint by leveraging PostgreSQL's GIST indexing capabilities.
    It is particularly useful for substructure and similarity searches.

    Attributes
    ----------
    name : str
        The name of the index.
    *expressions : ColumnElement
        The column(s) to be indexed.
    **kw : dict
        Additional keyword arguments for index creation.
    """

    def __init__(self, name: str, *expressions, **kw):
        kw["postgresql_using"] = "gist"
        super().__init__(name, *expressions, **kw)
