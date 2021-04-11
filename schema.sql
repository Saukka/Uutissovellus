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
