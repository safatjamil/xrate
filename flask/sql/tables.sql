CREATE TABLE rates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    currency VARCHAR(5) NOT NULL UNIQUE,
    rate DOUBLE(15) NOT NULL,
    date VARCHAR(15) NOT NULL,
    time VARCHAR(15) NOT NULL,
    timezone VARCHAR(50) NOT NULL
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(200) NOT NULL
);

CREATE TABLE details (
    pk_id INTEGER NOT NULL DEFAULT 1,
    id PRIMARY KEY NOT NULL DEFAULT 1,
    date VARCHAR(15) NOT NULL,
    time VARCHAR(15) NOT NULL,
    timezone VARCHAR(50) NOT NULL,
    CONSTRAINT uniq_pkid UNIQUE (pk_id),
    CONSTRAINT single_row CHECK(pk_id = 1)
);