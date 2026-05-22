from utils.db import execute
from utils.session import load_session

# Categorias de log disponíveis
CATEGORIAS = ["login", "usuário", "admin", "depósito", "layout"]

def log(categoria, descricao):
    # Registra uma ação no banco com o usuário da sessão atual e timestamp
    session = load_session()
    username = session["username"] if session else "sistema"
    execute(
        "INSERT INTO logs (username, categoria, descricao) VALUES (?, ?, ?)",
        (username, categoria, descricao)
    )
