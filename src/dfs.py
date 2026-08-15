def busca_profundidade(grafo, inicio, objetivo):
    visitados = set()
    ordem_visitados = []
    caminho = []

    encontrou = _dfs(
        grafo,
        inicio,
        objetivo,
        visitados,
        ordem_visitados,
        caminho
    )

    if encontrou:
        return caminho, ordem_visitados

    return None, ordem_visitados


def _dfs(
    grafo,
    atual,
    objetivo,
    visitados,
    ordem_visitados,
    caminho
):
    visitados.add(atual)
    ordem_visitados.append(atual)
    caminho.append(atual)

    if atual == objetivo:
        return True

    for vizinho in grafo.get(atual, []):
        destino = vizinho["destino"]

        if destino not in visitados:
            encontrou = _dfs(
                grafo,
                destino,
                objetivo,
                visitados,
                ordem_visitados,
                caminho
            )

            if encontrou:
                return True

    caminho.pop()

    return False