from utils.router import navigate
from utils.session import save_session
from utils.password import verify_password
from utils.log import log
from model.users import find_by_username
from model.admin import find_by_user_id
import adm.view as adm_view
import view.storage.view as storage_view

def login(window, username, password, feedback=None):
    # Busca o usuário pelo nome e verifica a senha
    user = find_by_username(username)
    if user and verify_password(password, user[2]):
        # Verifica se o usuário é admin e obtém seu nível de poder
        admin = find_by_user_id(user[0])
        is_admin = admin is not None
        power = admin[2] if admin else 0  # admin: (id, user_id, power)
        save_session(user[0], username, is_admin, power)
        log("login", f"Login realizado ({'área admin' if is_admin else 'depósito'})")
        # Redireciona para a tela correta conforme o perfil
        navigate(window, adm_view if is_admin else storage_view)
    else:
        log("login", f"Tentativa de login falhou para '{username}'")
        if feedback:
            feedback.config(text="Usuário ou senha inválidos.")
