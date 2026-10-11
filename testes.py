# testes de corretude dos algoritmos de ordenação
#
# uso: python testes.py
#
# os testes rodam para todos os algoritmos registrados em src/sorts;
# todos os algoritmos registrados devem estar implementados.
import random
import unittest

from src.cenarios import CENARIOS, chave_codigo, montar_cenario
from src.models import gerar_base_produtos
from src.sorts import ALGORITMOS

class TestesOrdenacao(unittest.TestCase):

    def setUp(self):
        estado = random.getstate()
        self.addCleanup(random.setstate, estado)
        random.seed(42)

    def para_cada_algoritmo(self, teste):
        for nome, algoritmo in ALGORITMOS.items():
            with self.subTest(algoritmo=nome):
                teste(algoritmo)

    def test_listas_triviais(self):
        def teste(algoritmo):
            for lista in ([], [7], [1, 2], [2, 1]):
                copia = list(lista)
                algoritmo(copia)
                self.assertEqual(copia, sorted(lista))
        self.para_cada_algoritmo(teste)

    def test_inteiros_aleatorios_com_repeticao(self):
        def teste(algoritmo):
            for _ in range(50):
                lista = [random.randint(0, 20) for _ in range(random.randint(0, 60))]
                copia = list(lista)
                algoritmo(copia)
                self.assertEqual(copia, sorted(lista))
        self.para_cada_algoritmo(teste)

    def test_produtos_em_todos_os_cenarios(self):
        base = gerar_base_produtos(500)
        esperado = sorted(base, key=chave_codigo)

        def teste(algoritmo):
            for cenario in CENARIOS:
                entrada = montar_cenario(base, cenario)
                algoritmo(entrada, chave_codigo)
                self.assertEqual(entrada, esperado, cenario)
        self.para_cada_algoritmo(teste)

class TestesInsertion(unittest.TestCase):

    def test_estavel(self):
        # chaves repetidas: a ordem original entre iguais deve ser mantida
        rng = random.Random(42)
        pares = [(rng.randint(0, 5), i) for i in range(200)]
        algoritmo = ALGORITMOS["Insertion Sort"]
        esperado = sorted(pares, key=lambda par: par[0])
        algoritmo(pares, lambda par: par[0])
        self.assertEqual(pares, esperado)

    def test_contagem_melhor_caso(self):
        # lista já ordenada: n-1 comparações e nenhuma movimentação -> O(n)
        lista = list(range(1_000))
        e = ALGORITMOS["Insertion Sort"](lista)
        self.assertEqual(e.comparacoes, 999)
        self.assertEqual(e.movimentacoes, 0)

    def test_contagem_pior_caso(self):
        # ordem inversa: n(n-1)/2 comparações -> O(n²)
        n = 1_000
        lista = list(range(n, 0, -1))
        e = ALGORITMOS["Insertion Sort"](lista)
        self.assertEqual(e.comparacoes, n * (n - 1) // 2)

class TestesQuick(unittest.TestCase):
    def test_contagens(self):
        # verifica a ordenação e as contagens exatas em listas pequenas:
        # vazia, unitária, ordenada, desordenada e com valores repetidos
        for entrada, comparacoes, movimentacoes in (
            ([], 0, 0), ([1], 0, 0), ([1, 2, 3], 3, 0),
            ([2, 1], 1, 2), ([2, 3, 1], 2, 4), ([3, 3, 3], 3, 0)
        ):
            # identifica qual entrada falhou sem interromper os outros casos
            with self.subTest(entrada=entrada):
                lista = entrada.copy()
                e = ALGORITMOS["Quick Sort"](lista)
                self.assertEqual(lista, sorted(entrada))
                self.assertEqual(e.comparacoes, comparacoes)
                self.assertEqual(e.movimentacoes, movimentacoes)

    def test_dez_mil_ordenados(self):
        # confirma que a pilha explícita permite processar 10.000 elementos
        n = 10000
        lista = list(range(n))
        e = ALGORITMOS["Quick Sort"](lista)
        self.assertEqual(lista, list(range(n)))
        self.assertEqual(e.comparacoes, n * (n - 1) // 2)
        # com o primeiro elemento como pivô, a entrada crescente gera
        # o pior caso: (n-1) + (n-2) + ... + 1 comparações
        self.assertEqual(e.movimentacoes, 0)

    def test_exemplo_nao_estavel(self):
        lista = [(2, "X"), (1, "A"), (1, "B")]
        # compara somente o primeiro valor de cada tupla
        ALGORITMOS["Quick Sort"](lista, lambda item: item[0])
        self.assertEqual(lista, [(1, "B"), (1, "A"), (2, "X")])


if __name__ == "__main__":
    unittest.main(verbosity=2)
