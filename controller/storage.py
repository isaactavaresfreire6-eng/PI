from model.storage import (
    get_layout as _get_layout, set_layout as _set_layout,
    get_sections as _get_sections, set_keyword as _set_keyword, clear_keyword,
    get_items as _get_items, get_items_at as _get_items_at,
    insert_item, update_item as _update_item, delete_item as _delete_item,
    search_items as _search_items
)
from utils.log import log

# Retorna o layout do depósito como dicionário
def get_layout():
    row = _get_layout()
    return {"columns": row[0], "rows": row[1]}

# Atualiza as dimensões do grid
def set_layout(columns, rows):
    _set_layout(columns, rows)
    log("layout", f"Layout alterado para {columns} colunas e {rows} linhas")

# Retorna todas as seções com suas palavras-chave
def get_sections():
    return _get_sections()

# Define a palavra-chave de uma seção
def set_keyword(letter, keyword):
    _set_keyword(letter, keyword)
    log("layout", f"Palavra-chave da seção '{letter}' definida como '{keyword}'")

# Remove a palavra-chave de uma seção
def delete_keyword(letter):
    clear_keyword(letter)
    log("layout", f"Palavra-chave da seção '{letter}' removida")

# Retorna todos os itens do depósito
def get_items():
    return _get_items()

# Retorna os itens de uma posição específica
def get_items_at(section, row):
    return _get_items_at(section, row)

# Cria um novo item no depósito
def create_item(name, description, section, row, quantity=1):
    insert_item(name, description, section, row, quantity)
    log("depósito", f"Item '{name}' criado em {section}{row} (qtd: {quantity})")

# Atualiza um item existente
def update_item(item_id, name, description, section, row, quantity=1):
    _update_item(item_id, name, description, section, row, quantity)
    log("depósito", f"Item '{name}' (ID {item_id}) atualizado em {section}{row} (qtd: {quantity})")

# Remove um item pelo ID
def delete_item(item_id):
    _delete_item(item_id)
    log("depósito", f"Item ID {item_id} removido")

# Busca itens por nome ou descrição
def search_items(query):
    return _search_items(query)
