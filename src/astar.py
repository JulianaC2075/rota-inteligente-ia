import heapq
import math


def calcular_heuristica(locais, atual, objetivo):
    local_atual = locais.loc[
        locais["id"] == atual
    ].iloc[0]

    local_objetivo = locais.loc[
        locais["id"] == objetivo
    ].iloc[0]

    diferenca_x = local_atual["x"] - local_objetivo["x"]
    diferenca_y = local_atual["y"] - local_objetivo["y"]

    distancia_euclidiana = math.sqrt(
        diferenca_x ** 2 + diferenca_y ** 2
    )

    # Fator conservador para manter a estimativa
    # abaixo dos custos reais das rotas deste cenário.
    return distancia_euclidiana * 0.9


def busca_a_estrela(grafo, locais, inicio, objetivo):
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
        locais,
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
                    locais,
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