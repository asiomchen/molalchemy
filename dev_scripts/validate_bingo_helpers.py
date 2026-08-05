from __future__ import annotations

import os
import time

from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    func,
    select,
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import OperationalError
from sqlalchemy.schema import CreateTable

from molalchemy.bingo import BingoMolComparator, BingoRxnComparator
from molalchemy.bingo import functions as bingo_func
from molalchemy.bingo.types import BingoBinaryReaction, BingoMol

DATABASE_URL = os.environ.get(
    "BINGO_DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@127.0.0.1:5432/postgres",
)


def declared_comparator_methods(comparator: type) -> set[str]:
    """Return methods declared directly on a comparator, excluding internals."""
    return {
        name
        for name, value in vars(comparator).items()
        if not name.startswith("_") and callable(value)
    }


def wait_for_db(engine) -> None:
    deadline = time.monotonic() + 60
    while True:
        try:
            with engine.connect() as conn:
                conn.exec_driver_sql("SELECT 1")
            return
        except OperationalError:
            if time.monotonic() >= deadline:
                raise
            time.sleep(1)


def main() -> None:
    engine = create_engine(DATABASE_URL, echo=False)
    wait_for_db(engine)

    metadata = MetaData()
    compounds = Table(
        "molalchemy_bingo_helper_validation",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String, nullable=False),
        Column("structure", BingoMol()),
        Column("query_structure", String, nullable=False),
    )
    reactions = Table(
        "molalchemy_bingo_reaction_helper_validation",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String, nullable=False),
        Column("reaction_data", BingoBinaryReaction()),
        Column("query_reaction", String, nullable=False),
    )

    with engine.begin() as conn:
        conn.exec_driver_sql(
            "DROP TABLE IF EXISTS molalchemy_bingo_reaction_helper_validation"
        )
        conn.exec_driver_sql("DROP TABLE IF EXISTS molalchemy_bingo_helper_validation")
        metadata.create_all(conn)
        conn.execute(
            compounds.insert(),
            [
                {
                    "id": 1,
                    "name": "benzene",
                    "structure": "c1ccccc1",
                    "query_structure": "c1ccccc1",
                },
                {
                    "id": 2,
                    "name": "ethanol",
                    "structure": "CCO",
                    "query_structure": "OCC",
                },
                {
                    "id": 3,
                    "name": "unknown",
                    "structure": None,
                    "query_structure": "CCO",
                },
            ],
        )
        conn.execute(
            reactions.insert(),
            [
                {
                    "id": 1,
                    "name": "ethanol oxidation",
                    "reaction_data": "CCO>>CC=O",
                    "query_reaction": "CCO>>CC=O",
                },
                {
                    "id": 2,
                    "name": "unknown reaction",
                    "reaction_data": None,
                    "query_reaction": "CCO>>CC=O",
                },
            ],
        )

    substructure_stmt = select(compounds.c.name).where(
        compounds.c.structure.has_substructure("c1ccccc1")
    )
    comparator_smarts_stmt = select(compounds.c.name).where(
        compounds.c.structure.has_smarts("[#6]-[#8]")
    )
    comparator_equals_stmt = select(compounds.c.name).where(
        compounds.c.structure.equals("OCC")
    )
    comparator_not_equals_stmt = (
        select(compounds.c.name)
        .where(compounds.c.structure.not_equals("CCO"))
        .order_by(compounds.c.id)
    )
    exact_stmt = select(compounds.c.name).where(
        bingo_func.mol_equals(compounds.c.structure, "CCO")
    )
    similarity_with_column_stmt = (
        select(compounds.c.name)
        .where(
            compounds.c.structure.similar_to(
                compounds.c.query_structure,
                minimum=0.95,
                maximum=1.0,
                metric="Tanimoto",
            )
        )
        .order_by(compounds.c.id)
    )
    smarts_stmt = select(compounds.c.name).where(
        bingo_func.mol_has_smarts(compounds.c.structure, "[#6]-[#8]")
    )
    function_stmt = (
        select(
            compounds.c.name,
            bingo_func.smiles(compounds.c.structure).label("smiles"),
            bingo_func.cansmiles(compounds.c.structure).label("canonical_smiles"),
            bingo_func.gross(compounds.c.structure).label("formula"),
            bingo_func.getmass(compounds.c.structure).label("mass"),
            bingo_func.getweight(compounds.c.structure, "").label("weight"),
            bingo_func.getsimilarity(
                compounds.c.structure, compounds.c.query_structure
            ).label("similarity_score"),
            bingo_func.inchi(compounds.c.structure, "").label("inchi"),
            bingo_func.inchikey(bingo_func.inchi(compounds.c.structure, "")).label(
                "inchikey"
            ),
            bingo_func.checkmolecule(compounds.c.structure).label("check_result"),
            func.length(bingo_func.molfile(compounds.c.structure)).label("molfile_len"),
            func.length(bingo_func.fingerprint(compounds.c.structure, "sim")).label(
                "fingerprint_len"
            ),
        )
        .where(compounds.c.name == "ethanol")
        .limit(1)
    )
    invalid_check_stmt = select(bingo_func.checkmolecule("not-a-mol"))
    reaction_exact_stmt = select(reactions.c.name).where(
        reactions.c.reaction_data.equals("CCO>>CC=O")
    )
    reaction_substructure_stmt = select(reactions.c.name).where(
        reactions.c.reaction_data.has_substructure("CCO>>CC=O")
    )
    reaction_smarts_stmt = select(reactions.c.name).where(
        reactions.c.reaction_data.has_smarts("CCO>>CC=O")
    )
    reaction_not_equals_stmt = select(reactions.c.name).where(
        reactions.c.reaction_data.not_equals("CCN>>CC=N")
    )
    native_equality_stmt = (
        select(compounds.c.name)
        .where(compounds.c.structure == compounds.c.query_structure)
        .order_by(compounds.c.id)
    )
    molecule_not_null_stmt = (
        select(compounds.c.name)
        .where(compounds.c.structure.__ne__(None))
        .order_by(compounds.c.id)
    )
    reaction_not_null_stmt = (
        select(reactions.c.name)
        .where(reactions.c.reaction_data.__ne__(None))
        .order_by(reactions.c.id)
    )
    reaction_function_stmt = (
        select(
            reactions.c.name,
            bingo_func.checkreaction(reactions.c.reaction_data).label("check_result"),
            bingo_func.rsmiles(reactions.c.reaction_data).label("reaction_smiles"),
            func.length(bingo_func.rxnfile(reactions.c.reaction_data)).label(
                "rxnfile_len"
            ),
        )
        .where(reactions.c.name == "ethanol oxidation")
        .limit(1)
    )

    comparator_statements = {
        ("BingoMolComparator", "has_substructure"): substructure_stmt,
        ("BingoMolComparator", "has_smarts"): comparator_smarts_stmt,
        ("BingoMolComparator", "equals"): comparator_equals_stmt,
        ("BingoMolComparator", "not_equals"): comparator_not_equals_stmt,
        ("BingoMolComparator", "similar_to"): similarity_with_column_stmt,
        ("BingoRxnComparator", "has_substructure"): reaction_substructure_stmt,
        ("BingoRxnComparator", "has_smarts"): reaction_smarts_stmt,
        ("BingoRxnComparator", "equals"): reaction_exact_stmt,
        ("BingoRxnComparator", "not_equals"): reaction_not_equals_stmt,
    }
    comparator_classes = (BingoMolComparator, BingoRxnComparator)
    declared_methods = {
        (comparator.__name__, method)
        for comparator in comparator_classes
        for method in declared_comparator_methods(comparator)
    }
    assert comparator_statements.keys() == declared_methods, (
        "live comparator coverage mismatch: "
        f"missing={sorted(declared_methods - comparator_statements.keys())}, "
        f"unexpected={sorted(comparator_statements.keys() - declared_methods)}"
    )

    print(str(CreateTable(compounds).compile(dialect=postgresql.dialect())))
    print(str(CreateTable(reactions).compile(dialect=postgresql.dialect())))
    print()
    print(substructure_stmt.compile(dialect=postgresql.dialect()))
    print(comparator_smarts_stmt.compile(dialect=postgresql.dialect()))
    print(comparator_equals_stmt.compile(dialect=postgresql.dialect()))
    print(comparator_not_equals_stmt.compile(dialect=postgresql.dialect()))
    print(exact_stmt.compile(dialect=postgresql.dialect()))
    print(smarts_stmt.compile(dialect=postgresql.dialect()))
    print(
        similarity_with_column_stmt.compile(
            dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}
        )
    )
    print(function_stmt.compile(dialect=postgresql.dialect()))
    print(reaction_exact_stmt.compile(dialect=postgresql.dialect()))
    print(reaction_substructure_stmt.compile(dialect=postgresql.dialect()))
    print(reaction_smarts_stmt.compile(dialect=postgresql.dialect()))
    print(reaction_not_equals_stmt.compile(dialect=postgresql.dialect()))
    print(
        native_equality_stmt.compile(
            dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}
        )
    )
    print(molecule_not_null_stmt.compile(dialect=postgresql.dialect()))
    print(reaction_not_null_stmt.compile(dialect=postgresql.dialect()))
    print(reaction_function_stmt.compile(dialect=postgresql.dialect()))

    with engine.connect() as conn:
        version = conn.exec_driver_sql("SELECT bingo.getversion()").scalar_one()
        comparator_results = {
            name: conn.execute(statement).scalars().all()
            for name, statement in comparator_statements.items()
        }
        substructure_rows = comparator_results[
            ("BingoMolComparator", "has_substructure")
        ]
        exact_rows = conn.execute(exact_stmt).scalars().all()
        smarts_rows = conn.execute(smarts_stmt).scalars().all()
        similarity_rows = comparator_results[("BingoMolComparator", "similar_to")]
        function_row = conn.execute(function_stmt).mappings().one()
        invalid_check = conn.execute(invalid_check_stmt).scalar_one()
        reaction_exact_rows = comparator_results[("BingoRxnComparator", "equals")]
        native_equality_rows = conn.execute(native_equality_stmt).scalars().all()
        molecule_not_null_rows = conn.execute(molecule_not_null_stmt).scalars().all()
        reaction_not_null_rows = conn.execute(reaction_not_null_stmt).scalars().all()
        reaction_function_row = conn.execute(reaction_function_stmt).mappings().one()

    print()
    print(f"Bingo version: {version}")
    print(f"substructure(c1ccccc1): {substructure_rows}")
    print(f"exact(CCO): {exact_rows}")
    print(f"smarts([#6]-[#8]): {smarts_rows}")
    print(f"similarity(structure, query_structure): {similarity_rows}")
    print(f"function wrappers on ethanol: {dict(function_row)}")
    print(f"checkmolecule(not-a-mol): {invalid_check}")
    print(f"reaction exact(CCO>>CC=O): {reaction_exact_rows}")
    print(f"native equality(structure, query_structure): {native_equality_rows}")
    print(f"structure IS NOT NULL via != None: {molecule_not_null_rows}")
    print(f"reaction IS NOT NULL via != None: {reaction_not_null_rows}")
    print(f"reaction function wrappers: {dict(reaction_function_row)}")
    for comparator_method, rows in comparator_results.items():
        print(f"live comparator {'.'.join(comparator_method)}: {rows}")

    assert substructure_rows == ["benzene"]
    assert exact_rows == ["ethanol"]
    assert smarts_rows == ["ethanol"]
    assert similarity_rows == ["benzene", "ethanol"]
    assert function_row["smiles"] == "CCO"
    assert function_row["canonical_smiles"] == "CCO"
    assert function_row["formula"] == "C2 O H6"
    assert 46.0 < function_row["mass"] < 47.0
    assert 46.0 < function_row["weight"] < 47.0
    assert function_row["similarity_score"] == 1
    assert function_row["inchi"].startswith("InChI=1S/C2H6O")
    assert function_row["inchikey"] == "LFQSCWFLJHTTHZ-UHFFFAOYSA-N"
    assert function_row["check_result"] is None
    assert function_row["molfile_len"] > 100
    assert function_row["fingerprint_len"] > 0
    assert "invalid character" in invalid_check
    assert reaction_exact_rows == ["ethanol oxidation"]
    # Native SQL equality is textual: "CCO" and chemically equivalent "OCC" differ.
    assert native_equality_rows == ["benzene"]
    assert molecule_not_null_rows == ["benzene", "ethanol"]
    assert reaction_not_null_rows == ["ethanol oxidation"]
    assert reaction_function_row["check_result"] is None
    assert reaction_function_row["reaction_smiles"]
    assert reaction_function_row["rxnfile_len"] > 100
    expected_comparator_results = {
        ("BingoMolComparator", "has_substructure"): ["benzene"],
        ("BingoMolComparator", "has_smarts"): ["ethanol"],
        ("BingoMolComparator", "equals"): ["ethanol"],
        ("BingoMolComparator", "not_equals"): ["benzene"],
        ("BingoMolComparator", "similar_to"): ["benzene", "ethanol"],
        ("BingoRxnComparator", "has_substructure"): ["ethanol oxidation"],
        ("BingoRxnComparator", "has_smarts"): ["ethanol oxidation"],
        ("BingoRxnComparator", "equals"): ["ethanol oxidation"],
        ("BingoRxnComparator", "not_equals"): ["ethanol oxidation"],
    }
    assert comparator_results == expected_comparator_results
    print(f"validated all {len(declared_methods)} declared Bingo comparator methods")


if __name__ == "__main__":
    main()
