# api.py
from fastapi import FastAPI
from typing import Optional  # Importante para parâmetros opcionais
import random

app = FastAPI()

# Vamos expandir nossa base de dados simulada para ter categorias
DADOS_MOCK = [
    {"produto": "Notebook", "categoria": "Eletronicos", "preco": 3500},
    {"produto": "Mouse", "categoria": "Acessorios", "preco": 50},
    {"produto": "Teclado", "categoria": "Acessorios", "preco": 120},
    {"produto": "Monitor", "categoria": "Eletronicos", "preco": 1200},
    {"produto": "Cadeira Gamer", "categoria": "Moveis", "preco": 800},
    {"produto": "Mesa Escritorio", "categoria": "Moveis", "preco": 600},
]


@app.get("/vendas")
# O FastAPI entende que 'categoria' não faz parte da rota, então é um Query Param (?categoria=...)
def ler_vendas(categoria: Optional[str] = None):
    # Filtra os dados se uma categoria for passada
    if categoria:
        # List comprehension para filtrar
        resultado = [item for item in DADOS_MOCK if item["categoria"] == categoria]
    else:
        resultado = DADOS_MOCK

    # Adiciona dados aleatórios de venda para cada item filtrado
    resposta_final = []
    for item in resultado:
        resposta_final.append({
            "produto": item["produto"],
            "categoria": item["categoria"],
            "preco": item["preco"],
            "quantidade_vendida": random.randint(1, 20)  # Simula venda
        })

    return resposta_final