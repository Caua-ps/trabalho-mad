"""
Resolucao exata por Programacao Inteira com OR-Tools (solver SCIP).
Usado como referencia otima para avaliar as estrategias greedy.

Modelo (Postos de Vigia, slide MAD2526_clp):
    min  sum_{p in P} x_p
    s.a. sum_{p in G[r]} x_p >= 1,  r in R
         x_p em {0,1}
"""

from ortools.linear_solver import pywraplp
from instance import Instance


def solve_exato(inst: Instance, time_limit_s: float = 60.0):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if solver is None:
        raise RuntimeError("SCIP nao disponivel")
    solver.SetTimeLimit(int(time_limit_s * 1000))

    x = {p: solver.IntVar(0, 1, f"x_{p}") for p in inst.P}

    for r in inst.R:
        cands = [x[p] for p in inst.G[r]]
        if not cands:
            raise ValueError(f"Retangulo {r} sem candidatos.")
        solver.Add(sum(cands) >= 1)

    solver.Minimize(sum(x.values()))

    status = solver.Solve()
    tempo = solver.wall_time() / 1000.0

    if status == pywraplp.Solver.OPTIMAL:
        S = {p for p in inst.P if x[p].solution_value() > 0.5}
        return S, int(round(solver.Objective().Value())), tempo
    return None, None, tempo


if __name__ == "__main__":
    from instance import instancia_fp3_ex7, carregar_ficheiro
    import sys

    print("Verificacao na instancia da fp3 ex.7:")
    inst = instancia_fp3_ex7()
    S, v, t = solve_exato(inst)
    print(f"  otimo: |S|={v}, S={sorted(S)}, tempo={t*1000:.1f} ms")
    assert v == 4

    if len(sys.argv) > 1:
        print(f"\nResolucao de {sys.argv[1]}:")
        insts = carregar_ficheiro(sys.argv[1])
        for i, inst in enumerate(insts, 1):
            S, v, t = solve_exato(inst)
            print(f"  #{i}: otimo={v}, tempo={t*1000:.1f} ms")
