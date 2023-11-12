# Initialisierung der SQLite3 Datenbank.
# ! SCRIPT NUR AUSFUEHREN, WENN KEINE DATENBANK EXISTIERT!

import sqlite3

database_name = "temps_db"

connection = sqlite3.connect(database_name)


connection.close()
