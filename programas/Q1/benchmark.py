"""
Estudo experimental da Q1: comparacao das duas estrategias greedy contra
o otimo de Programacao Inteira.

Para cada tamanho nr em {10, 20, 40, 80, 160}, le N instancias da pasta
indicada e reporta: tamanho medio e maximo, taxa de otimo, excesso medio
relativo ao otimo, e tempo medio do solver exato.
"""

import time
import statistics
import sys
from instance import carregar_ficheiro
from greedy import greedy_first_fail, greedy_max_cobertura
from exato import solve_exato


TAMANHOS = [10, 20, 40, 80, 160]


def cronometrar(func, *args):
    t0 = time.perf_counter()
    r = func(*args)
    t1 = time.perf_counter()
    return r, (t1 - t0) * 1000.0


def correr_bateria(diretorio):
    resultados = []

    for nr in TAMANHOS:
        path = f"{diretorio}/inst_{nr}.txt"
        try:
            insts = carregar_ficheiro(path)
        except FileNotFoundError:
            print(f"(saltado: {path} nao encontrado)")
            continue
        print(f"\nnr = {nr} retangulos ({len(insts)} instancias)")
        for idx, inst in enumerate(insts, 1):
            (S_ff,  t_ff)  = cronometrar(greedy_first_fail, inst)
            (S_mc,  t_mc)  = cronometrar(greedy_max_cobertura, inst)
            (S_opt_full, t_opt_calc) = cronometrar(solve_exato, inst)
            S_opt, v_opt, _ = S_opt_full
            if v_opt is None:
                continue
            resultados.append({
                "nr": nr, "idx": idx,
                "ff_n": len(S_ff), "ff_t": t_ff,
                "mc_n": len(S_mc), "mc_t": t_mc,
                "opt_n": v_opt,    "opt_t": t_opt_calc,
            })
            mff = "*" if len(S_ff) == v_opt else " "
            mmc = "*" if len(S_mc) == v_opt else " "
            print(f"  #{idx:2d}: opt={v_opt:3d}  "
                  f"ff={len(S_ff):3d}{mff}  mc={len(S_mc):3d}{mmc}   "
                  f"(t_opt={t_opt_calc:6.1f} ms)")
    return resultados


def resumir(resultados):
    print("\n" + "=" * 72)
    print(" RESUMO POR TAMANHO")
    print("=" * 72)

    cab = (f"{'nr':>4} | {'#inst':>5} | "
           f"{'opt_med':>7} {'opt_max':>7} | "
           f"{'ff_med':>7} {'ff_max':>6} {'ff %ot':>7} {'ff exc%':>8} | "
           f"{'mc_med':>7} {'mc_max':>6} {'mc %ot':>7} {'mc exc%':>8} | "
           f"{'t_opt ms':>9}")
    print(cab)
    print("-" * len(cab))

    for nr in TAMANHOS:
        rs = [r for r in resultados if r["nr"] == nr]
        if not rs:
            continue
        n = len(rs)
        opts = [r["opt_n"] for r in rs]
        ffs  = [r["ff_n"]  for r in rs]
        mcs  = [r["mc_n"]  for r in rs]
        ff_ok = sum(1 for r in rs if r["ff_n"] == r["opt_n"]) / n * 100
        mc_ok = sum(1 for r in rs if r["mc_n"] == r["opt_n"]) / n * 100
        ff_exc = statistics.mean(
            (r["ff_n"] - r["opt_n"]) / r["opt_n"] * 100 for r in rs)
        mc_exc = statistics.mean(
            (r["mc_n"] - r["opt_n"]) / r["opt_n"] * 100 for r in rs)
        t_opt = statistics.mean(r["opt_t"] for r in rs)

        print(f"{nr:>4} | {n:>5} | "
              f"{statistics.mean(opts):>7.2f} {max(opts):>7d} | "
              f"{statistics.mean(ffs):>7.2f} {max(ffs):>6d} "
              f"{ff_ok:>6.1f}% {ff_exc:>7.2f}% | "
              f"{statistics.mean(mcs):>7.2f} {max(mcs):>6d} "
              f"{mc_ok:>6.1f}% {mc_exc:>7.2f}% | "
              f"{t_opt:>9.1f}")


def gravar_csv(resultados, caminho="resultados_q1.csv"):
    import csv
    with open(caminho, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(resultados[0].keys()))
        w.writeheader()
        for r in resultados:
            w.writerow(r)
    print(f"\n-> {caminho}")


if __name__ == "__main__":
    diretorio = sys.argv[1] if len(sys.argv) > 1 else "../../casos_teste"
    res = correr_bateria(diretorio)
    if res:
        resumir(res)
        gravar_csv(res)
