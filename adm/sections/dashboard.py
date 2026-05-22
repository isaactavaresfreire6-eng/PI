import tkinter as tk
from controller.adm.dashboard import get_stats

# Exibe o painel com o total de usuários e admins cadastrados
def show(frame):
    total_users, total_admins = get_stats()

    tk.Label(frame, text="Painel", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=20)
    tk.Label(frame, text=f"Total de Usuários: {total_users}", font=("Arial", 14), bg="#f0f0f0").pack(pady=5)
    tk.Label(frame, text=f"Total de Admins: {total_admins}", font=("Arial", 14), bg="#f0f0f0").pack(pady=5)
