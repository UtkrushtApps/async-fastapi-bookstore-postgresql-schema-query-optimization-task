-- Authors
INSERT INTO authors (name) VALUES ('J.K. Rowling'), ('George Orwell'), ('Jane Austen'), ('Mark Twain'), ('J.R.R. Tolkien'), ('Agatha Christie');
-- Categories
INSERT INTO categories (name) VALUES ('Fantasy'), ('Science Fiction'), ('Classic'), ('Mystery'), ('Drama'), ('Children');
-- Books (500+ books, randomized)
DO $$
DECLARE
    i INT := 1;
    anames TEXT[] := ARRAY['J.K. Rowling', 'George Orwell', 'Jane Austen', 'Mark Twain', 'J.R.R. Tolkien', 'Agatha Christie'];
    cnames TEXT[] := ARRAY['Fantasy', 'Science Fiction', 'Classic', 'Mystery', 'Drama', 'Children'];
    aidx INT;
    cidx INT;
    authorid INT;
    catid INT;
BEGIN
    WHILE i <= 500 LOOP
        aidx := 1 + (random()*5)::INT;
        cidx := 1 + (random()*5)::INT;
        SELECT id INTO authorid FROM authors WHERE name = anames[aidx];
        SELECT id INTO catid FROM categories WHERE name = cnames[cidx];
        INSERT INTO books (title, author_id, category_id) VALUES (
            'Sample Book #' || i,
            authorid,
            catid
        );
        i := i + 1;
    END LOOP;
END$$;
