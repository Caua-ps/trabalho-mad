"""
Leitura e pre-processamento de instancias do gerador rectParts.c.

Formato do ficheiro:
    linha 1: s   (numero de instancias)
    para cada instancia:
        linha:   nr   (numero de retangulos)
        nr linhas:   id  nv  x1 y1  ...  xnv ynv

Identificacao do retangulo exterior por bounding box maxima.
Os vertices da borda externa sao descartados como candidatos a guarda
(ver alinea (b) do exercicio 7 da fp3).
"""

from collections import defaultdict


class Instance:

    def __init__(self, rid_verts, exterior_id):
        self.exterior = exterior_id
        self.all_rid_verts = rid_verts
        self.boundary = set(rid_verts[exterior_id])

        self.R = [r for r in rid_verts if r != exterior_id]
        self.G = {r: set(rid_verts[r]) - self.boundary for r in self.R}

        self.P = set()
        for verts in self.G.values():
            self.P.update(verts)

        self.V = defaultdict(set)
        for r, verts in self.G.items():
            for p in verts:
                self.V[p].add(r)
        self.V = dict(self.V)

    def __repr__(self):
        return (f"Instance(#retangulos={len(self.R)}, "
                f"#candidatos={len(self.P)}, exterior=R{self.exterior})")


def _bounding_box_area(verts):
    xs = [x for x, y in verts]
    ys = [y for x, y in verts]
    return (max(xs) - min(xs)) * (max(ys) - min(ys))


def _identificar_exterior(rid_verts):
    return max(rid_verts, key=lambda r: _bounding_box_area(rid_verts[r]))


def carregar_ficheiro(caminho):
    with open(caminho) as f:
        toks = f.read().split()
    it = iter(toks)

    n_inst = int(next(it))
    instancias = []
    for _ in range(n_inst):
        nr = int(next(it))
        rid_verts = {}
        for _ in range(nr):
            rid = int(next(it))
            nv = int(next(it))
            verts = set()
            for _ in range(nv):
                x = int(next(it))
                y = int(next(it))
                verts.add((x, y))
            rid_verts[rid] = verts
        exterior = _identificar_exterior(rid_verts)
        instancias.append(Instance(rid_verts, exterior))
    return instancias


def instancia_fp3_ex7():
    """Instancia do exercicio 7 da fp3 (com os nos internos numerados 1..8
    como no enunciado). Usada como caso de teste com otimo conhecido = 4."""
    rid_verts_simulado = {
        1:  frozenset({8}),
        2:  frozenset({8, 7}),
        3:  frozenset({7, 6, 4, 5}),
        4:  frozenset({7, 6, 8}),
        5:  frozenset({3, 4}),
        6:  frozenset({2, 1}),
        7:  frozenset({5, 4, 3, 2}),
        8:  frozenset({5, 6}),
        9:  frozenset({1, 3, 2}),
        10: frozenset({1}),
    }
    inst = Instance.__new__(Instance)
    inst.exterior = None
    inst.all_rid_verts = None
    inst.boundary = set()
    inst.R = list(rid_verts_simulado.keys())
    inst.G = {r: set(v) for r, v in rid_verts_simulado.items()}
    inst.P = set()
    for v in rid_verts_simulado.values():
        inst.P.update(v)
    inst.V = defaultdict(set)
    for r, verts in inst.G.items():
        for p in verts:
            inst.V[p].add(r)
    inst.V = dict(inst.V)
    return inst


if __name__ == "__main__":
    import sys
    caminho = sys.argv[1] if len(sys.argv) > 1 else "../../casos_teste/inst_10.txt"
    insts = carregar_ficheiro(caminho)
    print(f"Lidas {len(insts)} instancia(s) de {caminho}:")
    for i, inst in enumerate(insts, 1):
        print(f"  #{i}: {inst}")
