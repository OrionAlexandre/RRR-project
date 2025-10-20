import customtkinter as CTk
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.Base = declarative_base()
        self.Session = sessionmaker(bind=self.engine)

        # Définition du modèle pour accéder aux tables existantes
        self._define_models()

    def _define_models(self):
        """Définit les modèles pour accéder aux tables existantes"""
        # Vous pouvez adapter cette partie selon le nom de vos tables
        self.YEARS = ['2021', '2022', '2023', '2024', '2025']  # Ajustez selon vos tables

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
        """Convertit le nom du mois en nombre"""
        mois_dict = {
            "janvier": "01", "fevrier": "02", "mars": "03", "avril": "04",
            "mai": "05", "juin": "06", "juillet": "07", "aout": "08",
            "septembre": "09", "octobre": "10", "novembre": "11", "decembre": "12"
        }
        return mois_dict.get(month_name.lower(), "00")

    def format_data_value(self, month_name, value):
        """Formate la valeur selon le format 'MM-valeur'"""
        month_number = self.get_month_number(month_name)
        return f"{month_number}-{value}"

    def insert_data(self, registrar, year, month, category, value):
        """
        Insère les données dans la base de données existante
        """
        try:
            session = self.Session()

            # Récupère la classe de table pour l'année
            table_class = getattr(self, f'table_{year}')

            # Vérifie si une entrée existe déjà pour ce registrar
            existing_record = session.query(table_class).filter(
                table_class.nom_registrars == registrar
            ).first()

            formatted_value = self.format_data_value(month, value)

            # Mapping des catégories vers les colonnes
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

            if existing_record:
                # Met à jour l'enregistrement existant
                setattr(existing_record, column_name, formatted_value)
                print(f"✅ Donnée mise à jour: {registrar} - {year} - {month} - {category} = {value}")
            else:
                # Crée un nouvel enregistrement
                record_data = {"nom_registrars": registrar}
                record_data[column_name] = formatted_value

                new_record = table_class(**record_data)
                session.add(new_record)
                print(f"✅ Nouvelle donnée insérée: {registrar} - {year} - {month} - {category} = {value}")

            session.commit()
            session.close()
            return True

        except Exception as e:
            print(f"❌ Erreur lors de l'insertion: {e}")
            return False


# Variables globales
global month_value
global year_value
global registrar_value
global category_value


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


CTk.set_appearance_mode("light")

app = CTk.CTk()
app.title("Remplissage de la base de données")
app.geometry("400x600+40+60")
app.resizable(False, False)

registrars_list = ["IDS TECHNOLOGIE",
                   "HOSTEUR",
                   "NETMASTER SARL",
                   "IT NUM", ]

mois = [
    "janvier", "fevrier", "mars", "avril", "mai", "juin",
    "juillet", "aout", "septembre", "octobre", "novembre", "decembre"
]

# Configuration du padding pour tous les widgets
PADDING = 20

# Frame principal pour organiser les widgets
main_frame = CTk.CTkFrame(master=app)
main_frame.pack(padx=PADDING, pady=PADDING, fill="both", expand=True)

# 1. Registrar
label_1 = CTk.CTkLabel(master=main_frame, text="Registrar:")
label_1.pack(pady=(0, 5), anchor="w")
cbb_registrar = CTk.CTkComboBox(master=main_frame,
                                values=registrars_list,
                                command=lambda value: __registrar_value(value))
cbb_registrar.pack(pady=(0, 15), fill="x")

# 2. Année
label_2 = CTk.CTkLabel(master=main_frame, text="L'année:")
label_2.pack(pady=(0, 5), anchor="w")
cbb_year = CTk.CTkComboBox(master=main_frame,
                           values=[f"{i}" for i in range(2021, datetime.now().year + 1)],
                           command=lambda value: __year_value(value))
cbb_year.pack(pady=(0, 15), fill="x")

# 3. Mois
label_3 = CTk.CTkLabel(master=main_frame, text="Le mois:")
label_3.pack(pady=(0, 5), anchor="w")
cbb_month = CTk.CTkComboBox(master=main_frame,
                            values=[*mois],
                            command=lambda value: __month_value(value))
cbb_month.pack(pady=(0, 15), fill="x")

# 4. Catégorie
label_4 = CTk.CTkLabel(master=main_frame, text="La catégorie:")
label_4.pack(pady=(0, 5), anchor="w")
cbb_category = CTk.CTkComboBox(master=main_frame,
                               values=["Domaines actifs",
                                       "Totaux domaines",
                                       "Nouveaux domaines",
                                       "Domaines renouvellés",
                                       "Domaines résiliés",
                                       "Domaines en période grâces",
                                       "Domaines en période de rédemption"],
                               command=lambda value: __category_value(value))
cbb_category.pack(pady=(0, 15), fill="x")


# 5. La valeur à enregistrer
label_5 = CTk.CTkLabel(master=main_frame, text="Le nombre:")
label_5.pack(pady=(0, 5), anchor="w")
entry_value = CTk.CTkEntry(master=main_frame)
entry_value.pack(pady=(0, 15), anchor="w")


def get_month_int(month: str, month_list):
    """Convertit le nom du mois en nombre"""
    try:
        return month_list.index(month) + 1
    except ValueError:
        return -1


def validate():
    """Fonction de validation qui affiche toutes les valeurs sélectionnées"""
    print("=== VALIDATION ===")
    print(f"Registrar: {registrar_value}")
    print(f"Année: {year_value}")
    print(f"Mois: {month_value}")
    print(f"Catégorie: {category_value}")
    value = int(entry_value.get())

    db_manager = DatabaseManager("database.db")
    db_manager.insert_data(registrar=registrar_value, year=year_value, month=month_value , category=category_value, value=value)
    print("Succès !")




# Bouton de validation
submit_button = CTk.CTkButton(master=main_frame,
                              text="Valider",
                              command=validate)
submit_button.pack(pady=20)


if __name__ == '__main__':
    app.mainloop()