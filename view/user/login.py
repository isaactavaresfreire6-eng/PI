import tkinter as tk
from controller.user.login import login

# Tela de login: coleta usuário e senha e envia ao controller
def show(window):
    # Layout centralizado
    container_login = tk.Frame(window)
    container_login.pack(expand=True)

    tk.Label(container_login, text="Usuário:").pack(pady=5)
    entry_username = tk.Entry(container_login)
    entry_username.pack(pady=5)

    tk.Label(container_login, text="Senha:").pack(pady=5)
    entry_password = tk.Entry(container_login, show="*")
    entry_password.pack(pady=5)

    feedback = tk.Label(container_login, text="", fg="red")
    feedback.pack()

    def submit():
        username = entry_username.get()
        password = entry_password.get()
        if not username or not password:
            feedback.config(text="Preencha todos os campos.")
            return
        login(window, username, password, feedback)

    tk.Button(container_login, text="Entrar", command=submit).pack(pady=10)
    entry_username.bind("<Return>", lambda _: submit())
    entry_password.bind("<Return>", lambda _: submit())