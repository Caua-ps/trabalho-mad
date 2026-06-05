from typing import List, Tuple, Set, Dict


class InstanceQ2:
    def __init__(self, pontos_validos: List[Tuple[int, int]], faces_indices: List[List[int]]):
        self.pontos = pontos_validos
        self.faces = faces_indices
        self.num_variaveis = len(pontos_validos)
        self.num_faces = len(faces_indices)

    def __repr__(self):
        return f"InstanceQ2(Variaveis={self.num_variaveis}, Restricoes(Faces)={self.num_faces})"


def _area_bbox(verts: Set[Tuple[int, int]]) -> int:
    if not verts: return 0
    min_x, max_x = min(v[0] for v in verts), max(v[0] for v in verts)
    min_y, max_y = min(v[1] for v in verts), max(v[1] for v in verts)
    return (max_x - min_x) * (max_y - min_y)


def carregar_instancias_q2(caminho_ficheiro: str) -> List[InstanceQ2]:
    with open(caminho_ficheiro, 'r') as f:
        toks = f.read().split()

    if not toks:
        return []

    it = iter(toks)
    instancias_q2 = []

    try:
        n_inst = int(next(it))
        for _ in range(n_inst):
            nr = int(next(it))
            rid_verts: Dict[int, Set[Tuple[int, int]]] = {}

            for _ in range(nr):
                rid = int(next(it))
                nv = int(next(it))
                verts = set()
                for _ in range(nv):
                    verts.add((int(next(it)), int(next(it))))
                rid_verts[rid] = verts

            id_exterior = max(rid_verts, key=lambda r: _area_bbox(rid_verts[r]))
            borda = rid_verts[id_exterior]

            pontos_unicos_validos = set()
            faces_validas_pontos = []

            for rid, verts in rid_verts.items():
                if rid == id_exterior:
                    continue
                verts_interiores = verts - borda
                if verts_interiores:
                    faces_validas_pontos.append(verts_interiores)
                    pontos_unicos_validos.update(verts_interiores)

            lista_pontos = list(pontos_unicos_validos)
            ponto_para_idx = {ponto: idx for idx, ponto in enumerate(lista_pontos)}

            faces_indices = []
            for face_pontos in faces_validas_pontos:
                face_idx = [ponto_para_idx[p] for p in face_pontos]
                faces_indices.append(face_idx)

            instancias_q2.append(InstanceQ2(lista_pontos, faces_indices))

        return instancias_q2

    except StopIteration:
        return instancias_q2


if __name__ == "__main__":
    import sys

    caminho = sys.argv[1] if len(sys.argv) > 1 else "../../casos_teste/inst_10.txt"
    try:
        insts = carregar_instancias_q2(caminho)
        print(f"Lidas {len(insts)} instância(s) isoladas para Q2 de '{caminho}':")
        for i, inst in enumerate(insts, 1):
            print(f"  #{i}: {inst}")
    except FileNotFoundError:
        print(f"Erro: Ficheiro não encontrado no caminho {caminho}")