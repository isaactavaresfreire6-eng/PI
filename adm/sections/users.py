import tkinter as tk
from controller.adm.users import get_all_users, create_user

# Tela de gerenciamento de usuários com tabela, busca, ordenação e criação
def show(frame):
    tk.Label(frame, text="Usuários", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=20)

    top_bar = tk.Frame(frame, bg="#f0f0f0")
    top_bar.pack(anchor="center")
    tk.Button(top_bar, text="+ Novo Usuário", command=lambda: open_modal()).pack(side=tk.LEFT, padx=5)

    user_orders = ["id", "a-z", "z-a"]
    order_idx = [0]  # Índice mutável para controlar a ordenação atual

    order_btn = tk.Button(top_bar, text="ordenar por: id")
    order_btn.pack(side=tk.LEFT, padx=5)

    search_bar = tk.Frame(frame, bg="#f0f0f0")
    search_bar.pack(anchor="center", pady=5)
    tk.Label(search_bar, text="Pesquisar:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
    search_var = tk.StringVar()
    tk.Entry(search_bar, textvariable=search_var, width=30).pack(side=tk.LEFT)

    table_wrapper = tk.Frame(frame, bg="#f0f0f0")
    table_wrapper.pack(anchor="center", pady=10)

    def refresh(order=None):
        # Recarrega a tabela aplicando filtro de busca e ordenação
        if order is None:
            order = user_orders[order_idx[0]]
        for widget in table_wrapper.winfo_children():
            widget.destroy()
        query = search_var.get().strip().lower()
        rows = [r for r in get_all_users(order) if query in str(r[0]) or query in r[1].lower()]
        for col, header in enumerate(["ID", "Usuário"]):
            tk.Label(table_wrapper, text=header, font=("Arial", 11, "bold"), bg="#d0d0d0", relief=tk.RIDGE, width=20).grid(row=0, column=col, padx=1, pady=1)
        for row_idx2, (uid, username) in enumerate(rows, start=1):
            tk.Label(table_wrapper, text=uid, bg="#f0f0f0", relief=tk.RIDGE, width=20).grid(row=row_idx2, column=0, padx=1, pady=1)
            tk.Label(table_wrapper, text=username, bg="#f0f0f0", relief=tk.RIDGE, width=20).grid(row=row_idx2, column=1, padx=1, pady=1)

    def cycle_order():
        # Avança para o próximo critério de ordenação ciclicamente
        order_idx[0] = (order_idx[0] + 1) % len(user_orders)
        order = user_orders[order_idx[0]]
        order_btn.config(text=f"ordenar por: {order}")
        refresh(order)

    order_btn.config(command=cycle_order)
    search_var.trace_add("write", lambda *_: refresh())
    refresh()

    def open_modal():
        # Abre o formulário de criação de novo usuário
        modal = tk.Toplevel(frame)
        modal.title("Novo Usuário")
        modal.resizable(False, False)
        modal.grab_set()

        modal.update_idletasks()
        x = frame.winfo_rootx() + frame.winfo_width() // 2 - 150
        y = frame.winfo_rooty() + frame.winfo_height() // 2 - 100
        modal.geometry(f"300x200+{x}+{y}")

        tk.Label(modal, text="Novo Usuário", font=("Arial", 13, "bold")).pack(pady=10)

        form = tk.Frame(modal)
        form.pack(pady=5)

        tk.Label(form, text="Usuário:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        entry_username = tk.Entry(form, width=20)
        entry_username.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Senha:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        entry_password = tk.Entry(form, show="*", width=20)
        entry_password.grid(row=1, column=1, padx=5, pady=5)

        feedback = tk.Label(modal, text="", fg="red")
        feedback.pack()

        def submit():
            # Valida os campos e cria o usuário
            username = entry_username.get().strip()
            password = entry_password.get().strip()
            if not username or not password:
                feedback.config(text="Preencha todos os campos.")
                return
            if not create_user(username, password):
                feedback.config(text="Usuário já existe.")
                return
            refresh()
            modal.destroy()

        tk.Button(modal, text="Criar", command=submit).pack(pady=10)
