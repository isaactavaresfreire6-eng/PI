import os
import tempfile

# Arquivo temporário usado para persistir a sessão entre execuções
_session_file = os.path.join(tempfile.gettempdir(), "jackbox_session.tmp")


def save_session(user_id, username, is_admin, power=0):
    # Salva os dados da sessão no arquivo temporário (power=0 para não-admins)
    with open(_session_file, "w") as f:
        f.write(f"{user_id},{username},{int(is_admin)},{power}")


def load_session():
    # Lê a sessão salva; retorna None se não existir ou estiver inválida
    if not os.path.exists(_session_file):
        return None
    with open(_session_file, "r") as f:
        parts = f.read().strip().split(",")
    # Sessão antiga (3 campos) é descartada para forçar novo login com power
    if len(parts) != 4:
        return None
    return {"user_id": int(parts[0]), "username": parts[1], "is_admin": parts[2] == "1", "power": int(parts[3])}


def clear_session():
    # Remove o arquivo de sessão (logout)
    if os.path.exists(_session_file):
        os.remove(_session_file)
