import panel as pn
import pandas as pd

from db import session
from models import Triagem, Agendamento

id_triagem_em_edicao = None

select_agendamento_triagem = pn.widgets.Select(name='Agendamento', options={})
float_peso_triagem = pn.widgets.FloatInput(name='Peso (kg)', value=0.0, step=0.5)
txt_pressao_triagem = pn.widgets.TextInput(name='Pressão Arterial (ex: 120/80)')
select_resultado_triagem = pn.widgets.Select(name='Resultado', options=['Apto', 'Inapto'], value='Apto')
txt_obs_triagem = pn.widgets.TextAreaInput(name='Observações', height=80)
btn_salvar_triagem = pn.widgets.Button(name='Cadastrar / Atualizar', button_type='primary')

tabela_triagens = pn.widgets.Tabulator(
    name='Triagens',
    selectable=True,
    width=650,
    height=300
)

btn_editar_triagem = pn.widgets.Button(name='Editar Selecionado', button_type='warning', width=180)
btn_remover_triagem = pn.widgets.Button(name='Remover Selecionado', button_type='danger', width=180)


def texto(valor):
    return "" if valor is None else str(valor)


def atualizar_seletor_agendamentos_triagem():
    agendamentos = session.query(Agendamento).all()
    opcoes = {
        f"ID {a.id_agendamento} - Doador {a.id_usuario} - {texto(a.dia)}": a.id_agendamento
        for a in agendamentos
    }
    select_agendamento_triagem.options = opcoes


def atualizar_tabela_triagens():
    lista = session.query(Triagem).all()
    dados = {
        'ID': [texto(t.id_triagem) for t in lista],
        'Agendamento (ID)': [texto(t.id_agendamento) for t in lista],
        'Peso (kg)': [texto(t.peso) for t in lista],
        'Pressão': [texto(t.pressao_arterial) for t in lista],
        'Resultado': [texto(t.resultado) for t in lista],
        'Observações': [texto(t.observacoes) for t in lista]
    }
    tabela_triagens.value = pd.DataFrame(dados).fillna("")


def limpar_campos_triagem():
    float_peso_triagem.value = 0.0
    txt_pressao_triagem.value = ""
    select_resultado_triagem.value = 'Apto'
    txt_obs_triagem.value = ""


def salvar_triagem(event, atualizar_seletores=None):
    global id_triagem_em_edicao

    id_agendamento = select_agendamento_triagem.value
    pressao = texto(txt_pressao_triagem.value).strip()
    resultado = texto(select_resultado_triagem.value).strip()
    observacoes = texto(txt_obs_triagem.value).strip()
    peso = float_peso_triagem.value if float_peso_triagem.value is not None else 0.0

    if not id_agendamento:
        pn.state.notifications.error('Selecione um agendamento primeiro!')
        return

    if not pressao:
        pn.state.notifications.error('Preencha a pressão arterial!')
        return

    if not resultado:
        pn.state.notifications.error('Selecione o resultado!')
        return

    try:
        if id_triagem_em_edicao is not None:
            triagem = session.query(Triagem).filter_by(id_triagem=id_triagem_em_edicao).first()
            if not triagem:
                pn.state.notifications.error('Triagem não encontrada.')
                return

            triagem.id_agendamento = id_agendamento
            triagem.peso = peso
            triagem.pressao_arterial = pressao
            triagem.resultado = resultado
            triagem.observacoes = observacoes
            pn.state.notifications.success('Triagem atualizada com sucesso!')
        else:
            nova = Triagem(
                id_agendamento=id_agendamento,
                peso=peso,
                pressao_arterial=pressao,
                resultado=resultado,
                observacoes=observacoes
            )
            session.add(nova)
            pn.state.notifications.success('Triagem registrada com sucesso!')

        session.commit()

    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f'Erro ao salvar triagem: {e}')
        return

    id_triagem_em_edicao = None
    limpar_campos_triagem()
    atualizar_tabela_triagens()
    if atualizar_seletores:
        atualizar_seletores()


def preparar_edicao_triagem(event):
    global id_triagem_em_edicao

    selecionado = tabela_triagens.selection
    if not selecionado:
        pn.state.notifications.warning('Selecione uma linha na tabela primeiro!')
        return

    index = selecionado[0]
    dados_linha = tabela_triagens.value.iloc[index]
    id_triagem_em_edicao = int(float(dados_linha['ID']))

    triagem = session.query(Triagem).filter_by(id_triagem=id_triagem_em_edicao).first()
    if not triagem:
        pn.state.notifications.error('Triagem não encontrada.')
        return

    select_agendamento_triagem.value = triagem.id_agendamento
    float_peso_triagem.value = triagem.peso or 0.0
    txt_pressao_triagem.value = texto(triagem.pressao_arterial)
    select_resultado_triagem.value = triagem.resultado if triagem.resultado in ['Apto', 'Inapto'] else 'Apto'
    txt_obs_triagem.value = texto(triagem.observacoes)

    pn.state.notifications.info('Altere os dados nos campos acima e clique em Salvar.')


def remover_triagem(event, atualizar_seletores=None):
    selecionado = tabela_triagens.selection
    if not selecionado:
        pn.state.notifications.warning('Selecione uma linha na tabela primeiro!')
        return

    index = selecionado[0]
    dados_linha = tabela_triagens.value.iloc[index]
    id_alvo = int(float(dados_linha['ID']))

    try:
        triagem = session.query(Triagem).filter_by(id_triagem=id_alvo).first()
        if triagem:
            session.delete(triagem)
            session.commit()
            pn.state.notifications.success('Triagem removida com sucesso!')
            atualizar_tabela_triagens()
            if atualizar_seletores:
                atualizar_seletores()
        else:
            pn.state.notifications.error('Triagem não encontrada.')
    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f'Erro ao remover triagem: {e}')


def montar_aba():
    btn_salvar_triagem.on_click(salvar_triagem)
    btn_editar_triagem.on_click(preparar_edicao_triagem)
    btn_remover_triagem.on_click(remover_triagem)

    atualizar_tabela_triagens()

    return pn.Column(
        "### Gerenciar Triagens",
        pn.Row(
            pn.Column(
                select_agendamento_triagem,
                float_peso_triagem, txt_pressao_triagem,
                select_resultado_triagem, txt_obs_triagem,
                btn_salvar_triagem,
                width=320
            ),
            pn.Column(tabela_triagens, pn.Row(btn_editar_triagem, btn_remover_triagem))
        )
    )