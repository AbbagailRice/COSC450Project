CREATE DATABASE IF NOT EXISTS movie_db;
USE movie_db;

CREATE TABLE Genres (
    GenreID INT AUTO_INCREMENT PRIMARY KEY,
    GenreName VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE Certificates (
    CertificateID INT AUTO_INCREMENT PRIMARY KEY,
    CertificateName VARCHAR(20) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE People (
    PersonID INT AUTO_INCREMENT PRIMARY KEY,
    PersonName VARCHAR(255) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE Roles (
    RoleID INT AUTO_INCREMENT PRIMARY KEY,
    RoleName VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE Movies (
    MovieID INT AUTO_INCREMENT PRIMARY KEY,
    Series_Title VARCHAR(255) NOT NULL,
    Released_Year INT,
    RuntimeMinutes INT,
    Overview TEXT,
    Poster_Link VARCHAR(1024),
    IMDB_Rating DECIMAL(3, 1),
    Meta_score INT,
    No_of_Votes BIGINT,
    Gross_Revenue BIGINT,
    CertificateID INT,
    FOREIGN KEY (CertificateID) REFERENCES Certificates(CertificateID)
) ENGINE=InnoDB;

CREATE TABLE MovieGenres (
    MovieID INT NOT NULL,
    GenreID INT NOT NULL,
    PRIMARY KEY (MovieID, GenreID),
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID),
    FOREIGN KEY (GenreID) REFERENCES Genres(GenreID)
) ENGINE=InnoDB;

CREATE TABLE MoviePeople (
    MovieID INT NOT NULL,
    PersonID INT NOT NULL,
    RoleID INT NOT NULL,
    PRIMARY KEY (MovieID, PersonID, RoleID),
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID),
    FOREIGN KEY (PersonID) REFERENCES People(PersonID),
    FOREIGN KEY (RoleID) REFERENCES Roles(RoleID)
) ENGINE=InnoDB;

