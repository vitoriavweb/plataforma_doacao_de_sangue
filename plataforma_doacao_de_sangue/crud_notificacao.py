import datetime
import panel as pn
import pandas as pd

from db import session
from models import Notificacao, Usuario, Hemocentro

id_notificacao_em_edicao = None

TIPOS_SANGUINEOS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

select_usuario_notificacao = pn.widgets.Select(name='Doador (Destinatário)', options={})
select_inst_notificacao = pn.widgets.Select(name='Instituição (opcional)', options={})
date_envio_notificacao = pn.widgets.DatePicker(name='Data do Envio', value=datetime.date.today())
select_tipo_notificacao = pn.widgets.Select(
    name='Tipo Sanguíneo do Alerta',
    options=[''] + TIPOS_SANGUINEOS,
    value=''
)
txt_conteudo_notificacao = pn.widgets.TextAreaInput(name='Conteúdo da Mensagem', height=100)
btn_salvar_notificacao = pn.widgets.Button(name='Cadastrar / Atualizar', button_type='primary')

tabela_notificacoes = pn.widgets.Tabulator(
    name='Notificações',
    selectable=True,
    width=700,
    height=300
)

btn_editar_notificacao = pn.widgets.Button(name='Editar Selecionado', button_type='warning', width=180)
btn_remover_notificacao = pn.widgets.Button(name='Remover Selecionado', button_type='danger', width=180)


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


def atualizar_seletor_usuarios_notificacao():
    usuarios = session.query(Usuario).all()
    opcoes = {
        f"{texto(u.pnome)} {texto(u.unome)} (ID {u.id_usuario})": u.id_usuario
        for u in usuarios
    }
    select_usuario_notificacao.options = opcoes


def atualizar_seletor_instituicoes_notificacao():
    instituicoes = session.query(Hemocentro).all()
    opcoes = {
        f"{texto(i.nome)} (CNPJ {texto(i.cnpj)})": i.cnpj
        for i in instituicoes
    }
    select_inst_notificacao.options = opcoes


def atualizar_tabela_notificacoes():
    lista = session.query(Notificacao).all()

    dados = pd.DataFrame({
        'ID': [texto(n.id_notificacao) for n in lista],
        'Doador (ID)': [texto(n.id_usuario) for n in lista],
        'Instituição (CNPJ)': [texto(n.cnpj_instituicao) for n in lista],
        'Data do Envio': [formatar_data(n.data_envio) for n in lista],
        'Tipo Sanguíneo': [texto(n.tipo_sanguineo_alerta) for n in lista],
        'Mensagem': [texto(n.conteudo_mensagem) for n in lista]
    }).astype(str).replace({"None": "", "nan": "", "NaN": "", "<NA>": ""})

    tabela_notificacoes.value = dados


def limpar_campos_notificacao():
    date_envio_notificacao.value = datetime.date.today()
    select_tipo_notificacao.value = ''
    txt_conteudo_notificacao.value = ""
    select_usuario_notificacao.value = None
    select_inst_notificacao.value = None


