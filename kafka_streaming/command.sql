
CREATE TABLE netflix_prediction (
    "User_ID" bigint PRIMARY KEY,
    "Movie1" varchar(255),
    "Movie2" varchar(255),
    "Movie3" varchar(255),
    "Movie4" varchar(255),
    "Movie5" varchar(255)
);


INSERT INTO netflix_prediction ("User_ID", "Movie1", "Movie2", "Movie3", "Movie4", "Movie5") VALUES (123456789012345, 'The Shawshank Redemption', 'The Godfather', 'The Dark Knight', 'Pulp Fiction', 'Forrest Gump');

SELECT * FROM netflix_prediction

--DROP TABLE netflix_prediction;
