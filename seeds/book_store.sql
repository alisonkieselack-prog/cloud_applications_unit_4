DROP TABLE IF EXISTS books;
DROP SEQUENCE IF EXISTS books_id_seq;

CREATE SEQUENCE IF NOT EXISTS books_id_seq;
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    img_url text
);

INSERT INTO books (title, author, img_url) VALUES ('The Gruffalo', 'Julia Donaldson', './static/gruffalo.jpg');
INSERT INTO books (title, author, img_url) VALUES ('Ada Twist, Scientist', 'Andrea Beaty', './static/ada_twist.jpg');
INSERT INTO books (title, author, img_url) VALUES ('The Girl Who Drank the Moon', 'Kelly Barnhill', './static/girl_drank_moon.jpg');
INSERT INTO books (title, author, img_url) VALUES ('Dragons in a Bag', 'Zetta Elliott', './static/dragons_in_a_bag.jpg'); 