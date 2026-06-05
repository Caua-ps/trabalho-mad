import sys
from ortools.sat.python import cp_model
from instance_q2 import carregar_instancias_q2, InstanceQ2


def resolver_ortools(inst: InstanceQ2):
    model = cp_model.CpModel()

    x = [model.NewBoolVar(f'x_{i}') for i in range(len(inst.pontos))]

    for face in inst.faces:
        if not face:
            continue
        candidatos = [x[i] for i in face]
        model.Add(sum(candidatos) >= 1)

    model.Minimize(sum(x))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        posicoes = [inst.pontos[i] for i in range(len(inst.pontos)) if solver.Value(x[i]) == 1]
        return int(solver.ObjectiveValue()), posicoes
    else:
        return None, []


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "../../casos_teste/inst_10.txt"
    try:
        instancias = carregar_instancias_q2(path)

        for i, inst in enumerate(instancias, 1):
            print(f"\nA resolver Instancia #{i} com OR-Tools (CP-SAT):")
            minGuardas, posicoes = resolver_ortools(inst)

            if minGuardas is not None:
                print(f"Minimo de guardas: {minGuardas} / Posicoes: {sorted(posicoes)}")
            else:
                print("Nao foi possivel encontrar solucao.")

    except FileNotFoundError:
        print(f"Ficheiro '{path}' nao encontrado.")


if __name__ == "__main__":
    main()