============================================================
MAD CC3003 2025/26 - Trabalho Pratico
Vigilancia de Particoes Retangulares
============================================================

Grupo 06:
  202302423  Caua Pinheiro Souza
  202205324  Matheus Goncalves Guerra

Conteudo desta entrega:
  relatorio.pdf       - relatorio principal
  programas/          - codigo-fonte
    rectParts.c, types.h, macros.h  - gerador de instancias
    Q1/                              - estrategias greedy
    Q2/                              - programacao por restricoes e MAC
    Q3/                              - programacao dinamica (bitmask)
    Q4/                              - extensoes (cores, alcance)
  casos_teste/        - instancias de exemplo


============================================================
1. REQUISITOS
============================================================

- Python 3.8 ou superior
- biblioteca Google OR-Tools
  ($ pip install ortools)
- SWI-Prolog (para testar a implementacao clpfd da Q2)
- compilador C (para o gerador de instancias da professora)


============================================================
2. COMPILAR O GERADOR
============================================================

A partir de programas/:

    gcc rectParts.c -o gerador -lm


============================================================
3. GERAR INSTANCIAS
============================================================

O programa pede 'Number of rectangles?' e 'Number of instances?'.
Para gerar 20 instancias de 40 retangulos no ficheiro inst.txt:

    echo "40 20" | ./gerador inst.txt

(opcionalmente um segundo argumento para o ficheiro .tex com as figuras).

A pasta casos_teste/ contem instancias pre-geradas para teste rapido.


============================================================
4. EXECUTAR Q1 (estrategias greedy)
============================================================

A partir de programas/Q1/:

  Pre-processamento e leitura:
      python3 instance.py ../../casos_teste/inst_10.txt

  Estrategias greedy (com teste na fp3 ex.7):
      python3 greedy.py ../../casos_teste/inst_10.txt

  Solver exato (PI com OR-Tools):
      python3 exato.py ../../casos_teste/inst_10.txt

  Estudo experimental (greedy vs otimo, tabela de comparacao):
      python3 benchmark.py ../../casos_teste


============================================================
5. EXECUTAR Q2 (PI, CSP e MAC)
============================================================

  Modelo matematico (PI): ver ex2A.md em programas/Q2/.

A partir de programas/Q2/:

  Pre-processamento e otimizacao de matriz para a Q2:
      python3 instance_q2.py ../../casos_teste/inst_10.txt

  Solver MAC (Maintaining Arc Consistency com AC-3):
      python3 ex2B_MAC_AC3.py ../../casos_teste/inst_10.txt

  Solver OR-Tools (CP-SAT):
      python3 ex2C_ORTools.py ../../casos_teste/inst_10.txt

  Solver Prolog (clpfd):
      carregar o ficheiro no interpretador: swipl -s ex2C_prolog.pl


============================================================
6. EXECUTAR Q3 (programacao dinamica)
============================================================

  Avaliacao da aplicabilidade da PD: ver ex3.md em programas/Q3/.

A partir de programas/Q3/:

  Solver Programacao Dinamica (Bitmask DP):
      python3 ex3_DP.py ../../casos_teste/inst_10.txt


============================================================
7. EXECUTAR Q4 (extensoes)
============================================================

A partir de programas/Q4/:

  Leitura, grafo e calculo de alcance:
      python3 instance_q4.py ../../casos_teste/inst_10.txt

  Q4b - guardas com alcance D:
      python3 alcance.py ../../casos_teste/inst_10.txt

  Q4a - guardas com cores (Leituras A e B):
      python3 cores.py ../../casos_teste/inst_10.txt

  Estudos experimentais:
      python3 bench_alcance.py ../../casos_teste
      python3 bench_cores.py   ../../casos_teste


============================================================
8. ESTADO DAS QUESTOES
============================================================

  Q1 - estrategias greedy        IMPLEMENTADA
  Q2 - PI e CSP (modelo, MAC,
       OR-Tools, clpfd)           IMPLEMENTADA
  Q3 - programacao dinamica       IMPLEMENTADA
  Q4 - extensoes (cores+alcance)  IMPLEMENTADA


============================================================
9. NOTAS DE EXECUCAO
============================================================

- Os scripts aceitam um caminho para ficheiro de instancias ou
  para uma pasta com inst_10.txt, inst_20.txt, etc.
- Por defeito apontam para ../../casos_teste/ relativamente ao
  diretorio do script.
- O solver lexicografico de Q4a (cores.py) tem time limit de 60s
  por instancia; reportar "True" na coluna "otimo?" indica que o
  resultado e otimo provado.
