# Exercício 2a: Modelo Matemático

Para modelar o problema de vigilância de partições retangulares como um problema de otimização linear inteira, começamos definindo:

## 1. Conjuntos e Parâmetros
* $V$: Conjunto de todos os vértices únicos (os pontos de intersecção) da partição.
* $\Pi$: Conjunto de todos os retângulos (faces) que devem se checar.
* $A_{r,v}$: Matriz binária de incidência, com $A_{r,v} = 1$ se o vértice $v$ pertence ao retângulo $r$, e $0$ caso contrário.

## 2. Variáveis de Decisão
* $x_v \in \{0, 1\} \quad \forall v \in V$
  (Onde $x_v = 1$ significa que um guarda é colocado no vértice $v$, e $0$ caso contrário).

## 3. Função Objetivo
O objetivo é minimizar o número total de guardas colocados:
$$\min \sum_{v \in V} x_v$$

## 4. Restrições
Para garantir a cobertura total, cada retângulo $r \in \Pi$ tem de ter pelo menos 1 guarda num dos seus vértices incidentes:
$$\sum_{v \in V} A_{r,v} x_v \ge 1 \quad \forall r \in \Pi$$