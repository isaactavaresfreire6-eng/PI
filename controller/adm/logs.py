from model.logs import find_all, find_filtered, clear_all as _clear_all
from utils.log import CATEGORIAS

# Retorna todas as categorias disponíveis para filtro
def get_categorias():
    return CATEGORIAS

# Retorna logs com filtro opcional de categoria e busca
def get_logs(categoria=None, search=None):
    if not categoria and not search:
        return find_all()
    return find_filtered(categoria or None, search or None)

# Apaga todos os logs
def clear_logs():
    _clear_all()
