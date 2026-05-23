import psycopg2

def connect_to_database():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="hackaton",
            port = "5432",
            user="postgres",
            password="z9f4k5ty"
        )
        cursor = connection.cursor()
        print("Database connection successful!")
        return connection, cursor
    
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

def close_database_connection(connection, cursor):
    if cursor:
        cursor.close()
    if connection:
        connection.close()
        print("Database connection closed.")



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

def adicionar_lider(cursor, connection, telefone, matricula, nome, periodo, grupo, senha, email, monitor):
    erro=0
    aluno_exists = execute_query(cursor, "SELECT * FROM alunos WHERE telefone = %s", (telefone))
    if aluno_exists:
        print(f"Aluno {nome} já existe, falha no cadastro.")
        return
    execute_query(cursor, "INSERT INTO grupos (id, senha, monitor) VALUES (%s, %s, %s)", (telefone, senha, monitor))
    execute_query(cursor, "INSERT INTO alunos (telefone, matricula, nome, periodo, grupo, email, erro) VALUES (%s, %s, %s, %s, %s, %s, %s)", (telefone, matricula, nome, periodo, grupo, email, erro))
    connection.commit()

def adicionar_aluno(cursor, connection, telefone, matricula, nome, periodo, grupo, senha, email):
    erro=0

    aluno_exists = execute_query(cursor, "SELECT * FROM alunos WHERE telefone = %s", (telefone))
    if aluno_exists:
        print(f"Aluno {nome} já existe, falha no cadastro.")
        return
    
    grupo_exists = execute_query(cursor, "SELECT id FROM grupos WHERE id = %s", (grupo))
    if not grupo_exists:
        print(f"Grupo {grupo} não encontrado.")
        erro = 1
        grupo = 0

    if grupo_exists[0].senha != senha:
        print(f"Senha incorreta para o grupo {grupo}.")
        erro = 2
        grupo = 0

    execute_query(cursor, "INSERT INTO alunos (telefone, matricula, nome, periodo, grupo, email, erro) VALUES (%s, %s, %s, %s, %s, %s, %s)", (telefone, matricula, nome, periodo, grupo, email, erro)) 
    connection.commit()



def listar_monitores(cursor):
    return execute_query(cursor, "SELECT * FROM monitores")

def listar_alunos(cursor):
    return execute_query(cursor, "SELECT * FROM alunos")

def listar_grupos(cursor):
    return execute_query(cursor, "SELECT * FROM grupos")
