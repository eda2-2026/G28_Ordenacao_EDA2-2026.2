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

if __name__ == "__main__":
    demo_ordenacao_por_codigo()
    demo_estabilidade()
    demo_cenarios()
