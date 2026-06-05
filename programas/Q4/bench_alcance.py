"""
Estudo experimental Q4b: numero medio de guardas em funcao do alcance D.
"""

import statistics
import sys
from instance_q4 import carregar_q4
from alcance import solve_alcance

TAMANHOS = [10, 20, 40, 80]
DS = [0, 1, 2, 3, 4]


def correr(diretorio):
    print(f"{'nr':>4} | " + " | ".join(f"D={d:>1}" for d in DS))
    print("-" * 40)
    for nr in TAMANHOS:
        try:
            insts = carregar_q4(f"{diretorio}/inst_{nr}.txt")
        except FileNotFoundError:
            continue
        medias = []
        for d in DS:
            vals = []
            for inst in insts:
                _, v, _ = solve_alcance(inst, d)
                if v is not None:
                    vals.append(v)
            medias.append(statistics.mean(vals))
        print(f"{nr:>4} | " + " | ".join(f"{m:>3.1f}" for m in medias))


if __name__ == "__main__":
    diretorio = sys.argv[1] if len(sys.argv) > 1 else "../../casos_teste"
    print("Numero medio de guardas em funcao do alcance D\n")
    correr(diretorio)
