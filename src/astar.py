import heapq
import math


def criar_coordenadas(locais):
    coordenadas = {}

    for _, local in locais.iterrows():
        coordenadas[int(local["id"])] = (
            float(local["x"]),
            float(local["y"])
        )

    return coordenadas


def calcular_heuristica(coordenadas, atual, objetivo):
    x_atual, y_atual = coordenadas[atual]
    x_objetivo, y_objetivo = coordenadas[objetivo]

    diferenca_x = x_atual - x_objetivo
    diferenca_y = y_atual - y_objetivo

    distancia_euclidiana = math.sqrt(
        diferenca_x ** 2 + diferenca_y ** 2
    )

    return distancia_euclidiana * 0.9


def busca_a_estrela(grafo, coordenadas, inicio, objetivo):
    fila_prioridade = []

    custo_acumulado = {
        inicio: 0.0
    }

    pais = {
        inicio: None
    }

    ordem_visitados = []
    visitados = set()

    heuristica_inicial = calcular_heuristica(
        coordenadas,
        inicio,
        objetivo
    )

    heapq.heappush(
        fila_prioridade,
        (heuristica_inicial, inicio)
    )

    while fila_prioridade:
        _, atual = heapq.heappop(fila_prioridade)

        if atual in visitados:
            continue

        visitados.add(atual)
        ordem_visitados.append(atual)

        if atual == objetivo:
            break

        for vizinho in grafo.get(atual, []):
            destino = vizinho["destino"]
            distancia = vizinho["distancia_km"]

            novo_custo = (
                custo_acumulado[atual]
                + distancia
            )

            if (
                destino not in custo_acumulado
                or novo_custo < custo_acumulado[destino]
            ):
                custo_acumulado[destino] = novo_custo
                pais[destino] = atual

                heuristica = calcular_heuristica(
                    coordenadas,
                    destino,
                    objetivo
                )

                custo_estimado_total = (
                    novo_custo + heuristica
                )

                heapq.heappush(
                    fila_prioridade,
                    (
                        custo_estimado_total,
                        destino
                    )
                )

    if objetivo not in pais:
        return None, ordem_visitados, None

    caminho = []
    atual = objetivo

    while atual is not None:
        caminho.append(atual)
        atual = pais[atual]

    caminho.reverse()

    return (
        caminho,
        ordem_visitados,
        custo_acumulado[objetivo]
    )