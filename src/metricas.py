from time import perf_counter


def calcular_distancia_caminho(grafo, caminho):
    if not caminho or len(caminho) < 2:
        return 0.0

    distancia_total = 0.0

    for origem, destino in zip(
        caminho,
        caminho[1:]
    ):
        aresta_encontrada = None

        for vizinho in grafo.get(origem, []):
            if vizinho["destino"] == destino:
                aresta_encontrada = vizinho
                break

        if aresta_encontrada is None:
            raise ValueError(
                f"Não existe ligação entre {origem} e {destino}."
            )

        distancia_total += float(
            aresta_encontrada["distancia_km"]
        )

    return distancia_total


def medir_tempo_medio(
    funcao,
    *args,
    repeticoes=1000
):
    inicio = perf_counter()

    resultado = None

    for _ in range(repeticoes):
        resultado = funcao(*args)

    fim = perf_counter()

    tempo_total = fim - inicio

    tempo_medio_ms = (
        tempo_total / repeticoes
    ) * 1000

    return resultado, tempo_medio_ms