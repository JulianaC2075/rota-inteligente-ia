import math
from itertools import permutations

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

        caminho, visitados, custo = busca_a_estrela(
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


def planejar_rota_zona_otima(
    grafo,
    coordenadas,
    local_restaurante,
    locais_entrega
):
    melhor_ordem = None
    melhores_trechos = None

    menor_distancia = float("inf")
    melhor_vertices_analisados = 0

    cache_trechos = {}

    def obter_trecho(origem, destino):
        chave = (
            origem,
            destino
        )

        if chave not in cache_trechos:
            caminho, visitados, custo = busca_a_estrela(
                grafo,
                coordenadas,
                origem,
                destino
            )

            if caminho is None:
                return None

            cache_trechos[chave] = {
                "origem": origem,
                "destino": destino,
                "caminho": caminho,
                "distancia": custo,
                "vertices_analisados": len(visitados)
            }

        return cache_trechos[chave]

    for ordem in permutations(locais_entrega):
        atual = local_restaurante

        distancia_total = 0.0
        vertices_analisados_total = 0

        trechos = []

        rota_valida = True

        for destino in ordem:
            trecho = obter_trecho(
                atual,
                destino
            )

            if trecho is None:
                rota_valida = False
                break

            distancia_total += trecho[
                "distancia"
            ]

            vertices_analisados_total += trecho[
                "vertices_analisados"
            ]

            trechos.append(
                trecho.copy()
            )

            atual = destino

        if (
            rota_valida
            and distancia_total < menor_distancia
        ):
            menor_distancia = distancia_total

            melhor_ordem = list(
                ordem
            )

            melhores_trechos = trechos

            melhor_vertices_analisados = (
                vertices_analisados_total
            )

    if melhor_ordem is None:
        raise ValueError(
            "Não foi possível encontrar uma rota "
            "que atenda todas as entregas da zona."
        )

    return {
        "ordem_entregas": melhor_ordem,
        "trechos": melhores_trechos,
        "distancia_total": menor_distancia,
        "vertices_analisados": melhor_vertices_analisados
    }