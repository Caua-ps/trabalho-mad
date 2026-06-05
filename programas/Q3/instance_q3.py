from typing import List, Tuple, Set, Dict


class InstanceQ3:
    def __init__(self, pontos_validos: List[Tuple[int, int]], faces_indices: List[List[int]]):
        """
        pontos_validos: Lista de todas as coordenadas (x, y) únicas válidas.
        faces_indices: Lista onde cada elemento representa um retângulo (face),
                       contendo os índices dos vértices em `pontos_validos`.
        """
        self.pontos = pontos_validos
        self.faces = faces_indices
        self.num_variaveis = len(pontos_validos)
        self.num_faces = len(faces_indices)

    def __repr__(self):
        return f"InstanceQ3(Variaveis={self.num_variaveis}, Restricoes(Faces)={self.num_faces})"


def _area_bbox(verts: Set[Tuple[int, int]]) -> int:
    """Calcula a área da bounding box."""
    if not verts: return 0
    min_x, max_x = min(v[0] for v in verts), max(v[0] for v in verts)
    min_y, max_y = min(v[1] for v in verts), max(v[1] for v in verts)
    return (max_x - min_x) * (max_y - min_y)


def carregar_instancias_q3(caminho_ficheiro: str) -> List[InstanceQ3]:
    """
    Lê o ficheiro e devolve uma lista de instâncias otimizadas para a Q3.
    Remove automaticamente o retângulo exterior.
    """
    with open(caminho_ficheiro, 'r') as f:
        toks = f.read().split()

    if not toks:
        return []

    it = iter(toks)
    instancias_q3 = []

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

            # 1. Identificar e descartar o exterior
            id_exterior = max(rid_verts, key=lambda r: _area_bbox(rid_verts[r]))
            borda = rid_verts[id_exterior]

            # 2. Extrair vértices válidos (interiores)
            pontos_unicos_validos = set()
            faces_validas_pontos = []

            for rid, verts in rid_verts.items():
                if rid == id_exterior:
                    continue
                verts_interiores = verts - borda
                if verts_interiores:
                    faces_validas_pontos.append(verts_interiores)
                    pontos_unicos_validos.update(verts_interiores)

            # 3. Mapear pontos para índices inteiros 0..N
            lista_pontos = list(pontos_unicos_validos)
            ponto_para_idx = {ponto: idx for idx, ponto in enumerate(lista_pontos)}

            faces_indices = []
            for face_pontos in faces_validas_pontos:
                face_idx = [ponto_para_idx[p] for p in face_pontos]
                faces_indices.append(face_idx)

            instancias_q3.append(InstanceQ3(lista_pontos, faces_indices))

        return instancias_q3

    except StopIteration:
        return instancias_q3