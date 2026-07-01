import panel as pn
import pandas as pd

from db import session
from models import Hemocentro

cnpj_em_edicao = None

txt_cnpj = pn.widgets.TextInput(name='CNPJ da Instituição')
txt_nome = pn.widgets.TextInput(name='Nome do Hemocentro')
txt_cidade = pn.widgets.TextInput(name='Cidade')
btn_salvar = pn.widgets.Button(name='Cadastrar / Atualizar', button_type='primary')

tabela_instituicoes = pn.widgets.Tabulator(
    name='Instituições Cadastradas',
    selectable=True,
    width=600,
    height=300
)

btn_preparar_edicao = pn.widgets.Button(name='Editar Selecionado', button_type='warning', width=180)
btn_remover = pn.widgets.Button(name='Remover Selecionado', button_type='danger', width=180)


def atualizar_tabela_instituicoes():
    lista = session.query(Hemocentro).all()
    dados = {
        'CNPJ': [str(h.cnpj) if h.cnpj is not None else '' for h in lista],
        'Nome': [str(h.nome) if h.nome is not None else '' for h in lista],
        'Cidade': [str(h.cidade) if h.cidade is not None else '' for h in lista],
    }
    tabela_instituicoes.value = pd.DataFrame(dados)


def salvar_instituicao(event, atualizar_seletores=None):
    global cnpj_em_edicao

    cnpj = txt_cnpj.value.strip()
    nome = txt_nome.value.strip()
    cidade = txt_cidade.value.strip()

    if not cnpj or not nome:
        pn.state.notifications.error('Preencha o CNPJ e o Nome!')
        return

    try:
        if cnpj_em_edicao:
            instituicao = session.query(Hemocentro).filter_by(cnpj=cnpj_em_edicao).first()

            if instituicao:
                if cnpj_em_edicao != cnpj:
                    cnpj_ja_existe = session.query(Hemocentro).filter_by(cnpj=cnpj).first()
                    if cnpj_ja_existe:
                        pn.state.notifications.error('Já existe uma instituição com este CNPJ!')
                        return

                    instituicao.cnpj = cnpj
                    instituicao.nome = nome
                    instituicao.cidade = cidade
                else:
                    instituicao.nome = nome
                    instituicao.cidade = cidade

                pn.state.notifications.success('Instituição editada com sucesso!')
            else:
                pn.state.notifications.error('Instituição não encontrada para edição!')
                return
        else:
            existe = session.query(Hemocentro).filter_by(cnpj=cnpj).first()
            if existe:
                pn.state.notifications.error('Este CNPJ já está cadastrado!')
                return

            novo = Hemocentro(cnpj=cnpj, nome=nome, cidade=cidade)
            session.add(novo)
            pn.state.notifications.success('Instituição cadastrada com sucesso!')

        session.commit()

    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f'Erro ao salvar: {e}')
        return

    cnpj_em_edicao = None
    txt_cnpj.disabled = False
    txt_cnpj.value = ""
    txt_nome.value = ""
    txt_cidade.value = ""

    atualizar_tabela_instituicoes()
    if atualizar_seletores:
        atualizar_seletores()


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


def remover_instituicao(event, atualizar_seletores=None):
    selecionado = tabela_instituicoes.selection
    if not selecionado:
        pn.state.notifications.warning('Selecione uma linha na tabela primeiro!')
        return

    index = selecionado[0]
    dados_linha = tabela_instituicoes.value.iloc[index]
    cnpj_alvo = str(dados_linha['CNPJ'])

    try:
        instituicao = session.query(Hemocentro).filter_by(cnpj=cnpj_alvo).first()
        if instituicao:
            session.delete(instituicao)
            session.commit()
            pn.state.notifications.success('Instituição removida com sucesso!')
            atualizar_tabela_instituicoes()
            if atualizar_seletores:
                atualizar_seletores()
        else:
            pn.state.notifications.error('Instituição não encontrada!')
    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f'Erro ao remover: {e}')


def montar_aba(atualizar_seletores):
    """Recebe a função de atualizar seletores (definida em app.py) e liga os callbacks."""
    btn_salvar.on_click(lambda event: salvar_instituicao(event, atualizar_seletores))
    btn_preparar_edicao.on_click(preparar_edicao)
    btn_remover.on_click(lambda event: remover_instituicao(event, atualizar_seletores))

    atualizar_tabela_instituicoes()

    return pn.Column(
        "### Gerenciar Instituições (Hemocentros)",
        pn.Row(
            pn.Column(txt_cnpj, txt_nome, txt_cidade, btn_salvar, width=300),
            pn.Column(tabela_instituicoes, pn.Row(btn_preparar_edicao, btn_remover))
        )
    )