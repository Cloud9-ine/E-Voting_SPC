/* setup.sql
 * initializes the database
 */

DROP TABLE IF EXISTS Registration;
CREATE TABLE Registration (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(128) NOT NULL,
  passwd VARCHAR(128) NOT NULL,
  county VARCHAR(128) NOT NULL,
  zip INTEGER NOT NULL,
  dob_day INTEGER NOT NULL,
  dob_mon INTEGER NOT NULL,
  dob_year INTEGER NOT NULL,
  UNIQUE(name,passwd,county,zip,dob_day,dob_mon,dob_year)
);

DROP TABLE IF EXISTS Election;
CREATE TABLE Election (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  deadline_day INTEGER NOT NULL,
  deadline_mon INTEGER NOT NULL,
  deadline_year INTEGER NOT NULL,
  status INTEGER NOT NULL,
  UNIQUE(deadline_day,deadline_mon,deadline_year)
);

DROP TABLE IF EXISTS Office;
CREATE TABLE Office (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(128) NOT NULL,
  election INTEGER REFERENCES Election (id),
  UNIQUE(name,election)
);

DROP TABLE IF EXISTS AllowedZip;
CREATE TABLE AllowedZip (
  zip INTEGER NOT NULL PRIMARY KEY,
  office INTEGER REFERENCES Office (id),
  UNIQUE(zip,office)
);

DROP TABLE IF EXISTS Candidate;
CREATE TABLE Candidate (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(128) NOT NULL,
  votes INTEGER NOT NULL,
  office INTEGER REFERENCES Office(id),
  UNIQUE(name,office)
);

DROP TABLE IF EXISTS Vote;
CREATE TABLE Vote (
  voter INTEGER REFERENCES Registration (id),
  candidate INTEGER REFERENCES Candidate (id),
  office INTEGER REFERENCES Office (id),
  UNIQUE(voter,office)
);

INSERT INTO Election(deadline_day,deadline_mon,deadline_year,status) VALUES (05, 12, 121, 1);
INSERT INTO Office(name, election) VALUES ('Realism', 1), ('Impressionism', 1), ('Cubism', 1);
INSERT INTO Candidate(name,votes,office) VALUES ('Gustave Courbet', 0, 1), ('Jean-François Millet', 0, 1);
INSERT INTO Candidate(name,votes,office) VALUES ('Claude Monet', 0, 2), ('Pierre-Auguste Renoir', 0, 2);
INSERT INTO Candidate(name,votes,office) VALUES ('Pablo Picasso', 0, 3), ('Georges Braque', 0, 3);

.quit
