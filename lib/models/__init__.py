import sqlite3

CONN = sqlite3.connect('hospital.db')
CURSOR = CONN.cursor()