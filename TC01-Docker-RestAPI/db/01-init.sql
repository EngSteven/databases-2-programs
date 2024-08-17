-- create tasks database For postgres
CREATE DATABASE tasks;

\c tasks

CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT NOT NULL
);

INSERT INTO tasks (name, description) VALUES
('task1', 'This is task 1'),
('task2', 'This is task 2'),
('task3', 'This is task 3');