def salvar_notificacao(event, atualizar_seletores=None):
    global id_notificacao_em_edicao

    id_usuario = select_usuario_notificacao.value
    cnpj = select_inst_notificacao.value
    data_envio = date_envio_notificacao.value
    tipo_sanguineo = texto(select_tipo_notificacao.value).strip() or None
    conteudo = texto(txt_conteudo_notificacao.value).strip()

    if not id_usuario:
        pn.state.notifications.error('Selecione o doador que vai receber a notificação!')
        return

    if not data_envio:
        pn.state.notifications.error('Selecione a data do envio!')
        return

    if not conteudo:
        pn.state.notifications.error('Preencha o conteúdo da mensagem!')
        return

    try:
        if id_notificacao_em_edicao is not None:
            notificacao = session.query(Notificacao).filter_by(id_notificacao=id_notificacao_em_edicao).first()
            if not notificacao:
                pn.state.notifications.error('Notificação não encontrada.')
                return

            notificacao.id_usuario = id_usuario
            notificacao.cnpj_instituicao = cnpj
            notificacao.data_envio = data_envio
            notificacao.tipo_sanguineo_alerta = tipo_sanguineo
            notificacao.conteudo_mensagem = conteudo
            pn.state.notifications.success('Notificação atualizada com sucesso!')
        else:
            nova = Notificacao(
                id_usuario=id_usuario,
                cnpj_instituicao=cnpj,
                data_envio=data_envio,
                tipo_sanguineo_alerta=tipo_sanguineo,
                conteudo_mensagem=conteudo
            )
            session.add(nova)
            pn.state.notifications.success('Notificação enviada com sucesso!')

        session.commit()

    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f'Erro ao salvar notificação: {e}')
        return

    id_notificacao_em_edicao = None
    limpar_campos_notificacao()
    atualizar_tabela_notificacoes()
    if atualizar_seletores:
        atualizar_seletores()


def preparar_edicao_notificacao(event):
    global id_notificacao_em_edicao

    selecionado = tabela_notificacoes.selection
    if not selecionado:
        pn.state.notifications.warning('Selecione uma linha na tabela primeiro!')
        return

    index = selecionado[0]
    dados_linha = tabela_notificacoes.value.iloc[index]
    id_notificacao_em_edicao = int(dados_linha['ID'])

    notificacao = session.query(Notificacao).filter_by(id_notificacao=id_notificacao_em_edicao).first()
    if not notificacao:
        pn.state.notifications.error('Notificação não encontrada.')
        return

    select_usuario_notificacao.value = notificacao.id_usuario
    select_inst_notificacao.value = notificacao.cnpj_instituicao
    date_envio_notificacao.value = notificacao.data_envio or datetime.date.today()
    select_tipo_notificacao.value = (
        notificacao.tipo_sanguineo_alerta
        if notificacao.tipo_sanguineo_alerta in TIPOS_SANGUINEOS
        else ''
    )
    txt_conteudo_notificacao.value = texto(notificacao.conteudo_mensagem)

    pn.state.notifications.info('Altere os dados nos campos acima e clique em Salvar.')


def remover_notificacao(event, atualizar_seletores=None):
    selecionado = tabela_notificacoes.selection
    if not selecionado:
        pn.state.notifications.warning('Selecione uma linha na tabela primeiro!')
        return

    index = selecionado[0]
    dados_linha = tabela_notificacoes.value.iloc[index]
    id_alvo = int(dados_linha['ID'])

    try:
        notificacao = session.query(Notificacao).filter_by(id_notificacao=id_alvo).first()
        if notificacao:
            session.delete(notificacao)
            session.commit()
            pn.state.notifications.success('Notificação removida com sucesso!')
            atualizar_tabela_notificacoes()
            if atualizar_seletores:
                atualizar_seletores()
        else:
            pn.state.notifications.error('Notificação não encontrada.')
    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f'Erro ao remover notificação: {e}')


def montar_aba(atualizar_seletores=None):
    btn_salvar_notificacao.on_click(lambda event: salvar_notificacao(event, atualizar_seletores))
    btn_editar_notificacao.on_click(preparar_edicao_notificacao)
    btn_remover_notificacao.on_click(lambda event: remover_notificacao(event, atualizar_seletores))

    atualizar_tabela_notificacoes()
    atualizar_seletor_usuarios_notificacao()
    atualizar_seletor_instituicoes_notificacao()

    return pn.Column(
        "### Notificações de Alerta",
        pn.Row(
            pn.Column(
                select_usuario_notificacao,
                select_inst_notificacao,
                date_envio_notificacao,
                select_tipo_notificacao,
                txt_conteudo_notificacao,
                btn_salvar_notificacao,
                width=320
            ),
            pn.Column(
                tabela_notificacoes,
                pn.Row(btn_editar_notificacao, btn_remover_notificacao)
            )
        )
    )