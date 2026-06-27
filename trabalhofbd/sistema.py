import sqlite3

def conectar():
    return sqlite3.connect('doacoes.db')

# --- FUNÇÃO PARA CRIAR AS TABELAS (Caso não existam) ---
def inicializar_banco():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hemocentros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cidade TEXT NOT NULL
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS doadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT UNIQUE NOT NULL,
        tipo_sanguineo TEXT NOT NULL,
        contato TEXT
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS doacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_doador INTEGER,
        id_hemocentro INTEGER,
        data TEXT NOT NULL,
        quantidade_ml INTEGER NOT NULL,
        FOREIGN KEY (id_doador) REFERENCES doadores(id),
        FOREIGN KEY (id_hemocentro) REFERENCES hemocentros(id)
    )''')
    
    conexao.commit()
    conexao.close()

# --- FUNÇÕES DE CADASTRO E CONSULTA ---
def cadastrar_doador():
    print("\n--- CADASTRO DE DOADOR ---")
    nome = input("Nome completo: ")
    cpf = input("CPF: ")
    tipo = input("Tipo Sanguíneo (Ex: O+, A-): ").upper()
    contato = input("Telefone de contato: ")
    
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO doadores (nome, cpf, tipo_sanguineo, contato) VALUES (?, ?, ?, ?)", 
                       (nome, cpf, tipo, contato))
        conexao.commit()
        print("\n✅ Doador cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("\n❌ Erro: Este CPF já está cadastrado!")
    finally:
        conexao.close()

def listar_doadores():
    print("\n--- LISTA DE DOADORES CADASTRADOS ---")
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, cpf, tipo_sanguineo FROM doadores")
    doadores = cursor.fetchall()
    conexao.close()
    
    if not doadores:
        print("Nenhum doador encontrado.")
        return

    for d in doadores:
        print(f"ID: {d[0]} | Nome: {d[1]} | CPF: {d[2]} | Sangue: {d[3]}")

# --- MENU PRINCIPAL DO TERMINAL ---
def menu():
    inicializar_banco()
    while True:
        print("\n=================================")
        print("  SISTEMA DE DOAÇÃO DE SANGUE  ")
        print("=================================")
        print("1. Cadastrar Doador")
        print("2. Listar Doadores")
        print("0. Sair do Sistema")
        print("=================================")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            cadastrar_doador()
        elif opcao == "2":
            listar_doadores()
        elif opcao == "0":
            print("\nSaindo do sistema... Até logo!")
            break
        else:
            print("\n❌ Opção inválida! Tente novamente.")

# Executa o programa
if __name__ == "__main__":
    menu()