# experimentos reproduzíveis: python comparacao.py (gera um CSV e quatro gráficos de tempo)
import csv
import random
import statistics
from pathlib import Path
from time import perf_counter

from src.cenarios import CENARIOS, NOMES_CENARIOS, chave_codigo, montar_cenario
from src.models import gerar_base_produtos
from src.sorts import ALGORITMOS


def executar(tamanhos, repeticoes, semente):
    registros = []
    estado = random.getstate()
    try:
        for n in tamanhos:
            for repeticao in range(1, repeticoes + 1):
                # nova base por repetição, compartilhada por cenários e métodos
                random.seed(semente + n * 1000 + repeticao)
                base = gerar_base_produtos(n)
                esperado = sorted(base, key=chave_codigo)
                for cenario in CENARIOS:
                    entrada = montar_cenario(base, cenario)
                    algoritmos = list(ALGORITMOS.items())
                    if repeticao % 2 == 0:
                        algoritmos.reverse()
                    for nome, algoritmo in algoritmos:
                        lista = entrada.copy()
                        inicio = perf_counter()
                        e = algoritmo(lista, chave_codigo)
                        tempo = perf_counter() - inicio
                        if lista != esperado:
                            raise RuntimeError(f"Resultado incorreto: {nome}, {cenario}, N={n}")
                        registros.append(dict(n=n, cenario=cenario, algoritmo=nome,
                                              repeticao=repeticao, tempo_segundos=tempo,
                                              comparacoes=e.comparacoes, movimentacoes=e.movimentacoes))
                print(f"N={n}: repetição {repeticao}/{repeticoes} concluída", flush=True)
    finally:
        random.setstate(estado)
    return registros


def resumir(registros):
    grupos = {}
    for r in registros:
        grupos.setdefault((r['n'], r['cenario'], r['algoritmo']), []).append(r)
    return [dict(n=n, cenario=cenario, algoritmo=algoritmo,
                 **{campo: statistics.median(r[campo] for r in linhas)
                    for campo in ('tempo_segundos', 'comparacoes', 'movimentacoes')})
            for (n, cenario, algoritmo), linhas in grupos.items()]


def salvar_csv(caminho, linhas):
    with caminho.open('w', newline='', encoding='utf-8') as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=list(linhas[0]))
        writer.writeheader()
        writer.writerows(linhas)


def gerar_graficos(resumo, pasta):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    pasta.mkdir(parents=True, exist_ok=True)
    cores = {'Insertion Sort': '#2563eb', 'Quick Sort': '#d97706'}
    for cenario in CENARIOS:
        fig, ax = plt.subplots(figsize=(8, 4.8), layout='constrained')
        for nome in ALGORITMOS:
            linhas = sorted((r for r in resumo if r['cenario'] == cenario
                             and r['algoritmo'] == nome), key=lambda r: r['n'])
            ax.plot([r['n'] for r in linhas], [r['tempo_segundos'] for r in linhas],
                    marker='o', label=nome, color=cores.get(nome), linewidth=2)
        ax.set(title=f"Ordenação — {NOMES_CENARIOS[cenario]}",
               xlabel='Quantidade de produtos (N)', ylabel='Tempo mediano (segundos)')
        ax.set_ylim(bottom=0)
        ax.set_xticks(sorted({r['n'] for r in resumo}))
        ax.grid(alpha=0.25)
        ax.legend()
        fig.savefig(pasta / f'tempo_{cenario}.png', dpi=160)
        plt.close(fig)


# altere estas constantes se quiser uma execução menor para experimentar
TAMANHOS = [1000, 2500, 5000, 10000]
REPETICOES = 3
SEMENTE = 42


def main():
    pasta = Path(__file__).parent / 'resultados'
    pasta.mkdir(exist_ok=True)
    registros = executar(TAMANHOS, REPETICOES, SEMENTE)
    resumo = resumir(registros)
    salvar_csv(pasta / 'resumo.csv', resumo)
    gerar_graficos(resumo, pasta / 'graficos')
    print(f"CSV e gráficos salvos em {pasta.resolve()}")


if __name__ == '__main__':
    main()
