-- Схема базы данных агентства недвижимости.

CREATE TABLE IF NOT EXISTS apartments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address TEXT UNIQUE NOT NULL,
    area INTEGER NOT NULL,
    price INTEGER NOT NULL DEFAULT 0,
    is_sold INTEGER NOT NULL DEFAULT 0,
    is_rented INTEGER NOT NULL DEFAULT 0,
    type TEXT NOT NULL DEFAULT 'Apartment',
    payload TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    budget INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS agents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    experience INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS deals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    apartment_id INTEGER NOT NULL,
    client_id INTEGER,
    agent_id INTEGER,
    commission REAL DEFAULT 0,
    date TEXT NOT NULL,
    FOREIGN KEY (apartment_id) REFERENCES apartments(id),
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (agent_id) REFERENCES agents(id)
);
