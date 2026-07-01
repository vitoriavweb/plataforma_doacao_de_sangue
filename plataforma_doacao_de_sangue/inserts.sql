--usuarios
INSERT INTO usuario (pnome, mnome, unome, sexo, cpf, email, senha_login) VALUES
('Vitória', 'Vieira', 'Honório', 'F', '87498410498', 'vit@gmail.com', 'abcd123'),
('João', 'Carlos', 'Santos', 'M', '12345678901', 'joao@gmail.com', 'senha123'),
('Maria', 'Eduarda', 'Oliveira', 'F', '12345678902', 'maria@gmail.com', 'senha123'),
('Pedro', 'Henrique', 'Ribeiro', 'M', '12345678903', 'pedro@gmail.com', 'senha123'),
('Lucas', 'Gabriel', 'Almeida', 'M', '12345678904', 'lucas@gmail.com', 'senha123'),
('Mariana', 'Cruz', 'Teixeira', 'F', '12345678905', 'mariana@gmail.com', 'senha123'),
('André', 'Luiz', 'Carvalho', 'M', '12345678906', 'andre@gmail.com', 'senha123'),
('Larissa', 'Macedo', 'Viana', 'F', '12345678907', 'larissa@gmail.com', 'senha123'),
('Thiago', 'Ferreira', 'Cardoso', 'M', '12345678908', 'thiago@gmail.com', 'senha123'),
('Aline', 'Priscila', 'Borges', 'F', '12345678909', 'aline@gmail.com', 'senha123');

--doadores
INSERT INTO doador (id_usuario, tipo_sanguineo, id_endereco) VALUES
(1, 'O+', 1), 
(2, 'A+', 2),
(3, 'B+', 3),
(4, 'AB+', 4),
(5, 'O-', 1),
(6, 'A-', 2),
(7, 'B-', 3),
(8, 'AB-', 4),
(9, 'O+', 1),
(10, 'A+', 2);

--ADMS
INSERT INTO administrador (id_usuario) VALUES 
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10);

--ENDEREÇOS
INSERT INTO endereco (cep, cidade, rua, numero, estado) VALUES
('63900000', 'Quixadá', 'Rua Clarindo de Queiroz', 10, 'CE'),
('63900001', 'Quixadá', 'Avenida Plácido Castelo', 20, 'CE'),
('60000000', 'Fortaleza', 'Avenida da Universidade', 100, 'CE'),
('60000001', 'Fortaleza', 'Rua Barão do Rio Branco', 200, 'CE'),
('63900002', 'Quixadá', 'Rua Epitácio Pessoa', 45, 'CE'),
('63900003', 'Quixadá', 'Rua Rodrigues Júnior', 88, 'CE'),
('62000000', 'Sobral', 'Avenida Dom José', 500, 'CE'),
('63000000', 'Juazeiro do Norte', 'Rua São Pedro', 1000, 'CE'),
('60000002', 'Fortaleza', 'Avenida Santos Dumont', 1200, 'CE'),
('60000003', 'Fortaleza', 'Rua Monsenhor Tabosa', 350, 'CE');

--INSTITUIÇÕES
INSERT INTO instituicoes (nome, cnpj, horarios_funcionamento, id_endereco, id_usuario) VALUES
('Hemocentro 1', '11111111000101', '07:00 as 17:00', 1, 1),
('Hemocentro 2', '22222222000102', '07:00 as 17:00', 2, 2),
('Hemocentro 3', '33333333000103', '08:00 as 16:00', 3, 3),
('Hemocentro 4', '44444444000104', '08:00 as 16:00', 4, 4),
('Hemocentro 5', '55555555000105', '07:00 as 18:00', 1, 5),
('Hemocentro 6', '66666666000106', '07:00 as 18:00', 2, 6),
('Hemocentro 7', '77777777000107', '08:00 as 17:00', 3, 7),
('Hemocentro 8', '88888888000108', '07:00 as 13:00', 4, 8),
('Hemocentro 9', '99999999000109', '07:00 as 13:00', 1, 9),
('Hemocentro 10', '00000000000100', '08:00 as 16:00', 2, 10);

