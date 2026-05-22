from model.users import count as count_users
from model.admin import count as count_admins

def get_stats():
    # Retorna o total de usuários e admins para exibir no painel
    return count_users(), count_admins()
