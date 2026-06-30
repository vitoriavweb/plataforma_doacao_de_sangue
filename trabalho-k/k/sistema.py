import panel as pn
import pandas as pd
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, sessionmaker

pn.extension('tabulator', notifications=True)

engine = sa.create_engine("sqlite:///doacoes.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Hemocentro(Base):
    __tablename__ = 'hemocentro'
    cnpj = sa.Column(sa.String, primary_key=True)
    nome = sa.Column(sa.String)
    cidade = sa.Column(sa.String)

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

Base.metadata.create_all(engine)
cnpj_em_edicao = None
id_estoque_em_edicao = None 

# --- Componentes de Interface (Widgets) ---
txt_cnpj = pn.widgets.TextInput(name='CNPJ da Instituição')
txt_nome = pn.widgets.TextInput(name='Nome do Hemocentro')
txt_cidade = pn.widgets.TextInput(name='Cidade')
btn_salvar = pn.widgets.Button(name='💾 Cadastrar / Atualizar', button_type='primary')

tabela_instituicoes = pn.widgets.Tabulator(name='Instituições Cadastradas', selectable=True, width=600, height=300)

select_inst_estoque = pn.widgets.Select(name='Selecionar Instituição', options=[])
select_tipo_estoque = pn.widgets.Select(name='Tipo Sanguíneo', options=['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'])
int_qtd_estoque = pn.widgets.IntInput(name='Quantidade (ml)', value=0, step=50)
btn_salvar_estoque = pn.widgets.Button(name='📦 Salvar Estoque', button_type='success', width=280)
btn_editar_estoque = pn.widgets.Button(name='✏️ Editar Estoque Selecionado', button_type='warning', width=250)
tabela_estoque = pn.widgets.Tabulator(name='Estoque Atual', width=550, height=300, selectable=True) 

select_inst_solicitacao = pn.widgets.Select(name='Instituição Solicitante', options=[])
select_tipo_solicitacao = pn.widgets.Select(name='Tipo Sanguíneo Necessário', options=['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'])
btn_criar_solicitacao = pn.widgets.Button(name='🚨 Criar Solicitação', button_type='danger', width=280)
btn_atender_solicitacao = pn.widgets.Button(name='✅ Atender Selecionado', button_type='success', width=280)
tabela_solicitacoes = pn.widgets.Tabulator(name='Pedidos de Sangue', width=550, height=300, selectable=True)


# --- Funções de Atualização (Views) ---
def atualizar_seletores():
    instituicoes = session.query(Hemocentro).all()
    opcoes = {i.nome: i.cnpj for i in instituicoes}
    select_inst_estoque.options = opcoes
    select_inst_solicitacao.options = opcoes

def atualizar_tabela_instituicoes():
    lista = session.query(Hemocentro).all()
    dados = {
        'CNPJ': [h.cnpj for h in lista],
        'Nome': [h.nome for h in lista],
        'Cidade': [h.cidade for h in lista]
    }
    tabela_instituicoes.value = pd.DataFrame(dados)

def atualizar_tabela_estoque():
    lista = session.query(Estoque).all()
    dados = {
        'ID': [e.id for e in lista],
        'Instituição (CNPJ)': [str(e.cnpj_instituicao) for e in lista],
        'Tipo Sanguíneo': [str(e.tipo_sanguineo) for e in lista],
        'Qtd (ml)': [int(e.quantidade_ml) for e in lista]
    }
    tabela_estoque.value = pd.DataFrame(dados)

def atualizar_tabela_solicitacoes():
    lista = session.query(SolicitacaoSangue).all()
    dados = {
        'ID': [s.id for s in lista],
        'Instituição': [str(s.cnpj_instituicao) for s in lista],
        'Tipo Requerido': [str(s.tipo_sanguineo) for s in lista],
        'Status': [str(s.status) for s in lista]
    }
    tabela_solicitacoes.value = pd.DataFrame(dados)


# --- Funções de Eventos (Callbacks) ---
def salvar_instituicao(event):
    global cnpj_em_edicao
    if not txt_cnpj.value or not txt_nome.value:
        pn.state.notifications.error('Preencha o CNPJ e o Nome!')
        return
    
    if cnpj_em_edicao:
        instituicao = session.query(Hemocentro).filter_by(cnpj=cnpj_em_edicao).first()
        if instituicao:
            if cnpj_em_edicao != txt_cnpj.value:
                session.delete(instituicao)
                session.commit()
                instituicao = Hemocentro(cnpj=txt_cnpj.value, nome=txt_nome.value, cidade=txt_cidade.value)
                session.add(instituicao)
            else:
                instituicao.nome = txt_nome.value
                instituicao.cidade = txt_cidade.value
            pn.state.notifications.success('Instituição editada com sucesso!')
    else:
        existe = session.query(Hemocentro).filter_by(cnpj=txt_cnpj.value).first()
        if existe:
            pn.state.notifications.error('Este CNPJ já está cadastrado!')
            return
        novo = Hemocentro(cnpj=txt_cnpj.value, nome=txt_nome.value, cidade=txt_cidade.value)
        session.add(novo)
        pn.state.notifications.success('Instituição cadastrada com sucesso!')
    
    session.commit()
    cnpj_em_edicao = None
    txt_cnpj.disabled = False
    txt_cnpj.value = txt_nome.value = txt_cidade.value = ""
    atualizar_tabela_instituicoes()
    atualizar_seletores()

btn_salvar.on_click(salvar_instituicao)

btn_preparar_edicao = pn.widgets.Button(name='✏️ Editar Selecionado', button_type='warning', width=180)
btn_remover = pn.widgets.Button(name='❌ Remover Selecionado', button_type='danger', width=180)

def preparar_edicao(event):
    global cnpj_em_edicao
    selecionado = tabela_instituicoes.selection
    if not selecionado:
        pn.state.notifications.warning('Selecione uma linha na tabela primeiro!')
        return
    index = selecionado[0]
    dados_linha = tabela_instituicoes.value.iloc[index]
    
    cnpj_em_edicao = str(dados_linha['CNPJ'])
    txt_cnpj.value = cnpj_em_edicao
    txt_nome.value = str(dados_linha['Nome'])
    txt_cidade.value = str(dados_linha['Cidade'])
    pn.state.notifications.info('Altere os dados nos campos acima e clique em Salvar.')

def remover_instituicao(event):
    selecionado = tabela_instituicoes.selection
    if not selecionado:
        pn.state.notifications.warning('Selecione uma linha na tabela primeiro!')
        return
    index = selecionado[0]
    dados_linha = tabela_instituicoes.value.iloc[index]
    cnpj_alvo = str(dados_linha['CNPJ'])
    
    instituicao = session.query(Hemocentro).filter_by(cnpj=cnpj_alvo).first()
    if instituicao:
        session.delete(instituicao)
        session.commit()
        pn.state.notifications.success('Instituição removida com sucesso!')
        atualizar_tabela_instituicoes()
        atualizar_seletores()

btn_preparar_edicao.on_click(preparar_edicao)
btn_remover.on_click(remover_instituicao)

def adicionar_estoque(event):
    global id_estoque_em_edicao
    if not select_inst_estoque.value:
        pn.state.notifications.error('Cadastre uma instituição primeiro!')
        return
    
    if int_qtd_estoque.value < 0:
        pn.state.notifications.error('A quantidade não pode ser negativa!')
        return

    if id_estoque_em_edicao:
        item = session.query(Estoque).filter_by(id=id_estoque_em_edicao).first()
        if item:
            item.cnpj_instituicao = select_inst_estoque.value
            item.tipo_sanguineo = select_tipo_estoque.value
            item.quantidade_ml = int_qtd_estoque.value
            pn.state.notifications.success('Estoque alterado com sucesso!')
    else:
        item = session.query(Estoque).filter_by(cnpj_instituicao=select_inst_estoque.value, tipo_sanguineo=select_tipo_estoque.value).first()
        if item:
            item.quantidade_ml += int_qtd_estoque.value
            pn.state.notifications.success('Quantidade somada ao estoque existente!')
        else:
            item = Estoque(cnpj_instituicao=select_inst_estoque.value, tipo_sanguineo=select_tipo_estoque.value, quantidade_ml=int_qtd_estoque.value)
            session.add(item)
            pn.state.notifications.success('Novo lote de estoque adicionado!')
    
    session.commit()
    id_estoque_em_edicao = None
    select_inst_estoque.disabled = False
    select_tipo_estoque.disabled = False
    int_qtd_estoque.value = 0
    atualizar_tabela_estoque()

def preparar_edicao_estoque(event):
    global id_estoque_em_edicao
    selecionado = tabela_estoque.selection
    if not selecionado:
        pn.state.notifications.warning('Selecione uma linha na tabela de estoque primeiro!')
        return
    
    index = selecionado[0]
    dados_linha = tabela_estoque.value.iloc[index]
    id_estoque_em_edicao = int(dados_linha['ID'])
    
    select_inst_estoque.value = str(dados_linha['Instituição (CNPJ)'])
    select_tipo_estoque.value = str(dados_linha['Tipo Sanguíneo'])
    int_qtd_estoque.value = int(dados_linha['Qtd (ml)'])
    
    pn.state.notifications.info('Modifique a quantidade e clique em Salvar Estoque.')

btn_salvar_estoque.on_click(adicionar_estoque)
btn_editar_estoque.on_click(preparar_edicao_estoque)

def criar_solicitacao(event):
    if not select_inst_solicitacao.value:
        pn.state.notifications.error('Cadastre uma instituição primeiro!')
        return
    nova = SolicitacaoSangue(cnpj_instituicao=select_inst_solicitacao.value, tipo_sanguineo=select_tipo_solicitacao.value, status="Pendente")
    session.add(nova)
    session.commit()
    pn.state.notifications.success('Solicitação de urgência registrada!')
    atualizar_tabela_solicitacoes()

def atender_solicitacao(event):
    selecionado = tabela_solicitacoes.selection
    if not selecionado:
        pn.state.notifications.warning('Selecione uma linha na tabela de solicitações primeiro!')
        return
    
    index = selecionado[0]
    dados_linha = tabela_solicitacoes.value.iloc[index]
    solicitacao_id = int(dados_linha['ID'])
    
    solicitacao = session.query(SolicitacaoSangue).filter_by(id=solicitacao_id).first()
    
    if not solicitacao:
        pn.state.notifications.error('Solicitação não encontrada.')
        return
    
    if solicitacao.status == "Atendido":
        pn.state.notifications.warning('Esta solicitação já foi atendida!')
        return

    estoque_item = session.query(Estoque).filter_by(
        cnpj_instituicao=solicitacao.cnpj_instituicao, 
        tipo_sanguineo=solicitacao.tipo_sanguineo
    ).first()
    
    volume_bolsa = 450 
    
    if not estoque_item:
        pn.state.notifications.error(f'Não há nenhum estoque de {solicitacao.tipo_sanguineo} registrado para esta instituição!')
        return

    if estoque_item.quantidade_ml >= volume_bolsa:
        estoque_item.quantidade_ml -= volume_bolsa
        solicitacao.status = "Atendido"
        session.commit()
        
        pn.state.notifications.success(f'Sucesso! 450ml deduzidos do estoque.')
        atualizar_tabela_solicitacoes()
        atualizar_tabela_estoque()
    else:
        pn.state.notifications.error(f'Estoque insuficiente! Há apenas {estoque_item.quantidade_ml}ml disponíveis (Necessário: 450ml).')

btn_criar_solicitacao.on_click(criar_solicitacao)
btn_atender_solicitacao.on_click(atender_solicitacao)


# --- Estrutura de Layout das Abas ---
aba_instituicao = pn.Column(
    "### Gerenciar Instituições (Hemocentros)",
    pn.Row(
        pn.Column(txt_cnpj, txt_nome, txt_cidade, btn_salvar, width=300),
        pn.Column(tabela_instituicoes, pn.Row(btn_preparar_edicao, btn_remover))
    )
)

aba_estoque = pn.Column(
    "### Controle de Estoque de Sangue",
    pn.Row(
        pn.Column(select_inst_estoque, select_tipo_estoque, int_qtd_estoque, btn_salvar_estoque, width=300),
        pn.Column(tabela_estoque, btn_editar_estoque)
    )
)

aba_solicitacao = pn.Column(
    "### Solicitações de Sangue de Urgência",
    pn.Row(
        pn.Column(
            select_inst_solicitacao,
            select_tipo_solicitacao,
            btn_criar_solicitacao,
            pn.layout.Divider(),
            btn_atender_solicitacao,
            width=300
        ),
        pn.Column(tabela_solicitacoes)
    )
)

layout = pn.Tabs(
    ('Instituições (CRUD)', aba_instituicao),
    ('Estoque', aba_estoque),
    ('Solicitações', aba_solicitacao)
)

# --- Inicialização Inicial de Dados ---
atualizar_tabela_instituicoes()
atualizar_tabela_estoque()
atualizar_tabela_solicitacoes()
atualizar_seletores()

layout.show()