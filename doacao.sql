DROP TABLE IF EXISTS comprovante_doador CASCADE;
DROP TABLE IF EXISTS historico_doador CASCADE;
DROP TABLE IF EXISTS triagem CASCADE;
DROP TABLE IF EXISTS agendamento CASCADE;
DROP TABLE IF EXISTS campanhas CASCADE;
DROP TABLE IF EXISTS doacao_emergencia CASCADE;
DROP TABLE IF EXISTS hospitais CASCADE;
DROP TABLE IF EXISTS telefone CASCADE;
DROP TABLE IF EXISTS instituicoes CASCADE;
DROP TABLE IF EXISTS doador CASCADE;
DROP TABLE IF EXISTS administrador CASCADE;
DROP TABLE IF EXISTS endereco CASCADE;
DROP TABLE IF EXISTS usuario CASCADE;

CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY, --serial(geral numeros)
    pnome VARCHAR(15) NOT NULL,
	mnome VARCHAR(15) NOT NULL,
	unome VARCHAR(15) NOT NULL,
	sexo CHAR(1) NOT NULL,
    cpf CHAR(11) NOT NULL UNIQUE, --unique(coisa unica)
    email VARCHAR(100) UNIQUE,
    senha_login VARCHAR(50) NOT NULL
);

CREATE TABLE endereco (
    id_endereco SERIAL PRIMARY KEY, --chave primaria
    cep CHAR(8) NOT NULL, --char(tamanho fixo)
    cidade VARCHAR(40) NOT NULL, --varchar(tamanho variavel)
    rua VARCHAR(100) NOT NULL,
    numero INT NOT NULL, 
    estado CHAR(2) NOT NULL      
);

CREATE TABLE administrador (
    id_usuario INT PRIMARY KEY,
	id_endereco INT NOT NULL,

    CONSTRAINT fk_admin_usuario FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
	--referenciando a chave estrangeira
	CONSTRAINT fk_administrador_endereco FOREIGN KEY (id_endereco) REFERENCES endereco(id_endereco)
);

CREATE TABLE doador (
    id_usuario INT PRIMARY KEY, --integer(numeros inteiros)
    tipo_sanguineo VARCHAR(3) NOT NULL, 
    id_endereco INT NOT NULL, -- Coluna que vai guardar o ID do endereço
    
    -- Herança (O Doador É um Usuário):
    CONSTRAINT fk_doador_usuario FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    
    --Ligação com Endereço (O Doador TEM um Endereço):
    CONSTRAINT fk_doador_endereco FOREIGN KEY (id_endereco) REFERENCES endereco(id_endereco)
);

CREATE TABLE instituicoes (
    id_instituicao SERIAL PRIMARY KEY,
	nome VARCHAR(100) NOT NULL,
    cnpj CHAR(14) NOT NULL UNIQUE,
    horarios_funcionamento VARCHAR(100) NOT NULL,
    id_endereco INT NOT NULL,
    id_usuario INT NOT NULL, 

	--REFENRENCIA ADMINISTRADOR
    CONSTRAINT fk_instituicao_admin FOREIGN KEY (id_usuario) REFERENCES administrador(id_usuario),
	--REFENRENCIA ENDERECO
    CONSTRAINT fk_instituicao_endereco FOREIGN KEY (id_endereco) REFERENCES endereco(id_endereco)
);

CREATE TABLE telefone(
	id_instituicao int PRIMARY KEY,
	numero char(9) NOT NULL,

	--refenrencia instituicoes
	CONSTRAINT fk_telefone_instituicao FOREIGN KEY (id_instituicao) REFERENCES instituicoes(id_instituicao)
);

CREATE TABLE hospitais(
	id_hospital SERIAL PRIMARY KEY,
	nome VARCHAR(100) NOT NULL,
	cnpj CHAR(14),
	id_instituicao INT NOT NULL,

	--REFERENCIA INSTITUICAO
	CONSTRAINT fk_hospitais_instituicao FOREIGN KEY (id_instituicao) REFERENCES instituicoes(id_instituicao)
);

