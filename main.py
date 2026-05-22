import tkinter as tk
from utils.session import load_session
from utils.router import navigate
import view.user.login as login_view
import adm.view as adm_view
import view.storage.view as storage_view

# Ponto de entrada da aplicação

window = tk.Tk()
window.title("Login")

# Janela ocupa a tela inteira
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry(f"{width}x{height}+0+0")

# Redireciona para a tela correta com base na sessão salva
session = load_session()
if session:
    # Usuário já logado: vai para admin ou depósito conforme o perfil
    navigate(window, adm_view if session["is_admin"] else storage_view)
else:
    # Sem sessão: exibe tela de login
    navigate(window, login_view)

window.mainloop()
