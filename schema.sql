CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    desc TEXT,
    price INTEGER,
    image BLOB,
    category INTEGER,
    condition INTEGER,
    user_id INTEGER REFERENCES users
);
