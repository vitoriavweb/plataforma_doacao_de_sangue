import datetime
import panel as pn
import pandas as pd

from db import session
from models import Campanha, Hemocentro

id_campanha_em_edicao = None

txt_nome_campanha = pn.widgets.TextInput(name='Nome da Campanha')
date_inicio_campanha = pn.widgets.DatePicker(name='Data de Início', value=datetime.date.today())
date_fim_campanha = pn.widgets.DatePicker(name='Data de Fim', value=datetime.date.today())
txt_objetivo_campanha = pn.widgets.TextAreaInput(name='Objetivo', height=70)
txt_descricao_campanha = pn.widgets.TextAreaInput(name='Descrição', height=70)
select_inst_campanha = pn.widgets.Select(name='Instituição Responsável', options={})
btn_salvar_campanha = pn.widgets.Button(name='Cadastrar / Atualizar', button_type='primary')

tabela_campanhas = pn.widgets.Tabulator(
    name='Campanhas',
    selectable=True,
    width=700,
    height=300
)

btn_editar_campanha = pn.widgets.Button(name='Editar Selecionado', button_type='warning', width=180)
btn_remover_campanha = pn.widgets.Button(name='Remover Selecionado', button_type='danger', width=180)


def texto(valor):
    if valor is None:
        return ""
    try:
        if pd.isna(valor):
            return ""
    except Exception:
        pass
    s = str(valor).strip()
    if s.lower() in ("nan", "none", "<na>"):
        return ""
    return s


def formatar_data(valor):
    if valor is None:
        return ""
    if isinstance(valor, datetime.date):
        return valor.strftime("%Y-%m-%d")
    return texto(valor)


def atualizar_seletor_instituicoes_campanha():
    instituicoes = session.query(Hemocentro).all()
    opcoes = {
        f"{texto(i.nome)} (CNPJ {texto(i.cnpj)})": i.cnpj
        for i in instituicoes
    }
    select_inst_campanha.options = opcoes


def atualizar_tabela_campanhas():
    lista = session.query(Campanha).all()

    dados = pd.DataFrame({
        'ID': [texto(c.id_campanha) for c in lista],
        'Nome': [texto(c.nome) for c in lista],
        'Início': [formatar_data(c.data_inicio) for c in lista],
        'Fim': [formatar_data(c.data_fim) for c in lista],
        'Objetivo': [texto(c.objetivo) for c in lista],
        'Descrição': [texto(c.descricao) for c in lista],
        'Instituição (CNPJ)': [texto(c.cnpj_instituicao) for c in lista]
    }).astype(str).replace({"None": "", "nan": "", "NaN": "", "<NA>": ""})

    tabela_campanhas.value = dados


def limpar_campos_campanha():
    txt_nome_campanha.value = ""
    date_inicio_campanha.value = datetime.date.today()
    date_fim_campanha.value = datetime.date.today()
    txt_objetivo_campanha.value = ""
    txt_descricao_campanha.value = ""
    select_inst_campanha.value = None


