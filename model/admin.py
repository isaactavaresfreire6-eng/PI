from utils.db import query_all, query_one, execute

# Busca o registro de admin pelo ID do usuário
def find_by_user_id(user_id):
    return query_one("SELECT * FROM admin WHERE user_id=?", (user_id,))

# Retorna todos os admins com seus usuários, na ordem especificada
def find_all(order_clause="ORDER BY users.id ASC"):
    return query_all(f"""
        SELECT users.id, users.username, admin.power
        FROM admin
        JOIN users ON admin.user_id = users.id
        {order_clause}
    """)

# Insere um novo admin com o nível de poder informado
def insert(user_id, power):
    execute("INSERT INTO admin (user_id, power) VALUES (?, ?)", (user_id, power))

# Atualiza o nível de poder de um admin existente
def update_power(user_id, power):
    execute("UPDATE admin SET power = ? WHERE user_id = ?", (power, user_id))

# Retorna o total de admins cadastrados
def count():
    return query_one("SELECT COUNT(*) FROM admin")[0]
