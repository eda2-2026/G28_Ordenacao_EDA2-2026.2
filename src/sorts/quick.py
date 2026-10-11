# quick sort com primeiro pivô e o contrato comum dos algoritmos.

from typing import Any, Callable

from src.sorts.base import Estatisticas


def _particionar(
    lista: list, inicio: int, fim: int, metricas: Estatisticas, chave: Callable[[Any], Any]
) -> int:
    pivo = chave(lista[inicio])
    limite = inicio
    for atual in range(inicio + 1, fim + 1):
        metricas.comparacoes += 1
        if chave(lista[atual]) < pivo:
            limite += 1
            if limite != atual:
                lista[limite], lista[atual] = lista[atual], lista[limite]
                metricas.movimentacoes += 2
    if inicio != limite:
        lista[inicio], lista[limite] = lista[limite], lista[inicio]
        metricas.movimentacoes += 2
    return limite


def quick_sort(lista: list, chave: Callable[[Any], Any] = lambda x: x) -> Estatisticas:
    # ordena a própria lista em ordem crescente, sem recursão python.

    # processa o menor lado imediatamente e guarda o maior na pilha.
    # o pivô continua sendo o primeiro elemento de cada intervalo.
    # conta apenas comparações entre chaves e 
    # escritas em posições da lista (duas por troca efetiva). 
    # o tempo deve ser medido pelo chamador.
    
    metricas = Estatisticas()
    inicio, fim = 0, len(lista) - 1
    pendentes = []
    while True:
        while inicio < fim:
            pivo = _particionar(lista, inicio, fim, metricas, chave)
            if pivo - inicio < fim - pivo:
                if pivo + 1 < fim:
                    pendentes.append((pivo + 1, fim))
                fim = pivo - 1
            else:
                if inicio < pivo - 1:
                    pendentes.append((inicio, pivo - 1))
                inicio = pivo + 1
        if not pendentes:
            break
        inicio, fim = pendentes.pop()
    return metricas
