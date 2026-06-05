:- use_module(library(clpfd)).

% Predicado principal. Exemplo de uso:
% resolver(6, [[0,1,2,3], [2,3,4,5]], Guardas, Min).
resolver(NumVertices, Faces, Guardas, MinGuardas) :-
    % 1. Variáveis: Uma lista de N variáveis, onde cada uma pode ser 0 ou 1
    length(Guardas, NumVertices),
    Guardas ins 0..1,

    % 2. Restrições: Para cada face, pelo menos 1 guarda
    maplist(garantir_cobertura(Guardas), Faces),

    % 3. Função Objetivo: Somar todos os guardas
    sum(Guardas, #=, MinGuardas),

    % 4. Otimização: Minimizar a soma usando labeling
    labeling([min(MinGuardas)], Guardas).

% Aplica a restrição de >= 1 a uma face específica
garantir_cobertura(Guardas, FaceVertices) :-
    extrair_vars(FaceVertices, Guardas, VarsDaFace),
    sum(VarsDaFace, #>=, 1).

% Função auxiliar para mapear os índices dos vértices para as variáveis lógicas
extrair_vars([], _, []).
extrair_vars([V|Vs], Guardas, [G|Gs]) :-
    nth0(V, Guardas, G),
    extrair_vars(Vs, Guardas, Gs).