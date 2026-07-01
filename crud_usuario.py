import panel as pn
import pandas as pd

from db import session
from models import Usuario

id_usuario_em_edicao = None

txt_pnome = pn.widgets.TextInput(name='Primeiro Nome')
txt_mnome = pn.widgets.TextInput(name='Nome do Meio')
txt_unome = pn.widgets.TextInput(name='Último Nome')
select_sexo = pn.widgets.Select(name='Sexo', options=['M', 'F'])
txt_cpf = pn.widgets.TextInput(name='CPF (somente números)')
txt_email = pn.widgets.TextInput(name='Email')
txt_senha = pn.widgets.PasswordInput(name='Senha')
btn_salvar_usuario = pn.widgets.Button(name='Cadastrar / Atualizar', button_type='primary')

tabela_usuarios = pn.widgets.Tabulator(
    name='Usuários Cadastrados',
    selectable=True,
    width=650,
    height=300
)

btn_editar_usuario = pn.widgets.Button(name='Editar Selecionado', button_type='warning', width=180)
btn_remover_usuario = pn.widgets.Button(name='Remover Selecionado', button_type='danger', width=180)


def texto(valor):
    return "" if valor is None else str(valor)


def atualizar_tabela_usuarios():
    lista = session.query(Usuario).all()
    dados = {
        'ID': [texto(u.id_usuario) for u in lista],
        'Nome Completo': [
            f"{texto(u.pnome)} {texto(u.mnome)} {texto(u.unome)}".strip()
            for u in lista
        ],
        'Sexo': [texto(u.sexo) for u in lista],
        'CPF': [texto(u.cpf) for u in lista],
        'Email': [texto(u.email) for u in lista]
    }

    tabela_usuarios.value = pd.DataFrame(dados).fillna("")


def limpar_campos_usuario():
    txt_pnome.value = ""
    txt_mnome.value = ""
    txt_unome.value = ""
    select_sexo.value = 'M'
    txt_cpf.value = ""
    txt_email.value = ""
    txt_senha.value = ""


def salvar_usuario(event, atualizar_seletores=None):
    global id_usuario_em_edicao

    pnome = texto(txt_pnome.value).strip()
    mnome = texto(txt_mnome.value).strip()
    unome = texto(txt_unome.value).strip()
    sexo = texto(select_sexo.value).strip()
    cpf = texto(txt_cpf.value).strip()
    email = texto(txt_email.value).strip()
    senha = texto(txt_senha.value)

    if not pnome or not unome or not cpf:
        pn.state.notifications.error('Preencha ao menos Primeiro Nome, Último Nome e CPF!')
        return

    if len(cpf) != 11 or not cpf.isdigit():
        pn.state.notifications.error('O CPF deve conter exatamente 11 números!')
        return

    if sexo not in ['M', 'F']:
        pn.state.notifications.error('Selecione um sexo válido!')
        return

    try:
        if id_usuario_em_edicao is not None:
            usuario = session.query(Usuario).filter_by(id_usuario=id_usuario_em_edicao).first()
            if usuario:
                cpf_em_uso = session.query(Usuario).filter(
                    Usuario.cpf == cpf,
                    Usuario.id_usuario != id_usuario_em_edicao
                ).first()
                if cpf_em_uso:
                    pn.state.notifications.error('Este CPF já está cadastrado para outro usuário!')
                    return

                usuario.pnome = pnome
                usuario.mnome = mnome
                usuario.unome = unome
                usuario.sexo = sexo
                usuario.cpf = cpf
                usuario.email = email or None

                if senha:
                    usuario.senha_login = senha

                pn.state.notifications.success('Usuário atualizado com sucesso!')
            else:
                pn.state.notifications.error('Usuário não encontrado.')
                return
        else:
            existe = session.query(Usuario).filter_by(cpf=cpf).first()
            if existe:
                pn.state.notifications.error('Este CPF já está cadastrado!')
                return

            if not senha:
                pn.state.notifications.error('Defina uma senha para o novo usuário!')
                return

            novo = Usuario(
                pnome=pnome,
                mnome=mnome,
                unome=unome,
                sexo=sexo,
                cpf=cpf,
                email=email or None,
                senha_login=senha
            )
            session.add(novo)
            pn.state.notifications.success('Usuário cadastrado com sucesso!')

        session.commit()

    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f'Erro ao salvar usuário: {e}')
        return

    id_usuario_em_edicao = None
    limpar_campos_usuario()
    atualizar_tabela_usuarios()

    if atualizar_seletores:
        atualizar_seletores()


def preparar_edicao_usuario(event):
    global id_usuario_em_edicao

    selecionado = tabela_usuarios.selection
    if not selecionado:
        pn.state.notifications.warning('Selecione uma linha na tabela primeiro!')
        return

    index = selecionado[0]
    dados_linha = tabela_usuarios.value.iloc[index]
    id_usuario_em_edicao = int(dados_linha['ID'])

    usuario = session.query(Usuario).filter_by(id_usuario=id_usuario_em_edicao).first()
    if not usuario:
        pn.state.notifications.error('Usuário não encontrado.')
        return

    txt_pnome.value = texto(usuario.pnome)
    txt_mnome.value = texto(usuario.mnome)
    txt_unome.value = texto(usuario.unome)
    select_sexo.value = usuario.sexo if usuario.sexo in ['M', 'F'] else 'M'
    txt_cpf.value = texto(usuario.cpf)
    txt_email.value = texto(usuario.email)
    txt_senha.value = ""

    pn.state.notifications.info('Altere os dados acima e clique em Salvar. Deixe a senha em branco para manter a atual.')


def remover_usuario(event, atualizar_seletores=None):
    selecionado = tabela_usuarios.selection
    if not selecionado:
        pn.state.notifications.warning('Selecione uma linha na tabela primeiro!')
        return

    index = selecionado[0]
    dados_linha = tabela_usuarios.value.iloc[index]
    id_alvo = int(dados_linha['ID'])

    try:
        usuario = session.query(Usuario).filter_by(id_usuario=id_alvo).first()
        if usuario:
            session.delete(usuario)
            session.commit()
            pn.state.notifications.success('Usuário removido com sucesso!')
            atualizar_tabela_usuarios()
            if atualizar_seletores:
                atualizar_seletores()
        else:
            pn.state.notifications.error('Usuário não encontrado.')
    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f'Erro ao remover usuário: {e}')


def montar_aba(atualizar_seletores=None):
    btn_salvar_usuario.on_click(lambda event: salvar_usuario(event, atualizar_seletores))
    btn_editar_usuario.on_click(preparar_edicao_usuario)
    btn_remover_usuario.on_click(lambda event: remover_usuario(event, atualizar_seletores))

    atualizar_tabela_usuarios()

    return pn.Column(
        "### Gerenciar Usuários",
        pn.Row(
            pn.Column(
                txt_pnome, txt_mnome, txt_unome,
                select_sexo, txt_cpf, txt_email, txt_senha,
                btn_salvar_usuario,
                width=300
            ),
            pn.Column(tabela_usuarios, pn.Row(btn_editar_usuario, btn_remover_usuario))
        )
    )