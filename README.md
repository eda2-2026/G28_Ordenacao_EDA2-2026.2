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

## Integrantes

| Nome | GitHub |
|---|---|
| Enzo Lopes | [@lopes061](https://github.com/lopes061) |
| Luan Vinícius | [@luannvi](https://github.com/luannvi) |

## Vídeo de Apresentação

> *Link a adicionar.*
