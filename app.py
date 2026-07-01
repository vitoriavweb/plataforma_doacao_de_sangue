import panel as pn

from db import session
from models import Hemocentro

import crud_instituicoes as ci
import crud_estoque as ce
import crud_solicitacoes as cs
import crud_usuario as cu
import crud_agendamento as ca
import crud_triagem as ct

pn.extension('tabulator', notifications=True)


def atualizar_seletores_instituicao():
    instituicoes = session.query(Hemocentro).all()
    opcoes = {i.nome: i.cnpj for i in instituicoes}
    ce.select_inst_estoque.options = opcoes
    cs.select_inst_solicitacao.options = opcoes
    ca.select_inst_agendamento.options = opcoes


def atualizar_seletores_usuario():
    ca.atualizar_seletor_usuarios_agendamento()


def atualizar_seletores_agendamento():
    ct.atualizar_seletor_agendamentos_triagem()


aba_instituicao = ci.montar_aba(atualizar_seletores_instituicao)
aba_estoque = ce.montar_aba()
aba_solicitacao = cs.montar_aba()
aba_usuario = cu.montar_aba(atualizar_seletores_usuario)
aba_agendamento = ca.montar_aba(atualizar_seletores_agendamento)
aba_triagem = ct.montar_aba()

ci.atualizar_tabela_instituicoes()
ce.atualizar_tabela_estoque()
cs.atualizar_tabela_solicitacoes()
cu.atualizar_tabela_usuarios()
ca.atualizar_tabela_agendamentos()
ct.atualizar_tabela_triagens()

atualizar_seletores_instituicao()
atualizar_seletores_usuario()
atualizar_seletores_agendamento()

layout = pn.Tabs(
    ('Instituições (CRUD)', aba_instituicao),
    ('Estoque', aba_estoque),
    ('Solicitações', aba_solicitacao),
    ('Usuários (CRUD)', aba_usuario),
    ('Agendamentos (CRUD)', aba_agendamento),
    ('Triagens (CRUD)', aba_triagem)
)

layout.show()
