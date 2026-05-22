import tkinter as tk
from controller.adm.logs import get_logs, get_categorias, clear_logs
from utils.session import load_session

# Tela de logs: visível apenas para sysop, com busca e filtro por categoria
def show(frame):
    session = load_session()

    # Redireciona se não for sysop
    if not session or session["power"] != 9:
        tk.Label(frame, text="Acesso negado.", font=("Arial", 14), bg="#f0f0f0", fg="red").pack(expand=True)
        return

    tk.Label(frame, text="Logs", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=20)

    # Barra de controles: busca, filtro e botão de limpar
    controls = tk.Frame(frame, bg="#f0f0f0")
    controls.pack(anchor="center", pady=5)

    tk.Label(controls, text="Pesquisar:", bg="#f0f0f0").pack(side=tk.LEFT, padx=(0, 5))
    search_var = tk.StringVar()
    tk.Entry(controls, textvariable=search_var, width=25).pack(side=tk.LEFT, padx=(0, 15))

    tk.Label(controls, text="Categoria:", bg="#f0f0f0").pack(side=tk.LEFT, padx=(0, 5))
    categoria_var = tk.StringVar(value="todas")
    options = ["todas"] + get_categorias()
    tk.OptionMenu(controls, categoria_var, *options).pack(side=tk.LEFT, padx=(0, 15))

    tk.Button(controls, text="Limpar Logs", fg="red", relief=tk.FLAT,
              command=lambda: [clear_logs(), refresh()]).pack(side=tk.LEFT)

    # Tabela de logs com scroll
    table_frame = tk.Frame(frame, bg="#f0f0f0")
    table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    canvas = tk.Canvas(table_frame, bg="#f0f0f0")
    scrollbar = tk.Scrollbar(table_frame, orient=tk.VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    inner = tk.Frame(canvas, bg="#f0f0f0")
    canvas.create_window((0, 0), window=inner, anchor="nw")

    def refresh(*_):
        for w in inner.winfo_children():
            w.destroy()

        categoria = categoria_var.get()
        search = search_var.get().strip()

        logs = get_logs(
            categoria=None if categoria == "todas" else categoria,
            search=search or None
        )

        headers = ["Usuário", "Categoria", "Descrição", "Data/Hora"]
        widths = [14, 12, 40, 18]
        for col, (header, width) in enumerate(zip(headers, widths)):
            tk.Label(inner, text=header, font=("Arial", 10, "bold"), bg="#d0d0d0",
                     relief=tk.RIDGE, width=width).grid(row=0, column=col, padx=1, pady=1)

        if not logs:
            tk.Label(inner, text="Nenhum log encontrado.", fg="#888", bg="#f0f0f0").grid(
                row=1, column=0, columnspan=4, pady=10)
        else:
            for row_idx, (username, categoria, descricao, timestamp) in enumerate(logs, start=1):
                for col, (val, width) in enumerate(zip([username, categoria, descricao, timestamp], widths)):
                    tk.Label(inner, text=val, bg="#f0f0f0", relief=tk.RIDGE,
                             width=width, anchor="w").grid(row=row_idx, column=col, padx=1, pady=1)

        inner.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    search_var.trace_add("write", refresh)
    categoria_var.trace_add("write", refresh)
    refresh()
