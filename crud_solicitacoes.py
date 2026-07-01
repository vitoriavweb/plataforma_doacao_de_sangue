import panel as pn
import pandas as pd

from db import session
from models import SolicitacaoSangue, Estoque, Hemocentro

id_solicitacao_em_edicao = None

select_inst_solicitacao = pn.widgets.Select(name='Instituição Solicitante', options={})
select_tipo_solicitacao = pn.widgets.Select(
    name='Tipo Sanguíneo Necessário',
    options=['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
    value='A+'
)

btn_criar_solicitacao = pn.widgets.Button(
    name='Criar Solicitação',
    button_type='danger',
    width=280
)
btn_atender_solicitacao = pn.widgets.Button(
    name='Atender Selecionado',
    button_type='success',
    width=280
)

tabela_solicitacoes = pn.widgets.Tabulator(
    name='Pedidos de Sangue',
    width=550,
    height=300,
    selectable=True
)


def texto(valor):
    return "" if valor is None else str(valor)


def atualizar_tabela_solicitacoes():
    lista = session.query(SolicitacaoSangue).all()

    dados = pd.DataFrame({
        'ID': [texto(s.id) for s in lista],
        'Instituição': [texto(s.cnpj_instituicao) for s in lista],
        'Tipo Requerido': [texto(s.tipo_sanguineo) for s in lista],
        'Status': [texto(s.status) for s in lista],
    }).fillna("")

    tabela_solicitacoes.value = dados


def criar_solicitacao(event):
    instituicao = texto(select_inst_solicitacao.value).strip()
    tipo = texto(select_tipo_solicitacao.value).strip()

    if not instituicao:
        pn.state.notifications.error('Selecione uma instituição!')
        return

    if not tipo:
        pn.state.notifications.error('Selecione o tipo sanguíneo necessário!')
        return

    instituicao_existe = session.query(Hemocentro).filter_by(cnpj=instituicao).first()
    if not instituicao_existe:
        pn.state.notifications.error('A instituição selecionada não existe no cadastro!')
        return

    try:
        nova = SolicitacaoSangue(
            cnpj_instituicao=instituicao,
            tipo_sanguineo=tipo,
            status='Pendente'
        )
        session.add(nova)
        session.commit()

        pn.state.notifications.success('Solicitação registrada com sucesso!')
        atualizar_tabela_solicitacoes()

    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f'Erro ao criar solicitação: {e}')


def atender_solicitacao(event):
    selecionado = tabela_solicitacoes.selection
    if not selecionado:
        pn.state.notifications.warning('Selecione uma linha na tabela de solicitações primeiro!')
        return

    index = selecionado[0]
    dados_linha = tabela_solicitacoes.value.iloc[index]
    solicitacao_id = int(float(dados_linha['ID']))

    solicitacao = session.query(SolicitacaoSangue).filter_by(id=solicitacao_id).first()
    if not solicitacao:
        pn.state.notifications.error('Solicitação não encontrada.')
        return

    if texto(solicitacao.status) == 'Atendido':
        pn.state.notifications.warning('Esta solicitação já foi atendida!')
        return

    estoque_item = session.query(Estoque).filter_by(
        cnpj_instituicao=solicitacao.cnpj_instituicao,
        tipo_sanguineo=solicitacao.tipo_sanguineo
    ).first()

    volume_bolsa = 450

    if not estoque_item:
        pn.state.notifications.error(
            f'Não há estoque de {solicitacao.tipo_sanguineo} para esta instituição!'
        )
        return

    if estoque_item.quantidade_ml is None:
        estoque_item.quantidade_ml = 0

    if estoque_item.quantidade_ml >= volume_bolsa:
        try:
            estoque_item.quantidade_ml -= volume_bolsa
            solicitacao.status = 'Atendido'
            session.commit()

            pn.state.notifications.success('Solicitação atendida com sucesso! 450ml deduzidos do estoque.')
            atualizar_tabela_solicitacoes()
            atualizar_tabela_estoque()

        except Exception as e:
            session.rollback()
            pn.state.notifications.error(f'Erro ao atender solicitação: {e}')
    else:
        pn.state.notifications.error(
            f'Estoque insuficiente! Há apenas {estoque_item.quantidade_ml}ml disponíveis.'
        )


def montar_aba():
    btn_criar_solicitacao.on_click(criar_solicitacao)
    btn_atender_solicitacao.on_click(atender_solicitacao)

    atualizar_tabela_solicitacoes()

    return pn.Column(
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