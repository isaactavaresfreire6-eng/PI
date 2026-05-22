from utils.db import query_all, query_one, execute

# Busca usuário pelo nome de usuário
def find_by_username(username):
    return query_one("SELECT * FROM users WHERE username=?", (username,))

# Busca usuário pelo nome e hash da senha (login)
def find_by_credentials(username, password_hash):
    return query_one("SELECT * FROM users WHERE username=? AND password=?", (username, password_hash))

# Retorna todos os usuários na ordem especificada
def find_all(order_clause="ORDER BY id ASC"):
    return query_all(f"SELECT id, username FROM users {order_clause}")

# Retorna usuários que ainda não são admins
def find_without_admin():
    return query_all("SELECT id, username FROM users WHERE id NOT IN (SELECT user_id FROM admin)")

# Insere um novo usuário com a senha já em hash
def insert(username, password_hash):
    execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_hash))

# Retorna o total de usuários cadastrados
def count():
    return query_one("SELECT COUNT(*) FROM users")[0]
