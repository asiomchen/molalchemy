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

from molalchemy.bingo import functions as bingo_func
from molalchemy.bingo.types import BingoBinaryReaction, BingoMol

DATABASE_URL = os.environ.get(
    "BINGO_DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@127.0.0.1:5432/postgres",
)


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
        Column("structure", BingoMol(), nullable=False),
        Column("query_structure", String, nullable=False),
    )
    reactions = Table(
        "molalchemy_bingo_reaction_helper_validation",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String, nullable=False),
        Column("reaction_data", BingoBinaryReaction(), nullable=False),
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
                },
            ],
        )

    substructure_stmt = select(compounds.c.name).where(
        bingo_func.has_substructure(compounds.c.structure, "c1ccccc1")
    )
    exact_stmt = select(compounds.c.name).where(
        bingo_func.mol_equals(compounds.c.structure, "CCO")
    )
    similarity_with_column_stmt = (
        select(compounds.c.name)
        .where(
            bingo_func.similarity(
                compounds.c.structure,
                compounds.c.query_structure,
                0.95,
                1.0,
                "Tanimoto",
            )
        )
        .order_by(compounds.c.id)
    )
    smarts_stmt = select(compounds.c.name).where(
        bingo_func.matches_smarts(compounds.c.structure, "[#6]-[#8]")
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

    print(str(CreateTable(compounds).compile(dialect=postgresql.dialect())))
    print(str(CreateTable(reactions).compile(dialect=postgresql.dialect())))
    print()
    print(substructure_stmt.compile(dialect=postgresql.dialect()))
    print(exact_stmt.compile(dialect=postgresql.dialect()))
    print(smarts_stmt.compile(dialect=postgresql.dialect()))
    print(
        similarity_with_column_stmt.compile(
            dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}
        )
    )
    print(function_stmt.compile(dialect=postgresql.dialect()))
    print(reaction_exact_stmt.compile(dialect=postgresql.dialect()))
    print(reaction_function_stmt.compile(dialect=postgresql.dialect()))

    with engine.connect() as conn:
        version = conn.exec_driver_sql("SELECT bingo.getversion()").scalar_one()
        substructure_rows = conn.execute(substructure_stmt).scalars().all()
        exact_rows = conn.execute(exact_stmt).scalars().all()
        smarts_rows = conn.execute(smarts_stmt).scalars().all()
        similarity_rows = conn.execute(similarity_with_column_stmt).scalars().all()
        function_row = conn.execute(function_stmt).mappings().one()
        invalid_check = conn.execute(invalid_check_stmt).scalar_one()
        reaction_exact_rows = conn.execute(reaction_exact_stmt).scalars().all()
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
    print(f"reaction function wrappers: {dict(reaction_function_row)}")

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
    assert reaction_function_row["check_result"] is None
    assert reaction_function_row["reaction_smiles"]
    assert reaction_function_row["rxnfile_len"] > 100


if __name__ == "__main__":
    main()
