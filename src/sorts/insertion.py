# insertion sort (ordenação por inserção)
#
# ideia: a lista é dividida em uma parte já ordenada (à esquerda) e uma
# parte ainda não processada (à direita). a cada passo, pegamos o
# primeiro elemento não processado e o "inserimos" na posição correta
# da parte ordenada, deslocando uma casa para a direita todos os
# elementos maiores que ele — como quem organiza cartas na mão.
#
# complexidade:
# - melhor caso  O(n):  lista já ordenada. cada elemento é comparado só
#                       com o vizinho da esquerda e já está no lugar
#                       (n - 1 comparações, 0 deslocamentos).
# - caso médio   O(n²): lista aleatória. cada elemento anda, em média,
#                       metade da parte ordenada (~n²/4 comparações).
# - pior caso    O(n²): lista em ordem inversa. cada elemento anda até o
#                       início (~n²/2 comparações e deslocamentos).
#
# o custo é proporcional ao número de INVERSÕES da entrada (pares fora
# de ordem). por isso o insertion é excelente quando a lista está quase
# ordenada, mesmo sendo O(n²) no caso geral.
#
# propriedades: estável (não troca a ordem relativa de chaves iguais),
# in-place (memória extra O(1)) e online (ordena à medida que os dados
# chegam).
from typing import Any, Callable

from src.sorts.base import Estatisticas

def insertion_sort(lista: list, chave: Callable[[Any], Any] = lambda x: x) -> Estatisticas:
    comparacoes = 0
    movimentacoes = 0

    for i in range(1, len(lista)):
        atual = lista[i]
        chave_atual = chave(atual)
        j = i - 1

        # desloca para a direita os elementos MAIORES que o atual.
        # a condição é estritamente "maior": em caso de empate o laço
        # para, e o atual fica depois do igual -> algoritmo estável.
        while j >= 0:
            comparacoes += 1
            if chave(lista[j]) <= chave_atual:
                break
            lista[j + 1] = lista[j]
            movimentacoes += 1
            j -= 1

        # encaixa o elemento na posição que ficou livre
        if j + 1 != i:
            lista[j + 1] = atual
            movimentacoes += 1

    return Estatisticas(comparacoes, movimentacoes)
