"""
Estudo experimental Q4a: comparacao das leituras A e B.
"""

import statistics
import sys
from instance_q4 import carregar_q4
from cores import min_guardas, grafo_conflito, cromatico, lexicografico

TAMANHOS = [10, 20, 40, 80]


def correr(diretorio):
    print(f"{'nr':>4} | {'#inst':>5} | {'guardas':>7} | "
          f"{'A med':>5} {'A max':>5} | "
          f"{'B med':>5} {'B max':>5} {'B prov%':>7}")
    print("-" * 70)
    for nr in TAMANHOS:
        try:
            insts = carregar_q4(f"{diretorio}/inst_{nr}.txt")
        except FileNotFoundError:
            continue
        coresA, coresB, n_guardas = [], [], []
        b_prov, b_tot = 0, 0
        for inst in insts:
            S, g = min_guardas(inst)
            n_guardas.append(g)
            ncA, _ = cromatico(inst, S)
            coresA.append(ncA)
            _, ncB, prov = lexicografico(inst, time_limit_s=20)
            if ncB is not None:
                coresB.append(ncB)
                b_tot += 1
                if prov:
                    b_prov += 1
        pct = (b_prov / b_tot * 100) if b_tot else 0
        print(f"{nr:>4} | {len(insts):>5} | {statistics.mean(n_guardas):>7.1f} | "
              f"{statistics.mean(coresA):>5.2f} {max(coresA):>5d} | "
              f"{statistics.mean(coresB):>5.2f} {max(coresB):>5d} {pct:>6.0f}%")


if __name__ == "__main__":
    diretorio = sys.argv[1] if len(sys.argv) > 1 else "../../casos_teste"
    print("Numero de cores - Leitura A (solucao fixa) vs Leitura B (lexicografico)\n")
    correr(diretorio)
