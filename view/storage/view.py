import tkinter as tk
from utils.session import clear_session, load_session
from utils.router import navigate
from controller.storage import (
    get_layout,
    get_sections,
    get_items_at,
    create_item,
    update_item,
    delete_item,
    search_items,
)

# View de Depósito
# Exibe a tela principal do depósito: grid de seções, barra de pesquisa, modais de itens e opções de logout/admin.
def show(window):
    import view.user.login as login_view
    import adm.view as adm_view

    session = load_session()
    container = tk.Frame(window)
    container.pack(fill=tk.BOTH, expand=True)

    # Barra superior com título, botão de sair e (se admin) botão de ir para o painel
    top_bar = tk.Frame(container)
    top_bar.pack(fill=tk.X, padx=10, pady=10)

    tk.Label(top_bar, text="Depósito", font=("Arial", 16, "bold")).pack(side=tk.LEFT)

    def logout():
        # Encerra a sessão e volta para a tela de login
        clear_session()
        navigate(window, login_view)

    tk.Button(
        top_bar, text="Sair", bg="#a33", fg="white", relief=tk.FLAT, command=logout
    ).pack(side=tk.RIGHT)

    if session and session["is_admin"]:
        tk.Button(
            top_bar,
            text="Ir para Admin",
            bg="#2c5f8a",
            fg="white",
            relief=tk.FLAT,
            command=lambda: navigate(window, adm_view),
        ).pack(side=tk.RIGHT, padx=5)

    # Barra de pesquisa
    search_bar = tk.Frame(container)
    search_bar.pack(fill=tk.X, padx=10, pady=(0, 5))

    tk.Label(search_bar, text="Pesquisar:").pack(side=tk.LEFT, padx=(0, 5))
    search_var = tk.StringVar()
    tk.Entry(search_bar, textvariable=search_var, width=35).pack(side=tk.LEFT)

    search_results_frame = tk.Frame(container, bg="#f9f9f9", relief=tk.RIDGE, bd=1)

    # Carrega layout e seções do banco para montar o grid
    layout = get_layout()
    sections = {letter: keyword for letter, keyword in get_sections()}
    cols = layout["columns"]
    rows = layout["rows"]
    letters = [chr(65 + i) for i in range(26)]  # A-Z

    # Formulário modal para criar ou editar um item numa posição específica
    def open_item_form(parent, letter, row, item=None, on_save=None):
        form_modal = tk.Toplevel(parent)
        form_modal.title("Novo Item" if not item else "Editar Item")
        form_modal.resizable(False, False)
        form_modal.grab_set()
        form_modal.geometry("300x200")

        tk.Label(
            form_modal,
            text="Novo Item" if not item else "Editar Item",
            font=("Arial", 12, "bold"),
        ).pack(pady=10)

        form = tk.Frame(form_modal)
        form.pack()

        tk.Label(form, text="Nome:").grid(row=0, column=0, padx=5, pady=4, sticky="e")
        entry_name = tk.Entry(form, width=22)
        entry_name.insert(0, item[1] if item else "")
        entry_name.grid(row=0, column=1, padx=5)

        tk.Label(form, text="Descrição:").grid(
            row=1, column=0, padx=5, pady=4, sticky="e"
        )
        entry_desc = tk.Entry(form, width=22)
        entry_desc.insert(0, item[2] or "" if item else "")
        entry_desc.grid(row=1, column=1, padx=5)

        tk.Label(form, text="Quantidade:").grid(
            row=2, column=0, padx=5, pady=4, sticky="e"
        )
        entry_qty = tk.Entry(form, width=22)
        entry_qty.insert(0, str(item[3]) if item else "1")
        entry_qty.grid(row=2, column=1, padx=5)

        feedback = tk.Label(form_modal, text="", fg="red")
        feedback.pack()

        # Valida os campos e salva o item (criação ou atualização)
        def submit():
            name = entry_name.get().strip()
            desc = entry_desc.get().strip()
            qty = entry_qty.get().strip()
            if not name:
                feedback.config(text="Nome é obrigatório.")
                return
            if not qty.isdigit() or int(qty) < 1:
                feedback.config(text="Quantidade deve ser um número positivo.")
                return
            if item:
                update_item(item[0], name, desc, letter, row, int(qty))
            else:
                create_item(name, desc, letter, row, int(qty))
            form_modal.destroy()
            if on_save:
                on_save()

        tk.Button(form_modal, text="Salvar", command=submit).pack(pady=8)

    # Modal que lista os itens de uma posição (seção + linha) e permite adicionar, editar ou remover
    def open_items_modal(letter, row, refresh_rows_cb=None):
        modal = tk.Toplevel(window)
        modal.title(f"Seção {letter} - Linha {row}")
        modal.resizable(False, False)
        modal.grab_set()
        modal.geometry("360x420")

        tk.Label(modal, text=f"{letter}{row}", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(
            modal,
            text="+ Adicionar Item",
            command=lambda: open_item_form(
                modal,
                letter,
                row,
                on_save=lambda: [refresh_list(), refresh_rows_cb and refresh_rows_cb()],
            ),
        ).pack()

        list_frame = tk.Frame(modal)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Recarrega a lista de itens da posição, chamada após qualquer alteração
        def refresh_list():
            for w in list_frame.winfo_children():
                w.destroy()
            items = get_items_at(letter, row)
            if not items:
                tk.Label(list_frame, text="Nenhum item nesta posição.", fg="#888").pack(
                    expand=True
                )
                return
            for item_id, name, description, quantity in items:
                f = tk.Frame(list_frame, relief=tk.RIDGE, bd=1)
                f.pack(fill=tk.X, pady=3)
                tk.Label(f, text=name, font=("Arial", 11, "bold")).pack(
                    anchor="w", padx=5
                )
                if description:
                    tk.Label(f, text=description, fg="#555").pack(anchor="w", padx=5)
                tk.Label(f, text=f"Quantidade: {quantity}", fg="#777").pack(
                    anchor="w", padx=5
                )
                btn_row = tk.Frame(f)
                btn_row.pack(anchor="e", padx=5, pady=2)
                item = (item_id, name, description, quantity)
                tk.Button(
                    btn_row,
                    text="Editar",
                    command=lambda i=item: open_item_form(
                        modal,
                        letter,
                        row,
                        item=i,
                        on_save=lambda: [
                            refresh_list(),
                            refresh_rows_cb and refresh_rows_cb(),
                        ],
                    ),
                ).pack(side=tk.LEFT, padx=2)
                tk.Button(
                    btn_row,
                    text="Remover",
                    fg="red",
                    command=lambda i=item_id: [
                        delete_item(i),
                        refresh_list(),
                        refresh_rows_cb and refresh_rows_cb(),
                    ],
                ).pack(side=tk.LEFT, padx=2)

        refresh_list()
        tk.Button(modal, text="Fechar", command=modal.destroy).pack(pady=5)

    # Modal que exibe todas as linhas de uma seção, destacando as que têm itens
    def open_rows_modal(letter):
        modal = tk.Toplevel(window)
        modal.title(f"Seção {letter}")
        modal.resizable(False, False)
        modal.grab_set()
        modal.geometry("260x400")

        keyword = sections.get(letter)
        title = f"Seção {letter}" + (f" — {keyword}" if keyword else "")
        tk.Label(modal, text=title, font=("Arial", 13, "bold")).pack(pady=10)

        scroll_frame = tk.Frame(modal)
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        row_canvas = tk.Canvas(scroll_frame)
        row_scroll = tk.Scrollbar(
            scroll_frame, orient=tk.VERTICAL, command=row_canvas.yview
        )
        row_canvas.configure(yscrollcommand=row_scroll.set)
        row_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        row_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        inner = tk.Frame(row_canvas)
        row_canvas.create_window((0, 0), window=inner, anchor="nw")

        # Recarrega os botões de linha, colorindo os que têm itens
        def refresh_rows():
            for w in inner.winfo_children():
                w.destroy()
            for row in range(1, rows + 1):
                items = get_items_at(letter, row)
                label = f"{letter}{row}" + (
                    f"  ({len(items)} item{'s' if len(items) != 1 else ''})"
                    if items
                    else ""
                )
                bg = "#c8e6c9" if items else "#f0f0f0"
                tk.Button(
                    inner,
                    text=label,
                    bg=bg,
                    width=24,
                    anchor="w",
                    command=lambda r=row: open_items_modal(
                        letter, r, refresh_rows_cb=refresh_rows
                    ),
                ).pack(fill=tk.X, pady=1)
            inner.update_idletasks()
            row_canvas.config(scrollregion=row_canvas.bbox("all"))

        refresh_rows()
        tk.Button(modal, text="Fechar", command=modal.destroy).pack(pady=8)

    # Atualiza os resultados de busca em tempo real conforme o usuário digita
    def update_search(*_):
        query = search_var.get().strip()
        for w in search_results_frame.winfo_children():
            w.destroy()

        if not query:
            search_results_frame.pack_forget()
            return

        search_results_frame.pack(fill=tk.X, padx=10, pady=(0, 5))

        results = search_items(query)

        # Seções cujas letras ou palavras-chave batem com a busca
        col_matches = [
            (l, kw)
            for l, kw in sections.items()
            if query.lower() in l.lower() or (kw and query.lower() in kw.lower())
        ]

        if col_matches:
            tk.Label(
                search_results_frame,
                text="Seções:",
                font=("Arial", 10, "bold"),
                bg="#f9f9f9",
            ).pack(anchor="w", padx=8, pady=(5, 0))
            row_f = tk.Frame(search_results_frame, bg="#f9f9f9")
            row_f.pack(fill=tk.X, padx=8, pady=2)
            for letter, keyword in col_matches:
                label = f"{letter}" + (f" ({keyword})" if keyword else "")
                tk.Button(
                    row_f,
                    text=label,
                    relief=tk.FLAT,
                    bg="#dce8f5",
                    command=lambda l=letter: open_rows_modal(l),
                ).pack(side=tk.LEFT, padx=3, pady=2)

        if results:
            tk.Label(
                search_results_frame,
                text="Itens:",
                font=("Arial", 10, "bold"),
                bg="#f9f9f9",
            ).pack(anchor="w", padx=8, pady=(5, 0))
            for name, section, row, keyword in results:
                position = f"{section}{row}"
                label = f"{name}  —  {position}" + (f"  ({keyword})" if keyword else "")
                tk.Button(
                    search_results_frame,
                    text=label,
                    anchor="w",
                    relief=tk.FLAT,
                    bg="#f9f9f9",
                    activebackground="#eee",
                    command=lambda s=section, r=row: open_items_modal(s, r),
                ).pack(fill=tk.X, padx=8, pady=1)

        if not col_matches and not results:
            tk.Label(
                search_results_frame,
                text="Nenhum resultado encontrado.",
                fg="#888",
                bg="#f9f9f9",
            ).pack(padx=8, pady=5)

    search_var.trace_add("write", update_search)

    # Grid principal com scroll: cada coluna representa uma seção do depósito
    canvas_frame = tk.Frame(container)
    canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    canvas = tk.Canvas(canvas_frame, bg="white")
    scroll_y = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
    scroll_x = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
    canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.pack(fill=tk.BOTH, expand=True)

    grid_frame = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=grid_frame, anchor="nw")

    for col in range(cols):
        letter = letters[col] if col < len(letters) else "?"
        keyword = sections.get(letter)
        header_text = f"{letter}\n({keyword})" if keyword else letter
        tk.Button(
            grid_frame,
            text=header_text,
            font=("Arial", 10, "bold"),
            bg="#2c2c2c",
            fg="white",
            width=14,
            height=3,
            relief=tk.RIDGE,
            activebackground="#444",
            activeforeground="white",
            command=lambda l=letter: open_rows_modal(l),
        ).grid(row=0, column=col, padx=1, pady=1)

    grid_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