--TELEFONE
INSERT INTO telefone (id_instituicao, numero) VALUES
(1, '889911111'), 
(2, '889922222'),
(3, '859933333'),
(4, '859944444'),
(5, '889955555'),
(6, '889966666'),
(7, '859977777'),
(8, '889988888'),
(9, '889999999'),
(10, '859900000');

-- 7. HOSPITAIS
INSERT INTO hospitais (nome, cnpj, id_instituicao) VALUES
('Hospital A', '12345678000101', 1),
('Hospital B', '12345678000102', 2),
('Hospital C', '12345678000103', 3),
('Hospital D', '12345678000104', 4),
('Hospital E', '12345678000105', 5),
('Hospital F', '12345678000106', 6),
('Hospital G', '12345678000107', 7),
('Hospital H', '12345678000108', 8),
('Hospital I', '12345678000109', 9),
('Hospital J', '12345678000110', 10);

-- 8. DOAÇÃO EMERGÊNCIA
INSERT INTO doacao_emergencia (paciente_pnome, paciente_unome, descricao, tipo_sanguineo, id_hospital, id_instituicao) VALUES
('Paciente A', 'Sobrenome A', 'Urgente', 'O+', 1, 1), 
('Paciente B', 'Sobrenome B', 'Cirurgia', 'A-', 2, 2),
('Paciente C', 'Sobrenome C', 'Acidente', 'B+', 3, 3), 
('Paciente D', 'Sobrenome D', 'Urgente', 'AB-', 4, 4),
('Paciente E', 'Sobrenome E', 'Urgente', 'O-', 5, 5),
('Paciente F', 'Sobrenome F', 'Cirurgia', 'A+', 6, 6),
('Paciente G', 'Sobrenome G', 'Acidente', 'B-', 7, 7),
('Paciente H', 'Sobrenome H', 'Urgente', 'AB+', 8, 8),
('Paciente I', 'Sobrenome I', 'Urgente', 'O+', 9, 9),
('Paciente J', 'Sobrenome J', 'Cirurgia', 'A-', 10, 10);

-- 9. CAMPANHAS
INSERT INTO campanhas (data_inicio, data_fim, objetivo, descricao, nome, id_instituicao) VALUES
('2026-06-01', '2026-06-30', 'Meta A', 'Junho Vermelho', 'Campanha 1', 1),
('2026-06-01', '2026-06-30', 'Meta B', 'Junho Vermelho', 'Campanha 2', 2),
('2026-07-01', '2026-07-31', 'Meta C', 'Julho Solidario', 'Campanha 3', 3),
('2026-07-01', '2026-07-31', 'Meta D', 'Julho Solidario', 'Campanha 4', 4),
('2026-08-01', '2026-08-31', 'Meta E', 'Agosto Especial', 'Campanha 5', 5),
('2026-08-01', '2026-08-31', 'Meta F', 'Agosto Especial', 'Campanha 6', 6),
('2026-09-01', '2026-09-30', 'Meta G', 'Setembro Verde', 'Campanha 7', 7),
('2026-09-01', '2026-09-30', 'Meta H', 'Setembro Verde', 'Campanha 8', 8),
('2026-10-01', '2026-10-31', 'Meta I', 'Outubro Rosa', 'Campanha 9', 9),
('2026-11-01', '2026-11-30', 'Meta J', 'Novembro Azul', 'Campanha 10', 10);

