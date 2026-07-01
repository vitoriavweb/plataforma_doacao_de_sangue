import sqlalchemy as sa
from db import Base, engine


class Usuario(Base):
    __tablename__ = 'usuario'
    id_usuario = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    pnome = sa.Column(sa.String(15), nullable=False)
    mnome = sa.Column(sa.String(15), nullable=False)
    unome = sa.Column(sa.String(15), nullable=False)
    sexo = sa.Column(sa.String(1), nullable=False)
    cpf = sa.Column(sa.String(11), nullable=False, unique=True)
    email = sa.Column(sa.String(100), unique=True)
    senha_login = sa.Column(sa.String(50), nullable=False)


class Agendamento(Base):
    __tablename__ = 'agendamento'
    id_agendamento = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    horario = sa.Column(sa.String(100))
    local_doacao = sa.Column(sa.String(100))
    dia = sa.Column(sa.Date)
    status = sa.Column(sa.String(50), default="Agendado")
    num_atendimento = sa.Column(sa.Integer)
    id_usuario = sa.Column(sa.Integer, sa.ForeignKey('usuario.id_usuario'), nullable=False)
    cnpj_instituicao = sa.Column(sa.String, sa.ForeignKey('hemocentro.cnpj'), nullable=False)


class Triagem(Base):
    __tablename__ = 'triagem'
    id_triagem = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    id_agendamento = sa.Column(sa.Integer, sa.ForeignKey('agendamento.id_agendamento'), nullable=False)
    peso = sa.Column(sa.Float)
    pressao_arterial = sa.Column(sa.String(20))
    resultado = sa.Column(sa.String(20))
    observacoes = sa.Column(sa.String(250))


class Hemocentro(Base):
    __tablename__ = 'hemocentro'
    cnpj = sa.Column(sa.String, primary_key=True)
    nome = sa.Column(sa.String)
    cidade = sa.Column(sa.String)


class Hospital(Base):
    __tablename__ = 'hospital'
    id_hospital = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    nome = sa.Column(sa.String(100), nullable=False)
    cnpj = sa.Column(sa.String(14))
    cnpj_instituicao = sa.Column(sa.String, sa.ForeignKey('hemocentro.cnpj'), nullable=False)


class Campanha(Base):
    __tablename__ = 'campanha'
    id_campanha = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    nome = sa.Column(sa.String(100), nullable=False)
    data_inicio = sa.Column(sa.Date)
    data_fim = sa.Column(sa.Date)
    objetivo = sa.Column(sa.String(250))
    descricao = sa.Column(sa.String(250))
    cnpj_instituicao = sa.Column(sa.String, sa.ForeignKey('hemocentro.cnpj'), nullable=False)


class HistoricoDoador(Base):
    __tablename__ = 'historico_doador'
    id_historico = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    id_usuario = sa.Column(sa.Integer, sa.ForeignKey('usuario.id_usuario'), nullable=False)
    cnpj_instituicao = sa.Column(sa.String, sa.ForeignKey('hemocentro.cnpj'), nullable=False)
    local_doacao = sa.Column(sa.String(100), nullable=False, default="")
    volume_sangue = sa.Column(sa.String(50), nullable=False, default="")
    data_doacao = sa.Column(sa.Date, nullable=False)

class Estoque(Base):
    __tablename__ = 'estoque'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    cnpj_instituicao = sa.Column(sa.String, sa.ForeignKey('hemocentro.cnpj'))
    tipo_sanguineo = sa.Column(sa.String)
    quantidade_ml = sa.Column(sa.Integer)


class SolicitacaoSangue(Base):
    __tablename__ = 'solicitacao_sangue'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    cnpj_instituicao = sa.Column(sa.String, sa.ForeignKey('hemocentro.cnpj'))
    tipo_sanguineo = sa.Column(sa.String)
    status = sa.Column(sa.String, default="Pendente")


# Cria as tabelas no banco, caso ainda não existam
Base.metadata.create_all(engine)
