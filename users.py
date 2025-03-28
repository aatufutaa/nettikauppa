import db

def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_items(user_id):
    sql = "SELECT * FROM items WHERE user_id = ? ORDER BY id DESC"
    return db.query(sql, [user_id])

def create_user(username, password):
    sql = "INSERT INTO users (username, password) VALUES (?, ?)"
    db.execute(sql, [username, password])

def check_login(username, password):
    sql = "SELECT id, password FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None

    user_id = result[0]["id"]
    password1 = result[0]["password"]
    if password == password1:
        return user_id
    else:
        return None
