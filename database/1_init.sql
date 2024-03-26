CREATE OR REPLACE FUNCTION update_modified_column()
	RETURNS trigger LANGUAGE plpgsql AS $function$
BEGIN
    NEW.updated = now();
    RETURN NEW; 
END;
$function$;


CREATE TABLE users (
	id TEXT PRIMARY KEY,
	created timestamp NOT NULL DEFAULT NOW(),
	updated timestamp NOT NULL DEFAULT NOW(),
	email TEXT NOT NULL UNIQUE,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	type TEXT NOT NULL,
	password_hash TEXT NOT NULL
);

CREATE TRIGGER users_modtime BEFORE UPDATE
	ON users
	FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TABLE books (
	id TEXT PRIMARY KEY,
	created timestamp NOT NULL DEFAULT NOW(),
	updated timestamp NOT NULL DEFAULT NOW(),
	isbn TEXT NOT NULL,
	publisher TEXT NOT NULL,
	year INT NOT NULL,
	quantity INT NOT NULL,
	title TEXT NOT NULL,
	author TEXT NOT NULL
);

CREATE TRIGGER books_modtime BEFORE UPDATE
	ON books
	FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TABLE users_books (
	id SERIAL PRIMARY KEY,
	created timestamp NOT NULL DEFAULT NOW(),
	updated timestamp NOT NULL DEFAULT NOW(),
	user_id TEXT NOT NULL REFERENCES users(id),
	book_id TEXT NOT NULL REFERENCES books(id),
	status TEXT NOT NULL
);

CREATE TRIGGER users_books_modtime BEFORE UPDATE
	ON users_books
	FOR EACH ROW EXECUTE PROCEDURE update_modified_column();