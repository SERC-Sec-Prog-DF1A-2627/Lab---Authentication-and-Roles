-- Reset deletes only this demonstration database's tables.
DROP TABLE IF EXISTS auth_sessions;
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('student', 'staff', 'admin'))
);
