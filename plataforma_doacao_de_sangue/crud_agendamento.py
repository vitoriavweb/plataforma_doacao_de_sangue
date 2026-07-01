import datetime
import panel as pn
import pandas as pd

from db import session
from models import Agendamento, Usuario, Hemocentro

id_agendamento_em_edicao = None

select_usuario_agendamento = pn.widgets.Select(name='Doador (Usuário)', options={})
select_inst_agendamento = pn.widgets.Select(name='Instituição', options={})
date_dia_agendamento = pn.widgets.DatePicker(name='Dia', value=datetime.date.today())
txt_horario_agendamento = pn.widgets.TextInput(name='Horário (ex: 14:30)')
txt_local_agendamento = pn.widgets.TextInput(name='Local da Doação')
select_status_agendamento = pn.widgets.Select(
    name='Status',
    options=['Agendado', 'Confirmado', 'Realizado', 'Cancelado'],
    value='Agendado'
)
int_num_atendimento = pn.widgets.IntInput(name='Número de Atendimento', value=0)
btn_salvar_agendamento = pn.widgets.Button(name='Cadastrar / Atualizar', button_type='primary')

tabela_agendamentos = pn.widgets.Tabulator(
    name='Agendamentos',
    selectable=True,
    width=700,
    height=300
)

btn_editar_agendamento = pn.widgets.Button(name='Editar Selecionado', button_type='warning', width=180)
btn_remover_agendamento = pn.widgets.Button(name='Remover Selecionado', button_type='danger', width=180)


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
        return valor.strftime('%Y-%m-%d')
    return texto(valor)


def atualizar_seletor_usuarios_agendamento():
    usuarios = session.query(Usuario).all()
    opcoes = {f"{texto(u.pnome)} {texto(u.unome)} (ID {u.id_usuario})": u.id_usuario for u in usuarios}
    select_usuario_agendamento.options = opcoes


def atualizar_seletor_instituicoes_agendamento():
    instituicoes = session.query(Hemocentro).all()
    opcoes = {f"{texto(i.nome)} (CNPJ {texto(i.cnpj)})": i.cnpj for i in instituicoes}
    select_inst_agendamento.options = opcoes


def atualizar_tabela_agendamentos():
    lista = session.query(Agendamento).all()

    dados = pd.DataFrame({
        'ID': [texto(a.id_agendamento) for a in lista],
        'Doador (ID)': [texto(a.id_usuario) for a in lista],
        'Instituição (CNPJ)': [texto(a.cnpj_instituicao) for a in lista],
        'Dia': [formatar_data(a.dia) for a in lista],
        'Horário': [texto(a.horario) for a in lista],
        'Local': [texto(a.local_doacao) for a in lista],
        'Status': [texto(a.status) for a in lista],
        'Nº Atendimento': [texto(a.num_atendimento) for a in lista]
    }).astype(str).replace({"None": "", "nan": "", "NaN": "", "<NA>": ""})

    tabela_agendamentos.value = dados


def limpar_campos_agendamento():
    txt_horario_agendamento.value = ""
    txt_local_agendamento.value = ""
    date_dia_agendamento.value = datetime.date.today()
    select_status_agendamento.value = 'Agendado'
    int_num_atendimento.value = 0
    select_usuario_agendamento.value = None
    select_inst_agendamento.value = None


