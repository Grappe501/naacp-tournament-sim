CREATE TABLE IF NOT EXISTS teams (

    id SERIAL PRIMARY KEY,
    name TEXT,
    slug TEXT UNIQUE,
    conference TEXT

);
