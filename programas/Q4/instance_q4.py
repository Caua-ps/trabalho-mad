"""
Q4 - leitura de instancias preservando a ordem dos vertices ao longo da
fronteira de cada retangulo (necessario para reconstruir o grafo da
particao). Constroi tambem o grafo dos vertices e calcula o alcance D
de um guarda por BFS.

A camada de cobertura para D=0 coincide com a do instance.py da Q1
(verificavel por comparacao directa).
"""

from collections import defaultdict, deque


def carregar_ordenado(caminho):
    """Devolve lista de dicionarios { id_retangulo : [(x1,y1), (x2,y2), ...] }
    com a ordem dos vertices preservada."""
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
            verts = []
            for _ in range(nv):
                x = int(next(it))
                y = int(next(it))
                verts.append((x, y))
            rid_verts[rid] = verts
        instancias.append(rid_verts)
    return instancias


def _bbox_area(verts):
    xs = [x for x, y in verts]
    ys = [y for x, y in verts]
    return (max(xs) - min(xs)) * (max(ys) - min(ys))


class InstanceQ4:

    def __init__(self, rid_verts_ordenado):
        self.rid_verts = rid_verts_ordenado
        self.exterior = max(rid_verts_ordenado,
                            key=lambda r: _bbox_area(rid_verts_ordenado[r]))
        self.boundary = set(rid_verts_ordenado[self.exterior])

        self.R = [r for r in rid_verts_ordenado if r != self.exterior]
        self.G0 = {r: set(rid_verts_ordenado[r]) - self.boundary for r in self.R}
        self.P = set()
        for vs in self.G0.values():
            self.P.update(vs)
        self.V0 = defaultdict(set)
        for r, vs in self.G0.items():
            for p in vs:
                self.V0[p].add(r)
        self.V0 = dict(self.V0)

        self._construir_grafo()

    def _construir_grafo(self):
        """Grafo dos vertices da particao. Cada par consecutivo na fronteira
        de uma face define um segmento; vertices intermedios colineares
        (T-junctions) sao inseridos por subdivisao."""
        todos = set()
        for vs in self.rid_verts.values():
            todos.update(vs)
        self.nodes = todos

        por_x = defaultdict(list)
        por_y = defaultdict(list)
        for (x, y) in todos:
            por_x[x].append(y)
            por_y[y].append(x)
        for x in por_x:
            por_x[x] = sorted(set(por_x[x]))
        for y in por_y:
            por_y[y] = sorted(set(por_y[y]))

        adj = defaultdict(set)

        def add_segmento(a, b):
            (xa, ya), (xb, yb) = a, b
            if xa == xb:
                ys = [yy for yy in por_x[xa] if min(ya, yb) <= yy <= max(ya, yb)]
                ys = sorted(ys)
                for i in range(len(ys) - 1):
                    u, v = (xa, ys[i]), (xa, ys[i + 1])
                    adj[u].add(v)
                    adj[v].add(u)
            elif ya == yb:
                xs = [xx for xx in por_y[ya] if min(xa, xb) <= xx <= max(xa, xb)]
                xs = sorted(xs)
                for i in range(len(xs) - 1):
                    u, v = (xs[i], ya), (xs[i + 1], ya)
                    adj[u].add(v)
                    adj[v].add(u)

        for vs in self.rid_verts.values():
            n = len(vs)
            for i in range(n):
                add_segmento(vs[i], vs[(i + 1) % n])

        self.adj = {k: v for k, v in adj.items()}

    def alcance(self, D):
        """Devolve (G_D, V_D) para o alcance D, calculados por BFS limitado
        a profundidade D no grafo dos vertices. Para D=0 coincide com o
        problema base (incidencia)."""
        if D == 0:
            return ({r: set(self.G0[r]) for r in self.R},
                    {p: set(self.V0[p]) for p in self.P})

        V_D = {}
        for p in self.P:
            vistos = set()
            dist = {p: 0}
            fila = deque([p])
            while fila:
                u = fila.popleft()
                if u in self.V0:
                    vistos |= self.V0[u]
                if dist[u] == D:
                    continue
                for w in self.adj.get(u, ()):
                    if w not in dist:
                        dist[w] = dist[u] + 1
                        fila.append(w)
            V_D[p] = vistos

        G_D = defaultdict(set)
        for p, rs in V_D.items():
            for r in rs:
                G_D[r].add(p)
        for r in self.R:
            G_D.setdefault(r, set())
        return dict(G_D), V_D

    def __repr__(self):
        return (f"InstanceQ4(#ret={len(self.R)}, #cand={len(self.P)}, "
                f"#nos_grafo={len(self.nodes)}, exterior=R{self.exterior})")


def carregar_q4(caminho):
    return [InstanceQ4(rv) for rv in carregar_ordenado(caminho)]


if __name__ == "__main__":
    import sys
    caminho = sys.argv[1] if len(sys.argv) > 1 else "../../casos_teste/inst_10.txt"
    insts = carregar_q4(caminho)
    inst = insts[0]
    print(inst)
    print(f"  #arestas do grafo: {sum(len(v) for v in inst.adj.values())//2}")
    for D in [0, 1, 2, 3]:
        _, V_D = inst.alcance(D)
        cob_media = sum(len(V_D[p]) for p in inst.P) / len(inst.P)
        print(f"  D={D}: cobertura media por guarda = {cob_media:.2f} retangulos")