def salvar_agendamento(event, atualizar_seletores=None):
    global id_agendamento_em_edicao

    id_usuario = select_usuario_agendamento.value
    cnpj = select_inst_agendamento.value
    dia = date_dia_agendamento.value
    horario = texto(txt_horario_agendamento.value).strip()
    local = texto(txt_local_agendamento.value).strip()
    status = texto(select_status_agendamento.value).strip()
    num_atendimento = int_num_atendimento.value or 0

    if not id_usuario:
        pn.state.notifications.error('Cadastre um usuário/doador primeiro!')
        return

    if not cnpj:
        pn.state.notifications.error('Cadastre uma instituição primeiro!')
        return

    if not dia:
        pn.state.notifications.error('Selecione o dia!')
        return

    if not horario:
        pn.state.notifications.error('Preencha o horário!')
        return

    if not local:
        pn.state.notifications.error('Preencha o local da doação!')
        return

    if status not in ['Agendado', 'Confirmado', 'Realizado', 'Cancelado']:
        pn.state.notifications.error('Selecione um status válido!')
        return

    try:
        if id_agendamento_em_edicao is not None:
            agendamento = session.query(Agendamento).filter_by(id_agendamento=id_agendamento_em_edicao).first()
            if not agendamento:
                pn.state.notifications.error('Agendamento não encontrado.')
                return

            agendamento.id_usuario = id_usuario
            agendamento.cnpj_instituicao = cnpj
            agendamento.dia = dia
            agendamento.horario = horario
            agendamento.local_doacao = local
            agendamento.status = status
            agendamento.num_atendimento = num_atendimento
            pn.state.notifications.success('Agendamento atualizado com sucesso!')
        else:
            novo = Agendamento(
                id_usuario=id_usuario,
                cnpj_instituicao=cnpj,
                dia=dia,
                horario=horario,
                local_doacao=local,
                status=status,
                num_atendimento=num_atendimento
            )
            session.add(novo)
            pn.state.notifications.success('Agendamento criado com sucesso!')

        session.commit()

    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f'Erro ao salvar agendamento: {e}')
        return

    id_agendamento_em_edicao = None
    limpar_campos_agendamento()
    atualizar_tabela_agendamentos()
    if atualizar_seletores:
        atualizar_seletores()


def preparar_edicao_agendamento(event):
    global id_agendamento_em_edicao

    selecionado = tabela_agendamentos.selection
    if not selecionado:
        pn.state.notifications.warning('Selecione uma linha na tabela primeiro!')
        return

    index = selecionado[0]
    dados_linha = tabela_agendamentos.value.iloc[index]
    id_agendamento_em_edicao = int(dados_linha['ID'])

    agendamento = session.query(Agendamento).filter_by(id_agendamento=id_agendamento_em_edicao).first()
    if not agendamento:
        pn.state.notifications.error('Agendamento não encontrado.')
        return

    select_usuario_agendamento.value = agendamento.id_usuario
    select_inst_agendamento.value = agendamento.cnpj_instituicao
    date_dia_agendamento.value = agendamento.dia or datetime.date.today()
    txt_horario_agendamento.value = texto(agendamento.horario)
    txt_local_agendamento.value = texto(agendamento.local_doacao)
    select_status_agendamento.value = agendamento.status if agendamento.status in select_status_agendamento.options else 'Agendado'
    int_num_atendimento.value = agendamento.num_atendimento or 0

    pn.state.notifications.info('Altere os dados nos campos acima e clique em Salvar.')


def remover_agendamento(event, atualizar_seletores=None):
    selecionado = tabela_agendamentos.selection
    if not selecionado:
        pn.state.notifications.warning('Selecione uma linha na tabela primeiro!')
        return

    index = selecionado[0]
    dados_linha = tabela_agendamentos.value.iloc[index]
    id_alvo = int(dados_linha['ID'])

    try:
        agendamento = session.query(Agendamento).filter_by(id_agendamento=id_alvo).first()
        if agendamento:
            session.delete(agendamento)
            session.commit()
            pn.state.notifications.success('Agendamento removido com sucesso!')
            atualizar_tabela_agendamentos()
            if atualizar_seletores:
                atualizar_seletores()
        else:
            pn.state.notifications.error('Agendamento não encontrado.')
    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f'Erro ao remover agendamento: {e}')


def montar_aba(atualizar_seletores=None):
    btn_salvar_agendamento.on_click(lambda event: salvar_agendamento(event, atualizar_seletores))
    btn_editar_agendamento.on_click(preparar_edicao_agendamento)
    btn_remover_agendamento.on_click(lambda event: remover_agendamento(event, atualizar_seletores))

    atualizar_tabela_agendamentos()
    atualizar_seletor_usuarios_agendamento()
    atualizar_seletor_instituicoes_agendamento()

    return pn.Column(
        "### Gerenciar Agendamentos",
        pn.Row(
            pn.Column(
                select_usuario_agendamento,
                select_inst_agendamento,
                date_dia_agendamento,
                txt_horario_agendamento,
                txt_local_agendamento,
                select_status_agendamento,
                int_num_atendimento,
                btn_salvar_agendamento,
                width=320
            ),
            pn.Column(
                tabela_agendamentos,
                pn.Row(btn_editar_agendamento, btn_remover_agendamento)
            )
        )
    )