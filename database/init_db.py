
from core_db import DataBase

def initialize_database():
    database = DataBase()
    pass



if __name__ == "__main__":
    try:
        initialize_database()
    except Exception as e:
        print(f"<init_db.py> - Erreur: {e}")
