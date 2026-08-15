import math

from astar import busca_a_estrela


def distancia_euclidiana(coordenadas, origem, destino):
    x_origem, y_origem = coordenadas[origem]
    x_destino, y_destino = coordenadas[destino]

    return math.sqrt(
        (x_origem - x_destino) ** 2
        + (y_origem - y_destino) ** 2
    )


def escolher_proximo_local(
    atual,
    locais_pendentes,
    coordenadas
):
    return min(
        locais_pendentes,
        key=lambda destino: distancia_euclidiana(
            coordenadas,
            atual,
            destino
        )
    )


def planejar_rota_zona(
    grafo,
    coordenadas,
    local_restaurante,
    locais_entrega
):
    atual = local_restaurante

    pendentes = list(locais_entrega)

    ordem_entregas = []
    trechos = []

    distancia_total = 0.0
    vertices_analisados_total = 0

    while pendentes:
        proximo = escolher_proximo_local(
            atual,
            pendentes,
            coordenadas
        )

        (
            caminho,
            visitados,
            custo
        ) = busca_a_estrela(
            grafo,
            coordenadas,
            atual,
            proximo
        )

        if caminho is None:
            raise ValueError(
                f"Não foi possível encontrar rota "
                f"entre {atual} e {proximo}."
            )

        trechos.append(
            {
                "origem": atual,
                "destino": proximo,
                "caminho": caminho,
                "distancia": custo,
                "vertices_analisados": len(visitados)
            }
        )

        ordem_entregas.append(proximo)

        distancia_total += custo
        vertices_analisados_total += len(visitados)

        pendentes.remove(proximo)
        atual = proximo

    return {
        "ordem_entregas": ordem_entregas,
        "trechos": trechos,
        "distancia_total": distancia_total,
        "vertices_analisados": vertices_analisados_total
    }