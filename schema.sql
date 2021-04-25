CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    title TEXT,
    body TEXT,
    reporter TEXT,
    date TIMESTAMP 
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    topic TEXT
);

CREATE TABLE news_topics (
    id SERIAL PRIMARY KEY,
    news_id INTEGER REFERENCES news,
    topic_id INTEGER REFERENCES topics
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
    date TIMESTAMP
);
