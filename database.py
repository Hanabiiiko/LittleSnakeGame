import sqlite3

DB_NAME = 'snake_scores.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT UNIQUE NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_best_score(nickname):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT score FROM leaderboard WHERE nickname = ?', (nickname,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def save_score(nickname, score):
    current_best = get_best_score(nickname)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM leaderboard WHERE nickname = ?', (nickname,))
    exists = cursor.fetchone()

    if not exists:
        cursor.execute('INSERT INTO leaderboard (nickname, score) VALUES (?, ?)', (nickname, score))
    elif score > current_best:
        cursor.execute('UPDATE leaderboard SET score = ? WHERE nickname = ?', (score, nickname))
        
    conn.commit()
    conn.close()

def get_top_10():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT nickname, score FROM leaderboard ORDER BY score DESC LIMIT 10')
    results = cursor.fetchall()
    conn.close()
    return results