import sqlite3

conn = sqlite3.connect('../medications.db')  
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS medications (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    medicament_type TEXT NOT NULL
)
''')


medicaments = [
    ('Ibuprofeno', 'analgésicos'),
    ('Naproxeno', 'analgésicos'),
    ('Aspirina', 'analgésicos'),
    ('Diclofenaco', 'analgésicos')
]

cursor.executemany('INSERT INTO medications (name, medicament_type) VALUES (?, ?)', medicaments)
conn.commit()

conn.close()
