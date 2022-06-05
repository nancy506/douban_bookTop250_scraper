DROP TABLE IF EXISTS books;

-- CREATE TABLE user (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   username TEXT UNIQUE NOT NULL,
--   password TEXT NOT NULL
-- );

CREATE TABLE books (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  booktitle TEXT NOT NULL,
  year INT
);

-- INSERT INTO books
-- FROM './templates/title.csv'
-- WITH
-- (
--     FIRSTROW = 2, -- as 1st one is header
--     FIELDTERMINATOR = ',',  --CSV field delimiter
--     ROWTERMINATOR = '\n',   --Use to shift the control to next row
--     TABLOCK
-- );