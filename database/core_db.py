"""
Ce fichier contiendra toutes les opérations liées à la gestion de la base de données.
"""

from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from datetime import datetime


class DataBase:
    def __init__(self):
        self.year = datetime.now().year
        self.__database_url = f"sqlite:///database.db"

        self.__create_engine_and_base() # Création du moteur des modèles.
        pass

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
        pass

    def __create_engine_and_base(self):
        self.engine = create_engine(self.__database_url)
        self.Base = declarative_base()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        # Définition de la table.
        MOIS = [
            "janvier", "fevrier", "mars", "avril", "mai", "juin",
            "juillet", "aout", "septembre", "octobre", "novembre", "decembre"
        ]
        YEARS = [i for i in range(2021, self.year + 1)]

        for year in YEARS:
            for month in MOIS:
                class Mois(self.Base):
                    __tablename__ = f"{year}-{month}"

                    id = Column(Integer, primary_key=True, index=True)
                    nb_total_domaines = Column(Integer, default=0)
                    nb_domaines_actifs = Column(Integer, default=0)
                    nb_total_nouveaux = Column(Integer, default=0)
                    nb_domaines_resilises = Column(Integer, default=0)
                    nb_domaines_grace = Column(Integer, default=0)
                    nb_domaines_redemption = Column(Integer, default=0)
                    nb_domaines_expires = Column(Integer, default=0)
                    nb_domaines_litigieux = Column(Integer, default=0)

                # Création des tables.
                self.__create_tables()

        print("<core_db.py>: ✅ Base de données initialisée avec succès!")

        pass

    def __create_tables(self):
        """Crée toutes les tables dans la base de données"""
        self.Base.metadata.create_all(bind=self.engine)
        print("<core_db.py>: Tables créées avec succès!")

    # Méthodes supplémentaires qui peuvent nous être utiles.

    def drop_tables(self):
        """Supprime toutes les tables (pour le développement)"""
        self.Base.metadata.drop_all(bind=self.engine)
        print("Tables supprimées avec succès!")

    def reset_database(self):
        """Réinitialise complètement la base de données"""
        self.drop_tables()
        self.create_tables()
        print("Base de données réinitialisée!")






