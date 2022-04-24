DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS chirps;
CREATE TABLE chirps (
    id SERIAL PRIMARY KEY,
    user_id integer,
    title character varying(100) NOT NULL,
    body character varying(255) NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);

DROP TABLE IF EXISTS commentary;
CREATE TABLE commentary (
    id SERIAL PRIMARY KEY,
    chirp_id integer NOT NULL,
    user_id integer NOT NULL,
    body character varying(255) NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_chirps FOREIGN KEY (chirp_id) REFERENCES chirps(id)

);

INSERT INTO users (username, name, password) VALUES ('admin', 'Administrator', 'admin');
