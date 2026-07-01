import datetime
import panel as pn
import pandas as pd

from db import session
from models import HistoricoDoador, Usuario

id_historico_em_edicao = None

select_usuario_historico = pn.widgets.Select(name='Doador (Usuário)', options={})
select_inst_historico = pn.widgets.Select(name='Instituição', options={})
txt_local_historico = pn.widgets.TextInput(name='Local da Doação')
txt_volume_historico = pn.widgets.TextInput(name='Volume de Sangue (ex: 450ml)')
date_historico = pn.widgets.DatePicker(name='Data da Doação', value=datetime.date.today())
btn_salvar_historico = pn.widgets.Button(name='Cadastrar / Atualizar', button_type='primary')

tabela_historico = pn.widgets.Tabulator(
    name='Histórico de Doações',
    selectable=True,
    width=700,
    height=300
)

btn_editar_historico = pn.widgets.Button(name='Editar Selecionado', button_type='warning', width=180)
btn_remover_historico = pn.widgets.Button(name='Remover Selecionado', button_type='danger', width=180)


def texto(valor):
    if valor is None:
        return ""
    if pd.isna(valor):
        return ""
    return str(valor)


def atualizar_seletor_usuarios_historico():
    usuarios = session.query(Usuario).all()
    opcoes = {f"{texto(u.pnome)} {texto(u.unome)} (ID {u.id_usuario})": u.id_usuario for u in usuarios}
    select_usuario_historico.options = opcoes


def atualizar_seletor_instituicoes_historico():
    from models import Hemocentro
    insts = session.query(Hemocentro).all()
    opcoes = {f"{texto(i.nome)} (CNPJ {i.cnpj})": i.cnpj for i in insts}
    select_inst_historico.options = opcoes


def atualizar_tabela_historico():
    lista = session.query(HistoricoDoador).all()

    dados = pd.DataFrame({
        'ID': [texto(h.id_historico) for h in lista],
        'Doador (ID)': [texto(h.id_usuario) for h in lista],
        'Instituição (CNPJ)': [texto(h.cnpj_instituicao) for h in lista],
        'Local': [texto(h.local_doacao) for h in lista],
        'Volume': [texto(h.volume_sangue) for h in lista],
        'Data': [
            h.data_doacao.strftime('%Y-%m-%d') if h.data_doacao else ""
            for h in lista
        ]
    })

    tabela_historico.value = dados


def limpar_campos_historico():
    txt_local_historico.value = ""
    txt_volume_historico.value = ""
    date_historico.value = datetime.date.today()


def salvar_historico(event, atualizar_seletores=None):
    global id_historico_em_edicao

    id_usuario = select_usuario_historico.value
    cnpj_instituicao = select_inst_historico.value
    local_doacao = texto(txt_local_historico.value).strip()
    volume_sangue = texto(txt_volume_historico.value).strip()
    data_doacao = date_historico.value

    if not id_usuario:
        pn.state.notifications.error('Cadastre um usuário/doador primeiro!')
        return
    if not cnpj_instituicao:
        pn.state.notifications.error('Cadastre uma instituição primeiro!')
        return
    if not local_doacao:
        pn.state.notifications.error('Preencha o local da doação!')
        return
    if not volume_sangue:
        pn.state.notifications.error('Preencha o volume de sangue!')
        return
    if not data_doacao:
        pn.state.notifications.error('Preencha a data da doação!')
        return

    try:
        if id_historico_em_edicao is not None:
            historico = session.query(HistoricoDoador).filter_by(id_historico=id_historico_em_edicao).first()
            if not historico:
                pn.state.notifications.error('Registro não encontrado.')
                return

            historico.id_usuario = id_usuario
            historico.cnpj_instituicao = cnpj_instituicao
            historico.local_doacao = local_doacao
            historico.volume_sangue = volume_sangue
            historico.data_doacao = data_doacao
            pn.state.notifications.success('Registro de histórico atualizado com sucesso!')
        else:
            novo = HistoricoDoador(
                id_usuario=id_usuario,
                cnpj_instituicao=cnpj_instituicao,
                local_doacao=local_doacao,
                volume_sangue=volume_sangue,
                data_doacao=data_doacao
            )
            session.add(novo)
            pn.state.notifications.success('Registro de histórico criado com sucesso!')

        session.commit()

    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f'Erro ao salvar histórico: {e}')
        return

    id_historico_em_edicao = None
    limpar_campos_historico()
    atualizar_tabela_historico()
    if atualizar_seletores:
        atualizar_seletores()


def preparar_edicao_historico(event):
    global id_historico_em_edicao

    selecionado = tabela_historico.selection
    if not selecionado:
        pn.state.notifications.warning('Selecione uma linha na tabela primeiro!')
        return

    index = selecionado[0]
    dados_linha = tabela_historico.value.iloc[index]
    id_historico_em_edicao = int(dados_linha['ID'])

    historico = session.query(HistoricoDoador).filter_by(id_historico=id_historico_em_edicao).first()
    if not historico:
        pn.state.notifications.error('Registro não encontrado.')
        return

    select_usuario_historico.value = historico.id_usuario
    select_inst_historico.value = historico.cnpj_instituicao
    txt_local_historico.value = texto(historico.local_doacao)
    txt_volume_historico.value = texto(historico.volume_sangue)
    date_historico.value = historico.data_doacao or datetime.date.today()

    pn.state.notifications.info('Altere os dados nos campos acima e clique em Salvar.')


def remover_historico(event, atualizar_seletores=None):
    selecionado = tabela_historico.selection
    if not selecionado:
        pn.state.notifications.warning('Selecione uma linha na tabela primeiro!')
        return

    index = selecionado[0]
    dados_linha = tabela_historico.value.iloc[index]
    id_alvo = int(dados_linha['ID'])

    try:
        historico = session.query(HistoricoDoador).filter_by(id_historico=id_alvo).first()
        if historico:
            session.delete(historico)
            session.commit()
            pn.state.notifications.success('Registro removido com sucesso!')
            atualizar_tabela_historico()
            if atualizar_seletores:
                atualizar_seletores()
        else:
            pn.state.notifications.error('Registro não encontrado.')
    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f'Erro ao remover histórico: {e}')


def montar_aba(atualizar_seletores=None):
    btn_salvar_historico.on_click(lambda event: salvar_historico(event, atualizar_seletores))
    btn_editar_historico.on_click(preparar_edicao_historico)
    btn_remover_historico.on_click(lambda event: remover_historico(event, atualizar_seletores))

    atualizar_tabela_historico()

    return pn.Column(
        "### Gerenciar Histórico de Doadores",
        pn.Row(
            pn.Column(
                select_usuario_historico,
                select_inst_historico,
                txt_local_historico,
                txt_volume_historico,
                date_historico,
                btn_salvar_historico,
                width=320
            ),
            pn.Column(tabela_historico, pn.Row(btn_editar_historico, btn_remover_historico))
        )
    )