-- 10. AGENDAMENTO 
INSERT INTO agendamento (horario, local_doacao, dia, status, num_atendimento, id_doador, id_instituicao) VALUES
('08:00', 'Triagem 1', '2026-06-01', 'Concluido', 101, 5, 1),
('09:00', 'Triagem 1', '2026-06-01', 'Concluido', 102, 6, 2),
('10:00', 'Triagem 1', '2026-06-02', 'Concluido', 103, 7, 3),
('11:00', 'Triagem 1', '2026-06-02', 'Concluido', 104, 8, 4),
('13:00', 'Triagem 1', '2026-06-03', 'Concluido', 105, 9, 5),
('14:00', 'Triagem 1', '2026-06-03', 'Concluido', 106, 10, 6),
('15:00', 'Triagem 1', '2026-06-04', 'Concluido', 107, 1, 7),
('16:00', 'Triagem 1', '2026-06-04', 'Concluido', 108, 2, 8),
('17:00', 'Triagem 1', '2026-06-05', 'Concluido', 109, 3, 9),
('08:30', 'Triagem 1', '2026-06-05', 'Concluido', 110, 4, 10);

-- 11. TRIAGEM 
INSERT INTO triagem (id_agendamento, questionario) VALUES
(1, 'Apto'), 
(2, 'Apto'), 
(3, 'Apto'), 
(4, 'Apto'), 
(5, 'Apto'), 
(6, 'Apto'), 
(7, 'Apto'), 
(8, 'Apto'), 
(9, 'Apto'), 
(10, 'Apto');

INSERT INTO questionario (id_pergunta, pergunta) VALUES
(1, 'Teve febre recentemente?'),
(2, 'Fez tatuagem no ultimo ano?'),
('Teve sintomas de gripe?'),
(4, 'Pesa mais de 50kg?'),
(5, 'Dormiu bem esta noite?'),
(6, 'Ingeriu alcool nas ultimas 12h?'),
(7, 'Esta em jejum prolongado?'),
(8, 'Ja doou sangue este ano?'),
(9, 'Passou por cirurgia recente?'),
(10, 'Viajou para o exterior?');

INSERT INTO respostas_questionario (id_triagem, id_pergunta, resposta) VALUES
(1, 1, 'N'),
(2, 2, 'N'),
(3, 3, 'N'),
(4, 4, 'S'),
(5, 5, 'S'),
(6, 6, 'N'),
(7, 7, 'N'),
(8, 8, 'S'),
(9, 9, 'N'),
(10, 10, 'N');

-- 12. HISTÓRICO DOADOR 
INSERT INTO historico_doador (id_doador, id_instituicao, local_doacao, volume_sangue, data_doacao) VALUES
(5, 1, 'Inst 1', '450ml', '2026-06-01'), 
(6, 2, 'Inst 2', '450ml', '2026-06-01'), 
(7, 3, 'Inst 3', '450ml', '2026-06-02'), 
(8, 4, 'Inst 4', '450ml', '2026-06-02'), 
(9, 5, 'Inst 5', '450ml', '2026-06-03'), 
(10, 6, 'Inst 6', '450ml', '2026-06-03'), 
(1, 7, 'Inst 7', '450ml', '2026-06-04'), 
(2, 8, 'Inst 8', '450ml', '2026-06-04'), 
(3, 9, 'Inst 9', '450ml', '2026-06-05'), 
(4, 10, 'Inst 10', '450ml', '2026-06-05');

-- 13. COMPROVANTE DOADOR
INSERT INTO comprovante_doador (id_doador, id_instituicao, data_emissao, data_vencimento) VALUES
(5, 1, '2026-06-01', '2026-09-01'),
(6, 2, '2026-06-01', '2026-09-01'),
(7, 3, '2026-06-02', '2026-09-02'),
(8, 4, '2026-06-02', '2026-09-02'),
(9, 5, '2026-06-03', '2026-09-03'),
(10, 6, '2026-06-03', '2026-09-03'),
(1, 7, '2026-06-04', '2026-09-04'),
(2, 8, '2026-06-04', '2026-09-04'),
(3, 9, '2026-06-05', '2026-09-05'),
(4, 10, '2026-06-05', '2026-09-05');