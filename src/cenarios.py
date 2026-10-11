# cenários de entrada: a MESMA base de produtos chega ao algoritmo
# em quatro "formatos" diferentes. é aqui que a escolha do método de
# ordenação faz diferença — o mesmo algoritmo pode ser o mais rápido
# num cenário e o mais lento em outro.
#
# - aleatorio:      carga nova de produtos, sem ordem nenhuma
# - ordenado:       estoque que já está ordenado por código
# - quase_ordenado: estoque ordenado + um lote pequeno (1%) de produtos
#                   novos cadastrados no fim (reposição do dia a dia)
# - inverso:        lista em ordem decrescente de código
from src.models import Produto

CENARIOS = ["aleatorio", "ordenado", "quase_ordenado", "inverso"]

NOMES_CENARIOS = {
    "aleatorio": "Aleatório",
    "ordenado": "Já ordenado",
    "quase_ordenado": "Quase ordenado",
    "inverso": "Ordem inversa",
}

PROPORCAO_LOTE_NOVO = 0.01

def chave_codigo(p: Produto) -> int:
    return p.codigo

def montar_cenario(produtos: list[Produto], cenario: str) -> list[Produto]:
    # devolve uma NOVA lista (a base original não é alterada)
    if cenario == "aleatorio":
        return list(produtos)

    if cenario == "ordenado":
        return sorted(produtos, key=chave_codigo)

    if cenario == "inverso":
        return sorted(produtos, key=chave_codigo, reverse=True)

    if cenario == "quase_ordenado":
        # os primeiros 99% formam o estoque já ordenado; o 1% restante
        # é o lote novo, que chega fora de ordem no final da lista
        tamanho_lote = max(1, int(len(produtos) * PROPORCAO_LOTE_NOVO))
        estoque = sorted(produtos[:-tamanho_lote], key=chave_codigo)
        return estoque + produtos[-tamanho_lote:]

    raise ValueError(f"cenário desconhecido: {cenario}")
