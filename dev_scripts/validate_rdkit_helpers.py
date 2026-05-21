from __future__ import annotations

import os
import time

from sqlalchemy import (
    Column,
    Computed,
    Integer,
    MetaData,
    String,
    Table,
    cast,
    create_engine,
    func,
    select,
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import OperationalError
from sqlalchemy.schema import CreateTable

from molalchemy.rdkit import functions as rdkit_func
from molalchemy.rdkit.types import RdkitBitFingerprint, RdkitMol
from molalchemy.types import CString

DATABASE_URL = os.environ.get(
    "RDKIT_DATABASE_URL",
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
    molecules = Table(
        "molalchemy_rdkit_helper_validation",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String, nullable=False),
        Column("mol", RdkitMol(), nullable=False),
        Column(
            "morgan_fp",
            RdkitBitFingerprint(),
            Computed("morganbv_fp(mol)", persisted=True),
        ),
    )

    with engine.begin() as conn:
        conn.exec_driver_sql("DROP TABLE IF EXISTS molalchemy_rdkit_helper_validation")
        metadata.create_all(conn)
        conn.execute(
            molecules.insert(),
            [
                {"id": 1, "name": "benzene", "mol": "c1ccccc1"},
                {"id": 2, "name": "ethanol", "mol": "CCO"},
                {
                    "id": 3,
                    "name": "aspirin",
                    "mol": "CC(=O)OC1=CC=CC=C1C(=O)O",
                },
            ],
        )

    substructure_stmt = select(molecules.c.name).where(
        molecules.c.mol.has_substructure("c1ccccc1")
    )
    functional_substructure_stmt = select(molecules.c.name).where(
        rdkit_func.mol_has_substructure(molecules.c.mol, "c1ccccc1")
    )
    exact_stmt = select(molecules.c.name).where(molecules.c.mol.equals("CCO"))
    query_fp = rdkit_func.morganbv_fp(rdkit_func.mol_from_smiles("CCO"))
    tanimoto_stmt = select(molecules.c.name).where(
        molecules.c.morgan_fp.tanimoto(query_fp)
    )
    dice_stmt = select(molecules.c.name).where(molecules.c.morgan_fp.dice(query_fp))
    function_stmt = (
        select(
            molecules.c.name,
            rdkit_func.mol_to_smiles(molecules.c.mol).label("smiles"),
            rdkit_func.mol_formula(molecules.c.mol).label("formula"),
            rdkit_func.mol_amw(molecules.c.mol).label("amw"),
            rdkit_func.mol_exactmw(molecules.c.mol).label("exactmw"),
            rdkit_func.mol_inchi(molecules.c.mol, cast("", CString)).label("inchi"),
            rdkit_func.mol_inchikey(molecules.c.mol, cast("", CString)).label(
                "inchikey"
            ),
            rdkit_func.mol_numatoms(molecules.c.mol).label("num_atoms"),
            rdkit_func.mol_numheavyatoms(molecules.c.mol).label("num_heavy_atoms"),
            rdkit_func.mol_hba(molecules.c.mol).label("hba"),
            rdkit_func.mol_hbd(molecules.c.mol).label("hbd"),
            rdkit_func.tanimoto_sml(molecules.c.morgan_fp, query_fp).label(
                "tanimoto_score"
            ),
            rdkit_func.dice_sml(molecules.c.morgan_fp, query_fp).label("dice_score"),
            func.length(cast(rdkit_func.mol_to_ctab(molecules.c.mol), String)).label(
                "ctab_len"
            ),
            func.octet_length(rdkit_func.mol_send(molecules.c.mol)).label("pkl_len"),
        )
        .where(molecules.c.name == "ethanol")
        .limit(1)
    )

    print(str(CreateTable(molecules).compile(dialect=postgresql.dialect())))
    print()
    print(substructure_stmt.compile(dialect=postgresql.dialect()))
    print(functional_substructure_stmt.compile(dialect=postgresql.dialect()))
    print(exact_stmt.compile(dialect=postgresql.dialect()))
    print(tanimoto_stmt.compile(dialect=postgresql.dialect()))
    print(dice_stmt.compile(dialect=postgresql.dialect()))
    print(function_stmt.compile(dialect=postgresql.dialect()))

    with engine.connect() as conn:
        version = conn.exec_driver_sql("SELECT rdkit_version()").scalar_one()
        substructure_rows = conn.execute(substructure_stmt).scalars().all()
        functional_substructure_rows = (
            conn.execute(functional_substructure_stmt).scalars().all()
        )
        exact_rows = conn.execute(exact_stmt).scalars().all()
        tanimoto_rows = conn.execute(tanimoto_stmt).scalars().all()
        dice_rows = conn.execute(dice_stmt).scalars().all()
        function_row = conn.execute(function_stmt).mappings().one()

    print()
    print(f"RDKit version: {version}")
    print(f"substructure(c1ccccc1): {substructure_rows}")
    print(f"mol_has_substructure(c1ccccc1): {functional_substructure_rows}")
    print(f"exact(CCO): {exact_rows}")
    print(f"tanimoto fingerprint threshold(CCO): {tanimoto_rows}")
    print(f"dice fingerprint threshold(CCO): {dice_rows}")
    print(f"function wrappers on ethanol: {dict(function_row)}")

    assert substructure_rows == ["benzene", "aspirin"]
    assert functional_substructure_rows == ["benzene", "aspirin"]
    assert exact_rows == ["ethanol"]
    assert tanimoto_rows == ["ethanol"]
    assert dice_rows == ["ethanol"]
    assert function_row["smiles"] == "CCO"
    assert function_row["formula"] == "C2H6O"
    assert 46.0 < function_row["amw"] < 47.0
    assert 46.0 < function_row["exactmw"] < 47.0
    assert function_row["inchi"].startswith("InChI=1S/C2H6O")
    assert function_row["inchikey"] == "LFQSCWFLJHTTHZ-UHFFFAOYSA-N"
    assert function_row["num_atoms"] == 9
    assert function_row["num_heavy_atoms"] == 3
    assert function_row["hba"] == 1
    assert function_row["hbd"] == 1
    assert function_row["tanimoto_score"] == 1
    assert function_row["dice_score"] == 1
    assert function_row["ctab_len"] > 100
    assert function_row["pkl_len"] > 0


if __name__ == "__main__":
    main()
