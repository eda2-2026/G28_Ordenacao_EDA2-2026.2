from time import perf_counter
from src.models import Produto
from src.sorts import quick_sort

# demonstração do insertion sort no estoque da drogaria
#
# 1. ordena uma base pequena por código e mostra o antes/depois
# 2. mostra a estabilidade: ordenar por preço e depois por categoria
#    mantém os produtos de cada categoria em ordem de preço
# 3. mostra que o custo depende da forma como a entrada chega
from src.cenarios import CENARIOS, NOMES_CENARIOS, chave_codigo, montar_cenario
from src.models import gerar_base_produtos
from src.sorts import insertion_sort

def imprimir_produtos(produtos):
    print(f"  {'Código':>8} | {'Nome':<12} | {'Categoria':<16} | {'Preço':>9}")
    for p in produtos:
        print(f"  {p.codigo:>8} | {p.nome:<12} | {p.categoria:<16} | R$ {p.preco:>6.2f}")

def demo_ordenacao_por_codigo():
    print("=== 1. Ordenação por código ===")
    produtos = gerar_base_produtos(8)

    print("\nAntes:")
    imprimir_produtos(produtos)

    estatisticas = insertion_sort(produtos, chave_codigo)

    print("\nDepois:")
    imprimir_produtos(produtos)
    print(f"\n  {estatisticas.comparacoes} comparações, "
          f"{estatisticas.movimentacoes} movimentações")

def demo_estabilidade():
    print("\n=== 2. Estabilidade: preço e depois categoria ===")
    produtos = gerar_base_produtos(10)

    # primeiro por preço, depois por categoria: como o insertion é estável,
    # dentro de cada categoria os produtos continuam em ordem de preço
    insertion_sort(produtos, lambda p: p.preco)
    insertion_sort(produtos, lambda p: p.categoria)

    print("\nRelatório por categoria (preço crescente dentro de cada uma):")
    imprimir_produtos(produtos)

def demo_cenarios():
    n = 2_000
    print(f"\n=== 3. Mesmo algoritmo, entradas diferentes (N = {n}) ===\n")
    base = gerar_base_produtos(n)

    print(f"  {'Cenário':<15} | {'Comparações':>12} | {'Movimentações':>13}")
    print("  " + "-" * 46)
    for cenario in CENARIOS:
        entrada = montar_cenario(base, cenario)
        e = insertion_sort(entrada, chave_codigo)
        print(f"  {NOMES_CENARIOS[cenario]:<15} | {e.comparacoes:>12,} | "
              f"{e.movimentacoes:>13,}".replace(",", "."))


# demonstrações adicionais do quick sort e comparação dos dois métodos
def demo_quick_por_codigo():
    print("\n=== 4. Quick Sort: ordenação por código ===")
    produtos = gerar_base_produtos(8)
    print("\nAntes:")
    imprimir_produtos(produtos)
    estatisticas = quick_sort(produtos, chave_codigo)
    print("\nDepois:")
    imprimir_produtos(produtos)
    print(f"\n  {estatisticas.comparacoes} comparações, "
          f"{estatisticas.movimentacoes} movimentações")


def demo_quick_nao_estavel():
    print("\n=== 5. Quick Sort: exemplo de instabilidade ===")
    # preços já crescentes. B e C pertencem à mesma categoria
    base = [
        Produto(1, "Produto_A", "Higiene", 10.0, 1),
        Produto(2, "Produto_B", "Dermocosméticos", 20.0, 1),
        Produto(3, "Produto_C", "Dermocosméticos", 30.0, 1),
    ]
    print("\nEntrada já ordenada por preço:")
    imprimir_produtos(base)
    for nome, algoritmo in (("Insertion Sort", insertion_sort), ("Quick Sort", quick_sort)):
        lista = base.copy()
        algoritmo(lista, lambda p: p.categoria)
        print(f"\n{nome}: depois de ordenar por categoria:")
        imprimir_produtos(lista)
    print("\nNo Quick Sort, C fica antes de B: a ordem de preço em Dermocosméticos se perde.")
    print("Isso demonstra que Quick Sort não garante estabilidade.")


def demo_comparacao():
    n = 2_000
    print(f"\n=== 6. Comparação dos dois algoritmos (N = {n}) ===\n")
    base = gerar_base_produtos(n)
    esperado = sorted(base, key=chave_codigo)
    print(f"  {'Cenário':<15} | {'Algoritmo':<14} | {'Tempo (s)':>10} | "
          f"{'Comparações':>12} | {'Movimentações':>13}")
    print("  " + "-" * 76)
    for cenario in CENARIOS:
        entrada = montar_cenario(base, cenario)
        for nome, algoritmo in (("Insertion Sort", insertion_sort), ("Quick Sort", quick_sort)):
            # cada método recebe uma cópia da mesma entrada ainda não ordenada
            lista = entrada.copy()
            inicio = perf_counter()
            estatisticas = algoritmo(lista, chave_codigo)
            tempo = perf_counter() - inicio
            assert lista == esperado, f"Falha na ordenação: {nome}, {cenario}"
            print(f"  {NOMES_CENARIOS[cenario]:<15} | {nome:<14} | {tempo:>10.6f} | "
                  f"{estatisticas.comparacoes:>12} | {estatisticas.movimentacoes:>13}")
    print("\nTempos de uma execução; podem variar conforme o computador.")


if __name__ == "__main__":
    demo_ordenacao_por_codigo()
    demo_estabilidade()
    demo_cenarios()
    demo_quick_por_codigo()
    demo_quick_nao_estavel()
    demo_comparacao()
