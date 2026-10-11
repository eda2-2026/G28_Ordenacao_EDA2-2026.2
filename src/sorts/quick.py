# quick sort — implementação a cargo da dupla
#
# contrato (o mesmo do insertion_sort, ver src/sorts/base.py):
# - recebe (lista, chave) e ordena a lista NO LUGAR
# - devolve Estatisticas(comparacoes, movimentacoes)
#
# sugestão combinada: pivô = PRIMEIRO elemento, para expor a degradação
# para O(n²) nos cenários ordenado / quase ordenado / inverso.
# atenção: em entrada ordenada a recursão chega a profundidade n, o que
# estoura o limite padrão do python (~1000). usar pilha explícita
# (versão iterativa) ou sys.setrecursionlimit.
#
# enquanto esta função levantar NotImplementedError, o comparacao.py
# simplesmente pula o quick sort e roda só o insertion.
from typing import Any, Callable

from src.sorts.base import Estatisticas

def quick_sort(lista: list, chave: Callable[[Any], Any] = lambda x: x) -> Estatisticas:
    raise NotImplementedError("quick sort ainda não implementado")
