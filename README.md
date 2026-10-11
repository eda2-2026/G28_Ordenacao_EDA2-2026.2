# Ordenação no Estoque

Projeto prático desenvolvido para a disciplina de **Estrutura de Dados II**. O sistema simula o estoque de uma rede de drogarias para avaliar, na prática e na teoria, como diferentes **métodos de ordenação** se comportam conforme a forma em que os dados chegam.

## Cenário

Nosso cliente é o dono de uma **rede de drogarias com várias filiais** (o mesmo do [trabalho de busca](https://github.com/eda2-2026/G28_Busca_EDA2-2026.2)). No trabalho anterior mostramos que a busca binária é centenas de vezes mais rápida que a sequencial — **mas ela exige o cadastro ordenado**. A pergunta agora é: *qual método usar para manter o estoque ordenado por código?*

A resposta não é única. Os dados chegam de formas muito diferentes no dia a dia:

| Cenário | Situação real na drogaria |
| :--- | :--- |
| **Aleatório** | carga inicial de um sistema novo / importação de outra filial |
| **Já ordenado** | reprocessamento de um estoque que já está em ordem |
| **Quase ordenado** | estoque ordenado + um **lote pequeno (1%)** de produtos novos cadastrado no fim (reposição diária) |
| **Ordem inversa** | relatório exportado em ordem decrescente |

O objetivo do trabalho é mostrar que **a escolha do método de ordenação precisa levar em conta o formato da entrada**: o mesmo algoritmo pode ser o melhor num cenário e o pior em outro.

## Objetivos

### MVP (essencial)

Comparar dois métodos de ordenação com comportamentos opostos:

1. **Insertion Sort** — $O(n)$ no melhor caso, $O(n^2)$ no médio e no pior caso.
2. **Quick Sort** (pivô = primeiro elemento) — $O(n \log n)$ no caso médio, degradando para $O(n^2)$ em entradas ordenadas.

- Ordenar a base de produtos por **código** nos quatro cenários acima.
- Medir **tempo**, **número de comparações** e **número de movimentações**.
- Experimentos com bases de $1.000$, $2.500$, $5.000$ e $10.000$ produtos.
- Gráficos de desempenho ($Tempo \times N$) e comparação com a análise assintótica.

### Extras

- Demonstração de **estabilidade** (ordenar por preço e depois por categoria).
- Testes automatizados de corretude.

## Tecnologias

- **Linguagem:** Python 3.10+
- **Biblioteca Externa:**
  - `matplotlib`: geração dos gráficos comparativos de desempenho.

## Estrutura
```text
├── assets/
│   ├── insertion_tempo_cenarios.png  # tempo x N do insertion nos 4 cenários
│   ├── insertion_comparacoes.png     # comparações medidas x curvas teóricas
│   ├── comparacao_cenarios.png       # tempo por cenário no maior N (todos os algoritmos)
│   └── ultimos_resultados.json       # dados da última execução do benchmark
│
├── src/
│   ├── __init__.py
│   ├── models.py                     # classe Produto e gerador de base aleatória
│   ├── cenarios.py                   # montagem dos 4 cenários de entrada
│   └── sorts/
│       ├── __init__.py               # registro dos algoritmos comparados
│       ├── base.py                   # contrato comum (Estatisticas)
│       ├── insertion.py              # insertion sort
│       └── quick.py                  # quick sort
│
├── .gitignore
├── comparacao.py                     # benchmark: algoritmos x cenários x tamanhos
├── main.py                           # demonstração do insertion sort
├── plot_results.py                   # leitura do JSON e geração dos gráficos
├── testes.py                         # testes de corretude
└── README.md
```

## Como rodar

```bash
# 1. criar e ativar o ambiente virtual (opcional, mas recomendado)
# no windows:
python -m venv venv
.\venv\Scripts\Activate.ps1

# no linux / macOS:
python3 -m venv venv
source venv/bin/activate

# 2. instalar dependências
pip install matplotlib

# 3. execução dos scripts
# demonstração (ordenação, estabilidade e custo por cenário)
python main.py

# testes de corretude
python testes.py

# benchmark (padrão: 1.000, 2.500, 5.000 e 10.000) — leva cerca de 1 minuto
python comparacao.py

# ou com tamanhos personalizados
python comparacao.py 500 2000 4000

# gerar os gráficos na pasta assets/ a partir do último benchmark
python plot_results.py
```

> **Por que não 100.000 produtos, como no trabalho de busca?** Os cenários $O(n^2)$ ficam inviáveis em Python: o Insertion Sort em ordem inversa já leva ~7,7 s com 10.000 produtos; com 100.000 seriam ~100× mais (mais de 12 minutos por execução).

## Insertion Sort

### Funcionamento

A lista é dividida em uma parte **já ordenada** (à esquerda) e uma parte **ainda não processada** (à direita). A cada passo, o primeiro elemento não processado é retirado e **inserido na posição correta** da parte ordenada, deslocando uma casa para a direita todos os elementos maiores que ele — como quem organiza cartas de baralho na mão.

```text
[ 3 | 7 1 5 ]   -> 7 já está no lugar           (1 comparação)
[ 3 7 | 1 5 ]   -> 1 anda até o início           (2 comparações, 2 deslocamentos)
[ 1 3 7 | 5 ]   -> 5 passa pelo 7 e para no 3     (2 comparações, 1 deslocamento)
[ 1 3 5 7 ]
```

```python
for i in range(1, len(lista)):
    atual = lista[i]
    j = i - 1
    while j >= 0 and chave(lista[j]) > chave(atual):
        lista[j + 1] = lista[j]   # desloca o maior para a direita
        j -= 1
    lista[j + 1] = atual          # encaixa na posição livre
```

### Análise de complexidade

O trabalho do Insertion Sort é proporcional ao número de **inversões** da entrada (pares de elementos fora de ordem): cada deslocamento desfaz exatamente uma inversão.

| Caso | Entrada | Comparações | Complexidade |
| :--- | :--- | :--- | :--- |
| **Melhor** | já ordenada | $n - 1$ (cada elemento só olha o vizinho) | $O(n)$ |
| **Quase ordenado** | ordenada + lote de $n/100$ itens no fim | $\approx \frac{n}{100} \cdot \frac{n}{2} = \frac{n^2}{200}$ | $O(n \cdot k)$, com $k$ itens fora do lugar |
| **Médio** | aleatória | $\approx \frac{n^2}{4}$ (cada elemento anda metade da parte ordenada) | $O(n^2)$ |
| **Pior** | ordem inversa | $\frac{n(n-1)}{2}$ (cada elemento anda até o início) | $O(n^2)$ |

**Propriedades:**
- **Estável:** o laço só desloca elementos *estritamente maiores*, então produtos com chaves iguais mantêm a ordem original (ver `main.py`, demonstração 2).
- **In-place:** memória extra $O(1)$.
- **Online:** consegue ordenar à medida que os dados chegam — ideal para inserir produtos novos em um estoque já ordenado.

## Quick Sort

> *Seção a cargo da dupla — implementação em `src/sorts/quick.py`.*

## Integrantes

| Nome | GitHub |
|---|---|
| Enzo Lopes | [@lopes061](https://github.com/lopes061) |
| Luan Vinícius | [@luannvi](https://github.com/luannvi) |

## Vídeo de Apresentação

> *Link a adicionar.*
