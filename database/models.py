from sqlalchemy import Column, Integer

from core_db import DataBase

# Création de l'instance de base de données
db_instance = DataBase()
Base = db_instance.Base


class Mois(Base):
    __tablename__ = "MOIS"

    id = Column(Integer, primary_key=True, index=True)
    nb_total_domaines = Column(Integer, default=0)
    nb_domaines_actifs = Column(Integer, default=0)
    nb_total_nouveaux = Column(Integer, default=0)
    nb_domaines_resilises = Column(Integer, default=0)
    nb_domaines_grace = Column(Integer, default=0)
    nb_domaines_redemption = Column(Integer, default=0)
    nb_domaines_expires = Column(Integer, default=0)
    nb_domaines_litigieux = Column(Integer, default=0)
