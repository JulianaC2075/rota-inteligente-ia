from collections import deque


def busca_largura(grafo, inicio, objetivo):
    fila = deque([inicio])

    visitados = {inicio}
    pais = {inicio: None}
    ordem_visitados = []

    while fila:
        atual = fila.popleft()
        ordem_visitados.append(atual)

        if atual == objetivo:
            break

        for vizinho in grafo.get(atual, []):
            destino = vizinho["destino"]

            if destino not in visitados:
                visitados.add(destino)
                pais[destino] = atual
                fila.append(destino)

    if objetivo not in pais:
        return None, ordem_visitados

    caminho = []
    atual = objetivo

    while atual is not None:
        caminho.append(atual)
        atual = pais[atual]

    caminho.reverse()

    return caminho, ordem_visitados