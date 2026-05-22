from utils.db import query_all, query_one, execute

# --- Layout do depósito ---

# Retorna as dimensões atuais do grid (colunas e linhas)
def get_layout():
    return query_one("SELECT columns, rows FROM storage_layout WHERE id = 1")

# Atualiza as dimensões do grid
def set_layout(columns, rows):
    execute("UPDATE storage_layout SET columns = ?, rows = ? WHERE id = 1", (columns, rows))

# --- Seções (colunas A-Z) ---

# Retorna todas as seções com suas palavras-chave
def get_sections():
    return query_all("SELECT letter, keyword FROM storage_sections ORDER BY letter ASC")

# Define a palavra-chave de uma seção
def set_keyword(letter, keyword):
    execute("UPDATE storage_sections SET keyword = ? WHERE letter = ?", (keyword or None, letter))

# Remove a palavra-chave de uma seção
def clear_keyword(letter):
    execute("UPDATE storage_sections SET keyword = NULL WHERE letter = ?", (letter,))

# --- Itens ---

# Retorna todos os itens ordenados por seção e linha
def get_items():
    return query_all("SELECT id, name, description, section, row, quantity FROM storage_items ORDER BY section, row")

# Retorna os itens de uma posição específica (seção + linha)
def get_items_at(section, row):
    return query_all("SELECT id, name, description, quantity FROM storage_items WHERE section = ? AND row = ?", (section, row))

# Insere um novo item no depósito
def insert_item(name, description, section, row, quantity):
    execute(
        "INSERT INTO storage_items (name, description, section, row, quantity) VALUES (?, ?, ?, ?, ?)",
        (name, description or None, section.upper(), row, quantity)
    )

# Atualiza os dados de um item existente
def update_item(item_id, name, description, section, row, quantity):
    execute(
        "UPDATE storage_items SET name=?, description=?, section=?, row=?, quantity=? WHERE id=?",
        (name, description or None, section.upper(), row, quantity, item_id)
    )

# Remove um item pelo ID
def delete_item(item_id):
    execute("DELETE FROM storage_items WHERE id = ?", (item_id,))

# Busca itens por nome ou descrição, retornando também a palavra-chave da seção
def search_items(query):
    q = f"%{query}%"
    return query_all("""
        SELECT i.name, i.section, i.row, s.keyword
        FROM storage_items i
        LEFT JOIN storage_sections s ON i.section = s.letter
        WHERE i.name LIKE ? OR i.description LIKE ?
        ORDER BY i.section, i.row
    """, (q, q))
