"""
Q4b - guardas com maior alcance.

Modelo identico ao da Q2a, com G[r] substituido por G_D[r]:
    G_D[r] = { p em P : algum vertice a distancia <= D de p ve r }
Para D=0 recupera-se exatamente o problema base.
"""

from ortools.linear_solver import pywraplp
from instance_q4 import carregar_q4


def solve_alcance(inst, D, time_limit_s=60.0):
    G_D, V_D = inst.alcance(D)

    solver = pywraplp.Solver.CreateSolver('SCIP')
    solver.SetTimeLimit(int(time_limit_s * 1000))

    x = {p: solver.IntVar(0, 1, f"x_{p}") for p in inst.P}
    for r in inst.R:
        cands = [x[p] for p in G_D[r]]
        if not cands:
            raise ValueError(f"Retangulo {r} sem candidatos com D={D}.")
        solver.Add(sum(cands) >= 1)
    solver.Minimize(sum(x.values()))

    status = solver.Solve()
    tempo = solver.wall_time() / 1000.0
    if status == pywraplp.Solver.OPTIMAL:
        S = {p for p in inst.P if x[p].solution_value() > 0.5}
        return S, int(round(solver.Objective().Value())), tempo
    return None, None, tempo


if __name__ == "__main__":
    import sys
    caminho = sys.argv[1] if len(sys.argv) > 1 else "../../casos_teste/inst_10.txt"
    insts = carregar_q4(caminho)
    inst = insts[0]
    print(f"{inst}\n")
    print("Efeito do alcance D no numero minimo de guardas:")
    print(f"  {'D':>2} | {'#guardas':>8} | {'tempo (ms)':>10}")
    print("  " + "-" * 28)
    for D in range(0, 6):
        S, v, t = solve_alcance(inst, D)
        print(f"  {D:>2} | {v:>8} | {t*1000:>10.1f}")
