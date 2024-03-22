CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	created timestamp NOT NULL DEFAULT NOW(),
	updated timestamp NOT NULL DEFAULT NOW(),
	email TEXT NOT NULL UNIQUE,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	type INTEGER NOT NULL,
	password_hash TEXT NOT NULL
);
CREATE TABLE books (
	id SERIAL PRIMARY KEY,
	created timestamp NOT NULL DEFAULT NOW(),
	updated timestamp NOT NULL DEFAULT NOW(),
	title TEXT NOT NULL,
	author TEXT NOT NULL,
	year INTEGER NOT NULL
);
CREATE TABLE users_books (
	id SERIAL PRIMARY KEY,
	created timestamp NOT NULL DEFAULT NOW(),
	updated timestamp NOT NULL DEFAULT NOW(),
	user_id INTEGER NOT NULL REFERENCES users(id),
	book_id INTEGER NOT NULL REFERENCES books(id),
	status TEXT NOT NULL,
);