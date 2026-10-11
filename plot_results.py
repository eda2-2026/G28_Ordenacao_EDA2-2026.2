# lê o json salvo pelo comparacao.py e gera os gráficos em assets/
#
# 1. insertion_tempo_cenarios.png  -> tempo x N do insertion nos 4 cenários
# 2. insertion_comparacoes.png     -> comparações medidas x curvas teóricas
# 3. quick_tempo_cenarios.png      -> tempo x N do quick nos 4 cenários
# 4. quick_comparacoes.png         -> comparações do quick x referências teóricas
# 5. comparacao_cenarios.png       -> barras por cenário no maior N, para
#                                     todos os algoritmos disponíveis
import json
from pathlib import Path
import math
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.cenarios import CENARIOS, NOMES_CENARIOS

PASTA_ASSETS = Path(__file__).resolve().parent / "assets"
ARQUIVO_DADOS = PASTA_ASSETS / "ultimos_resultados.json"

CORES_CENARIOS = {
    "aleatorio": "#3498db",
    "ordenado": "#2ecc71",
    "quase_ordenado": "#f1c40f",
    "inverso": "#e74c3c",
}

CORES_ALGORITMOS = ["#8e44ad", "#e67e22", "#16a085", "#2c3e50"]

def filtrar(resultados, algoritmo, cenario):
    linhas = sorted((r for r in resultados
                     if r["algoritmo"] == algoritmo and r["cenario"] == cenario),
                    key=lambda r: r["n"])
    return [r["n"] for r in linhas], linhas

def formatar_tempo(ms: float) -> str:
    return f"{ms / 1000:.2f} s" if ms >= 1000 else f"{ms:.2f} ms"

def grafico_tempo_insertion(resultados):
    plt.figure(figsize=(10, 6))
    for cenario in CENARIOS:
        N, linhas = filtrar(resultados, "Insertion Sort", cenario)
        plt.plot(N, [r["tempo_ms"] for r in linhas], marker="o", linewidth=2,
                 color=CORES_CENARIOS[cenario], label=NOMES_CENARIOS[cenario])

    plt.title("Insertion Sort: o mesmo algoritmo, quatro entradas diferentes",
              fontsize=13, fontweight="bold")
    plt.xlabel("Tamanho da Base (N)", fontsize=11)
    plt.ylabel("Tempo de Ordenação (ms) - Escala Log", fontsize=11)
    plt.yscale("log")
    plt.xticks(N, labels=[f"{n:,}".replace(",", ".") for n in N])
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(loc="upper left", frameon=True)
    plt.tight_layout()
    plt.savefig(PASTA_ASSETS / "insertion_tempo_cenarios.png", dpi=300)
    plt.close()
    print("-> Gráfico 'assets/insertion_tempo_cenarios.png' gerado!")

