import panel as pn
import pandas as pd

from db import session
from models import Hospital

id_hospital_em_edicao = None

txt_nome_hospital = pn.widgets.TextInput(name='Nome do Hospital')
txt_cnpj_hospital = pn.widgets.TextInput(name='CNPJ do Hospital')
select_inst_hospital = pn.widgets.Select(name='Instituição Vinculada', options={})

btn_salvar_hospital = pn.widgets.Button(name='Cadastrar / Atualizar', button_type='primary')

tabela_hospitais = pn.widgets.Tabulator(
    name='Hospitais Cadastrados',
    selectable=True,
    width=650,
    height=300
)

btn_editar_hospital = pn.widgets.Button(name='Editar Selecionado', button_type='warning', width=180)
btn_remover_hospital = pn.widgets.Button(name='Remover Selecionado', button_type='danger', width=180)


def texto(valor):
    return "" if valor is None else str(valor)


def atualizar_tabela_hospitais():
    lista = session.query(Hospital).all()
    dados = {
        'ID': [texto(h.id_hospital) for h in lista],
        'Nome': [texto(h.nome) for h in lista],
        'CNPJ': [texto(h.cnpj) for h in lista],
        'Instituição (CNPJ)': [texto(h.cnpj_instituicao) for h in lista]
    }
    tabela_hospitais.value = pd.DataFrame(dados).fillna("")


def limpar_campos_hospital():
    txt_nome_hospital.value = ""
    txt_cnpj_hospital.value = ""
    select_inst_hospital.value = None


def salvar_hospital(event, atualizar_seletores=None):
    global id_hospital_em_edicao

    nome = texto(txt_nome_hospital.value).strip()
    cnpj = texto(txt_cnpj_hospital.value).strip()
    cnpj_instituicao = select_inst_hospital.value

    if not nome:
        pn.state.notifications.error('Preencha o nome do hospital!')
        return

    if not cnpj_instituicao:
        pn.state.notifications.error('Cadastre uma instituição primeiro!')
        return

    try:
        if id_hospital_em_edicao is not None:
            hospital = session.query(Hospital).filter_by(id_hospital=id_hospital_em_edicao).first()
            if not hospital:
                pn.state.notifications.error('Hospital não encontrado.')
                return

            hospital.nome = nome
            hospital.cnpj = cnpj or None
            hospital.cnpj_instituicao = cnpj_instituicao
            pn.state.notifications.success('Hospital atualizado com sucesso!')
        else:
            novo = Hospital(
                nome=nome,
                cnpj=cnpj or None,
                cnpj_instituicao=cnpj_instituicao
            )
            session.add(novo)
            pn.state.notifications.success('Hospital cadastrado com sucesso!')

        session.commit()

    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f'Erro ao salvar hospital: {e}')
        return

    id_hospital_em_edicao = None
    limpar_campos_hospital()
    atualizar_tabela_hospitais()

    if atualizar_seletores:
        atualizar_seletores()


def preparar_edicao_hospital(event):
    global id_hospital_em_edicao

    selecionado = tabela_hospitais.selection
    if not selecionado:
        pn.state.notifications.warning('Selecione uma linha na tabela primeiro!')
        return

    index = selecionado[0]
    dados_linha = tabela_hospitais.value.iloc[index]
    id_hospital_em_edicao = int(float(dados_linha['ID']))

    hospital = session.query(Hospital).filter_by(id_hospital=id_hospital_em_edicao).first()
    if not hospital:
        pn.state.notifications.error('Hospital não encontrado.')
        return

    txt_nome_hospital.value = texto(hospital.nome)
    txt_cnpj_hospital.value = texto(hospital.cnpj)
    select_inst_hospital.value = hospital.cnpj_instituicao

    pn.state.notifications.info('Altere os dados nos campos acima e clique em Salvar.')


def remover_hospital(event, atualizar_seletores=None):
    selecionado = tabela_hospitais.selection
    if not selecionado:
        pn.state.notifications.warning('Selecione uma linha na tabela primeiro!')
        return

    index = selecionado[0]
    dados_linha = tabela_hospitais.value.iloc[index]
    id_alvo = int(float(dados_linha['ID']))

    try:
        hospital = session.query(Hospital).filter_by(id_hospital=id_alvo).first()
        if hospital:
            session.delete(hospital)
            session.commit()
            pn.state.notifications.success('Hospital removido com sucesso!')
            atualizar_tabela_hospitais()
            if atualizar_seletores:
                atualizar_seletores()
        else:
            pn.state.notifications.error('Hospital não encontrado.')
    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f'Erro ao remover hospital: {e}')


def montar_aba(atualizar_seletores=None):
    btn_salvar_hospital.on_click(lambda event: salvar_hospital(event, atualizar_seletores))
    btn_editar_hospital.on_click(preparar_edicao_hospital)
    btn_remover_hospital.on_click(lambda event: remover_hospital(event, atualizar_seletores))

    atualizar_tabela_hospitais()

    return pn.Column(
        "### Gerenciar Hospitais",
        pn.Row(
            pn.Column(
                txt_nome_hospital,
                txt_cnpj_hospital,
                select_inst_hospital,
                btn_salvar_hospital,
                width=300
            ),
            pn.Column(tabela_hospitais, pn.Row(btn_editar_hospital, btn_remover_hospital))
        )
    )