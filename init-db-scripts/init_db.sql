-- Tworzymy tabelę użytkowników
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Tworzymy tabelę kursów
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Tworzymy tabelę uniwersytetów
CREATE TABLE universities (
    university_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Tworzymy tabelę plików
CREATE TABLE files (
    file_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    file_text TEXT,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    course_id INT REFERENCES courses(course_id) ON DELETE SET NULL,
    university_id INT REFERENCES universities(university_id) ON DELETE SET NULL
);

-- Tworzymy tabelę ulubionych plików (favourite)
CREATE TABLE favourites (
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    file_id INT REFERENCES files(file_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, file_id)
);

-- Dodajemy przykładowych użytkowników
INSERT INTO users (name, surname, email, password)
VALUES
('John', 'Doe', 'john.doe@example.com', 'hashed_password_1'),
('Jane', 'Smith', 'jane.smith@example.com', 'hashed_password_2');

-- Dodajemy przykładowe kursy
INSERT INTO courses (name)
VALUES
('Mathematics 101'),
('Physics 101'),
('Computer Science 101');

-- Dodajemy przykładowe uniwersytety
INSERT INTO universities (name)
VALUES
('Politechnika Krakowska'),
('Akademia Górniczo-Hutnicza');

-- Dodajemy przykładowe pliki
INSERT INTO files (name, file_text, user_id, course_id, university_id)
VALUES
('Math Homework 1', 'This is the content of Math Homework 1.', 1, 1, 1),
('Physics Lab Report', 'This is a physics lab report.', 2, 2, 2);

-- Dodajemy przykładowe ulubione pliki
INSERT INTO favourites (user_id, file_id)
VALUES
(1, 1),
(2, 2);
