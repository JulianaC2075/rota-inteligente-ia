import pandas as pd


def carregar_locais(caminho="data/locais.csv"):
    return pd.read_csv(caminho)


def carregar_rotas(caminho="data/rotas.csv"):
    return pd.read_csv(caminho)


def construir_grafo(rotas):
    grafo = {}

    for _, rota in rotas.iterrows():
        origem = int(rota["origem"])
        destino = int(rota["destino"])
        distancia = float(rota["distancia_km"])
        tempo = int(rota["tempo_min"])

        if origem not in grafo:
            grafo[origem] = []

        if destino not in grafo:
            grafo[destino] = []

        grafo[origem].append(
            {
                "destino": destino,
                "distancia_km": distancia,
                "tempo_min": tempo,
            }
        )

        grafo[destino].append(
            {
                "destino": origem,
                "distancia_km": distancia,
                "tempo_min": tempo,
            }
        )

    return grafo