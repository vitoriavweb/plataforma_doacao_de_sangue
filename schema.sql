CREATE TABLE Personagens (id INT PRIMARY KEY, nome VARCHAR(100), casa VARCHAR(50));
CREATE TABLE Dragoes (id INT PRIMARY KEY, nome VARCHAR(100), personagem_id INT);
CREATE TABLE Batalhas (id INT PRIMARY KEY, nome VARCHAR(100), ano INT);
CREATE TABLE Participacoes_Batalhas (personagem_id INT, batalha_id INT, resultado VARCHAR(50));
CREATE TABLE Relacionamentos (personagem_1_id INT, personagem_2_id INT, tipo_relacao VARCHAR(50));

INSERT INTO Personagens VALUES (1, 'Rhaenyra', 'Targaryen');
INSERT INTO Personagens VALUES (2,'Daemon', 'Targaryen');
INSERT INTO Personagens VALUES (3,'Alicent', 'Hightower');
INSERT INTO Personagens VALUES (4, 'Otto', 'Hightower');
INSERT INTO Personagens VALUES (5,'Criston', 'Cole');

INSERT INTO Dragoes VALUES (1,'Syrax', 1);
INSERT INTO Dragoes VALUES (2, 'Caraxes', 2);

INSERT INTO Batalhas VALUES (1, 'Batalha 1', 129);
INSERT INTO Batalhas VALUES (2, 'Batalha 2', 132);
INSERT INTO Batalhas VALUES (3,'Batalha 3', 133);

INSERT INTO Participacoes_Batalhas VALUES (1, 2, 'Venceu');
INSERT INTO Participacoes_Batalhas VALUES (2, 3, 'Venceu');
INSERT INTO Participacoes_Batalhas VALUES (5, 1,'Venceu');

INSERT INTO Relacionamentos VALUES (1, 2, 'Casados');
INSERT INTO Relacionamentos VALUES (3, 4, 'Filha e Pai');