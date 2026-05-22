from utils.db import query_all, execute

# Retorna todos os logs, do mais recente ao mais antigo
def find_all():
    return query_all("SELECT username, categoria, descricao, timestamp FROM logs ORDER BY id DESC")

# Retorna logs filtrados por categoria e/ou texto de busca
def find_filtered(categoria=None, search=None):
    conditions = []
    params = []

    if categoria:
        conditions.append("categoria = ?")
        params.append(categoria)

    if search:
        conditions.append("(username LIKE ? OR descricao LIKE ?)")
        params.extend([f"%{search}%", f"%{search}%"])

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    return query_all(f"SELECT username, categoria, descricao, timestamp FROM logs {where} ORDER BY id DESC", params)

# Remove todos os logs (apenas sysop)
def clear_all():
    execute("DELETE FROM logs")
