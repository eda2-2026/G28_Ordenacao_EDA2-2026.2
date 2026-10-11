# modelo do produto e gerador de dados
import random
from dataclasses import dataclass

CATEGORIAS = ["Medicamentos", "Higiene", "Perfumaria", "Dermocosméticos", "Infantil"]

@dataclass
class Produto:
    codigo: int # chave única (código de barras / sku)
    nome: str
    categoria: str
    preco: float
    quantidade: int

def gerar_base_produtos(n: int) -> list[Produto]:
    # gera uma lista com N produtos aleatórios na memória

    # gera N códigos únicos aleatórios
    codigos = random.sample(range(100_000, 1_000_000 + n * 10), n)
    produtos = []

    for i, cod in enumerate(codigos):
        p = Produto(
            codigo=cod,
            nome=f"Produto_{i + 1}",
            categoria=random.choice(CATEGORIAS),
            preco=round(random.uniform(2.0, 150.0), 2),
            quantidade=random.randint(1, 500)
        )
        produtos.append(p)

    return produtos
