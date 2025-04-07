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

CREATE TABLE category (
    name TEXT UNIQUE
);

CREATE TABLE condition (
    name TEXT UNIQUE
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users,
    item_id INTEGER REFERENCES items,
    comment TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO category (name) VALUES ("autot");
INSERT INTO category (name) VALUES ("elektroniikka");
INSERT INTO category (name) VALUES ("vaatteet");
INSERT INTO category (name) VALUES ("huonekalut");
INSERT INTO category (name) VALUES ("lelut");

INSERT INTO condition (name) VALUES ("erinomainen");
INSERT INTO condition (name) VALUES ("hyvä");
INSERT INTO condition (name) VALUES ("kohtalainen");
INSERT INTO condition (name) VALUES ("huono");