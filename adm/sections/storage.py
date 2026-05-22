import tkinter as tk
from controller.storage import (
    get_layout, set_layout,
    get_sections, set_keyword, delete_keyword,
    get_items, create_item, update_item, delete_item
)

# Tela administrativa do depósito: gerencia layout, seções e itens
def show(frame):
    tk.Label(frame, text="Storage", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=20)

    # --- Layout ---
    tk.Label(frame, text="Layout", font=("Arial", 13, "bold"), bg="#f0f0f0").pack()

    layout_frame = tk.Frame(frame, bg="#f0f0f0")
    layout_frame.pack(pady=5)

    layout = get_layout()

    tk.Label(layout_frame, text="Colunas:", bg="#f0f0f0").grid(row=0, column=0, padx=5, sticky="e")
    entry_columns = tk.Entry(layout_frame, width=6)
    entry_columns.insert(0, str(layout["columns"]))
    entry_columns.grid(row=0, column=1, padx=5)

    tk.Label(layout_frame, text="Linhas:", bg="#f0f0f0").grid(row=0, column=2, padx=5, sticky="e")
    entry_rows = tk.Entry(layout_frame, width=6)
    entry_rows.insert(0, str(layout["rows"]))
    entry_rows.grid(row=0, column=3, padx=5)

    layout_feedback = tk.Label(frame, text="", bg="#f0f0f0", fg="green")
    layout_feedback.pack()

    def save_layout():
        # Valida e salva as novas dimensões do grid
        cols = entry_columns.get().strip()
        rows = entry_rows.get().strip()
        if not cols.isdigit() or not rows.isdigit() or int(cols) < 1 or int(rows) < 1:
            layout_feedback.config(text="Valores inválidos.", fg="red")
            return
        set_layout(int(cols), int(rows))
        layout_feedback.config(text="Layout salvo!", fg="green")

    tk.Button(layout_frame, text="Salvar", command=save_layout).grid(row=0, column=4, padx=10)

    # --- Seções ---
    tk.Label(frame, text="Seções (A-Z)", font=("Arial", 13, "bold"), bg="#f0f0f0").pack(pady=(15, 5))

    sections_wrapper = tk.Frame(frame, bg="#f0f0f0")
    sections_wrapper.pack(anchor="center", pady=5)

    def refresh_sections():
        # Recarrega a tabela de seções com suas palavras-chave
        for w in sections_wrapper.winfo_children():
            w.destroy()
        sections = get_sections()
        for col, header in enumerate(["Seção", "Palavra-chave", "Ações"]):
            tk.Label(sections_wrapper, text=header, font=("Arial", 11, "bold"), bg="#d0d0d0", relief=tk.RIDGE, width=18).grid(row=0, column=col, padx=1, pady=1)
        for row_idx, (letter, keyword) in enumerate(sections, start=1):
            tk.Label(sections_wrapper, text=letter, bg="#f0f0f0", relief=tk.RIDGE, width=18).grid(row=row_idx, column=0, padx=1, pady=1)
            tk.Label(sections_wrapper, text=keyword or "-", bg="#f0f0f0", relief=tk.RIDGE, width=18).grid(row=row_idx, column=1, padx=1, pady=1)
            btn_frame = tk.Frame(sections_wrapper, bg="#f0f0f0", relief=tk.RIDGE)
            btn_frame.grid(row=row_idx, column=2, padx=1, pady=1)
            tk.Button(btn_frame, text="Editar", command=lambda l=letter, k=keyword: open_keyword_modal(l, k)).pack(side=tk.LEFT, padx=2)
            tk.Button(btn_frame, text="Apagar", fg="red", command=lambda l=letter: [delete_keyword(l), refresh_sections()]).pack(side=tk.LEFT, padx=2)

    def open_keyword_modal(letter, current_keyword):
        # Abre o modal para editar a palavra-chave de uma seção
        modal = tk.Toplevel(frame)
        modal.title(f"Seção {letter}")
        modal.resizable(False, False)
        modal.grab_set()
        x = frame.winfo_rootx() + frame.winfo_width() // 2 - 150
        y = frame.winfo_rooty() + frame.winfo_height() // 2 - 80
        modal.geometry(f"300x160+{x}+{y}")

        tk.Label(modal, text=f"Palavra-chave para seção {letter}:", font=("Arial", 11)).pack(pady=10)
        entry = tk.Entry(modal, width=25)
        entry.insert(0, current_keyword or "")
        entry.pack(pady=5)

        feedback = tk.Label(modal, text="", fg="red")
        feedback.pack()

        def submit():
            # Valida e salva a palavra-chave
            kw = entry.get().strip()
            if not kw:
                feedback.config(text="Digite uma palavra-chave.")
                return
            set_keyword(letter, kw)
            refresh_sections()
            modal.destroy()

        tk.Button(modal, text="Salvar", command=submit).pack(pady=5)

    refresh_sections()

    # --- Itens ---
    tk.Label(frame, text="Itens", font=("Arial", 13, "bold"), bg="#f0f0f0").pack(pady=(15, 5))

    top_bar = tk.Frame(frame, bg="#f0f0f0")
    top_bar.pack(anchor="center")
    tk.Button(top_bar, text="+ Novo Item", command=lambda: open_item_modal()).pack()

    items_wrapper = tk.Frame(frame, bg="#f0f0f0")
    items_wrapper.pack(anchor="center", pady=5)

    def refresh_items():
        # Recarrega a tabela de itens do depósito
        for w in items_wrapper.winfo_children():
            w.destroy()
        items = get_items()
        for col, header in enumerate(["ID", "Nome", "Descrição", "Seção", "Linha", "Qtd", "Ações"]):
            tk.Label(items_wrapper, text=header, font=("Arial", 11, "bold"), bg="#d0d0d0", relief=tk.RIDGE, width=14).grid(row=0, column=col, padx=1, pady=1)
        for row_idx, (iid, name, desc, section, row, qty) in enumerate(items, start=1):
            for col, val in enumerate([iid, name, desc or "-", section, row, qty]):
                tk.Label(items_wrapper, text=val, bg="#f0f0f0", relief=tk.RIDGE, width=14).grid(row=row_idx, column=col, padx=1, pady=1)
            btn_frame = tk.Frame(items_wrapper, bg="#f0f0f0", relief=tk.RIDGE)
            btn_frame.grid(row=row_idx, column=6, padx=1, pady=1)
            tk.Button(btn_frame, text="Editar", command=lambda i=(iid, name, desc, section, row, qty): open_item_modal(i)).pack(side=tk.LEFT, padx=2)
            tk.Button(btn_frame, text="Apagar", fg="red", command=lambda i=iid: [delete_item(i), refresh_items()]).pack(side=tk.LEFT, padx=2)

    def open_item_modal(item=None):
        # Abre o formulário para criar ou editar um item
        modal = tk.Toplevel(frame)
        modal.title("Novo Item" if not item else "Editar Item")
        modal.resizable(False, False)
        modal.grab_set()
        x = frame.winfo_rootx() + frame.winfo_width() // 2 - 160
        y = frame.winfo_rooty() + frame.winfo_height() // 2 - 130
        modal.geometry(f"320x280+{x}+{y}")

        tk.Label(modal, text="Novo Item" if not item else "Editar Item", font=("Arial", 13, "bold")).pack(pady=10)

        form = tk.Frame(modal)
        form.pack(pady=5)

        fields = [("Nome:", 0), ("Descrição:", 1), ("Seção (A-Z):", 2), ("Linha:", 3), ("Quantidade:", 4)]
        entries = []
        defaults = ["", "", "", "", "1"] if not item else [item[1], item[2] or "", item[3], str(item[4]), str(item[5])]

        for (label, row_idx), default in zip(fields, defaults):
            tk.Label(form, text=label).grid(row=row_idx, column=0, padx=5, pady=4, sticky="e")
            e = tk.Entry(form, width=22)
            e.insert(0, default)
            e.grid(row=row_idx, column=1, padx=5)
            entries.append(e)

        feedback = tk.Label(modal, text="", fg="red")
        feedback.pack()

        def submit():
            # Valida os campos e salva o item (criação ou atualização)
            name, desc, section, row, qty = [e.get().strip() for e in entries]
            if not name or not section or not row:
                feedback.config(text="Preencha os campos obrigatórios.")
                return
            if len(section) != 1 or not section.isalpha():
                feedback.config(text="Seção deve ser uma letra (A-Z).")
                return
            if not row.isdigit() or int(row) < 1:
                feedback.config(text="Linha deve ser um número positivo.")
                return
            if not qty.isdigit() or int(qty) < 1:
                feedback.config(text="Quantidade deve ser um número positivo.")
                return
            if item:
                update_item(item[0], name, desc, section, int(row), int(qty))
            else:
                create_item(name, desc, section, int(row), int(qty))
            refresh_items()
            modal.destroy()

        tk.Button(modal, text="Salvar", command=submit).pack(pady=8)

    refresh_items()
