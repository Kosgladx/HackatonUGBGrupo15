import psycopg2

def connect_to_database():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="hackatonteste2",
            port = "5433",
            user="postgres",
            password="z9f4k5ty"
        )
        cursor = connection.cursor()
        print("Database connection successful!")
        return connection, cursor
    
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    return

def close_database_connection(connection, cursor):
    if cursor:
        cursor.close()
    if connection:
        connection.close()
        print("Database connection closed.")
    return



def execute_query(cursor, query, params=None):
    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print("Error executing query", error)
        return None
    


def adicionar_monitor(cursor, connection, telefone, experiencia, nome, email):
    monitor_exists = execute_query(cursor, "SELECT * FROM monitores WHERE telefone = %s", (telefone))
    if monitor_exists:
        print(f"Monitor {nome} já existe, falha no cadastro.")
        return
    execute_query(cursor, "INSERT INTO monitores (telefone, experiencia, nome, email) VALUES (%s, %s, %s, %s)", (telefone, experiencia, nome, email))
    connection.commit()
    return 

def adicionar_lider(cursor, connection, telefone, matricula, nome, periodo, grupo, senha, email, monitor):
    erro=0
    aluno_exists = execute_query(cursor, "SELECT * FROM alunos WHERE telefone = %s", (telefone))

    if aluno_exists:
        print(f"Aluno {nome} já existe, falha no cadastro.")
        return
    execute_query(cursor, "INSERT INTO grupos (id, senha, monitor) VALUES (%s, %s, %s)", (grupo, senha, monitor))
    execute_query(cursor, "INSERT INTO alunos (telefone, matricula, nome, periodo, grupo, email, erro) VALUES (%s, %s, %s, %s, %s, %s, %s)", (telefone, matricula, nome, periodo, grupo, email, erro))
    connection.commit()
    return

def adicionar_aluno(cursor, connection, telefone, matricula, nome, periodo, grupo, senha, email):
    erro=0

    aluno_exists = execute_query(cursor, "SELECT * FROM alunos WHERE telefone = %s", (telefone,))
    if aluno_exists:
        print(f"Aluno {nome} já existe, falha no cadastro.")
        return
    
    grupo_exists = execute_query(cursor, "SELECT * FROM grupos WHERE id = %s", (grupo,))
    print(grupo_exists)
    if not grupo_exists:
        print(f"Grupo {grupo} não encontrado.")
        erro = 1
        grupo = 0
    elif grupo_exists[0][1] != senha:
        print(f"Senha incorreta para o grupo {grupo}.")
        erro = 2
        grupo = 0

    execute_query(cursor, "INSERT INTO alunos (telefone, matricula, nome, periodo, grupo, email, erro) VALUES (%s, %s, %s, %s, %s, %s, %s)", (telefone, matricula, nome, periodo, grupo, email, erro)) 
    connection.commit()
    return

def adicionar_semwhats(connection, cursor, telefone):
    semwhats_exists = execute_query(cursor, "SELECT * FROM semwhats WHERE id = %s", (telefone,))
    if semwhats_exists:
        print(f"Telefone {telefone} já existe na lista de sem WhatsApp, falha no cadastro.")
        return
    execute_query(cursor, "INSERT INTO semwhats (id) VALUES (%s)", (telefone,))
    connection.commit()
    return

def adicionar_grupo(cursor, connection, id, senha, monitor):
    grupo_exists = execute_query(cursor, "SELECT * FROM grupos WHERE id = %s", (id,))
    if grupo_exists:
        print(f"Grupo {id} já existe, falha no cadastro.")
        return
    execute_query(cursor, "INSERT INTO grupos (id, senha, monitor) VALUES (%s, %s, %s)", (id, senha, monitor))
    connection.commit()
    return

def adicionar_monitor(cursor, connection, telefone, experiencia, nome, email):
    monitor_exists = execute_query(cursor, "SELECT * FROM monitores WHERE telefone = %s", (telefone,))
    if monitor_exists:
        print(f"Monitor {nome} já existe, falha no cadastro.")
        return
    execute_query(cursor, "INSERT INTO monitores (telefone, experiencia, nome, email) VALUES (%s, %s, %s, %s)", (telefone, experiencia, nome, email))
    connection.commit()
    return

def listar_monitores(cursor):
    return execute_query(cursor, "SELECT * FROM monitores")

def listar_alunos(cursor):
    return execute_query(cursor, "SELECT * FROM alunos")

def listar_grupos(cursor):
    return execute_query(cursor, "SELECT * FROM grupos")

def listar_alunos_semwhats(cursor):
    return execute_query(cursor, "SELECT * FROM semwhats")

def listar_alunos_por_grupo(cursor, grupo):
    return execute_query(cursor, "SELECT * FROM alunos WHERE grupo = %s", (grupo,))

def listar_alunossem_grupo(cursor):
    return execute_query(cursor, "SELECT * FROM alunos WHERE grupo = 0")

def listar_alunos_com_erro(cursor):
    return execute_query(cursor, "SELECT * FROM alunos WHERE erro != 0")

def listar_telefones_grupos(cursor):
    grupos = execute_query(cursor, "SELECT id,monitor FROM grupos WHERE monitor IS NOT NULL AND id != 0")
    alunos = [[] for _ in range(len(grupos))]
    for i, grupo in enumerate(grupos):
        grupo_alunos = execute_query(cursor, "SELECT telefone FROM alunos WHERE grupo = %s", (grupo[0],))
        alunos[i] = grupo_alunos + [grupo[1]]
    return alunos

def listar_telefones(cursor):
    return execute_query(cursor, "SELECT telefone FROM alunos ") + execute_query(cursor, "SELECT telefone FROM monitores ")
