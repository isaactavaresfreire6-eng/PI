import tkinter as tk
import adm.sections.dashboard as dashboard
import adm.sections.users as users
import adm.sections.admins as admins
import adm.sections.settings as settings
import adm.sections.logs as logs
import adm.sections.storage as storage
from utils.session import clear_session, load_session
from utils.router import navigate

# Seções disponíveis na barra lateral do painel admin
SECTIONS = [
    ("Painel", dashboard),
    ("Usuários", users),
    ("Admins", admins),
    ("Storage", storage),
    ("Logs", logs),
    ("Configurações", settings),
]

# Tela principal do painel administrativo com barra lateral de navegação
def show(window):
    import view.user.login as login_view

    # Redireciona para login se não houver sessão de admin
    session = load_session()
    if not session or not session["is_admin"]:
        navigate(window, login_view)
        return

    container = tk.Frame(window)
    container.pack(fill=tk.BOTH, expand=True)

    # Barra lateral escura à esquerda
    sidebar_frame = tk.Frame(container, width=200, bg="#2c2c2c")
    sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
    sidebar_frame.pack_propagate(False)

    tk.Label(sidebar_frame, text="Admin", bg="#2c2c2c", fg="white", font=("Arial", 14, "bold")).pack(pady=15)

    def logout():
        clear_session()
        # amazonq-ignore-next-line
        navigate(window, login_view)

    def switch_to_storage():
        import view.storage.view as storage_view
        # amazonq-ignore-next-line
        navigate(window, storage_view)

    # Botões fixos no rodapé da barra lateral
    tk.Button(
        sidebar_frame, text="Ir para Storage", anchor="w",
        bg="#2c5f8a", fg="white", relief=tk.FLAT,
        activebackground="#3a7ab5", activeforeground="white",
        width=20, padx=10,
        command=switch_to_storage
    ).pack(side=tk.BOTTOM, fill=tk.X)

    tk.Button(
        sidebar_frame, text="Sair", anchor="w",
        bg="#a33", fg="white", relief=tk.FLAT,
        activebackground="#c44", activeforeground="white",
        width=20, padx=10,
        command=logout
    ).pack(side=tk.BOTTOM, fill=tk.X, pady=5)

    # Canvas com scroll para os botões de navegação
    sidebar_canvas = tk.Canvas(sidebar_frame, bg="#2c2c2c", highlightthickness=0)
    scrollbar = tk.Scrollbar(sidebar_frame, orient=tk.VERTICAL, command=sidebar_canvas.yview)
    sidebar_canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    sidebar_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    sidebar_list = tk.Frame(sidebar_canvas, bg="#2c2c2c")
    sidebar_canvas.create_window((0, 0), window=sidebar_list, anchor="nw")

    # Área de conteúdo à direita onde cada seção é carregada
    iframe = tk.Frame(container, bg="#f0f0f0")
    iframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def load_section(module):
        # Limpa o conteúdo atual e carrega a seção selecionada
        for widget in iframe.winfo_children():
            widget.destroy()
        module.show(iframe)

    # Cria um botão na barra lateral para cada seção
    for label, module in SECTIONS:
        btn = tk.Button(
            sidebar_list, text=label, anchor="w",
            bg="#2c2c2c", fg="white", relief=tk.FLAT,
            activebackground="#444", activeforeground="white",
            width=20, padx=10,
            command=lambda m=module: load_section(m)
        )
        btn.pack(fill=tk.X, pady=2)

    sidebar_list.update_idletasks()
    sidebar_canvas.config(scrollregion=sidebar_canvas.bbox("all"))

    # Abre o painel como tela inicial
    load_section(dashboard)
