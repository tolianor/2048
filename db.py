import sqlite3

con = sqlite3.connect("score.db")

_dbContext = con.cursor()

_dbContext.execute("""CREATE TABLE IF NOT EXISTS score_2048 (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name text,
                   score int
                   )""")


def the_best():
    _dbContext.execute("""
        SELECT name gamer, max(score) score FROM score_2048 
        GROUP BY name 
        ORDER by score DESC 
        limit 3
    """)
    return _dbContext.fetchall()


def insert_result(name, score):
    _dbContext.execute(f"INSERT INTO score_2048 (name, score) VALUES ('{name}', '{score}')")
    con.commit()
