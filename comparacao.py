# benchmark dos métodos de ordenação nos quatro cenários de entrada
#
# uso:
#   python comparacao.py               -> testa com 1.000, 2.500, 5.000 e 10.000
#   python comparacao.py 500 2000      -> testa com os tamanhos passados
#
# metodologia: para cada tamanho N é gerada UMA base de produtos. a partir
# dela montamos os quatro cenários (aleatório, já ordenado, quase ordenado
# e ordem inversa) e entregamos exatamente a mesma entrada a cada
# algoritmo, sempre em uma cópia nova (a ordenação é in-place).
#
# para cada execução medimos:
# - tempo (ms): mediana de REPETICOES execuções, para reduzir o ruído do SO
# - comparações e movimentações: contadas pelo próprio algoritmo; não
#   dependem da máquina, então mostram a complexidade "pura"
#
# após cada execução conferimos se a lista saiu de fato ordenada.
#
# por que não 100.000 como no trabalho de busca? os cenários O(n²) ficam
# inviáveis em python: o insertion na ordem inversa já leva ~7 s com
# 10.000 produtos, e com 100.000 levaria ~100x mais (mais de 10 minutos
# por execução).
import json
from pathlib import Path
import random
import statistics
import sys
import time

from src.cenarios import CENARIOS, NOMES_CENARIOS, chave_codigo, montar_cenario
from src.models import gerar_base_produtos
from src.sorts import ALGORITMOS

TAMANHOS_PADRAO = [1_000, 2_500, 5_000, 10_000]
REPETICOES = 3
ARQUIVO_RESULTADOS = Path(__file__).resolve().parent / "assets" / "ultimos_resultados.json"

def esta_ordenada(lista) -> bool:
    return all(chave_codigo(lista[i]) <= chave_codigo(lista[i + 1])
               for i in range(len(lista) - 1))

def medir(algoritmo, entrada) -> dict:
    esperado = sorted(entrada, key=chave_codigo)
    if REPETICOES < 1:
        raise ValueError("REPETICOES deve ser pelo menos 1")
    tempos = []
    estatisticas = None
    for _ in range(REPETICOES):
        copia = list(entrada)
        inicio = time.perf_counter()
        estatisticas = algoritmo(copia, chave_codigo)
        tempos.append((time.perf_counter() - inicio) * 1000)

        if copia != esperado:
            raise AssertionError("o algoritmo devolveu a lista fora de ordem")

    return {
        "tempo_ms": statistics.median(tempos),
        "comparacoes": estatisticas.comparacoes,
        "movimentacoes": estatisticas.movimentacoes,
    }

def algoritmos_disponiveis() -> dict:
    # um algoritmo ainda não implementado levanta NotImplementedError:
    # nesse caso ele fica de fora do benchmark
    disponiveis = {}
    for nome, algoritmo in ALGORITMOS.items():
        try:
            algoritmo([2, 1])
            disponiveis[nome] = algoritmo
        except NotImplementedError:
            print(f"Aviso: {nome} ainda não implementado — ficará de fora.")
    return disponiveis

def imprimir_tabela(resultados, algoritmo, campo, titulo, formato):
    print(f"\n{algoritmo} — {titulo}")
    print(f"{'N':>8} | " + " | ".join(f"{NOMES_CENARIOS[c]:>15}" for c in CENARIOS))
    print("-" * (11 + 18 * len(CENARIOS)))

    tamanhos = sorted({r["n"] for r in resultados})
    for n in tamanhos:
        linha = {r["cenario"]: r[campo] for r in resultados
                 if r["n"] == n and r["algoritmo"] == algoritmo}
        print(f"{n:>8} | " + " | ".join(f"{formato(linha[c]):>15}" for c in CENARIOS))

def main():
    tamanhos = [int(a) for a in sys.argv[1:]] or TAMANHOS_PADRAO
    if not tamanhos or any(n < 2 for n in tamanhos):
        raise SystemExit("Use tamanhos inteiros maiores ou iguais a 2.")
    tamanhos = sorted(set(tamanhos))
    random.seed(42)
    algoritmos = algoritmos_disponiveis()

    resultados = []
    for n in tamanhos:
        print(f"Gerando base de {n} produtos...")
        base = gerar_base_produtos(n)

        for cenario in CENARIOS:
            entrada = montar_cenario(base, cenario)

            for nome, algoritmo in algoritmos.items():
                print(f"  {nome:<15} {NOMES_CENARIOS[cenario]:<15}", end="", flush=True)
                medicao = medir(algoritmo, entrada)
                print(f"{medicao['tempo_ms']:>12.2f} ms")
                resultados.append({"n": n, "cenario": cenario, "algoritmo": nome, **medicao})

    for nome in algoritmos:
        imprimir_tabela(resultados, nome, "tempo_ms", "tempo (ms)",
                        lambda v: f"{v:.2f}")
        imprimir_tabela(resultados, nome, "comparacoes", "comparações",
                        lambda v: f"{v:,}".replace(",", "."))

    # salva os resultados em arquivo json para plot_results.py
    ARQUIVO_RESULTADOS.parent.mkdir(parents=True, exist_ok=True)
    with open(ARQUIVO_RESULTADOS, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)
    print(f"\nResultados salvos em '{ARQUIVO_RESULTADOS}'.")

if __name__ == "__main__":
    main()
