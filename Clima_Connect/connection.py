from rethinkdb import RethinkDB
import psycopg2

r = RethinkDB()

# Função para conectar ao RethinkDB
def connect_to_rethinkdb(host, port, db, user, password):
    try:
        conn = r.connect(
            host=host,
            port=port,
            db=db,
            user=user,
            password=password
        ).repl()
        print("Conexão ao RethinkDB bem-sucedida!")
        return conn
    except r.errors.ReqlDriverError as e:
        print(f"Erro de conexão ao RethinkDB: {e}")
        return None

# Função para conectar ao PostgreSQL
def connect_to_postgresql(host, port, dbname, user, password):
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Conexão ao PostgreSQL bem-sucedida!")
        return conn
    except psycopg2.Error as e:
        print(f"Erro de conexão ao PostgreSQL: {e}")
        return None
