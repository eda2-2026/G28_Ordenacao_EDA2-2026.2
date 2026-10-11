# contrato comum dos algoritmos de ordenação
#
# todo algoritmo recebe (lista, chave), ordena a lista NO LUGAR
# (in-place) e devolve um objeto Estatisticas com as operações feitas.
# assim o benchmark trata qualquer método da mesma forma.
from dataclasses import dataclass

@dataclass
class Estatisticas:
    comparacoes: int = 0   # comparações entre chaves
    movimentacoes: int = 0 # escritas de elementos na lista (deslocamentos/trocas)
