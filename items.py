import db

def add_item(title, desc, price, image, category, condition, user_id):
    sql = """INSERT INTO items (title, desc, price, image, category, condition, user_id)
             VALUES (?, ?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [title, desc, price, image, category, condition, user_id])

    item_id = db.last_insert_id()
    return item_id

def get_items():
    sql = """SELECT items.*, users.username
             FROM items
            JOIN users ON items.user_id = users.id"""
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT *
             FROM items, users
             WHERE items.user_id = users.id AND
                   items.id = ?"""
    result = db.query(sql, [item_id])
    return result[0] if result else None

def update_item(item_id, title, desc, price, image, category, condition):
    sql = """UPDATE items SET title = ?,
                              desc = ?,
                              price = ?,
                              image = ?,
                              category = ?,
                              condition = ?
                          WHERE id = ?"""
    db.execute(sql, [title, desc, price, image, category, condition, item_id])

def remove_item(item_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def find_items(query):
    sql = """SELECT *
             FROM items
             WHERE title LIKE ? OR desc LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])

def get_category_list():
    sql = "SELECT * FROM category"
    return [row[0] for row in db.query(sql)]

def get_condition_list():
    sql = "SELECT * FROM condition"
    return [row[0] for row in db.query(sql)]