"""
Fichier de rendu des différentes vues ou chemin d'urls.
"""

from flask import render_template, request

def enregistrer_routes(app, db):
    @app.route("/")
    def home():  # put application's code here
        return render_template("index.html")

    @app.route('/domaines')
    def domaines():  # put application's code here
        return render_template("tables.html")

    @app.route("/statistiques")
    def statistiques():
        return render_template("statistic.html")

    @app.route("/correlations")
    def correlations():
        return render_template("correlations.html")
    pass