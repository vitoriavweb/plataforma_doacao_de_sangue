-- 1. Tabela ENDERECO (Criada primeiro, pois outras dependem dela)
CREATE TABLE ENDERECO (
    cep INT PRIMARY KEY,
    cidade VARCHAR(100) NOT NULL,
    rua VARCHAR(150) NOT NULL,
    numero INT NOT NULL,
    estado VARCHAR(50) NOT NULL
);

-- 2. Tabela USUARIO (Base para Administrador e Doador)
CREATE TABLE USUARIO (
    id_usuario INT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    CPF VARCHAR(14) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_login VARCHAR(255) NOT NULL
);

-- 3. Tabela ADMINISTRADOR
CREATE TABLE ADMINISTRADOR (
    id_usuario INT PRIMARY KEY,
    FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario) ON DELETE CASCADE
);

-- 4. Tabela DOADOR
CREATE TABLE DOADOR (
    id_usuario INT PRIMARY KEY,
    tipo_sanguineo VARCHAR(3) NOT NULL,
    endereco_cep INT,
    FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (endereco_cep) REFERENCES ENDERECO(cep)
);

-- 5. Tabela INSTITUICOES
CREATE TABLE INSTITUICOES (
    id_instituicao INT PRIMARY KEY,
    cnpj VARCHAR(18) UNIQUE NOT NULL,
    horario_funcionamento VARCHAR(100),
    endereco_cep INT,
    id_administrador INT,
    FOREIGN KEY (endereco_cep) REFERENCES ENDERECO(cep),
    FOREIGN KEY (id_administrador) REFERENCES ADMINISTRADOR(id_usuario)
);

-- 6. Tabela TELEFONE (Chave primária composta ou baseada na instituição)
CREATE TABLE TELEFONE (
    id_instituicao INT,
    numero INT,
    PRIMARY KEY (id_instituicao, numero),
    FOREIGN KEY (id_instituicao) REFERENCES INSTITUICOES(id_instituicao) ON DELETE CASCADE
);

-- 7. Tabela HOSPITAIS
CREATE TABLE HOSPITAIS (
    id_hospital INT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    id_instituicao INT,
    FOREIGN KEY (id_instituicao) REFERENCES INSTITUICOES(id_instituicao)
);

-- 8. Tabela DOACAO_EMERGENCIA
CREATE TABLE DOACAO_EMERGENCIA (
    id_emergencia INT PRIMARY KEY,
    paciente VARCHAR(150) NOT NULL,
    descricao TEXT,
    tipo_sanguineo VARCHAR(3) NOT NULL,
    id_hospital INT,
    id_instituicao INT,
    FOREIGN KEY (id_hospital) REFERENCES HOSPITAIS(id_hospital),
    FOREIGN KEY (id_instituicao) REFERENCES INSTITUICOES(id_instituicao)
);

-- 9. Tabela CAMPANHAS
CREATE TABLE CAMPANHAS (
    id_campanha INT PRIMARY KEY,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    objetivo VARCHAR(255),
    descricao TEXT,
    nome VARCHAR(150) NOT NULL,
    id_instituicao INT,
    FOREIGN KEY (id_instituicao) REFERENCES INSTITUICOES(id_instituicao)
);

-- 10. Tabela AGENDAMENTO   
DROP TABLE IF EXISTS AGENDAMENTO;
CREATE TABLE AGENDAMENTO (
    id_agendamento INT PRIMARY KEY,
    horario VARCHAR(50) NOT NULL,
    local VARCHAR(150),
    dia DATE NOT NULL,
    status VARCHAR(50),
    num_atendimento INT,
    id_doador INT,
    id_instituicao INT,
    FOREIGN KEY (id_doador) REFERENCES DOADOR(id_usuario),
    FOREIGN KEY (id_instituicao) REFERENCES INSTITUICOES(id_instituicao)
);

-- 11. Tabela TRIAGEM
CREATE TABLE TRIAGEM (
    id_triagem INT PRIMARY KEY,
    id_agendamento INT UNIQUE, -- UNIQUE garante a relação 1 para 1 do seu diagrama
    questionario TEXT,
    teve_febre BOOLEAN,
    fez_tatuagem BOOLEAN,
    observacoes TEXT,
    FOREIGN KEY (id_agendamento) REFERENCES AGENDAMENTO(id_agendamento)
);

-- 12. Tabela HISTORICO_DOADOR
CREATE TABLE HISTORICO_DOADOR (
    id_historico INT PRIMARY KEY,
    id_doador INT,
    local_doacao VARCHAR(150),
    volume_sangue DECIMAL(5,2),
    doacoes_realizadas INT,
    FOREIGN KEY (id_doador) REFERENCES DOADOR(id_usuario)
);

-- 13. Tabela COMPROVANTE_DOADOR
CREATE TABLE COMPROVANTE_DOADOR (
    id_comprovante INT PRIMARY KEY,
    id_doador INT,
    id_instituicao INT,
    data_emissao DATE NOT NULL,
    informacoes_doador TEXT,
    informacoes_instituicao TEXT,
    FOREIGN KEY (id_doador) REFERENCES DOADOR(id_usuario),
    FOREIGN KEY (id_instituicao) REFERENCES INSTITUICOES(id_instituicao)
);