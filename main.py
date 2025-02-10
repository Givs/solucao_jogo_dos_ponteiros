#!/usr/bin/env python3
"""
Solução do Jogo dos Ponteiros

Descrição do problema:
  - Ambiente: Uma grade 2x2 (quatro células: (0,0), (0,1), (1,0) e (1,1)) onde cada célula contém um ponteiro que pode estar
    apontando para uma das 4 direções: 0, 1, 2 ou 3 (por exemplo, 0: cima, 1: direita, 2: baixo, 3: esquerda).
  - Estado: Representado por uma tupla de 6 elementos:
         (agent_row, agent_col, p00, p01, p10, p11)
    onde (agent_row, agent_col) é a posição do agente e pXY é a direção do ponteiro na célula (X, Y).
  - Ações:
       * Movimentos: "up", "down", "left", "right" (validados pelos limites da grade).
       * Rotações: "rotate_cw" (horário) e "rotate_ccw" (anti‐horário) – atuam sobre o ponteiro da célula onde o agente está.
  - Objetivo: Atingir um estado em que todos os ponteiros estejam apontando para a mesma direção (qualquer que seja).

A estratégia de busca adotada é o A* (astar_search), com uma heurística personalizada que soma:
  (i) O custo mínimo de rotações necessárias para alinhar cada ponteiro a uma “direção meta”
  (ii) Um lower bound do custo de movimentação (calculado como a soma do custo mínimo para que o agente alcance
       todas as células que precisem ser “corrigidas”, usando uma árvore geradora mínima – MST – com distância de Manhattan).

As funções auxiliares (como cálculo da distância Manhattan e do custo MST) foram implementadas para enriquecer a
heurística e tornar o código único.
"""

import random
from aiaa.search import Problem, astar_search


# Função auxiliar: distância de Manhattan entre duas posições (tuplas (row, col))
def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


# Função auxiliar: dado um conjunto de pontos, calcula o custo da árvore geradora mínima (MST) usando distâncias de Manhattan.
def compute_mst(points):
    """
    Calcula o custo de uma MST para um conjunto de pontos.
    Utiliza um algoritmo guloso (variante do Prim) para conjuntos pequenos.
    """
    if not points:
        return 0
    points = list(points)
    visited = {points[0]}
    remaining = set(points[1:])
    total_cost = 0
    while remaining:
        min_edge = None
        min_cost = float('inf')
        for v in visited:
            for w in remaining:
                cost = manhattan(v, w)
                if cost < min_cost:
                    min_cost = cost
                    min_edge = w
        total_cost += min_cost
        visited.add(min_edge)
        remaining.remove(min_edge)
    return total_cost


