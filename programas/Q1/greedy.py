"""
Estrategias greedy para a cobertura de particoes retangulares.

(1) GREEDY_FIRST_FAIL
    Escolher em cada iteracao o retangulo nao coberto com menos candidatos
    disponiveis (|G[r] \\ S|). Entre os candidatos desse retangulo, escolher
    o que cobre mais retangulos ainda nao cobertos.
    Corresponde a relacao entre greedy e first-fail discutida na alinea (a)
    do exercicio 7 da fp3.

(2) GREEDY_MAX_COBERTURA
    Em cada iteracao, escolher o vertice p que maximiza |V[p] cap nao_cob|.
    E a estrategia greedy classica de set cover (analoga ao Kruskal por peso
    minimo ou ao knapsack fracionario por razao valor/peso).
"""

from instance import Instance


def _verifica(inst: Instance, S: set) -> bool:
    cobertos = set()
    for p in S:
        cobertos |= inst.V[p]
    return cobertos >= set(inst.R)


def greedy_first_fail(inst: Instance) -> set:
    nao_cobertos = set(inst.R)
    S = set()

    while nao_cobertos:
        def candidatos(r):
            return inst.G[r] - S
        r_star = min(nao_cobertos, key=lambda r: (len(candidatos(r)), r))
        cands = candidatos(r_star)
        if not cands:
            raise RuntimeError(f"Retangulo {r_star} sem candidatos.")

        def cobertura_extra(p):
            return len(inst.V[p] & nao_cobertos)
        p_star = max(cands, key=lambda p: (cobertura_extra(p), -hash(p)))

        S.add(p_star)
        nao_cobertos -= inst.V[p_star]

    assert _verifica(inst, S)
    return S


def greedy_max_cobertura(inst: Instance) -> set:
    nao_cobertos = set(inst.R)
    S = set()
    disponiveis = set(inst.P)

    while nao_cobertos:
        def cobertura(p):
            return len(inst.V[p] & nao_cobertos)
        p_star = max(disponiveis, key=lambda p: (cobertura(p), -hash(p)))
        if cobertura(p_star) == 0:
            raise RuntimeError("Sem vertices uteis e ainda ha retangulos por cobrir.")
        S.add(p_star)
        disponiveis.discard(p_star)
        nao_cobertos -= inst.V[p_star]

    assert _verifica(inst, S)
    return S


if __name__ == "__main__":
    from instance import instancia_fp3_ex7, carregar_ficheiro
    import sys

    print("Teste 1: instancia da fp3 ex.7 (otimo conhecido = 4)")
    inst = instancia_fp3_ex7()
    S1 = greedy_first_fail(inst)
    S2 = greedy_max_cobertura(inst)
    print(f"  first-fail:     |S|={len(S1)}, S={sorted(S1)}")
    print(f"  max-cobertura:  |S|={len(S2)}, S={sorted(S2)}")

    if len(sys.argv) > 1:
        print(f"\nTeste 2: {sys.argv[1]}")
        insts = carregar_ficheiro(sys.argv[1])
        for i, inst in enumerate(insts, 1):
            S1 = greedy_first_fail(inst)
            S2 = greedy_max_cobertura(inst)
            print(f"  #{i}: first-fail={len(S1)}  max-cobertura={len(S2)}")
