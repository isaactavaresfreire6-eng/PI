from utils.password import hash_password
from model.users import find_all, find_without_admin, insert, find_by_username
from utils.log import log

# Mapeamento das opções de ordenação para cláusulas SQL
ORDER_USERS = {
    "id":  "ORDER BY id ASC",
    "a-z": "ORDER BY username ASC",
    "z-a": "ORDER BY username DESC",
}

def get_all_users(order="id"):
    # Retorna todos os usuários na ordem solicitada
    return find_all(ORDER_USERS.get(order, "ORDER BY id ASC"))

def get_users_without_admin():
    # Retorna usuários que ainda não possuem perfil de admin
    return find_without_admin()

def create_user(username, password):
    # Retorna False se o username já existir, True se criado com sucesso
    if find_by_username(username):
        return False
    insert(username, hash_password(password))
    log("usuário", f"Usuário '{username}' criado")
    return True
