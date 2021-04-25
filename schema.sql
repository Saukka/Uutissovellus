CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    title TEXT,
    body TEXT,
    reporter TEXT,
    date TIMESTAMP,
    views INTEGER,
    topic TEXT,
    visible INTEGER 
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    topic TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    usertype TEXT
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    news_id INTEGER,
    username TEXT,
    comment TEXT,
    date TIMESTAMP,
    visible INTEGER
);
