import sys
from instance_q3 import carregar_instancias_q3, InstanceQ3


class SolverDP:
    def __init__(self, inst: InstanceQ3):
        self.inst = inst
        self.nFaces = inst.num_faces
        self.nVertices = inst.num_variaveis

        self.objMask = (1 << self.nFaces) - 1

        self.coberturaVertices = [0] * self.nVertices
        for indxFace, verticesFace in enumerate(inst.faces):
            for v in verticesFace:
                self.coberturaVertices[v] |= (1 << indxFace)

        self.verticesUteis = [v for v in range(self.nVertices) if self.coberturaVertices[v] > 0]

        self.memo = {}
        self.choice = {}

    def dp(self, mask: int) -> int:
        if mask == self.objMask:
            return 0

        if mask in self.memo:
            return self.memo[mask]

        melhorCusto = float('inf')
        melhorV = -1

        for v in self.verticesUteis:
            novaMask = mask | self.coberturaVertices[v]

            if novaMask != mask:
                custo = 1 + self.dp(novaMask)
                if custo < melhorCusto:
                    melhorCusto = custo
                    melhorV = v

        self.memo[mask] = melhorCusto
        self.choice[mask] = melhorV
        return melhorCusto

    def resolver(self):
        sys.setrecursionlimit(20000)

        minGuardas = self.dp(0)

        if minGuardas == float('inf'):
            return None, []

        posicoes = []
        currentMask = 0
        while currentMask != self.objMask:
            v = self.choice[currentMask]
            posicoes.append(self.inst.pontos[v])
            currentMask |= self.coberturaVertices[v]

        return minGuardas, posicoes


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "../../casos_teste/inst_10.txt"
    try:
        instancias = carregar_instancias_q3(path)

        for i, inst in enumerate(instancias, 1):
            print(f"\nInstância #{i} com Programação Dinâmica (Bitmask):")

            solver = SolverDP(inst)
            minGuardas, posicoes = solver.resolver()

            if minGuardas is not None:
                print(f"Mínimo de guardas: {minGuardas} / Posições: {sorted(posicoes)} / Estados na Memoization: {len(solver.memo)}")
            else:
                print("Nenhuma solução encontrada.")

    except FileNotFoundError:
        print(f"Ficheiro '{path}' não encontrado.")


if __name__ == "__main__":
    main()