def salvar_campanha(event, atualizar_seletores=None):
    global id_campanha_em_edicao

    nome = texto(txt_nome_campanha.value).strip()
    objetivo = texto(txt_objetivo_campanha.value).strip()
    descricao = texto(txt_descricao_campanha.value).strip()
    cnpj_instituicao = select_inst_campanha.value
    data_inicio = date_inicio_campanha.value
    data_fim = date_fim_campanha.value

    if not nome:
        pn.state.notifications.error('Preencha o nome da campanha!')
        return

    if not cnpj_instituicao:
        pn.state.notifications.error('Cadastre uma instituição primeiro!')
        return

    if not data_inicio:
        pn.state.notifications.error('Preencha a data de início!')
        return

    if not data_fim:
        pn.state.notifications.error('Preencha a data de fim!')
        return

    if data_fim < data_inicio:
        pn.state.notifications.error('A data de fim não pode ser anterior à data de início!')
        return

    try:
        if id_campanha_em_edicao is not None:
            campanha = session.query(Campanha).filter_by(id_campanha=id_campanha_em_edicao).first()
            if not campanha:
                pn.state.notifications.error('Campanha não encontrada.')
                return

            campanha.nome = nome
            campanha.data_inicio = data_inicio
            campanha.data_fim = data_fim
            campanha.objetivo = objetivo
            campanha.descricao = descricao
            campanha.cnpj_instituicao = cnpj_instituicao
            pn.state.notifications.success('Campanha atualizada com sucesso!')
        else:
            nova = Campanha(
                nome=nome,
                data_inicio=data_inicio,
                data_fim=data_fim,
                objetivo=objetivo,
                descricao=descricao,
                cnpj_instituicao=cnpj_instituicao
            )
            session.add(nova)
            pn.state.notifications.success('Campanha cadastrada com sucesso!')

        session.commit()

    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f'Erro ao salvar campanha: {e}')
        return

    id_campanha_em_edicao = None
    limpar_campos_campanha()
    atualizar_tabela_campanhas()
    if atualizar_seletores:
        atualizar_seletores()


def preparar_edicao_campanha(event):
    global id_campanha_em_edicao

    selecionado = tabela_campanhas.selection
    if not selecionado:
        pn.state.notifications.warning('Selecione uma linha na tabela primeiro!')
        return

    index = selecionado[0]
    dados_linha = tabela_campanhas.value.iloc[index]
    id_campanha_em_edicao = int(dados_linha['ID'])

    campanha = session.query(Campanha).filter_by(id_campanha=id_campanha_em_edicao).first()
    if not campanha:
        pn.state.notifications.error('Campanha não encontrada.')
        return

    txt_nome_campanha.value = texto(campanha.nome)
    date_inicio_campanha.value = campanha.data_inicio or datetime.date.today()
    date_fim_campanha.value = campanha.data_fim or datetime.date.today()
    txt_objetivo_campanha.value = texto(campanha.objetivo)
    txt_descricao_campanha.value = texto(campanha.descricao)
    select_inst_campanha.value = campanha.cnpj_instituicao

    pn.state.notifications.info('Altere os dados nos campos acima e clique em Salvar.')


def remover_campanha(event, atualizar_seletores=None):
    selecionado = tabela_campanhas.selection
    if not selecionado:
        pn.state.notifications.warning('Selecione uma linha na tabela primeiro!')
        return

    index = selecionado[0]
    dados_linha = tabela_campanhas.value.iloc[index]
    id_alvo = int(dados_linha['ID'])

    try:
        campanha = session.query(Campanha).filter_by(id_campanha=id_alvo).first()
        if campanha:
            session.delete(campanha)
            session.commit()
            pn.state.notifications.success('Campanha removida com sucesso!')
            atualizar_tabela_campanhas()
            if atualizar_seletores:
                atualizar_seletores()
        else:
            pn.state.notifications.error('Campanha não encontrada.')
    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f'Erro ao remover campanha: {e}')


def montar_aba(atualizar_seletores=None):
    btn_salvar_campanha.on_click(lambda event: salvar_campanha(event, atualizar_seletores))
    btn_editar_campanha.on_click(preparar_edicao_campanha)
    btn_remover_campanha.on_click(lambda event: remover_campanha(event, atualizar_seletores))

    atualizar_tabela_campanhas()
    atualizar_seletor_instituicoes_campanha()

    return pn.Column(
        "### Gerenciar Campanhas",
        pn.Row(
            pn.Column(
                txt_nome_campanha,
                date_inicio_campanha,
                date_fim_campanha,
                txt_objetivo_campanha,
                txt_descricao_campanha,
                select_inst_campanha,
                btn_salvar_campanha,
                width=320
            ),
            pn.Column(
                tabela_campanhas,
                pn.Row(btn_editar_campanha, btn_remover_campanha)
            )
        )
    )