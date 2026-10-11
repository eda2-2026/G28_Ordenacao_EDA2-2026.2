# testes de corretude dos algoritmos de ordenação
#
# uso: python testes.py
#
# os testes rodam para todos os algoritmos registrados em src/sorts;
# os que ainda levantam NotImplementedError são pulados.
import random
import unittest

from src.cenarios import CENARIOS, chave_codigo, montar_cenario
from src.models import gerar_base_produtos
from src.sorts import ALGORITMOS

class TestesOrdenacao(unittest.TestCase):

    def para_cada_algoritmo(self, teste):
        for nome, algoritmo in ALGORITMOS.items():
            with self.subTest(algoritmo=nome):
                try:
                    teste(algoritmo)
                except NotImplementedError:
                    self.skipTest(f"{nome} ainda não implementado")

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
        pares = [(random.randint(0, 5), i) for i in range(200)]
        algoritmo = ALGORITMOS["Insertion Sort"]
        algoritmo(pares, lambda par: par[0])
        self.assertEqual(pares, sorted(pares, key=lambda par: par[0]))

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

if __name__ == "__main__":
    unittest.main(verbosity=2)
