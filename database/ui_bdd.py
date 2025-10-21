import customtkinter as CTk
from datetime import datetime
from core_db import DataBase, DomaineStat  # On importe le modèle et la gestion
from sqlalchemy.orm import sessionmaker

# Variables globales
month_value = "janvier"
year_value = "2021"
registrar_value = "IDS TECHNOLOGIE"
category_value = "Domaines actifs"

def __month_value(month: str):
    global month_value
    month_value = month
    print(f"Mois sélectionné: {month_value}")

def __year_value(year: str):
    global year_value
    year_value = year
    print(f"Année sélectionnée: {year_value}")

def __registrar_value(registrar: str):
    global registrar_value
    registrar_value = registrar
    print(f"Registrar sélectionné: {registrar_value}")

def __category_value(category: str):
    global category_value
    category_value = category
    print(f"Catégorie sélectionnée: {category_value}")

# Initialisation de la base (une fois)
db_instance = DataBase()
engine = db_instance.engine
Session = sessionmaker(bind=engine)

# Mapping mois → numéro
MOIS_DICT = {
    "janvier": 1, "fevrier": 2, "mars": 3, "avril": 4,
    "mai": 5, "juin": 6, "juillet": 7, "aout": 8,
    "septembre": 9, "octobre": 10, "novembre": 11, "decembre": 12
}

CATEGORY_MAPPING = {
    "Domaines actifs": "nb_domaines_actifs",
    "Totaux domaines": "nb_total_domaines",
    "Nouveaux domaines": "nb_nouveaux",
    "Domaines renouvellés": "nb_renouvelles",
    "Domaines résiliés": "nb_resilies",
    "Domaines en période grâces": "nb_grace",
    "Domaines en période de rédemption": "nb_redemption"
}

def validate():
    try:
        registrar = registrar_value
        year = int(year_value)
        month_name = month_value
        category = category_value
        value = int(entry_value.get())

        mois = MOIS_DICT.get(month_name.lower())
        if mois is None:
            print(f"❌ Mois invalide : {month_name}")
            return

        column_name = CATEGORY_MAPPING.get(category)
        if not column_name:
            print(f"❌ Catégorie inconnue : {category}")
            return

        session = Session()
        # Recherche ou création
        record = session.query(DomaineStat).filter_by(
            registrateur=registrar,
            annee=year,
            mois=mois
        ).first()

        if not record:
            record = DomaineStat(registrateur=registrar, annee=year, mois=mois)

        setattr(record, column_name, value)
        session.add(record)
        session.commit()
        session.close()

        print(f"✅ Donnée enregistrée : {registrar} | {year}-{mois:02d} | {category} = {value}")
        entry_value.delete(0, 'end')  # Vider le champ

    except ValueError:
        print("❌ Veuillez entrer un nombre entier.")
    except Exception as e:
        print(f"❌ Erreur : {e}")

# --- Interface graphique (inchangée) ---
CTk.set_appearance_mode("light")
app = CTk.CTk()
app.title("Remplissage de la base de données")
app.geometry("400x600+40+60")
app.resizable(False, False)

registrars_list = ["IDS TECHNOLOGIE", "HOSTEUR", "NETMASTER SARL", "IT NUM"]
mois = [
    "janvier", "fevrier", "mars", "avril", "mai", "juin",
    "juillet", "aout", "septembre", "octobre", "novembre", "decembre"
]

PADDING = 20
main_frame = CTk.CTkFrame(master=app)
main_frame.pack(padx=PADDING, pady=PADDING, fill="both", expand=True)

# 1. Registrar
CTk.CTkLabel(master=main_frame, text="Registrar:").pack(pady=(0, 5), anchor="w")
cbb_registrar = CTk.CTkComboBox(master=main_frame, values=registrars_list, command=__registrar_value)
cbb_registrar.pack(pady=(0, 15), fill="x")

# 2. Année
CTk.CTkLabel(master=main_frame, text="L'année:").pack(pady=(0, 5), anchor="w")
cbb_year = CTk.CTkComboBox(master=main_frame, values=[str(i) for i in range(2021, datetime.now().year + 1)], command=__year_value)
cbb_year.pack(pady=(0, 15), fill="x")

# 3. Mois
CTk.CTkLabel(master=main_frame, text="Le mois:").pack(pady=(0, 5), anchor="w")
cbb_month = CTk.CTkComboBox(master=main_frame, values=mois, command=__month_value)
cbb_month.pack(pady=(0, 15), fill="x")

# 4. Catégorie
CTk.CTkLabel(master=main_frame, text="La catégorie:").pack(pady=(0, 5), anchor="w")
cbb_category = CTk.CTkComboBox(master=main_frame,
    values=[
        "Domaines actifs", "Totaux domaines", "Nouveaux domaines",
        "Domaines renouvellés", "Domaines résiliés",
        "Domaines en période grâces", "Domaines en période de rédemption"
    ],
    command=__category_value
)
cbb_category.pack(pady=(0, 15), fill="x")

# 5. Valeur
CTk.CTkLabel(master=main_frame, text="Le nombre:").pack(pady=(0, 5), anchor="w")
entry_value = CTk.CTkEntry(master=main_frame)
entry_value.pack(pady=(0, 15), anchor="w")

# Bouton
CTk.CTkButton(master=main_frame, text="Valider", command=validate).pack(pady=20)

if __name__ == '__main__':
    app.mainloop()