## 3. Avaliação da Aplicação de Programação Dinâmica

Para que a aplicação desta técnica valha a pena, devemos avaliar se é possível repartir este problema em subproblemas que seja independetes e que valha mais a pena que aplicar outras possíveis soluções  

### 3.1. A Dificuldade da Subestrutura em Grafos 2D Arbitrários

Ao modelarmos a partição retangular num grafo (onde os retângulos são elementos a cobrir e os vértices são os pontos de decisão), acabamos com uma estrutura muito densa e com diversos ciclos.

A decisão de colocar um guarda num vértice $v_i$ resolve a cobertura dos retângulos incidentes, mas altera o "estado" necessário para tomar decisões nos vértices vizinhos. Como o mapa é bidimensional, estas decisões propagam-se em várias direções, fechando ciclos e destruindo a independência local exigida pela Programação Dinâmica clássica (como a que é aplicada em árvores ou sequências lineares). O estado necessário para memorizar um subproblema não se resume a um único nó, mas sim a toda a fronteira de intersecção com o resto do mapa.

### 3.2. Programação Dinâmica de Perfil (Profile DP)
A única forma exata de aplicar Programação Dinâmica a este problema de grelha bidimensional seria através de uma técnica conhecida como **Programação Dinâmica de Perfil** (*Profile DP* ou varrimento de linha). 

O algoritmo funcionaria da seguinte forma teórica:
1. Uma linha imaginária varre o mapa ortogonal da esquerda para a direita (ou de cima para baixo).
2. A linha interseta, a qualquer momento, um conjunto de retângulos, formando uma "fronteira" ou "perfil" de largura $W$.
3. O estado da PD teria de memorizar todas as combinações possíveis de cobertura para os retângulos dessa fronteira.
4. Para cada nova coluna avançada, o algoritmo testaria todas as permutações válidas de guardas e faria a transição de estados.

### 3.3. Complexidade e Conclusão
A complexidade temporal e espacial da Programação Dinâmica de Perfil é governada pelo tamanho máximo da fronteira $W$. O número de estados a memorizar em cada passo cresce exponencialmente, na ordem de $\mathcal{O}(2^W)$. 

No nosso caso de estudo (ex: instância com 40 retângulos e 82 vértices interligados num espaço denso), a largura do perfil $W$ atinge valores que tornam a complexidade espacial impraticável em tempo útil, originando uma explosão combinatória na tabela de memorização.

**Conclusão:**
Embora este método possa ser utilizado para resolver o problema, sua aplicação é consideravelmente inferior e computacionalmente mais pesada que, por exemplo, a abordagem utilizada no exercício 2.
