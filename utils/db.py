import sqlite3
import os
import re

# Caminho para o banco de dados SQLite
db_path = os.path.join(os.path.dirname(__file__), "../model/database.db")


def get_connection():
    # Retorna uma nova conexão com o banco de dados
    return sqlite3.connect(db_path)


def _sanitize(value):
    # Bloqueia valores com padrões perigosos de SQL injection
    if isinstance(value, str):
        if re.search(r"(--|;|/\*|\*/|xp_)", value, re.IGNORECASE):
            raise ValueError(f"Potentially unsafe value detected: {value!r}")
    return value


def _sanitize_params(params):
    # Sanitiza todos os parâmetros antes de enviar ao banco
    return tuple(_sanitize(p) for p in params)


def query_all(sql, params=()):
    # Executa uma consulta e retorna todas as linhas
    with get_connection() as conn:
        with conn:
            cursor = conn.execute(sql, _sanitize_params(params))
            return cursor.fetchall()


def query_one(sql, params=()):
    # Executa uma consulta e retorna apenas a primeira linha
    with get_connection() as conn:
        with conn:
            cursor = conn.execute(sql, _sanitize_params(params))
            return cursor.fetchone()


def execute(sql, params=()):
    # Executa um comando SQL sem retorno (INSERT, UPDATE, DELETE)
    with get_connection() as conn:
        with conn:
            conn.execute(sql, _sanitize_params(params))
