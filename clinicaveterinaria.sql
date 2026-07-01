-- 1
SELECT * FROM Animal 
WHERE animal_id IN (
    SELECT animal_id FROM Consulta 
    WHERE data_consulta BETWEEN '2024-01-01' AND '2024-12-31'
);
--2 
SELECT * FROM Animal 
WHERE animal_id NOT IN (
    SELECT animal_id FROM Consulta 
    WHERE animal_id IS NOT NULL
);
--3
SELECT * FROM Tutor t
WHERE EXISTS (
    SELECT 1 FROM Animal a
    JOIN Consulta c ON a.animal_id = c.animal_id
    WHERE a.tutor_id = t.tutor_id
);
--4
SELECT * FROM Tutor t
WHERE NOT EXISTS (
    SELECT 1 FROM Animal a
    JOIN Consulta c ON a.animal_id = c.animal_id
    WHERE a.tutor_id = t.tutor_id
);
--5
SELECT * FROM Procedimento
WHERE valor > ANY (
    SELECT p.valor FROM Procedimento p
    JOIN Consulta_Procedimento cp ON p.procedimento_id = cp.procedimento_id
    JOIN Consulta c ON cp.consulta_id = c.consulta_id
    WHERE c.data_consulta BETWEEN '2024-01-01' AND '2024-12-31'
);
--6
SELECT * FROM Procedimento
WHERE valor > ALL (
    SELECT p.valor FROM Procedimento p
    JOIN Consulta_Procedimento cp ON p.procedimento_id = cp.procedimento_id
    JOIN Consulta c ON cp.consulta_id = c.consulta_id
    WHERE c.data_consulta BETWEEN '2024-01-01' AND '2024-12-31'
);

--7
SELECT animal_id FROM Consulta WHERE data_consulta BETWEEN '2024-01-01' AND '2024-12-31'
INTERSECT
SELECT animal_id FROM Consulta WHERE data_consulta BETWEEN '2025-01-01' AND '2025-12-31';
--8
SELECT animal_id FROM Consulta WHERE data_consulta BETWEEN '2024-01-01' AND '2024-12-31'
INTERSECT ALL
SELECT animal_id FROM Consulta WHERE data_consulta BETWEEN '2025-01-01' AND '2025-12-31';
--9
SELECT animal_id FROM Consulta WHERE data_consulta BETWEEN '2024-01-01' AND '2024-12-31'
UNION
SELECT animal_id FROM Consulta WHERE data_consulta BETWEEN '2025-01-01' AND '2025-12-31';
--10
SELECT t.tutor_id, t.nome FROM Tutor t
JOIN Animal a ON t.tutor_id = a.tutor_id
JOIN Consulta c ON a.animal_id = c.animal_id
EXCEPT
SELECT t.tutor_id, t.nome FROM Tutor t
JOIN Animal a ON t.tutor_id = a.tutor_id
JOIN Consulta c ON a.animal_id = c.animal_id
JOIN Consulta_Procedimento cp ON c.consulta_id = cp.consulta_id
JOIN Procedimento p ON cp.procedimento_id = p.procedimento_id
WHERE p.descricao LIKE '%Cirurgia%';