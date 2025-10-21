"""
Ce fichier contiendra toutes les opérations liées à la gestion de la base de données.
"""
from sqlalchemy import create_engine, Column, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class DomaineStat(Base):
    __tablename__ = "domaine_stats"

    id = Column(Integer, primary_key=True, index=True)
    registrateur = Column(String, nullable=False)
    annee = Column(Integer, nullable=False)
    mois = Column(Integer, nullable=False)  # 1 à 12

    nb_total_domaines = Column(Integer, default=0)
    nb_domaines_actifs = Column(Integer, default=0)
    nb_nouveaux = Column(Integer, default=0)
    nb_renouvelles = Column(Integer, default=0)
    nb_resilies = Column(Integer, default=0)
    nb_grace = Column(Integer, default=0)
    nb_redemption = Column(Integer, default=0)
    nb_expires = Column(Integer, default=0)
    nb_litigieux = Column(Integer, default=0)

    __table_args__ = (UniqueConstraint('registrateur', 'annee', 'mois', name='_unique_reg_mois_annee'),)

class DataBase:
    def __init__(self, db_path="database.db"):
        self.__database_url = f"sqlite:///{db_path}"
        self.__create_engine_and_base()

    def get_database(self):
        """FastAPI-style dependency"""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def __create_engine_and_base(self):
        self.engine = create_engine(self.__database_url, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        print("<core_db.py>: ✅ Base de données initialisée avec succès!")

    def drop_tables(self):
        Base.metadata.drop_all(bind=self.engine)
        print("Tables supprimées avec succès!")

    def reset_database(self):
        self.drop_tables()
        Base.metadata.create_all(bind=self.engine)
        print("Base de données réinitialisée!")