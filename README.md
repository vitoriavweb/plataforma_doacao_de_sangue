# Plataforma Doação de Sangue Colaboarativa

Disciplina de Fundamentos de Banco de Dados - UFC 2026.1

---

## Rodando o projeto

```
python app.py
```

---

## Estrutura do projeto

```
PLATAFORMA_DOACAO_DE_SANGUE/
├── app.py                  # Entry point
├── db.py                   # Database
├── models.py               # Cração de tabelas
├── doacao.sql              # Script de criação do banco
├── inserts.sql             # Script de inserção de dados
├── crud_agendamento.py     # CRUD de agendamento de doações
├── crud_estoque.py         # CRUD de estoque de sangue
├── crud_instituicoes.py    # CRUD de instituições parceiras
├── crud_solicitacoes.py    # CRUD de solicitações de estoque de sangue
├── crud_triagem.py         # CRUD de triagem dos doadores
├── crud_usuario.py         # CRUD de usuarios
├── crud_historico.py       # CRUD de historico do doador
├── crud_hospital.py        # CRUD de hospitais parceiros
├── crud_campanhas.py       # CRUD de campanhas de doação 
├── crud_notificações.py    # CRUD de notificações 
```

---

## Divisão das telas por membro

| Membro | Telas |
|--------|-------|
| Vitória | Usuários, Triagem, Agendamentos, campanhas |
| Tharsyla | Hospitais, Historico, notificações |
| Kemilly | Instituições, Estoque, Solicitações |