CREATE TABLE doacao_emergencia(
	id_emergencia SERIAL PRIMARY KEY,
	paciente_pnome VARCHAR(15) NOT NULL,
	paciente_unome VARCHAR(15) NOT NULL,
	descricao VARCHAR(300),
	tipo_sanguineo_paciente VARCHAR(50) NOT NULL,
	id_hospital INTEGER NOT NULL,
	id_instituicao INT NOT NULL,

	--REFERENCIA HOSPITAIS
	CONSTRAINT fk_emergencia_hospital FOREIGN KEY (id_hospital) REFERENCES hospitais(id_hospital),
	--referencia instituicao
	CONSTRAINT fk_emergencia_instituicao FOREIGN KEY (id_instituicao) REFERENCES instituicoes(id_instituicao)
);

CREATE TABLE campanhas(
	id_campanha SERIAL PRIMARY KEY,
	data_inicio DATE,
	data_fim DATE,
	objetivo VARCHAR(250),
	descricao VARCHAR(250),
	nome VARCHAR(100) NOT NULL,
	id_instituicao INT NOT NULL,

	--REFERENCIA INSTITUICOES
	CONSTRAINT fk_campanhas_instituicoes FOREIGN KEY (id_instituicao) REFERENCES instituicoes(id_instituicao)
);

CREATE TABLE agendamento(
	id_agendamento SERIAL PRIMARY KEY,
	horario VARCHAR(100),
	local_doacao VARCHAR(100), --poderia ser o id do endereco? o endereco ter id ta certo??
	dia DATE,
	status VARCHAR(50),
	num_atendimento INT,
	id_doador INT NOT NULL,
	id_instituicao INT NOT NULL,

	--referencia doador
	CONSTRAINT fk_agendamento_doador FOREIGN KEY (id_doador) REFERENCES doador(id_usuario),
	--refenrencia instituicoes 
	CONSTRAINT fk_agendamento_instituicoes FOREIGN KEY (id_instituicao) REFERENCES instituicoes(id_instituicao)
);

CREATE TABLE triagem(
	id_triagem SERIAL PRIMARY KEY,
	id_agendamento INT NOT NULL,
	
	--REFERENCIA AGENDAMENTO
	CONSTRAINT fk_triagem_agendamento FOREIGN KEY (id_agendamento) REFERENCES agendamento(id_agendamento)
);

CREATE TABLE questionario(
	id_pergunta SERIAL PRIMARY KEY,
	pergunta VARCHAR(250) NOT NULL
);

CREATE TABLE respostas_questionario(
	id_triagem INT NOT NULL,
	id_pergunta INT NOT NULL,
	resposta CHAR(1) NOT NULL,
	PRIMARY KEY(id_triagem, id_pergunta),

	CONSTRAINT fk_respostas_triagem FOREIGN KEY (id_triagem) REFERENCES triagem (id_triagem),
	CONSTRAINT fk_respostas_pergunta FOREIGN KEY (id_pergunta) REFERENCES questionario(id_pergunta)
);

CREATE TABLE historico_doador(
	id_historico SERIAL PRIMARY KEY,
	id_instituicao INT NOT NULL,
	id_doador INT NOT NULL,
	local_doacao VARCHAR(100),
	volume_sangue VARCHAR(50),
	data_doacao DATE,
	
	--REFENRENCIA DOADOR
	CONSTRAINT fk_historico_doador FOREIGN KEY (id_doador) REFERENCES doador(id_usuario),
	CONSTRAINT fk_historico_instituicao FOREIGN KEY (id_instituicao) REFERENCES instituicoes(id_instituicao)
);

CREATE TABLE comprovante_doador(
	id_comprovante SERIAL PRIMARY KEY,
	id_doador INT NOT NULL,
	id_instituicao INT NOt NULL,
	data_emissao DATE,
	data_vencimento DATE,

	--REFERENCIA DOADOR
	CONSTRAINT fk_comprovante_doador FOREIGN KEY (id_doador) REFERENCES doador (id_usuario),
	---refenrecia instituicoes
	CONSTRAINT fk_comprovante_instituicao FOREIGN KEY (id_instituicao) REFERENCES instituicoes(id_instituicao)
);
