import panel as pn
import pandas as pd

from db import session
from models import Estoque

id_estoque_em_edicao = None

select_inst_estoque = pn.widgets.Select(name='Selecionar Instituição', options=[])
select_tipo_estoque = pn.widgets.Select(
    name='Tipo Sanguíneo',
    options=['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
)
int_qtd_estoque = pn.widgets.IntInput(name='Quantidade (ml)', value=0, step=50)

btn_salvar_estoque = pn.widgets.Button(
    name='Salvar Estoque',
    button_type='success',
    width=280
)
btn_editar_estoque = pn.widgets.Button(
    name='Editar Estoque Selecionado',
    button_type='warning',
    width=250
)

tabela_estoque = pn.widgets.Tabulator(
    name='Estoque Atual',
    width=550,
    height=300,
    selectable=True
)


def texto(v):
    return "" if v is None else str(v)


def atualizar_tabela_estoque():
    lista = session.query(Estoque).all()

    dados = {
        'ID': [texto(e.id) for e in lista],
        'Instituição (CNPJ)': [texto(e.cnpj_instituicao) for e in lista],
        'Tipo Sanguíneo': [texto(e.tipo_sanguineo) for e in lista],
        'Qtd (ml)': [texto(e.quantidade_ml) for e in lista]
    }

    tabela_estoque.value = pd.DataFrame(dados)


def adicionar_estoque(event):
    global id_estoque_em_edicao

    cnpj = texto(select_inst_estoque.value).strip()
    tipo = texto(select_tipo_estoque.value).strip()
    qtd = int_qtd_estoque.value if int_qtd_estoque.value is not None else 0

    if not cnpj:
        pn.state.notifications.error('Cadastre uma instituição primeiro!')
        return

    if not tipo:
        pn.state.notifications.error('Selecione um tipo sanguíneo!')
        return

    if qtd < 0:
        pn.state.notifications.error('A quantidade não pode ser negativa!')
        return

    try:
        if id_estoque_em_edicao is not None:
            item = session.query(Estoque).filter_by(id=id_estoque_em_edicao).first()

            if not item:
                pn.state.notifications.error('Item de estoque não encontrado!')
                return

            item.cnpj_instituicao = cnpj
            item.tipo_sanguineo = tipo
            item.quantidade_ml = qtd

            pn.state.notifications.success('Estoque alterado com sucesso!')

        else:
            item = session.query(Estoque).filter_by(
                cnpj_instituicao=cnpj,
                tipo_sanguineo=tipo
            ).first()

            if item:
                item.quantidade_ml = (item.quantidade_ml or 0) + qtd
                pn.state.notifications.success('Quantidade somada ao estoque existente!')
            else:
                novo = Estoque(
                    cnpj_instituicao=cnpj,
                    tipo_sanguineo=tipo,
                    quantidade_ml=qtd
                )
                session.add(novo)
                pn.state.notifications.success('Novo lote de estoque adicionado!')

        session.commit()

    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f'Erro ao salvar estoque: {e}')
        return

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

    cnpj = texto(dados_linha['Instituição (CNPJ)']).strip()
    tipo = texto(dados_linha['Tipo Sanguíneo']).strip()
    qtd = dados_linha['Qtd (ml)']

    select_inst_estoque.value = cnpj
    select_tipo_estoque.value = tipo

    try:
        int_qtd_estoque.value = int(float(qtd))
    except Exception:
        int_qtd_estoque.value = 0

    pn.state.notifications.info('Modifique os dados e clique em Salvar Estoque.')


def montar_aba():
    btn_salvar_estoque.on_click(adicionar_estoque)
    btn_editar_estoque.on_click(preparar_edicao_estoque)

    atualizar_tabela_estoque()

    return pn.Column(
        "### Controle de Estoque de Sangue",
        pn.Row(
            pn.Column(
                select_inst_estoque,
                select_tipo_estoque,
                int_qtd_estoque,
                btn_salvar_estoque,
                width=300
            ),
            pn.Column(
                tabela_estoque,
                btn_editar_estoque
            )
        )
    )