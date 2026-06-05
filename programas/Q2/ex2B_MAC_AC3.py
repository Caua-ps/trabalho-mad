import sys
from instance_q2 import carregar_instancias_q2, InstanceQ2


class SolverMAC:
    def __init__(self, inst: InstanceQ2):
        self.inst = inst
        self.melhorSolucao = None
        self.minGuardas = float('inf')
        self.pontos = inst.pontos
        self.faces = inst.faces

    def propagar_mac(self, atribuicoes):
        alterou = True
        while alterou:
            alterou = False
            for face in self.faces:
                semAtribuicoes = 0
                guardas = 0
                ultimoLivre = -1

                for v in face:
                    if atribuicoes[v] == 1:
                        guardas += 1
                    elif atribuicoes[v] == -1:
                        semAtribuicoes += 1
                        ultimoLivre = v

                if guardas == 0 and semAtribuicoes == 0:
                    return False

                if guardas == 0 and semAtribuicoes == 1:
                    atribuicoes[ultimoLivre] = 1
                    alterou = True
        return True

    def resolver_rec(self, currentVar, atribuicoes, currentGuardas):
        if currentGuardas >= self.minGuardas:
            return

        if currentVar == len(atribuicoes):
            faceValida = True
            for face in self.faces:
                if not any(atribuicoes[v] == 1 for v in face):
                    faceValida = False
                    break
            if faceValida:
                self.minGuardas = currentGuardas
                self.melhorSolucao = list(atribuicoes)
            return

        if atribuicoes[currentVar] != -1:
            soma = 1 if atribuicoes[currentVar] == 1 else 0
            self.resolver_rec(currentVar + 1, atribuicoes, currentGuardas + soma)
            return

        backup1 = list(atribuicoes)
        backup1[currentVar] = 1
        if self.propagar_mac(backup1):
            self.resolver_rec(currentVar + 1, backup1, currentGuardas + 1)

        backup2 = list(atribuicoes)
        backup2[currentVar] = 0
        if self.propagar_mac(backup2):
            self.resolver_rec(currentVar + 1, backup2, currentGuardas)

    def resolver(self):
        atribuicoes = [-1] * len(self.pontos)
        self.resolver_rec(0, atribuicoes, 0)

        if self.melhorSolucao:
            posicoes = [self.pontos[i] for i, val in enumerate(self.melhorSolucao) if val == 1]
            return self.minGuardas, posicoes
        return None, []


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "../../casos_teste/inst_10.txt"
    try:
        instancias = carregar_instancias_q2(path)

        for i, inst in enumerate(instancias, 1):
            print(f"\nInstancia #{i} com MAC:")
            solver = SolverMAC(inst)
            minGuardas, posicoes = solver.resolver()

            if minGuardas is not None:
                    print(f"Minimo de guardas: {minGuardas} / Posicoes: {sorted(posicoes)}")
            else:
                print("Nenhuma solucao encontrada.")

    except FileNotFoundError:
        print(f"Ficheiro '{path}' nao encontrado.")


if __name__ == "__main__":
    main()