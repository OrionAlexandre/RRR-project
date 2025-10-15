"""
Fichier de création des différents modèles de tables des bdd.
"""
from datetime import datetime
from app import db

mois = ["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre", "decembre"]

for mois_ in mois:
    class Mois(db.model):
        __tablename__ = f"{mois}"

        nb_total_domaines = db.Column(db.Integer, default=0)
        nb_domaines_actifs = db.Column(db.Integer, default=0)
        nb_total_nouveaux = db.Column(db.Integer, default=0)
        nb_domaines_resilises = db.Column(db.Integer, default=0)
        nb_domaines_grace = db.Column(db.Integer, default=0)
        nb_domaines_redemption = db.Column(db.Integer, default=0)
        nb_domaines_expires = db.Column(db.Integer, default=0)
        nb_domaines_litigieux = db.Column(db.Integer, default=0)
