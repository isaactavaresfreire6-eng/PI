from model.admin import find_all, insert, update_power
from utils.log import log

# Mapeamento das opções de ordenação para cláusulas SQL
ORDER_ADMINS = {
    "id":    "ORDER BY users.id ASC",
    "a-z":   "ORDER BY users.username ASC",
    "z-a":   "ORDER BY users.username DESC",
    "poder": "ORDER BY admin.power DESC",
}

def get_admins(order="id"):
    # Retorna todos os admins na ordem solicitada
    return find_all(ORDER_ADMINS.get(order, "ORDER BY users.id ASC"))

def create_admin(user_id, power):
    # Promove um usuário a admin com o nível de poder informado
    insert(user_id, power)
    log("admin", f"Usuário ID {user_id} promovido a admin com nível {power}")

def update_admin(user_id, power):
    # Atualiza o nível de poder de um admin existente
    update_power(user_id, power)
    log("admin", f"Nível do admin ID {user_id} alterado para {power}")
