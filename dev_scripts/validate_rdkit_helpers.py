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

from molalchemy.rdkit import (
    RdkitFPComparator,
    RdkitMolComparator,
    RdkitReactionComparator,
    RdkitSettings,
    configure_engine,
)
from molalchemy.rdkit import functions as rdkit_func
from molalchemy.rdkit.types import RdkitBitFingerprint, RdkitMol, RdkitReaction
from molalchemy.types import CString

DATABASE_URL = os.environ.get(
    "RDKIT_DATABASE_URL",
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
    configured_gucs = {
        "rdkit.tanimoto_threshold": "0.55",
        "rdkit.dice_threshold": "0.45",
        "rdkit.do_chiral_sss": "on",
        "rdkit.do_enhanced_stereo_sss": "off",
        "rdkit.sss_fp_size": "2048",
        "rdkit.morgan_fp_size": "2048",
        "rdkit.featmorgan_fp_size": "2048",
        "rdkit.layered_fp_size": "2048",
        "rdkit.rdkit_fp_size": "2048",
        "rdkit.torsion_fp_size": "2048",
        "rdkit.atompair_fp_size": "2048",
        "rdkit.avalon_fp_size": "2048",
    }
    baseline_settings = RdkitSettings(
        tanimoto_threshold=0.55,
        dice_threshold=0.45,
        do_chiral_sss=True,
        do_enhanced_stereo_sss=False,
        sss_fp_size=2048,
        morgan_fp_size=2048,
        featmorgan_fp_size=2048,
        layered_fp_size=2048,
        rdkit_fp_size=2048,
        torsion_fp_size=2048,
        atompair_fp_size=2048,
        avalon_fp_size=2048,
    )
    engine = configure_engine(
        create_engine(DATABASE_URL, echo=False, pool_size=1, max_overflow=0),
        baseline_settings,
    )
    wait_for_db(engine)

    with engine.connect() as conn:
        actual_gucs = {
            name: conn.exec_driver_sql(f"SHOW {name}").scalar_one()
            for name in configured_gucs
        }
    assert actual_gucs == configured_gucs

    # Prove that checkout reapplies the baseline to a reused physical connection.
    with engine.begin() as conn:
        conn.exec_driver_sql("SET rdkit.tanimoto_threshold = 0.13")
    with engine.connect() as conn:
        reapplied_tanimoto = conn.exec_driver_sql(
            "SHOW rdkit.tanimoto_threshold"
        ).scalar_one()
    assert reapplied_tanimoto == configured_gucs["rdkit.tanimoto_threshold"]

    # Engine.dispose() replaces the pool. The baseline must follow the engine
    # so that connections created by the replacement pool are configured too.
    engine.dispose()
    with engine.connect() as conn:
        reapplied_after_dispose = conn.exec_driver_sql(
            "SHOW rdkit.tanimoto_threshold"
        ).scalar_one()
    assert reapplied_after_dispose == configured_gucs["rdkit.tanimoto_threshold"]

    # Reconfiguration must also remove the saved listener cleanly after the
    # engine has replaced its pool.
    configure_engine(engine, RdkitSettings(tanimoto_threshold=0.65))
    with engine.connect() as conn:
        reconfigured_after_dispose = conn.exec_driver_sql(
            "SHOW rdkit.tanimoto_threshold"
        ).scalar_one()
    assert reconfigured_after_dispose == "0.65"
    configure_engine(engine, baseline_settings)

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
    nullable_molecules = Table(
        "molalchemy_rdkit_null_validation",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String, nullable=False),
        Column("mol", RdkitMol()),
    )
    nullable_reactions = Table(
        "molalchemy_rdkit_reaction_null_validation",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String, nullable=False),
        Column("rxn", RdkitReaction()),
    )

    with engine.begin() as conn:
        conn.exec_driver_sql(
            "DROP TABLE IF EXISTS molalchemy_rdkit_reaction_null_validation"
        )
        conn.exec_driver_sql("DROP TABLE IF EXISTS molalchemy_rdkit_null_validation")
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
        conn.execute(
            nullable_molecules.insert(),
            [
                {"id": 1, "name": "benzene", "mol": "c1ccccc1"},
                {"id": 2, "name": "unknown", "mol": None},
            ],
        )
        conn.execute(
            nullable_reactions.insert(),
            [
                {"id": 1, "name": "ethanol oxidation", "rxn": "CCO>>CC=O"},
                {"id": 2, "name": "unknown reaction", "rxn": None},
            ],
        )

    substructure_stmt = (
        select(molecules.c.name)
        .where(molecules.c.mol.has_substructure("c1ccccc1"))
        .order_by(molecules.c.id)
    )
    smarts_stmt = (
        select(molecules.c.name)
        .where(molecules.c.mol.has_smarts("[CH3][CH2][OH]"))
        .order_by(molecules.c.id)
    )
    reverse_substructure_stmt = (
        select(molecules.c.name)
        .where(molecules.c.mol.is_substructure_of("CCO"))
        .order_by(molecules.c.id)
    )
    functional_substructure_stmt = (
        select(molecules.c.name)
        .where(rdkit_func.mol_has_substructure(molecules.c.mol, "c1ccccc1"))
        .order_by(molecules.c.id)
    )
    exact_stmt = select(molecules.c.name).where(molecules.c.mol.equals("CCO"))
    native_equivalent_stmt = (
        select(molecules.c.name)
        .where(molecules.c.mol == "OCC")
        .order_by(molecules.c.id)
    )
    explicit_equivalent_stmt = (
        select(molecules.c.name)
        .where(molecules.c.mol.equals("OCC"))
        .order_by(molecules.c.id)
    )
    native_not_equivalent_stmt = (
        select(molecules.c.name)
        .where(molecules.c.mol != "OCC")
        .order_by(molecules.c.id)
    )
    explicit_not_equivalent_stmt = (
        select(molecules.c.name)
        .where(molecules.c.mol.not_equals("OCC"))
        .order_by(molecules.c.id)
    )
    query_mol = rdkit_func.qmol_from_smiles(cast("CCO", CString))
    query_substructure_stmt = (
        select(molecules.c.name)
        .where(molecules.c.mol.has_query_substructure(query_mol))
        .order_by(molecules.c.id)
    )
    reverse_query_substructure_stmt = (
        select(molecules.c.name)
        .where(molecules.c.mol.is_query_substructure_of(query_mol))
        .order_by(molecules.c.id)
    )
    query_fp = rdkit_func.morganbv_fp(rdkit_func.mol_from_smiles("CCO"))
    tanimoto_stmt = select(molecules.c.name).where(
        molecules.c.morgan_fp.tanimoto_matches(query_fp)
    )
    dice_stmt = select(molecules.c.name).where(
        molecules.c.morgan_fp.dice_matches(query_fp)
    )
    tanimoto_knn_stmt = select(molecules.c.name).order_by(
        molecules.c.morgan_fp.tanimoto_distance(query_fp), molecules.c.id
    )
    dice_knn_stmt = select(molecules.c.name).order_by(
        molecules.c.morgan_fp.dice_distance(query_fp), molecules.c.id
    )
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
    molecule_null_stmt = select(nullable_molecules.c.name).where(
        nullable_molecules.c.mol.__eq__(None)
    )
    reaction_null_stmt = select(nullable_reactions.c.name).where(
        nullable_reactions.c.rxn.__eq__(None)
    )
    reaction_explicit_equals_stmt = select(nullable_reactions.c.name).where(
        nullable_reactions.c.rxn.equals("OCC>>O=CC")
    )
    reaction_explicit_not_equals_stmt = select(nullable_reactions.c.name).where(
        nullable_reactions.c.rxn.not_equals("CCN>>CC=N")
    )
    reaction_substructure_stmt = select(nullable_reactions.c.name).where(
        nullable_reactions.c.rxn.has_substructure("CCO>>CC=O")
    )
    reaction_reverse_substructure_stmt = select(nullable_reactions.c.name).where(
        nullable_reactions.c.rxn.is_substructure_of("CCO>>CC=O")
    )
    reaction_smarts_stmt = select(nullable_reactions.c.name).where(
        nullable_reactions.c.rxn.has_smarts("CCO>>CC=O")
    )
    reaction_substructure_fp_stmt = select(nullable_reactions.c.name).where(
        nullable_reactions.c.rxn.has_substructure_fp("CCO>>CC=O")
    )
    reaction_reverse_substructure_fp_stmt = select(nullable_reactions.c.name).where(
        nullable_reactions.c.rxn.is_substructure_fp_of("CCO>>CC=O")
    )

    comparator_statements = {
        ("RdkitMolComparator", "has_substructure"): substructure_stmt,
        ("RdkitMolComparator", "has_smarts"): smarts_stmt,
        ("RdkitMolComparator", "is_substructure_of"): reverse_substructure_stmt,
        ("RdkitMolComparator", "equals"): explicit_equivalent_stmt,
        ("RdkitMolComparator", "not_equals"): explicit_not_equivalent_stmt,
        ("RdkitMolComparator", "has_query_substructure"): query_substructure_stmt,
        (
            "RdkitMolComparator",
            "is_query_substructure_of",
        ): reverse_query_substructure_stmt,
        ("RdkitReactionComparator", "has_substructure"): reaction_substructure_stmt,
        (
            "RdkitReactionComparator",
            "is_substructure_of",
        ): reaction_reverse_substructure_stmt,
        ("RdkitReactionComparator", "equals"): reaction_explicit_equals_stmt,
        (
            "RdkitReactionComparator",
            "not_equals",
        ): reaction_explicit_not_equals_stmt,
        ("RdkitReactionComparator", "has_smarts"): reaction_smarts_stmt,
        (
            "RdkitReactionComparator",
            "has_substructure_fp",
        ): reaction_substructure_fp_stmt,
        (
            "RdkitReactionComparator",
            "is_substructure_fp_of",
        ): reaction_reverse_substructure_fp_stmt,
        ("RdkitFPComparator", "tanimoto_matches"): tanimoto_stmt,
        ("RdkitFPComparator", "dice_matches"): dice_stmt,
        ("RdkitFPComparator", "tanimoto_distance"): tanimoto_knn_stmt,
        ("RdkitFPComparator", "dice_distance"): dice_knn_stmt,
    }
    comparator_classes = (
        RdkitMolComparator,
        RdkitReactionComparator,
        RdkitFPComparator,
    )
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

    print(str(CreateTable(molecules).compile(dialect=postgresql.dialect())))
    print(str(CreateTable(nullable_molecules).compile(dialect=postgresql.dialect())))
    print(str(CreateTable(nullable_reactions).compile(dialect=postgresql.dialect())))
    print()
    print(substructure_stmt.compile(dialect=postgresql.dialect()))
    print(smarts_stmt.compile(dialect=postgresql.dialect()))
    print(reverse_substructure_stmt.compile(dialect=postgresql.dialect()))
    print(functional_substructure_stmt.compile(dialect=postgresql.dialect()))
    print(exact_stmt.compile(dialect=postgresql.dialect()))
    print(native_equivalent_stmt.compile(dialect=postgresql.dialect()))
    print(explicit_equivalent_stmt.compile(dialect=postgresql.dialect()))
    print(native_not_equivalent_stmt.compile(dialect=postgresql.dialect()))
    print(explicit_not_equivalent_stmt.compile(dialect=postgresql.dialect()))
    print(tanimoto_stmt.compile(dialect=postgresql.dialect()))
    print(dice_stmt.compile(dialect=postgresql.dialect()))
    print(tanimoto_knn_stmt.compile(dialect=postgresql.dialect()))
    print(dice_knn_stmt.compile(dialect=postgresql.dialect()))
    print(function_stmt.compile(dialect=postgresql.dialect()))
    print(molecule_null_stmt.compile(dialect=postgresql.dialect()))
    print(reaction_null_stmt.compile(dialect=postgresql.dialect()))
    print(reaction_explicit_equals_stmt.compile(dialect=postgresql.dialect()))
    print(reaction_explicit_not_equals_stmt.compile(dialect=postgresql.dialect()))
    print(query_substructure_stmt.compile(dialect=postgresql.dialect()))
    print(reverse_query_substructure_stmt.compile(dialect=postgresql.dialect()))
    print(reaction_substructure_stmt.compile(dialect=postgresql.dialect()))
    print(reaction_reverse_substructure_stmt.compile(dialect=postgresql.dialect()))
    print(reaction_smarts_stmt.compile(dialect=postgresql.dialect()))
    print(reaction_substructure_fp_stmt.compile(dialect=postgresql.dialect()))
    print(reaction_reverse_substructure_fp_stmt.compile(dialect=postgresql.dialect()))

    with engine.connect() as conn:
        version = conn.exec_driver_sql("SELECT rdkit_version()").scalar_one()
        comparator_results = {
            name: conn.execute(statement).scalars().all()
            for name, statement in comparator_statements.items()
        }
        substructure_rows = comparator_results[
            ("RdkitMolComparator", "has_substructure")
        ]
        functional_substructure_rows = (
            conn.execute(functional_substructure_stmt).scalars().all()
        )
        exact_rows = conn.execute(exact_stmt).scalars().all()
        native_equivalent_rows = conn.execute(native_equivalent_stmt).scalars().all()
        explicit_equivalent_rows = comparator_results[("RdkitMolComparator", "equals")]
        native_not_equivalent_rows = (
            conn.execute(native_not_equivalent_stmt).scalars().all()
        )
        explicit_not_equivalent_rows = comparator_results[
            ("RdkitMolComparator", "not_equals")
        ]
        tanimoto_rows = comparator_results[("RdkitFPComparator", "tanimoto_matches")]
        dice_rows = comparator_results[("RdkitFPComparator", "dice_matches")]
        tanimoto_knn_rows = comparator_results[
            ("RdkitFPComparator", "tanimoto_distance")
        ]
        dice_knn_rows = comparator_results[("RdkitFPComparator", "dice_distance")]
        function_row = conn.execute(function_stmt).mappings().one()
        molecule_null_rows = conn.execute(molecule_null_stmt).scalars().all()
        reaction_null_rows = conn.execute(reaction_null_stmt).scalars().all()
        reaction_explicit_equals_rows = comparator_results[
            ("RdkitReactionComparator", "equals")
        ]
        reaction_explicit_not_equals_rows = comparator_results[
            ("RdkitReactionComparator", "not_equals")
        ]

    print()
    print(f"RDKit version: {version}")
    print(f"configured RDKit GUCs: {actual_gucs}")
    print(f"reapplied tanimoto threshold: {reapplied_tanimoto}")
    print(f"reapplied after engine disposal: {reapplied_after_dispose}")
    print(f"reconfigured after engine disposal: {reconfigured_after_dispose}")
    print(f"substructure(c1ccccc1): {substructure_rows}")
    print(f"mol_has_substructure(c1ccccc1): {functional_substructure_rows}")
    print(f"exact(CCO): {exact_rows}")
    print(f"native molecule equality(CCO, OCC): {native_equivalent_rows}")
    print(f"explicit molecule equality(CCO, OCC): {explicit_equivalent_rows}")
    print(f"native molecule inequality(CCO, OCC): {native_not_equivalent_rows}")
    print(f"explicit molecule inequality(CCO, OCC): {explicit_not_equivalent_rows}")
    print(f"tanimoto fingerprint threshold(CCO): {tanimoto_rows}")
    print(f"dice fingerprint threshold(CCO): {dice_rows}")
    print(f"tanimoto KNN(CCO): {tanimoto_knn_rows}")
    print(f"dice KNN(CCO): {dice_knn_rows}")
    print(f"function wrappers on ethanol: {dict(function_row)}")
    print(f"mol IS NULL via == None: {molecule_null_rows}")
    print(f"reaction IS NULL via == None: {reaction_null_rows}")
    print(
        "explicit reaction equality(CCO>>CC=O, OCC>>O=CC): "
        f"{reaction_explicit_equals_rows}"
    )
    print(f"explicit reaction inequality: {reaction_explicit_not_equals_rows}")
    for comparator_method, rows in comparator_results.items():
        print(f"live comparator {'.'.join(comparator_method)}: {rows}")

    assert substructure_rows == ["benzene", "aspirin"]
    assert functional_substructure_rows == ["benzene", "aspirin"]
    assert exact_rows == ["ethanol"]
    # Unlike Bingo storage equality, both RDKit molecule spellings call mol_eq.
    assert native_equivalent_rows == ["ethanol"]
    assert explicit_equivalent_rows == native_equivalent_rows
    assert native_not_equivalent_rows == ["benzene", "aspirin"]
    assert explicit_not_equivalent_rows == native_not_equivalent_rows
    assert tanimoto_rows == ["ethanol"]
    assert dice_rows == ["ethanol"]
    assert tanimoto_knn_rows[0] == "ethanol"
    assert dice_knn_rows[0] == "ethanol"
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
    assert molecule_null_rows == ["unknown"]
    assert reaction_null_rows == ["unknown reaction"]
    # RDKit reaction equality must use the explicit operators: native `=` is an
    # unimplemented operator shell in the cartridge versions covered here.
    assert reaction_explicit_equals_rows == ["ethanol oxidation"]
    assert reaction_explicit_not_equals_rows == ["ethanol oxidation"]
    expected_comparator_results = {
        ("RdkitMolComparator", "has_substructure"): ["benzene", "aspirin"],
        ("RdkitMolComparator", "has_smarts"): ["ethanol"],
        ("RdkitMolComparator", "is_substructure_of"): ["ethanol"],
        ("RdkitMolComparator", "equals"): ["ethanol"],
        ("RdkitMolComparator", "not_equals"): ["benzene", "aspirin"],
        ("RdkitMolComparator", "has_query_substructure"): ["ethanol", "aspirin"],
        ("RdkitMolComparator", "is_query_substructure_of"): [
            "ethanol",
            "aspirin",
        ],
        ("RdkitReactionComparator", "has_substructure"): ["ethanol oxidation"],
        ("RdkitReactionComparator", "is_substructure_of"): ["ethanol oxidation"],
        ("RdkitReactionComparator", "equals"): ["ethanol oxidation"],
        ("RdkitReactionComparator", "not_equals"): ["ethanol oxidation"],
        ("RdkitReactionComparator", "has_smarts"): ["ethanol oxidation"],
        ("RdkitReactionComparator", "has_substructure_fp"): ["ethanol oxidation"],
        (
            "RdkitReactionComparator",
            "is_substructure_fp_of",
        ): ["ethanol oxidation"],
        ("RdkitFPComparator", "tanimoto_matches"): ["ethanol"],
        ("RdkitFPComparator", "dice_matches"): ["ethanol"],
        ("RdkitFPComparator", "tanimoto_distance"): [
            "ethanol",
            "aspirin",
            "benzene",
        ],
        ("RdkitFPComparator", "dice_distance"): [
            "ethanol",
            "aspirin",
            "benzene",
        ],
    }
    assert comparator_results == expected_comparator_results
    print(f"validated all {len(declared_methods)} declared RDKit comparator methods")


if __name__ == "__main__":
    main()
