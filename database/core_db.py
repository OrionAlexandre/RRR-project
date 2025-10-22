"""
Ce fichier contiendra toutes les opérations liées à la gestion de la base de données.
"""
from sqlalchemy import create_engine, Column, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

# === Ancien modèle : tables par année (conservé pour compatibilité) ===
# (Les tables 2021, 2022, etc. restent créées comme avant)

# === Nouvelle table : statistiques trimestrielles globales ===
class StatistiqueTrimestrielle(Base):
    __tablename__ = "statistiques_trimestrielles"

    id = Column(Integer, primary_key=True, index=True)
    annee = Column(Integer, nullable=False)
    trimestre = Column(Integer, nullable=False)  # 1, 2, 3, 4

    nb_total_domaines = Column(Integer, default=0)
    nb_domaines_actifs = Column(Integer, default=0)
    nb_domaines_expires = Column(Integer, default=0)
    nb_domaines_resilies = Column(Integer, default=0)

    __table_args__ = (UniqueConstraint('annee', 'trimestre', name='_unique_annee_trimestre'),)


class DataBase:
    def __init__(self):
        self.year = datetime.now().year
        self.__database_url = "sqlite:///database.db"
        self.__create_engine_and_base()

    def get_database(self):
        """
        Se chargera de retourner la base de données.
        :return:
        """
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def __create_engine_and_base(self):
        self.engine = create_engine(self.__database_url, connect_args={"check_same_thread": False})
        self.Base = declarative_base()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        # Recréer les anciennes tables (par année) — pour ne pas casser l'UI existante
        YEARS = [i for i in range(2021, self.year + 1)]
        for year in YEARS:
            type(
                f"Table{year}",
                (self.Base,),
                {
                    '__tablename__': str(year),
                    'id': Column(Integer, primary_key=True, index=True),
                    'nom_registrars': Column(String, default=""),
                    'nb_total_domaines': Column(String, default=""),
                    'nb_domaines_actifs': Column(String, default=""),
                    'nb_total_nouveaux': Column(String, default=""),
                    'nb_domaines_renouvelles': Column(String, default=""),
                    'nb_domaines_resilises': Column(String, default=""),
                    'nb_domaines_grace': Column(String, default=""),
                    'nb_domaines_redemption': Column(String, default=""),
                    'nb_domaines_expires': Column(String, default=""),
                    'nb_domaines_litigieux': Column(String, default="")
                }
            )

        # Créer TOUTES les tables (y compris la nouvelle)
        Base.metadata.create_all(bind=self.engine)
        print("<core_db.py>: ✅ Base de données initialisée avec succès!")

    def __create_tables(self):
        """Crée toutes les tables dans la base de données"""
        Base.metadata.create_all(bind=self.engine)
        print("<core_db.py>: Tables créées avec succès!")

    def drop_tables(self):
        """Supprime toutes les tables (pour le développement)"""
        Base.metadata.drop_all(bind=self.engine)
        print("Tables supprimées avec succès!")

    def reset_database(self):
        """Réinitialise complètement la base de données"""
        self.drop_tables()
        self.__create_tables()
        print("Base de données réinitialisée!")