def grafico_comparacoes_insertion(resultados):
    plt.figure(figsize=(10, 6))
    for cenario in CENARIOS:
        N, linhas = filtrar(resultados, "Insertion Sort", cenario)
        # medições como pontos; as curvas teóricas passam por cima deles
        plt.scatter(N, [r["comparacoes"] for r in linhas], s=90, zorder=2,
                    color=CORES_CENARIOS[cenario], label=f"{NOMES_CENARIOS[cenario]} (medido)")

    # curvas teóricas: melhor caso n-1, caso médio ~n²/4, pior caso ~n²/2
    # (ver a derivação no README)
    N_curva = list(range(N[0], N[-1] + 1, max(1, (N[-1] - N[0]) // 100)))
    plt.plot(N_curva, [n - 1 for n in N_curva], ls="--", color="#1e8449", zorder=3,
             label="Teórico melhor caso: n − 1")
    # quase ordenado: lote de n/100 itens novos, cada um anda ~n/2 casas
    plt.plot(N_curva, [n * n / 200 for n in N_curva], ls="--", color="#b7950b", zorder=3,
             label="Teórico quase ordenado: n²/200")
    plt.plot(N_curva, [n * n / 4 for n in N_curva], ls="--", color="#1f618d", zorder=3,
             label="Teórico caso médio: n²/4")
    plt.plot(N_curva, [n * n / 2 for n in N_curva], ls="--", color="#922b21", zorder=3,
             label="Teórico pior caso: n²/2")

    plt.title("Insertion Sort: comparações medidas x análise assintótica",
              fontsize=13, fontweight="bold")
    plt.xlabel("Tamanho da Base (N)", fontsize=11)
    plt.ylabel("Número de Comparações - Escala Log", fontsize=11)
    plt.yscale("log")
    plt.xticks(N, labels=[f"{n:,}".replace(",", ".") for n in N])
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(loc="upper left", frameon=True, fontsize=9)
    plt.tight_layout()
    plt.savefig(PASTA_ASSETS / "insertion_comparacoes.png", dpi=300)
    plt.close()
    print("-> Gráfico 'assets/insertion_comparacoes.png' gerado!")

def grafico_tempo_quick(resultados):
    plt.figure(figsize=(10, 6))
    for cenario in CENARIOS:
        N, linhas = filtrar(resultados, "Quick Sort", cenario)
        plt.plot(N, [r["tempo_ms"] for r in linhas], marker="o", linewidth=2,
                 color=CORES_CENARIOS[cenario], label=NOMES_CENARIOS[cenario])

    plt.title("Quick Sort: o mesmo algoritmo, quatro entradas diferentes",
              fontsize=13, fontweight="bold")
    plt.xlabel("Tamanho da Base (N)", fontsize=11)
    plt.ylabel("Tempo de Ordenação (ms) - Escala Log", fontsize=11)
    plt.yscale("log")
    plt.xticks(N, labels=[f"{n:,}".replace(",", ".") for n in N])
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(loc="upper left", frameon=True)
    plt.tight_layout()
    plt.savefig(PASTA_ASSETS / "quick_tempo_cenarios.png", dpi=300)
    plt.close()
    print("-> Gráfico 'assets/quick_tempo_cenarios.png' gerado!")

def grafico_comparacoes_quick(resultados):
    plt.figure(figsize=(10, 6))
    for cenario in CENARIOS:
        N, linhas = filtrar(resultados, "Quick Sort", cenario)
        plt.scatter(N, [r["comparacoes"] for r in linhas], s=90, zorder=2,
                    color=CORES_CENARIOS[cenario], label=f"{NOMES_CENARIOS[cenario]} (medido)")

    N_curva = list(range(N[0], N[-1] + 1, max(1, (N[-1] - N[0]) // 100)))
    # referência de crescimento, não uma previsão exata das contagens
    plt.plot(N_curva, [2 * n * math.log(n) for n in N_curva], ls="--",
             color="#1f618d", label="Referência caso médio: 2n ln(n)")
    plt.plot(N_curva, [n * (n - 1) / 2 for n in N_curva], ls="--",
             color="#922b21", label="Pior caso exato: n(n − 1)/2")
    plt.title("Quick Sort: comparações medidas x análise assintótica",
              fontsize=13, fontweight="bold")
    plt.xlabel("Tamanho da Base (N)", fontsize=11)
    plt.ylabel("Número de Comparações - Escala Log", fontsize=11)
    plt.yscale("log")
    plt.xticks(N, labels=[f"{n:,}".replace(",", ".") for n in N])
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(loc="upper left", frameon=True, fontsize=9)
    plt.tight_layout()
    plt.savefig(PASTA_ASSETS / "quick_comparacoes.png", dpi=300)
    plt.close()
    print("-> Gráfico 'assets/quick_comparacoes.png' gerado!")

def grafico_barras_cenarios(resultados):
    maior_n = max(r["n"] for r in resultados)
    algoritmos = list(dict.fromkeys(r["algoritmo"] for r in resultados))
    largura = 0.8 / len(algoritmos)

    plt.figure(figsize=(10, 6))
    for i, algoritmo in enumerate(algoritmos):
        tempos = []
        for cenario in CENARIOS:
            linha = next(r for r in resultados if r["n"] == maior_n
                         and r["algoritmo"] == algoritmo and r["cenario"] == cenario)
            tempos.append(linha["tempo_ms"])

        posicoes = [c + (i - (len(algoritmos) - 1) / 2) * largura
                    for c in range(len(CENARIOS))]
        barras = plt.bar(posicoes, tempos, width=largura, label=algoritmo,
                         color=CORES_ALGORITMOS[i % len(CORES_ALGORITMOS)])
        for barra, tempo in zip(barras, tempos):
            plt.text(barra.get_x() + barra.get_width() / 2, tempo * 1.15,
                     formatar_tempo(tempo), ha="center", va="bottom", fontsize=9)

    titulo = " x ".join(algoritmos)
    plt.title(f"{titulo}: tempo por cenário (N = {maior_n:,})".replace(",", "."),
              fontsize=13, fontweight="bold")
    plt.ylabel("Tempo de Ordenação (ms) - Escala Log", fontsize=11)
    plt.yscale("log")
    plt.ylim(top=plt.ylim()[1] * 5) # espaço para os rótulos
    plt.xticks(range(len(CENARIOS)), [NOMES_CENARIOS[c] for c in CENARIOS])
    plt.grid(True, axis="y", which="both", ls="--", alpha=0.5)
    plt.legend(loc="upper left", frameon=True)
    plt.tight_layout()
    plt.savefig(PASTA_ASSETS / "comparacao_cenarios.png", dpi=300)
    plt.close()
    print("-> Gráfico 'assets/comparacao_cenarios.png' gerado!")

def main():
    if not ARQUIVO_DADOS.exists():
        print(f"Erro: Arquivo '{ARQUIVO_DADOS}' não encontrado.")
        print("Execute primeiro o script de benchmark: python comparacao.py")
        sys.exit(1)

    # lê exatamente os dados salvos pelo comparacao.py
    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
        resultados = json.load(f)

    print(f"Carregando dados da última execução de '{ARQUIVO_DADOS}'...")

    if any(r["algoritmo"] == "Insertion Sort" for r in resultados):
        grafico_tempo_insertion(resultados)
        grafico_comparacoes_insertion(resultados)
    if any(r["algoritmo"] == "Quick Sort" for r in resultados):
        grafico_tempo_quick(resultados)
        grafico_comparacoes_quick(resultados)
    grafico_barras_cenarios(resultados)

if __name__ == "__main__":
    main()
