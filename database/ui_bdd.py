import customtkinter as CTk
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# === Ancien DatabaseManager (inchangé pour compatibilité) ===
class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.Base = declarative_base()
        self.Session = sessionmaker(bind=self.engine)
        self._define_models()

    def _define_models(self):
        self.YEARS = ['2021', '2022', '2023', '2024', '2025']
        for year in self.YEARS:
            table_class = type(
                f"Table{year}",
                (self.Base,),
                {
                    '__tablename__': year,
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
            setattr(self, f'table_{year}', table_class)

    def get_month_number(self, month_name):
        mois_dict = {
            "janvier": "01", "fevrier": "02", "mars": "03", "avril": "04",
            "mai": "05", "juin": "06", "juillet": "07", "aout": "08",
            "septembre": "09", "octobre": "10", "novembre": "11", "decembre": "12"
        }
        return mois_dict.get(month_name.lower(), "00")

    def format_data_value(self, month_name, value):
        month_number = self.get_month_number(month_name)
        return f"{month_number}-{value}"

    def insert_data(self, registrar, year, month, category, value):
        try:
            session = self.Session()
            table_class = getattr(self, f'table_{year}')
            formatted_value = self.format_data_value(month, value)
            category_mapping = {
                "Domaines actifs": "nb_domaines_actifs",
                "Totaux domaines": "nb_total_domaines",
                "Nouveaux domaines": "nb_total_nouveaux",
                "Domaines renouvellés": "nb_domaines_renouvelles",
                "Domaines résiliés": "nb_domaines_resilises",
                "Domaines en période grâces": "nb_domaines_grace",
                "Domaines en période de rédemption": "nb_domaines_redemption"
            }
            column_name = category_mapping.get(category)
            if not column_name:
                print(f"❌ Catégorie non reconnue: {category}")
                session.close()
                return False

            record_data = {
                "nom_registrars": registrar,
                "nb_total_domaines": "",
                "nb_domaines_actifs": "",
                "nb_total_nouveaux": "",
                "nb_domaines_renouvelles": "",
                "nb_domaines_resilises": "",
                "nb_domaines_grace": "",
                "nb_domaines_redemption": "",
                "nb_domaines_expires": "",
                "nb_domaines_litigieux": ""
            }
            record_data[column_name] = formatted_value
            new_record = table_class(**record_data)
            session.add(new_record)
            session.commit()
            print(f"✅ NOUVELLE ligne insérée: {registrar} - {year} - {month} - {category} = {value}")
            print(f"   ID de la nouvelle ligne: {new_record.id}")
            session.close()
            return True
        except Exception as e:
            print(f"❌ Erreur lors de l'insertion: {e}")
            return False

# === Variables globales ===
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

# === NOUVELLE FONCTION : Gestion des données trimestrielles ===
def inserer_stat_trimestrielle(annee: int, trimestre: int, total: int, actifs: int, expires: int, resilies: int):
    # Import local pour éviter conflit
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, Integer, UniqueConstraint
    from sqlalchemy.orm import sessionmaker

    Base = declarative_base()

    class StatistiqueTrimestrielle(Base):
        __tablename__ = "statistiques_trimestrielles"
        id = Column(Integer, primary_key=True, index=True)
        annee = Column(Integer, nullable=False)
        trimestre = Column(Integer, nullable=False)
        nb_total_domaines = Column(Integer, default=0)
        nb_domaines_actifs = Column(Integer, default=0)
        nb_domaines_expires = Column(Integer, default=0)
        nb_domaines_resilies = Column(Integer, default=0)
        __table_args__ = (UniqueConstraint('annee', 'trimestre', name='_unique_annee_trimestre'),)

    engine = create_engine("sqlite:///database.db", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        record = session.query(StatistiqueTrimestrielle).filter_by(annee=annee, trimestre=trimestre).first()
        if not record:
            record = StatistiqueTrimestrielle(annee=annee, trimestre=trimestre)
        record.nb_total_domaines = total
        record.nb_domaines_actifs = actifs
        record.nb_domaines_expires = expires
        record.nb_domaines_resilies = resilies
        session.add(record)
        session.commit()
        print(f"✅ Trimestre {trimestre} de {annee} enregistré !")
    except Exception as e:
        session.rollback()
        print(f"❌ Erreur : {e}")
    finally:
        session.close()

def open_trimester_window():
    tri_window = CTk.CTkToplevel()
    tri_window.title("Données Trimestrielles")
    tri_window.geometry("400x500")
    tri_window.resizable(False, False)

    frame = CTk.CTkFrame(tri_window)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    CTk.CTkLabel(frame, text="Année :").pack(anchor="w", pady=(0, 5))
    entry_annee = CTk.CTkEntry(frame)
    entry_annee.pack(fill="x", pady=(0, 10))

    CTk.CTkLabel(frame, text="Trimestre :").pack(anchor="w", pady=(0, 5))
    cbb_tri = CTk.CTkComboBox(frame, values=["1", "2", "3", "4"])
    cbb_tri.set("1")
    cbb_tri.pack(fill="x", pady=(0, 10))

    fields = {}
    labels = ["Total domaines", "Domaines actifs", "Domaines expirés", "Domaines résiliés"]
    for lbl in labels:
        CTk.CTkLabel(frame, text=f"{lbl} :").pack(anchor="w", pady=(0, 5))
        entry = CTk.CTkEntry(frame)
        entry.pack(fill="x", pady=(0, 8))
        fields[lbl] = entry

    def save():
        try:
            annee = int(entry_annee.get())
            tri = int(cbb_tri.get())
            total = int(fields["Total domaines"].get() or 0)
            actifs = int(fields["Domaines actifs"].get() or 0)
            expires = int(fields["Domaines expirés"].get() or 0)
            resilies = int(fields["Domaines résiliés"].get() or 0)
            inserer_stat_trimestrielle(annee, tri, total, actifs, expires, resilies)
            tri_window.destroy()
        except Exception as e:
            print(f"❌ Erreur de saisie : {e}")

    CTk.CTkButton(frame, text="Enregistrer", command=save).pack(pady=20)

# === Interface principale ===
CTk.set_appearance_mode("light")
app = CTk.CTk()
app.title("Remplissage de la base de données")
app.geometry("400x650+40+60")
app.resizable(False, False)

registrars_list = ["IDS TECHNOLOGIE", "HOSTEUR", "NETMASTER SARL", "IT NUM"]
mois = ["janvier", "fevrier", "mars", "avril", "mai", "juin",
        "juillet", "aout", "septembre", "octobre", "novembre", "decembre"]

PADDING = 20
main_frame = CTk.CTkFrame(master=app)
main_frame.pack(padx=PADDING, pady=PADDING, fill="both", expand=True)

# --- Anciens widgets ---
CTk.CTkLabel(main_frame, text="Registrar:").pack(pady=(0, 5), anchor="w")
cbb_registrar = CTk.CTkComboBox(main_frame, values=registrars_list, command=__registrar_value)
cbb_registrar.pack(pady=(0, 15), fill="x")

CTk.CTkLabel(main_frame, text="L'année:").pack(pady=(0, 5), anchor="w")
cbb_year = CTk.CTkComboBox(main_frame, values=[str(i) for i in range(2021, datetime.now().year + 1)], command=__year_value)
cbb_year.pack(pady=(0, 15), fill="x")

CTk.CTkLabel(main_frame, text="Le mois:").pack(pady=(0, 5), anchor="w")
cbb_month = CTk.CTkComboBox(main_frame, values=mois, command=__month_value)
cbb_month.pack(pady=(0, 15), fill="x")

CTk.CTkLabel(main_frame, text="La catégorie:").pack(pady=(0, 5), anchor="w")
cbb_category = CTk.CTkComboBox(main_frame,
    values=["Domaines actifs", "Totaux domaines", "Nouveaux domaines",
            "Domaines renouvellés", "Domaines résiliés",
            "Domaines en période grâces", "Domaines en période de rédemption"],
    command=__category_value)
cbb_category.pack(pady=(0, 15), fill="x")

CTk.CTkLabel(main_frame, text="Le nombre:").pack(pady=(0, 5), anchor="w")
entry_value = CTk.CTkEntry(main_frame)
entry_value.pack(pady=(0, 15), anchor="w")

CTk.CTkButton(main_frame, text="Valider (mensuel)", command=lambda: validate()).pack(pady=10)
CTk.CTkButton(main_frame, text="📊 Saisir données trimestrielles", command=open_trimester_window).pack(pady=10)

def validate():
    try:
        value = int(entry_value.get())
        db_manager = DatabaseManager("database.db")
        db_manager.insert_data(registrar_value, year_value, month_value, category_value, value)
        entry_value.delete(0, 'end')
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == '__main__':
    app.mainloop()