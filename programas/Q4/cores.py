"""
Q4a - guardas com cores.

Restricao: guardas que veem o mesmo retangulo tem cores distintas.
Equivalente a uma restricao all_distinct sobre as cores dos guardas
em cada G[r].

Duas leituras da pergunta "para o numero minimo de guardas, qual o
numero minimo de cores?":

  LEITURA A - colorir uma solucao otima fixa de guardas com o minimo
              de cores (numero cromatico do grafo de conflito).
  LEITURA B - lexicografica: entre todas as solucoes com o numero
              minimo de guardas, escolher a que minimiza as cores.
"""

from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model
from instance_q4 import carregar_q4


def min_guardas(inst, time_limit_s=60.0):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    solver.SetTimeLimit(int(time_limit_s * 1000))
    x = {p: solver.IntVar(0, 1, f"x_{p}") for p in inst.P}
    for r in inst.R:
        solver.Add(sum(x[p] for p in inst.G0[r]) >= 1)
    solver.Minimize(sum(x.values()))
    solver.Solve()
    S = {p for p in inst.P if x[p].solution_value() > 0.5}
    return S, int(round(solver.Objective().Value()))


def grafo_conflito(inst, S):
    arestas = set()
    Sl = list(S)
    for r in inst.R:
        guardas_r = [p for p in Sl if p in inst.G0[r]]
        for i in range(len(guardas_r)):
            for j in range(i + 1, len(guardas_r)):
                a, b = guardas_r[i], guardas_r[j]
                arestas.add((min(a, b), max(a, b)))
    return arestas


def cromatico(inst, S, time_limit_s=30.0):
    """Numero cromatico do grafo de conflito de S (Leitura A)."""
    arestas = grafo_conflito(inst, S)
    Sl = list(S)
    n = len(Sl)
    if n == 0:
        return 0, {}

    model = cp_model.CpModel()
    K = n
    cor = {p: model.NewIntVar(0, K - 1, f"cor_{p}") for p in Sl}
    for (a, b) in arestas:
        model.Add(cor[a] != cor[b])
    maxcor = model.NewIntVar(0, K - 1, "maxcor")
    for p in Sl:
        model.Add(cor[p] <= maxcor)
    model.Add(cor[Sl[0]] == 0)  # quebra de simetria
    model.Minimize(maxcor)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_s
    solver.Solve(model)
    n_cores = int(solver.Value(maxcor)) + 1
    atribuicao = {p: int(solver.Value(cor[p])) for p in Sl}
    return n_cores, atribuicao


def lexicografico(inst, time_limit_s=60.0):
    """Leitura B: minimiza guardas, depois cores. Modelo unico em CP-SAT.

    Variaveis booleanas y[p,k] = 'guarda p ativo com cor k'.
    usa[k] = 'cor k usada por algum guarda'.

    Restricoes: cobertura; soma(x)=G*; Sum_k y[p,k] = x[p];
        por retangulo r e cor k: Sum_{p em G[r]} y[p,k] <= 1;
        y[p,k] <= usa[k]; quebra de simetria usa[k] >= usa[k+1].
    Objetivo: minimizar Sum_k usa[k].
    """
    _, Gstar = min_guardas(inst)

    model = cp_model.CpModel()
    P = list(inst.P)
    K = max(len(inst.G0[r]) for r in inst.R)

    x = {p: model.NewBoolVar(f"x_{p}") for p in P}
    y = {(p, k): model.NewBoolVar(f"y_{p}_{k}") for p in P for k in range(K)}
    usa = {k: model.NewBoolVar(f"usa_{k}") for k in range(K)}

    for r in inst.R:
        model.Add(sum(x[p] for p in inst.G0[r]) >= 1)
    model.Add(sum(x.values()) == Gstar)
    for p in P:
        model.Add(sum(y[(p, k)] for k in range(K)) == x[p])
    for r in inst.R:
        for k in range(K):
            model.Add(sum(y[(p, k)] for p in inst.G0[r]) <= 1)
    for p in P:
        for k in range(K):
            model.Add(y[(p, k)] <= usa[k])
    for k in range(K - 1):
        model.Add(usa[k] >= usa[k + 1])

    model.Minimize(sum(usa.values()))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_s
    solver.parameters.num_search_workers = 8
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return Gstar, None, False
    n_cores = int(sum(solver.Value(usa[k]) for k in range(K)))
    provado = (status == cp_model.OPTIMAL)
    return Gstar, n_cores, provado


if __name__ == "__main__":
    import sys
    caminho = sys.argv[1] if len(sys.argv) > 1 else "../../casos_teste/inst_10.txt"
    insts = carregar_q4(caminho)

    print("Leitura A (colorir uma solucao otima fixa de guardas):\n")
    print(f"  {'inst':>4} | {'#guardas':>8} | {'#conflitos':>10} | {'#cores (A)':>10}")
    print("  " + "-" * 42)
    for i, inst in enumerate(insts, 1):
        S, g = min_guardas(inst)
        arestas = grafo_conflito(inst, S)
        nc, _ = cromatico(inst, S)
        print(f"  {i:>4} | {g:>8} | {len(arestas):>10} | {nc:>10}")

    print("\nLeitura B (lexicografico):\n")
    print(f"  {'inst':>4} | {'#guardas':>8} | {'#cores (B)':>10} | {'otimo?':>7}")
    print("  " + "-" * 40)
    for i, inst in enumerate(insts, 1):
        g, nc, prov = lexicografico(inst)
        print(f"  {i:>4} | {g:>8} | {str(nc):>10} | {str(prov):>7}")
