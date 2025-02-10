# Jogo dos Ponteiros

Este projeto implementa a solução do **Jogo dos Ponteiros** utilizando o algoritmo A* da biblioteca AIMA. O objetivo é fazer com que todos os ponteiros de uma grade 2×2 apontem para a mesma direção.

## Passos e Estrutura do Projeto

1. **Criação da Pasta `aiaa`:**  
   - Copiamos os arquivos `search.py` e `utils.py` do repositório AIMA para uma pasta chamada `aiaa` dentro do nosso projeto.  
   - **Por quê?** Para isolar e integrar apenas os módulos necessários (como a classe `Problem` e os algoritmos de busca) sem precisar incorporar todo o repositório AIMA.

2. **Função `main.py`:**  
   - O arquivo principal (`main.py`) define o problema (classe `PointerGameProblem`) e o agente (`PointerAgent`), que utiliza o algoritmo A\* (`astar_search`) para encontrar uma sequência de ações que leve o estado inicial ao estado objetivo.
   
3. **Funções Auxiliares:**  
   - **`manhattan(p1, p2)`**: Calcula a distância de Manhattan entre duas posições (representadas como tuplas), sendo utilizada na avaliação do custo de movimentação.  
   - **`compute_mst(points)`**: Calcula o custo de uma árvore geradora mínima (MST) para um conjunto de pontos. Essa função contribui para estimar um lower bound do custo de movimentação na heurística do A\*.

   Essas duas funções foram criadas para enriquecer a heurística personalizada do A*, combinando o custo mínimo de rotações com uma estimativa do custo de movimentação (baseada em distâncias e na MST).

## Exemplos de Saída

### Exemplo 1

```plaintext
=== JOGO DOS PONTEIROS ===

Solução encontrada!
Sequência de ações: ['rotate_cw', 'rotate_cw', 'left', 'rotate_ccw']
Número de passos: 4

--- Execução da solução ---
Estado inicial:
  Posição do Agente: (0, 1)
  Ponteiros: {'(0,0)': 3, '(0,1)': 0, '(1,0)': 2, '(1,1)': 2}

Ação executada: rotate_cw
  Posição do Agente: (0, 1)
  Ponteiros: {'(0,0)': 3, '(0,1)': 1, '(1,0)': 2, '(1,1)': 2}

Ação executada: rotate_cw
  Posição do Agente: (0, 1)
  Ponteiros: {'(0,0)': 3, '(0,1)': 2, '(1,0)': 2, '(1,1)': 2}

Ação executada: left
  Posição do Agente: (0, 0)
  Ponteiros: {'(0,0)': 3, '(0,1)': 2, '(1,0)': 2, '(1,1)': 2}

Ação executada: rotate_ccw
  Posição do Agente: (0, 0)
  Ponteiros: {'(0,0)': 2, '(0,1)': 2, '(1,0)': 2, '(1,1)': 2}

Objetivo atingido!


############### Exemplo 2 ######################

Solução encontrada!
Sequência de ações: ['rotate_cw', 'up', 'rotate_ccw', 'right', 'rotate_cw', 'rotate_cw']
Número de passos: 6

--- Execução da solução ---
Estado inicial:
  Posição do Agente: (1, 0)
  Ponteiros: {'(0,0)': 2, '(0,1)': 3, '(1,0)': 0, '(1,1)': 1}

Ação executada: rotate_cw
  Posição do Agente: (1, 0)
  Ponteiros: {'(0,0)': 2, '(0,1)': 3, '(1,0)': 1, '(1,1)': 1}

Ação executada: up
  Posição do Agente: (0, 0)
  Ponteiros: {'(0,0)': 2, '(0,1)': 3, '(1,0)': 1, '(1,1)': 1}

Ação executada: rotate_ccw
  Posição do Agente: (0, 0)
  Ponteiros: {'(0,0)': 1, '(0,1)': 3, '(1,0)': 1, '(1,1)': 1}

Ação executada: right
  Posição do Agente: (0, 1)
  Ponteiros: {'(0,0)': 1, '(0,1)': 3, '(1,0)': 1, '(1,1)': 1}

Ação executada: rotate_cw
  Posição do Agente: (0, 1)
  Ponteiros: {'(0,0)': 1, '(0,1)': 0, '(1,0)': 1, '(1,1)': 1}

Ação executada: rotate_cw
  Posição do Agente: (0, 1)
  Ponteiros: {'(0,0)': 1, '(0,1)': 1, '(1,0)': 1, '(1,1)': 1}

Objetivo atingido!