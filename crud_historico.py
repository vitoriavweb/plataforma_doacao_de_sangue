import datetime
import panel as pn
import pandas as pd

from db import session
from models import Historico, Agendamento, Hemocentro

id_historico_em_edicao = None

select_agendamento_historico = pn.widgets.Select(name='Agendamento', options={})
# Mantido por compatibilidade com o app.py, que tenta atualizar esse seletor.
# Não precisa aparecer na interface.
select_inst_historico = pn.widgets.Select(name='Instituição', options={}, visible=False)

date_data_doacao_historico = pn.widgets.DatePicker(
    name='Data da Doação',
    value=datetime.date.today()
)
txt_local_historico = pn.widgets.TextInput(name='Local da Doação')
int_volume_historico = pn.widgets.IntInput(
    name='Volume Coletado (ml)',
    value=450,
    step=10
)
btn_salvar_historico = pn.widgets.Button(
    name='Cadastrar / Atualizar',
    button_type='primary'
)

tabela_historicos = pn.widgets.Tabulator(
    name='Histórico',
    selectable=True,
    width=700,
    height=300
)

btn_editar_historico = pn.widgets.Button(
    name='Editar Selecionado',
    button_type='warning',
    width=180
)
btn_remover_historico = pn.widgets.Button(
    name='Remover Selecionado',
    button_type='danger',
    width=180
)


def texto(valor):
    if valor is None:
        return ""
    if pd.isna(valor):
        return ""
    return str(valor)


def atualizar_seletor_agendamentos_historico():
    agendamentos = session.query(Agendamento).all()
    opcoes = {
        f"ID {a.id_agendamento} - Doador {a.id_usuario} - {texto(a.dia)}": a.id_agendamento
        for a in agendamentos
    }
    select_agendamento_historico.options = opcoes


def atualizar_seletor_instituicoes_historico():
    instituicoes = session.query(Hemocentro).all()
    opcoes = {
        f"{texto(i.nome)} (CNPJ {texto(i.cnpj)})": i.cnpj
        for i in instituicoes
    }
    select_inst_historico.options = opcoes


def atualizar_tabela_historicos():
    lista = session.query(Historico).all()

    dados = pd.DataFrame({
        'ID': [texto(h.id_historico) for h in lista],
        'Agendamento (ID)': [texto(h.id_agendamento) for h in lista],
        'Data da Doação': [
            h.data_doacao.strftime('%Y-%m-%d') if h.data_doacao else ""
            for h in lista
        ],
        'Local': [texto(h.local) for h in lista],
        'Volume (ml)': [texto(h.volume_ml) for h in lista]
    }).astype(str).replace({"None": "", "nan": ""})

    tabela_historicos.value = dados


def limpar_campos_historico():
    date_data_doacao_historico.value = datetime.date.today()
    txt_local_historico.value = ""
    int_volume_historico.value = 450
    select_agendamento_historico.value = None


def salvar_historico(event, atualizar_seletores=None):
    global id_historico_em_edicao

    id_agendamento = select_agendamento_historico.value
    data_doacao = date_data_doacao_historico.value
    local = texto(txt_local_historico.value).strip()
    volume_ml = int_volume_historico.value or 0

    if not id_agendamento:
        pn.state.notifications.error('Selecione um agendamento primeiro!')
        return

    if not data_doacao:
        pn.state.notifications.error('Selecione a data da doação!')
        return

    if not local:
        pn.state.notifications.error('Preencha o local da doação!')
        return

    if volume_ml <= 0:
        pn.state.notifications.error('Informe um volume de sangue válido!')
        return

    try:
        if id_historico_em_edicao is not None:
            historico = session.query(Historico).filter_by(id_historico=id_historico_em_edicao).first()
            if not historico:
                pn.state.notifications.error('Registro de histórico não encontrado.')
                return

            historico.id_agendamento = id_agendamento
            historico.data_doacao = data_doacao
            historico.local = local
            historico.volume_ml = volume_ml
            pn.state.notifications.success('Histórico atualizado com sucesso!')
        else:
            novo = Historico(
                id_agendamento=id_agendamento,
                data_doacao=data_doacao,
                local=local,
                volume_ml=volume_ml
            )
            session.add(novo)
            pn.state.notifications.success('Histórico registrado com sucesso!')

        session.commit()

    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f'Erro ao salvar histórico: {e}')
        return

    id_historico_em_edicao = None
    limpar_campos_historico()
    atualizar_tabela_historicos()
    if atualizar_seletores:
        atualizar_seletores()


def preparar_edicao_historico(event):
    global id_historico_em_edicao

    selecionado = tabela_historicos.selection
    if not selecionado:
        pn.state.notifications.warning('Selecione uma linha na tabela primeiro!')
        return

    index = selecionado[0]
    dados_linha = tabela_historicos.value.iloc[index]
    id_historico_em_edicao = int(dados_linha['ID'])

    historico = session.query(Historico).filter_by(id_historico=id_historico_em_edicao).first()
    if not historico:
        pn.state.notifications.error('Registro de histórico não encontrado.')
        return

    select_agendamento_historico.value = historico.id_agendamento
    date_data_doacao_historico.value = historico.data_doacao or datetime.date.today()
    txt_local_historico.value = texto(historico.local)
    int_volume_historico.value = historico.volume_ml or 0

    pn.state.notifications.info('Altere os dados nos campos acima e clique em Salvar.')


def remover_historico(event, atualizar_seletores=None):
    selecionado = tabela_historicos.selection
    if not selecionado:
        pn.state.notifications.warning('Selecione uma linha na tabela primeiro!')
        return

    index = selecionado[0]
    dados_linha = tabela_historicos.value.iloc[index]
    id_alvo = int(dados_linha['ID'])

    try:
        historico = session.query(Historico).filter_by(id_historico=id_alvo).first()
        if historico:
            session.delete(historico)
            session.commit()
            pn.state.notifications.success('Registro de histórico removido com sucesso!')
            atualizar_tabela_historicos()
            if atualizar_seletores:
                atualizar_seletores()
        else:
            pn.state.notifications.error('Registro de histórico não encontrado.')
    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f'Erro ao remover histórico: {e}')


def montar_aba(atualizar_seletores=None):
    btn_salvar_historico.on_click(lambda event: salvar_historico(event, atualizar_seletores))
    btn_editar_historico.on_click(preparar_edicao_historico)
    btn_remover_historico.on_click(lambda event: remover_historico(event, atualizar_seletores))

    atualizar_tabela_historicos()
    atualizar_seletor_agendamentos_historico()
    atualizar_seletor_instituicoes_historico()

    return pn.Column(
        "### Histórico de Doações",
        pn.Row(
            pn.Column(
                select_agendamento_historico,
                date_data_doacao_historico,
                txt_local_historico,
                int_volume_historico,
                btn_salvar_historico,
                width=320
            ),
            pn.Column(
                tabela_historicos,
                pn.Row(btn_editar_historico, btn_remover_historico)
            )
        )
    )