# Classe que modela o ambiente do Jogo.
class PointerGameProblem(Problem):
    def __init__(self, initial_state=None):
        """
        Se nenhum estado inicial for fornecido, cria um estado aleatório:
          - A posição do agente é sorteada entre as 4 células.
          - Cada ponteiro recebe um valor aleatório entre 0 e 3.
        """
        if initial_state is None:
            agent_row = random.randint(0, 1)
            agent_col = random.randint(0, 1)
            p00 = random.randint(0, 3)
            p01 = random.randint(0, 3)
            p10 = random.randint(0, 3)
            p11 = random.randint(0, 3)
            initial_state = (agent_row, agent_col, p00, p01, p10, p11)
        super().__init__(initial_state)

    def actions(self, state):
        """
        Retorna a lista de ações possíveis a partir do estado atual.
        Considera:
          - Movimentos válidos (respeitando os limites da grade 2x2).
          - Rotações (sempre disponíveis).
        """
        actions = []
        agent_row, agent_col = state[0], state[1]
        # Movimentos: verificar se não estamos no limite da grade
        if agent_row > 0:
            actions.append("up")
        if agent_row < 1:
            actions.append("down")
        if agent_col > 0:
            actions.append("left")
        if agent_col < 1:
            actions.append("right")
        # Rotações sempre disponíveis na célula onde o agente está.
        actions.append("rotate_cw")
        actions.append("rotate_ccw")
        return actions

    def result(self, state, action):
        """
        Retorna o novo estado resultante da aplicação de 'action' em 'state'.
        Para movimentos, apenas a posição do agente é alterada.
        Para rotações, o valor do ponteiro na célula atual do agente é atualizado.
        """
        agent_row, agent_col, p00, p01, p10, p11 = state
        pointers = [p00, p01, p10, p11]
        if action == "up":
            new_agent_row = agent_row - 1
            new_agent_col = agent_col
            return new_agent_row, new_agent_col, p00, p01, p10, p11
        elif action == "down":
            new_agent_row = agent_row + 1
            new_agent_col = agent_col
            return new_agent_row, new_agent_col, p00, p01, p10, p11
        elif action == "left":
            new_agent_row = agent_row
            new_agent_col = agent_col - 1
            return new_agent_row, new_agent_col, p00, p01, p10, p11
        elif action == "right":
            new_agent_row = agent_row
            new_agent_col = agent_col + 1
            return new_agent_row, new_agent_col, p00, p01, p10, p11
        elif action == "rotate_cw":
            # Rota no sentido horário o ponteiro da célula onde o agente se encontra.
            idx = agent_row * 2 + agent_col
            new_pointers = pointers.copy()
            new_pointers[idx] = (new_pointers[idx] + 1) % 4
        elif action == "rotate_ccw":
            # Rota no sentido anti‐horário.
            idx = agent_row * 2 + agent_col
            new_pointers = pointers.copy()
            new_pointers[idx] = (new_pointers[idx] - 1) % 4
        else:
            # Caso não seja uma ação reconhecida, retorna o mesmo estado.
            return state

        # Na rotação, a posição do agente não muda.
        return agent_row, agent_col, new_pointers[0], new_pointers[1], new_pointers[2], new_pointers[3]

    def goal_test(self, state):
        """
        Testa se o estado é meta: todos os ponteiros (posições 2 a 5) devem ter o mesmo valor.
        """
        return state[2] == state[3] == state[4] == state[5]

    def path_cost(self, c, state1, action, state2):
        # Cada ação tem custo unitário.
        return c + 1

    def h(self, node):
        # Se 'node' for um Node, extraia o estado; caso contrário, já é o estado.
        if hasattr(node, 'state'):
            state = node.state
        else:
            state = node

        agent_pos = (state[0], state[1])
        # Mapeia as posições das células para os valores dos ponteiros
        pointers = {
            (0, 0): state[2],
            (0, 1): state[3],
            (1, 0): state[4],
            (1, 1): state[5]
        }
        best = float('inf')
        # Avalia cada possível direção meta t
        for t in range(4):
            cells_to_fix = []  # células onde o ponteiro não está na direção t
            rotation_sum = 0  # custo total de rotação para ajustar os ponteiros
            for pos, p in pointers.items():
                # custo mínimo de rotação (em módulo 4)
                r_cost = min(abs(p - t), 4 - abs(p - t))
                if r_cost > 0:
                    cells_to_fix.append(pos)
                    rotation_sum += r_cost
            # Se não há células a ajustar, custo de movimentação é zero.
            if not cells_to_fix:
                movement_cost = 0
            else:
                # Custo mínimo para que o agente chegue a alguma célula que precise de ajuste.
                min_agent_to_cell = min(manhattan(agent_pos, cell) for cell in cells_to_fix)
                # Custo da MST entre as células que precisam ser visitadas.
                mst_cost = compute_mst(cells_to_fix)
                movement_cost = min_agent_to_cell + mst_cost
            candidate = rotation_sum + movement_cost
            if candidate < best:
                best = candidate
        return best


# Classe que modela o agente que utiliza o problema e a estratégia de busca para encontrar e executar a solução.
class PointerAgent:
    def __init__(self, problem):
        self.problem = problem
        self.current_state = problem.initial
        self.solution_actions = []  # sequência de ações a serem executadas
        self.solution_node = None

    def plan(self):
        """
        Utiliza o A* (astar_search) para encontrar uma sequência de ações que leve do estado inicial ao objetivo.
        """
        self.solution_node = astar_search(self.problem)
        if self.solution_node is not None:
            self.solution_actions = self.solution_node.solution()
        return self.solution_actions

    def execute_plan(self):
        """
        Executa (simula) a sequência de ações encontrada, imprimindo os estados intermediários.
        """
        state = self.current_state
        print("Estado inicial:")
        self.print_state(state)
        for action in self.solution_actions:
            state = self.problem.result(state, action)
            print("\nAção executada:", action)
            self.print_state(state)
        if self.problem.goal_test(state):
            print("\nObjetivo atingido!")
        else:
            print("\nObjetivo não atingido.")

    def print_state(self, state):
        agent_pos = (state[0], state[1])
        pointers = {"(0,0)": state[2],
                    "(0,1)": state[3],
                    "(1,0)": state[4],
                    "(1,1)": state[5]}
        print("  Posição do Agente:", agent_pos)
        print("  Ponteiros:", pointers)


if __name__ == '__main__':
    # Cria o problema com estado inicial aleatório
    problem = PointerGameProblem()
    print("=== JOGO DOS PONTEIROS ===")
    agent = PointerAgent(problem)

    # Planeja a solução usando A* com a heurística personalizada
    actions = agent.plan()
    if actions is not None and len(actions) > 0:
        print("\nSolução encontrada!")
        print("Sequência de ações:", actions)
        print("Número de passos:", len(actions))
        print("\n--- Execução da solução ---")
        agent.execute_plan()
    else:
        print("Nenhuma solução foi encontrada.")
