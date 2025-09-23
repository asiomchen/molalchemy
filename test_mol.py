from rdkit import Chem
from sqlalchemy import (
    Boolean,
    Integer,
    String,
    engine,
    select,
    text,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    sessionmaker,
)

from molalchemy.rdkit import index, types

eng = engine.create_engine(
    "postgresql+psycopg://postgres:example@localhost:5432/postgres", echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=eng)
with SessionLocal() as session:
    session.execute(text("CREATE EXTENSION IF NOT EXISTS rdkit"))
    session.commit()
    print(
        session.execute(text("SELECT rdkit_version(), rdkit_toolkit_version()")).all()
    )


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class Molecule(Base):
    __tablename__ = "molecules"
    __table_args__ = (index.RdkitIndex("mol_gist_idx", "mol"),)
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    name: Mapped[str] = mapped_column(String(100), unique=True)
    mol: Mapped[Chem.Mol] = mapped_column(types.RdkitMol(return_type="mol"))
    is_nsaid: Mapped[bool] = mapped_column(Boolean, default=False)


Molecule.__table__.drop(eng, checkfirst=True)
Molecule.metadata.create_all(eng, checkfirst=False)

with SessionLocal() as s:
    mol = Molecule(
        name="Aspirin",
        mol=Chem.MolFromSmiles("CC(=O)OC1=CC=CC=C1C(=O)O"),
        is_nsaid=True,
    )
    s.add(mol)
    s.commit()
stmt = select(Molecule).where(Molecule.name == "Aspirin")
print(stmt.compile(eng))
with SessionLocal() as s:
    aspirin = s.execute(stmt).scalar_one()
    print(aspirin)
