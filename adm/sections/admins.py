import tkinter as tk
from controller.adm.settings import get_admins, create_admin, update_admin
from controller.adm.users import get_users_without_admin
from utils.session import load_session

# Tela de gerenciamento de admins com tabela, busca, ordenação e criação
def show(frame):
    # Nível de poder do admin logado (sysop = 9)
    session = load_session()
    my_power = session["power"] if session else 0

    tk.Label(frame, text="Admins", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=20)

    top_bar = tk.Frame(frame, bg="#f0f0f0")
    top_bar.pack(anchor="center")
    # Somente sysop pode criar novos admins
    if my_power == 9:
        tk.Button(top_bar, text="+ Novo Admin", command=lambda: open_modal()).pack(side=tk.LEFT, padx=5)

    admin_orders = ["id", "a-z", "z-a", "poder"]
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

    def refresh_table(order=None):
        # Recarrega a tabela aplicando filtro de busca e ordenação
        if order is None:
            order = admin_orders[order_idx[0]]
        for widget in table_wrapper.winfo_children():
            widget.destroy()
        query = search_var.get().strip().lower()
        rows = [r for r in get_admins(order) if query in r[1].lower() or query in str(r[2])]
        for col, header in enumerate(["Usuário", "Nível", "Ações"]):
            tk.Label(table_wrapper, text=header, font=("Arial", 11, "bold"), bg="#d0d0d0", relief=tk.RIDGE, width=20).grid(row=0, column=col, padx=1, pady=1)
        for row_idx2, (uid, username, power) in enumerate(rows, start=1):
            tk.Label(table_wrapper, text=username, bg="#f0f0f0", relief=tk.RIDGE, width=20).grid(row=row_idx2, column=0, padx=1, pady=1)
            tk.Label(table_wrapper, text=power, bg="#f0f0f0", relief=tk.RIDGE, width=20).grid(row=row_idx2, column=1, padx=1, pady=1)
            btn_frame = tk.Frame(table_wrapper, bg="#f0f0f0", relief=tk.RIDGE)
            btn_frame.grid(row=row_idx2, column=2, padx=1, pady=1)
            # Sysop pode editar qualquer admin, exceto outros sysops (nível 9)
            if my_power == 9 and power != 9:
                tk.Button(btn_frame, text="Editar", command=lambda i=uid, p=power: open_edit_modal(i, p)).pack(padx=4, pady=2)
            else:
                tk.Label(btn_frame, text="—", bg="#f0f0f0", width=8).pack(padx=4, pady=2)

    def cycle_order():
        # Avança para o próximo critério de ordenação ciclicamente
        order_idx[0] = (order_idx[0] + 1) % len(admin_orders)
        order = admin_orders[order_idx[0]]
        order_btn.config(text=f"ordenar por: {order}")
        refresh_table(order)

    order_btn.config(command=cycle_order)
    search_var.trace_add("write", lambda *_: refresh_table())
    refresh_table()

    def open_edit_modal(user_id, current_power):
        # Abre o formulário para alterar o nível de poder de um admin (apenas sysop)
        modal = tk.Toplevel(frame)
        modal.title("Editar Nível")
        modal.resizable(False, False)
        modal.grab_set()
        x = frame.winfo_rootx() + frame.winfo_width() // 2 - 150
        y = frame.winfo_rooty() + frame.winfo_height() // 2 - 80
        modal.geometry(f"300x160+{x}+{y}")

        tk.Label(modal, text="Novo nível (1-8):", font=("Arial", 11)).pack(pady=10)
        entry_power = tk.Entry(modal, width=10)
        entry_power.insert(0, str(current_power))
        entry_power.pack(pady=5)

        feedback = tk.Label(modal, text="", fg="red")
        feedback.pack()

        def submit():
            # Valida e salva o novo nível
            power = entry_power.get().strip()
            if not power.isdigit() or not (1 <= int(power) <= 8):
                feedback.config(text="Nível deve ser entre 1 e 8.")
                return
            update_admin(user_id, int(power))
            refresh_table()
            modal.destroy()

        tk.Button(modal, text="Salvar", command=submit).pack(pady=5)

    def open_modal():
        # Abre o formulário para promover um usuário a admin
        users = get_users_without_admin()

        modal = tk.Toplevel(frame)
        modal.title("Novo Admin")
        modal.resizable(False, False)
        modal.grab_set()

        modal.update_idletasks()
        x = frame.winfo_rootx() + frame.winfo_width() // 2 - 150
        y = frame.winfo_rooty() + frame.winfo_height() // 2 - 100
        modal.geometry(f"300x220+{x}+{y}")

        tk.Label(modal, text="Novo Admin", font=("Arial", 13, "bold")).pack(pady=10)

        form = tk.Frame(modal)
        form.pack(pady=5)

        tk.Label(form, text="Usuário:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Popula o dropdown com usuários sem perfil de admin
        user_var = tk.StringVar()
        if users:
            user_var.set(f"{users[0][0]} - {users[0][1]}")
            options = [f"{uid} - {username}" for uid, username in users]
        else:
            user_var.set("Nenhum usuário disponível")
            options = ["Nenhum usuário disponível"]

        tk.OptionMenu(form, user_var, *options).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Nível (1-8):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        entry_power = tk.Entry(form, width=20)
        entry_power.grid(row=1, column=1, padx=5, pady=5)

        feedback = tk.Label(modal, text="", fg="red")
        feedback.pack()

        def submit():
            # Valida os campos e cria o admin
            if not users:
                feedback.config(text="Nenhum usuário disponível.")
                return
            power = entry_power.get().strip()
            if not power.isdigit() or not (1 <= int(power) <= 8):
                feedback.config(text="Nível deve ser entre 1 e 8.")
                return
            user_id = int(user_var.get().split(" - ")[0])
            create_admin(user_id, int(power))
            refresh_table()
            modal.destroy()

        tk.Button(modal, text="Criar", command=submit).pack(pady=10)
