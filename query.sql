-- 1)
SELECT Personagens.nome, Dragoes.nome
FROM Personagens
INNER JOIN Dragoes ON Personagens.id = Dragoes.personagem_id;


-- 2)
SELECT DISTINCT Personagens.nome
FROM Personagens
INNER JOIN Participacoes_Batalhas ON Personagens.id = Participacoes_Batalhas.personagem_id
INNER JOIN Batalhas ON Participacoes_Batalhas.batalha_id = Batalhas.id
WHERE Batalhas.ano BETWEEN 132 AND 133;


-- 3)
SELECT Dragoes.nome, Personagens.nome
FROM Dragoes
INNER JOIN Personagens ON Dragoes.personagem_id = Personagens.id
WHERE Dragoes.nome LIKE '%r';


-- 4)
SELECT Personagens.nome
FROM Personagens
LEFT JOIN Dragoes ON Personagens.id = Dragoes.personagem_id
WHERE Dragoes.id IS NULL;


-- 5) 
SELECT DISTINCT Personagens.nome, Personagens.casa
FROM Personagens
LEFT JOIN Dragoes ON Personagens.id = Dragoes.personagem_id
LEFT JOIN Participacoes_Batalhas ON Personagens.id = Participacoes_Batalhas.personagem_id
WHERE Dragoes.id IS NOT NULL OR Participacoes_Batalhas.batalha_id IS NOT NULL;


-- 6)
SELECT Personagens.nome
FROM Personagens
WHERE Personagens.casa IN ('Targaryen', 'Hightower');


-- 7)
SELECT DISTINCT Personagens.nome
FROM Personagens
INNER JOIN Participacoes_Batalhas ON Personagens.id = Participacoes_Batalhas.personagem_id
WHERE Personagens.casa = 'Targaryen';


-- 8)
SELECT Personagens.nome
FROM Personagens
INNER JOIN Dragoes ON Personagens.id = Dragoes.personagem_id
WHERE Dragoes.nome LIKE 'S%';


-- 9) 
SELECT Personagens.nome, Batalhas.nome
FROM Personagens
INNER JOIN Participacoes_Batalhas ON Personagens.id = Participacoes_Batalhas.personagem_id
INNER JOIN Batalhas ON Participacoes_Batalhas.batalha_id = Batalhas.id
WHERE Participacoes_Batalhas.resultado = 'Venceu';


--10)
SELECT 
    p1.nome AS personagem_principal, 
    Relacionamentos.tipo_relacao, 
    p2.nome AS personagem_relacionado
FROM Relacionamentos
INNER JOIN Personagens AS p1 ON Relacionamentos.personagem_1_id = p1.id
INNER JOIN Personagens AS p2 ON Relacionamentos.personagem_2_id = p2.id;